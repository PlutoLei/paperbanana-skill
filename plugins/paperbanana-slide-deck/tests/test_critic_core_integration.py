"""Opt-in offline integration against a separately installed/pinned core tree.

PAPERBANANA_CORE_PATH must point to the intended core checkout. Run with that
checkout's dependencies installed. Only the VLM's network boundary is replaced;
the real Settings, CriticAgent, image loader, templates and response parser run.
"""

import contextlib
import json
import os
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch

import test_review_editable as contract


CORE_PATH = os.environ.get("PAPERBANANA_CORE_PATH")


@unittest.skipUnless(CORE_PATH, "Set PAPERBANANA_CORE_PATH for pinned-core offline integration")
class CoreIntegrationTest(contract.ReviewContractTest):
    def setUp(self):
        super().setUp()
        self.raw_response = None
        sys.path.insert(0, str(Path(CORE_PATH).resolve()))
        self.addCleanup(lambda: sys.path.remove(str(Path(CORE_PATH).resolve())))
        import paperbanana
        self.assertTrue(Path(paperbanana.__file__).resolve().is_relative_to(Path(CORE_PATH).resolve()))
        from PIL import Image
        Image.new("RGB", (16, 9), "white").save(self.png)
        manifest = json.loads(self.manifest.read_text())
        manifest["slides"][0]["sha256"] = contract.digest(self.png)
        self.manifest.write_text(json.dumps(manifest))

    @contextlib.contextmanager
    def backend(self):
        test = self
        # This is a deliberately credential-free environment and directory.
        old_cwd = Path.cwd()
        os.chdir(self.root)
        try:
            with patch.dict(os.environ, {"VLM_PROVIDER": "gemini", "VLM_MODEL": "configured-model",
                                         "OPENAI_VLM_MODEL": "saved-openai-model"}, clear=True):
                from paperbanana.providers.base import VLMProvider
                from paperbanana.providers.registry import ProviderRegistry

                class OfflineVLM(VLMProvider):
                    def __init__(self, settings):
                        self.settings = settings

                    @property
                    def name(self):
                        return self.settings.vlm_provider

                    @property
                    def model_name(self):
                        return self.settings.effective_vlm_model

                    async def generate(self, prompt, images=None, system_prompt=None,
                                       temperature=1.0, max_tokens=16384, response_format=None):
                        test.calls += 1
                        test.assertIn("Sample result", prompt)
                        test.assertEqual(len(images), 1)
                        if test.failure:
                            raise test.failure
                        if test.during_call:
                            test.during_call()
                        if test.raw_response is not None:
                            return test.raw_response
                        if isinstance(test.suggestions, str):
                            return test.suggestions
                        return json.dumps({"critic_suggestions": test.suggestions,
                                           "score": test.score, "revised_description": None})

                with patch.object(ProviderRegistry, "create_vlm", side_effect=OfflineVLM), \
                        patch.object(socket.socket, "connect", side_effect=AssertionError("network forbidden")):
                    yield
        finally:
            os.chdir(old_cwd)

    def test_raw_invalid_scores_and_missing_suggestions_cannot_be_normalized_into_success(self):
        responses = [
            {"critic_suggestions": [], "score": "NaN"},
            {"critic_suggestions": [], "score": 999},
            {"critic_suggestions": [], "score": True},
            {"score": 9},
            {"critic_suggestions": [], "score": "9"},
            {"critic_suggestions": [], "score": float("nan")},
            {"critic_suggestions": [], "score": float("inf")},
            {"critic_suggestions": [], "score": -1},
        ]
        for response in responses:
            with self.subTest(response=response):
                self.raw_response = json.dumps(response)
                code, payload = self.run_review()
                self.assertEqual(code, 1)
                self.assertEqual(payload["status"], "unreviewed")
                self.assertIsNone(payload["score"])


if __name__ == "__main__":
    unittest.main()
