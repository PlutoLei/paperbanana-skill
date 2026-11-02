import hashlib
import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch

MODULE = pathlib.Path(__file__).parents[1] / "scripts/editable/render-previews.py"


class RenderPreviewTest(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.exists(), "render-previews.py must produce verifiable preview inputs")
        spec = importlib.util.spec_from_file_location("render_previews", MODULE)
        self.render = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.render)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.spec = self.root / "slide-spec.json"
        self.spec.write_text(json.dumps({"slides": [{"id": "intro"}, {"id": "results"}]}))
        self.output = self.root / "rendered"
        self.argv = ["--spec", str(self.spec), "--output-dir", str(self.output)]
        self.fail_conversion = False
        self.page_count = 2
        self.deck_bytes = b"current PPTX"
        self.during_render = None

    def external_command(self, command, **kwargs):
        tool = pathlib.Path(command[0]).name
        if tool == "bun":
            pathlib.Path(command[-1]).write_bytes(self.deck_bytes)
        elif tool == "soffice":
            profile = next(arg for arg in command if arg.startswith("-env:UserInstallation="))
            self.assertIn("file:", profile)
            if self.fail_conversion:
                raise subprocess.CalledProcessError(1, command)
            output_dir = pathlib.Path(command[command.index("--outdir") + 1])
            (output_dir / "deck.pdf").write_bytes(b"current PDF")
        elif tool == "pdftoppm":
            for number in range(1, self.page_count + 1):
                pathlib.Path(f"{command[-1]}-{number}.png").write_bytes(f"page {number}".encode())
            if self.during_render:
                self.during_render()
        else:
            raise AssertionError(f"Unexpected executable {tool}")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    def run_render(self):
        with patch.object(self.render.subprocess, "run", side_effect=self.external_command):
            return self.render.main(self.argv)

    def test_builds_and_normalizes_pages_with_matching_manifest(self):
        self.assertEqual(self.run_render(), 0)
        manifest = json.loads((self.output / "render-manifest.json").read_text())
        self.assertEqual(manifest["spec_sha256"], hashlib.sha256(self.spec.read_bytes()).hexdigest())
        self.assertEqual([page["slide_id"] for page in manifest["slides"]], ["intro", "results"])
        self.assertEqual([page["file"] for page in manifest["slides"]], ["slide-01.png", "slide-02.png"])
        for entry in [manifest["pptx"], *manifest["slides"]]:
            self.assertEqual(entry["sha256"], hashlib.sha256((self.output / entry["file"]).read_bytes()).hexdigest())

    def test_failed_rebuild_keeps_previous_successful_output(self):
        self.assertEqual(self.run_render(), 0)
        original = {p.name: p.read_bytes() for p in self.output.iterdir()}
        self.fail_conversion = True
        self.assertEqual(self.run_render(), 1)
        self.assertEqual({p.name: p.read_bytes() for p in self.output.iterdir()}, original)

    def test_failure_during_publication_restores_previous_complete_generation(self):
        self.assertEqual(self.run_render(), 0)
        original = {p.name: p.read_bytes() for p in self.output.iterdir()}
        real_replace = self.render.os.replace
        calls = 0

        def fail_second_replace(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated publication failure")
            return real_replace(source, destination)

        self.deck_bytes = b"new PPTX generation"
        with patch.object(self.render.os, "replace", side_effect=fail_second_replace):
            self.assertEqual(self.run_render(), 1)
        self.assertEqual({p.name: p.read_bytes() for p in self.output.iterdir()}, original)

    def test_rollback_io_failure_retains_recoverable_previous_generation(self):
        self.assertEqual(self.run_render(), 0)
        original = {p.name: p.read_bytes() for p in self.output.iterdir()}
        real_replace = self.render.os.replace
        calls = 0

        def fail_publication_and_restore(source, destination):
            nonlocal calls
            calls += 1
            if calls in (2, 3):
                raise OSError("simulated persistent I/O failure")
            return real_replace(source, destination)

        with patch.object(self.render.os, "replace", side_effect=fail_publication_and_restore):
            self.assertEqual(self.run_render(), 1)
        backups = list(self.root.glob(".rendered.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual({p.name: p.read_bytes() for p in backups[0].iterdir()}, original)
        self.assertFalse(self.output.exists())

    def test_wrong_page_count_is_not_published(self):
        self.page_count = 1
        self.assertEqual(self.run_render(), 1)
        self.assertFalse((self.output / "render-manifest.json").exists())

    def test_unknown_destination_file_is_preserved(self):
        self.output.mkdir()
        note = self.output / "my-notes.txt"
        note.write_text("keep me")
        self.assertEqual(self.run_render(), 1)
        self.assertEqual(note.read_text(), "keep me")
        self.assertFalse((self.output / "render-manifest.json").exists())

    def add_nested_asset(self):
        asset = self.root / "figure.png"
        asset.write_bytes(b"source figure")
        spec = json.loads(self.spec.read_text())
        spec["slides"][0]["elements"] = [{"id": "group", "type": "group", "children": [
            {"id": "figure", "type": "image", "path": "figure.png",
             "sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}]}]
        self.spec.write_text(json.dumps(spec))
        return asset

    def test_manifest_binds_nested_image_source_assets(self):
        asset = self.add_nested_asset()
        self.assertEqual(self.run_render(), 0)
        manifest = json.loads((self.output / "render-manifest.json").read_text())
        self.assertEqual(manifest.get("assets"), [{"slide_id": "intro", "element_id": "figure",
                          "path": "figure.png", "sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}])

    def test_asset_changed_during_render_does_not_replace_previous_generation(self):
        asset = self.add_nested_asset()
        self.assertEqual(self.run_render(), 0)
        original = {p.name: p.read_bytes() for p in self.output.iterdir()}
        self.during_render = lambda: asset.write_bytes(b"changed during render")
        self.assertEqual(self.run_render(), 1)
        self.assertEqual({p.name: p.read_bytes() for p in self.output.iterdir()}, original)

    def test_output_cannot_contain_a_source_asset_even_through_directory_alias(self):
        self.output.mkdir()
        asset = self.output / "slide-01.png"
        asset.write_bytes(b"source figure must be preserved")
        alias = self.root / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        spec = json.loads(self.spec.read_text())
        spec["slides"][0]["elements"] = [{"id": "group", "type": "group", "children": [
            {"id": "figure", "type": "image", "path": "rendered/slide-01.png",
             "sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}]}]
        self.spec.write_text(json.dumps(spec))
        for output in [self.output, alias / "rendered"]:
            with self.subTest(output=output):
                asset.write_bytes(b"source figure must be preserved")
                before = asset.read_bytes()
                with patch.object(self.render.subprocess, "run", side_effect=self.external_command) as run:
                    code = self.render.main(self.argv[:-1] + [str(output)])
                self.assertEqual(asset.read_bytes(), before)
                self.assertEqual(code, 1)
                run.assert_not_called()

    def test_output_cannot_contain_the_spec_even_with_a_generated_filename(self):
        self.output.mkdir()
        spec = self.output / "render-manifest.json"
        spec.write_bytes(self.spec.read_bytes())
        before = spec.read_bytes()
        with patch.object(self.render.subprocess, "run", side_effect=self.external_command) as run:
            code = self.render.main(["--spec", str(spec), "--output-dir", str(self.output)])
        self.assertEqual(spec.read_bytes(), before)
        self.assertEqual(code, 1)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
