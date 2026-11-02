import hashlib
import importlib.util
import json
import os
import pathlib
import tempfile
import types
import unittest
from unittest.mock import patch

MODULE = pathlib.Path(__file__).parents[1] / "scripts/editable/review-editable.py"
SPEC = importlib.util.spec_from_file_location("review_editable", MODULE)
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MappingTest(unittest.TestCase):
    def test_unmapped_critic_text_retains_its_full_meaning(self):
        got = review.map_suggestions("slide-02", ["title", "chart"],
                                     ["chart: labels overlap", "Note: reduce clutter"])
        self.assertEqual(got, ["slide-02/chart: labels overlap",
                               "slide-02/unmapped: Note: reduce clutter"])


class RawResponseTest(unittest.TestCase):
    def test_raw_json_does_not_allow_score_coercion_or_missing_fields(self):
        for response in [
            {"critic_suggestions": [], "score": "NaN"},
            {"critic_suggestions": [], "score": 999},
            {"critic_suggestions": [], "score": True},
            {"score": 9},
            {"critic_suggestions": [], "score": "9"},
            {"critic_suggestions": [], "score": float("nan")},
            {"critic_suggestions": [], "score": float("inf")},
        ]:
            with self.subTest(response=response), self.assertRaises(ValueError):
                review.validate_raw_response(json.dumps(response))

    def test_raw_numeric_score_or_actionable_suggestions_remain_usable(self):
        for response in [{"critic_suggestions": [], "score": 0},
                         {"critic_suggestions": [], "score": 10},
                         {"critic_suggestions": ["title: correct label"], "score": None}]:
            review.validate_raw_response(json.dumps(response))


class ReviewContractTest(unittest.TestCase):
    """Strict doubles mirror the public core interface, without provider SDKs."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.spec = self.root / "slide-spec.json"
        self.spec.write_text(json.dumps({"slides": [{
            "id": "result", "title": "Sample result", "speaker_notes": "Illustrative data",
            "elements": [{"id": "title", "type": "text", "x": 0, "y": 0,
                          "w": 3, "h": 1, "text": "Sample result"}],
        }]}))
        self.previews = self.root / "rendered"
        self.previews.mkdir()
        self.png = self.previews / "slide-01.png"
        self.png.write_bytes(b"preview fixture")
        self.pptx = self.previews / "deck.pptx"
        self.pptx.write_bytes(b"deck fixture")
        self.manifest = self.previews / "render-manifest.json"
        self.manifest.write_text(json.dumps({
            "schema_version": 2, "spec_sha256": digest(self.spec), "assets": [],
            "pptx": {"file": "deck.pptx", "sha256": digest(self.pptx)},
            "slides": [{"slide_id": "result", "index": 1,
                        "file": "slide-01.png", "sha256": digest(self.png)}],
        }))
        self.output = self.root / "review.json"
        self.argv = ["--spec", str(self.spec), "--rendered-dir", str(self.previews),
                     "--output", str(self.output)]
        self.suggestions = ["title: increase spacing", "Note: check the caption"]
        self.score = 6.0
        self.failure = None
        self.during_call = None
        self.calls = 0

    def backend(self):
        test = self

        class Settings:
            def __init__(self, **kwargs):
                self.vlm_provider = "gemini"
                self.vlm_model = "configured-model"
                self.openai_vlm_model = "saved-openai-model"
                self.prompt_dir = None
                self.__dict__.update(kwargs)

        class Provider:
            def __init__(self, settings):
                self.name = settings.vlm_provider
                self.model_name = (settings.openai_vlm_model if self.name == "openai"
                                   else settings.vlm_model)

        class Registry:
            @staticmethod
            def create_vlm(settings):
                return Provider(settings)

        class Critic:
            def __init__(self, vlm_provider, prompt_dir="prompts"):
                self.vlm = vlm_provider

            async def run(self, image_path, description, source_context, caption,
                          diagram_type, user_feedback=None):
                test.calls += 1
                if test.failure:
                    raise test.failure
                if test.during_call:
                    test.during_call()
                if caption != "Sample result" or diagram_type != "slide":
                    raise ValueError("missing communicative intent or slide type")
                return types.SimpleNamespace(critic_suggestions=test.suggestions,
                                             score=test.score, revised_description=None)

        modules = {}
        for name, attrs in {
            "paperbanana": {}, "paperbanana.agents": {}, "paperbanana.core": {},
            "paperbanana.providers": {},
            "paperbanana.agents.critic": {"CriticAgent": Critic},
            "paperbanana.core.config": {"Settings": Settings},
            "paperbanana.core.types": {"DiagramType": types.SimpleNamespace(SLIDE="slide")},
            "paperbanana.core.utils": {"find_prompt_dir": lambda: "test-prompts"},
            "paperbanana.providers.registry": {"ProviderRegistry": Registry},
        }.items():
            module = types.ModuleType(name)
            module.__dict__.update(attrs)
            modules[name] = module
        return patch.dict("sys.modules", modules)

    def run_review(self, extra=()):
        with self.backend():
            code = review.main(self.argv + list(extra))
        return code, json.loads(self.output.read_text())

    def test_configured_provider_async_caption_and_suggestions_reach_report(self):
        code, payload = self.run_review()
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "needs-revision")
        self.assertEqual(payload["slides"][0]["raw_suggestions"], self.suggestions)
        self.assertEqual(payload["suggestions"], ["result/title: increase spacing",
                                                 "result/unmapped: Note: check the caption"])
        self.assertEqual(payload["provider"], {"name": "gemini", "model": "configured-model"})
        self.assertEqual(payload["inputs"]["spec_sha256"], digest(self.spec))
        self.assertEqual(self.calls, 1)

    def test_explicit_model_overrides_provider_specific_saved_model(self):
        code, payload = self.run_review(["--vlm-provider", "openai", "--vlm-model", "chosen"])
        self.assertEqual(code, 0)
        self.assertEqual(payload["provider"], {"name": "openai", "model": "chosen"})

    def test_empty_unscored_response_is_unreviewed(self):
        self.suggestions, self.score = [], None
        code, payload = self.run_review()
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "unreviewed")
        self.assertEqual(len(payload["slides"]), 1)
        self.assertEqual(payload["slides"][0]["status"], "unreviewed")

    def test_scored_no_issue_response_is_reviewed_without_scientific_approval(self):
        self.suggestions, self.score = [], 8.5
        code, payload = self.run_review()
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "reviewed")
        self.assertEqual(payload["score"], 8.5)
        self.assertNotIn("publication-ready", payload["slides"][0]["summary"])

    def test_provider_failure_marks_slide_and_deck_unreviewed(self):
        self.failure = TimeoutError("remote timeout")
        code, payload = self.run_review()
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "unreviewed")
        self.assertEqual(len(payload["slides"]), 1)
        self.assertEqual(payload["slides"][0]["error"], "TimeoutError")

    def test_malformed_suggestions_are_not_accepted(self):
        self.suggestions = "looks fine"
        code, payload = self.run_review()
        self.assertEqual(code, 1)
        self.assertEqual(len(payload["slides"]), 1)
        self.assertEqual(payload["slides"][0]["status"], "unreviewed")

    def test_missing_changed_or_wrong_page_inputs_stop_before_model_calls(self):
        mutations = [
            lambda: self.manifest.unlink(),
            lambda: self.spec.write_text(self.spec.read_text() + "\n"),
            lambda: self.png.write_bytes(b"a changed preview"),
            lambda: self.pptx.write_bytes(b"a changed deck"),
            lambda: self.png.unlink(),
        ]
        originals = {p: p.read_bytes() for p in [self.manifest, self.spec, self.png, self.pptx]}
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                for path, content in originals.items():
                    path.write_bytes(content)
                mutate()
                code, payload = self.run_review()
                self.assertEqual(code, 1)
                self.assertEqual(payload["status"], "unreviewed")
                self.assertEqual(self.calls, 0)
                self.assertEqual(len(payload["slides"]), 1)

    def test_wrong_manifest_slide_id_stops_before_model_calls(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["slides"][0]["slide_id"] = "another-slide"
        self.manifest.write_text(json.dumps(manifest))
        code, payload = self.run_review()
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "unreviewed")
        self.assertEqual(self.calls, 0)

    def test_legacy_manifest_cannot_claim_asset_verification(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["schema_version"] = 1
        self.manifest.write_text(json.dumps(manifest))
        code, payload = self.run_review()
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "unreviewed")
        self.assertEqual(self.calls, 0)

    def test_input_changed_during_review_invalidates_report(self):
        self.during_call = lambda: self.png.write_bytes(b"new generation")
        code, payload = self.run_review()
        self.assertEqual(self.calls, 1)
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "unreviewed")

    def add_nested_asset(self):
        asset = self.root / "figure.png"
        asset.write_bytes(b"original source image")
        source = json.loads(self.spec.read_text())
        source["slides"][0]["elements"].append({
            "id": "group", "type": "group", "x": 0, "y": 1, "w": 3, "h": 2,
            "children": [{"id": "figure", "type": "image", "path": "figure.png",
                          "sha256": digest(asset), "x": 0, "y": 0, "w": 3, "h": 2}],
        })
        self.spec.write_text(json.dumps(source))
        manifest = json.loads(self.manifest.read_text())
        manifest["spec_sha256"] = digest(self.spec)
        manifest["assets"] = [{"slide_id": "result", "element_id": "figure",
                               "path": "figure.png", "sha256": digest(asset)}]
        self.manifest.write_text(json.dumps(manifest))
        return asset

    def test_changed_nested_image_asset_stops_before_model_calls(self):
        asset = self.add_nested_asset()
        asset.write_bytes(b"changed source image")
        code, payload = self.run_review()
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "unreviewed")
        self.assertEqual(self.calls, 0)

    def test_asset_changed_during_review_invalidates_report(self):
        asset = self.add_nested_asset()
        self.during_call = lambda: asset.write_bytes(b"changed during review")
        code, payload = self.run_review()
        self.assertEqual(self.calls, 1)
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "unreviewed")

    def test_output_cannot_overwrite_spec_or_render_inputs(self):
        for target in [self.spec, self.png, self.manifest, self.pptx]:
            with self.subTest(target=target):
                before = target.read_bytes()
                argv = self.argv[:-1] + [str(target)]
                with self.backend():
                    self.assertEqual(review.main(argv), 1)
                self.assertEqual(target.read_bytes(), before)
                self.assertEqual(self.calls, 0)

    def test_output_cannot_overwrite_source_image_or_its_file_aliases(self):
        asset = self.add_nested_asset()
        original = asset.read_bytes()
        symbolic = self.root / "figure-symbolic.png"
        symbolic.symlink_to(asset)
        hard = self.root / "figure-hard.png"
        os.link(asset, hard)
        for target in [asset, symbolic, hard]:
            for dry_run in [False, True]:
                with self.subTest(target=target, dry_run=dry_run):
                    asset.write_bytes(original)
                    argv = self.argv[:-1] + [str(target)] + (["--dry-run"] if dry_run else [])
                    with patch.object(review, "create_critic", side_effect=AssertionError("no provider")):
                        code = review.main(argv)
                    self.assertEqual(asset.read_bytes(), original)
                    self.assertEqual(code, 1)

    def test_bad_hash_or_invalid_slide_cannot_write_error_report_over_asset(self):
        asset = self.add_nested_asset()
        source = json.loads(self.spec.read_text())
        for invalid_context in [False, True]:
            for dry_run in [False, True]:
                with self.subTest(invalid_context=invalid_context, dry_run=dry_run):
                    asset.write_bytes(b"changed source with stale declared hash")
                    current = json.loads(json.dumps(source))
                    if invalid_context:
                        del current["slides"][0]["title"]
                    self.spec.write_text(json.dumps(current))
                    before = asset.read_bytes()
                    argv = self.argv[:-1] + [str(asset)] + (["--dry-run"] if dry_run else [])
                    self.assertEqual(review.main(argv), 1)
                    self.assertEqual(asset.read_bytes(), before)

    def test_missing_source_asset_is_still_protected_as_an_output_path(self):
        asset = self.add_nested_asset()
        asset.unlink()
        code = review.main(self.argv[:-1] + [str(asset), "--dry-run"])
        self.assertEqual(code, 1)
        self.assertFalse(asset.exists())

    def test_output_cannot_overwrite_hardlinked_spec_or_preview(self):
        for source in [self.spec, self.png, self.manifest, self.pptx]:
            with self.subTest(source=source):
                before = source.read_bytes()
                alias = self.root / (source.name + ".alias")
                os.link(source, alias)
                code = review.main(self.argv[:-1] + [str(alias), "--dry-run"])
                self.assertEqual(source.read_bytes(), before)
                self.assertEqual(code, 1)

    def test_output_alias_created_during_review_cannot_overwrite_source(self):
        asset = self.add_nested_asset()
        original = asset.read_bytes()
        self.during_call = lambda: self.output.symlink_to(asset)
        with self.backend():
            code = review.main(self.argv)
        self.assertEqual(code, 1)
        self.assertEqual(self.calls, 1)
        self.assertEqual(asset.read_bytes(), original)

    def test_dry_run_does_not_need_backend_or_claim_review(self):
        self.manifest.unlink()
        with patch.dict("sys.modules", {"paperbanana": None}):
            code = review.main(self.argv + ["--dry-run"])
        payload = json.loads(self.output.read_text())
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "dry-run")
        self.assertEqual(self.calls, 0)

if __name__ == "__main__":
    unittest.main()
