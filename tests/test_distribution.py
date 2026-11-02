"""A distributed deck skill must build without files from the source checkout."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_standalone_deck_skill_builds_from_unrelated_working_directory(self):
        source = ROOT / "plugins/paperbanana-slide-deck"
        # This is the folder supplied to a skill-folder installer, not a plugin host.
        self.assertTrue((source / "SKILL.md").is_file(), "the installable bundle needs its own entrypoint")
        with tempfile.TemporaryDirectory(prefix="paperbanana-distribution-") as tmp:
            temp = Path(tmp)
            bundle = temp / "skills/paperbanana-slide-deck"
            shutil.copytree(source, bundle, ignore=shutil.ignore_patterns("node_modules", "__pycache__", "tests"))
            setup = subprocess.run(["bun", "install", "--frozen-lockfile", "--ignore-scripts"], cwd=bundle, capture_output=True, text=True)
            self.assertEqual(setup.returncode, 0, setup.stdout + setup.stderr)
            deck = temp / "input"
            deck.mkdir()
            shutil.copyfile(ROOT / "examples/editable-demo/slide-spec.json", deck / "slide-spec.json")
            output = temp / "built.pptx"
            run = subprocess.run(["bun", str(bundle / "scripts/build-deck.ts"), "--mode", "editable", str(deck), "--output", str(output)], cwd=temp, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertGreater(output.stat().st_size, 0)
            for reference in ("editable-slide-spec.md", "style-guide.md", "outline-format.md"):
                self.assertTrue((bundle / "references" / reference).is_file(), reference)


if __name__ == "__main__":
    unittest.main()
