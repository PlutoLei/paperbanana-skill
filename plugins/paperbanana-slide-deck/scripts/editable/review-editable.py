#!/usr/bin/env python3
"""Preview-only Critic adapter for editable PaperBanana decks.

Sends rendered slide previews (slide-NN.png) through PaperBanana's CriticAgent
and maps each suggestion back to a slide/element ID. This adapter never
modifies the PPTX or the preview PNGs: review findings are applied only by
editing slide-spec.json and rebuilding the deck.

PaperBanana is imported only inside main(), so the mapping helpers stay
importable (and unit-testable) without the package installed. --dry-run writes
the per-slide Critic context as JSON without importing PaperBanana or making
any network call.
"""

import argparse
import asyncio
import hashlib
import importlib.util
import json
import math
import pathlib
import sys
from datetime import datetime, timezone

_INPUT_SPEC = importlib.util.spec_from_file_location(
    "paperbanana_render_inputs", pathlib.Path(__file__).resolve().with_name("render_inputs.py"))
_INPUTS = importlib.util.module_from_spec(_INPUT_SPEC)
_INPUT_SPEC.loader.exec_module(_INPUTS)


def map_suggestions(slide_id: str, element_ids: list[str], suggestions: list[str]) -> list[str]:
    mapped = []
    for suggestion in suggestions:
        owner = next((element_id for element_id in element_ids
                      if suggestion.startswith(f"{element_id}:")), "unmapped")
        text = suggestion.split(':', 1)[1].strip() if owner != "unmapped" else suggestion
        mapped.append(f"{slide_id}/{owner}: {text}")
    return mapped


def collect_element_ids(elements: list[dict]) -> list[str]:
    ids = []
    for element in elements:
        ids.append(element["id"])
        if element.get("type") == "group":
            ids.extend(collect_element_ids(element.get("children", [])))
    return ids


def describe_element(element: dict, offset_x: float = 0.0, offset_y: float = 0.0) -> list[str]:
    x = element["x"] + offset_x
    y = element["y"] + offset_y
    line = (f"- {element['id']} ({element['type']}) "
            f"box x={x:.2f} y={y:.2f} w={element['w']:.2f} h={element['h']:.2f}")
    if element.get("text"):
        line += f" text={json.dumps(element['text'], ensure_ascii=False)}"
    if element.get("rows") is not None:
        line += f" rows={json.dumps(element['rows'], ensure_ascii=False)}"
    if element.get("series") is not None:
        line += f" series={json.dumps(element['series'], ensure_ascii=False)}"
    if element.get("alt_text"):
        line += f" alt_text={json.dumps(element['alt_text'], ensure_ascii=False)}"
    lines = [line]
    if element.get("type") == "group":
        for child in element.get("children", []):
            lines.extend(describe_element(child, x, y))
    return lines


def build_slide_context(slide: dict, rendered_dir: pathlib.Path, index: int) -> dict:
    preview = rendered_dir / f"slide-{index:02d}.png"
    description_lines = [f"Slide {index}: {slide['title']}", "Elements:"]
    for element in slide["elements"]:
        description_lines.extend(describe_element(element))
    return {
        "slide_id": slide["id"],
        "index": index,
        "title": slide["title"],
        "preview_png": str(preview),
        "preview_exists": preview.exists(),
        "element_ids": collect_element_ids(slide["elements"]),
        "description": "\n".join(description_lines),
        "source_context": slide["speaker_notes"],
    }


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Review rendered editable-deck previews with PaperBanana Critic.")
    parser.add_argument("--spec", required=True, help="Path to slide-spec.json")
    parser.add_argument("--rendered-dir", required=True,
                        help="Directory produced by render-previews.py (includes render-manifest.json)")
    parser.add_argument("--output", required=True, help="Review JSON path outside rendered-dir")
    parser.add_argument("--vlm-provider", default=None, help="Critic VLM provider override")
    parser.add_argument("--vlm-model", default=None, help="Critic VLM model override")
    parser.add_argument("--dry-run", action="store_true",
                        help="Write per-slide Critic context only; no PaperBanana import, no network")
    return parser.parse_args(argv)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_output(path: str, payload: dict) -> None:
    pathlib.Path(path).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_output_path(output: pathlib.Path, spec_path: pathlib.Path,
                      rendered_dir: pathlib.Path, spec) -> None:
    """Reject input aliases before dry-run, error, or review report writes."""
    resolved = output.resolve()
    if resolved.is_relative_to(rendered_dir.resolve()):
        raise ValueError("review output must be outside rendered-dir")
    protected = [spec_path, *_INPUTS.source_image_paths(spec, spec_path),
                 rendered_dir / "deck.pptx", rendered_dir / "deck.pdf",
                 rendered_dir / "render-manifest.json", *rendered_dir.glob("slide-*.png")]
    for source in protected:
        if (resolved == source.resolve()
                or (output.exists() and source.exists() and output.samefile(source))):
            raise ValueError("review output must not overwrite the spec, a source image, or a render input")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_render_inputs(spec_path: pathlib.Path, rendered_dir: pathlib.Path,
                         contexts: list[dict]) -> dict:
    """Validate the build/render record before constructing any remote provider.

    This establishes correspondence to the recorded render, not scientific
    correctness or cryptographic attestation of an untrusted manifest.
    """
    manifest_path = rendered_dir / "render-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 2:
        raise ValueError("render manifest v2 required; run render-previews.py again")
    if manifest.get("spec_sha256") != sha256(spec_path):
        raise ValueError("spec changed after rendering; run render-previews.py again")
    assets = _INPUTS.collect_assets(json.loads(spec_path.read_text(encoding="utf-8")), spec_path)
    if manifest.get("assets") != assets:
        raise ValueError("image assets do not match the render manifest")
    pptx = manifest.get("pptx", {})
    if pptx.get("file") != "deck.pptx" or pptx.get("sha256") != sha256(rendered_dir / "deck.pptx"):
        raise ValueError("PPTX does not match the render manifest")
    pages = manifest.get("slides")
    if not isinstance(pages, list) or len(pages) != len(contexts):
        raise ValueError("rendered page count does not match the spec")
    for context, page in zip(contexts, pages):
        expected_name = f"slide-{context['index']:02d}.png"
        if (page.get("slide_id") != context["slide_id"]
                or page.get("index") != context["index"] or page.get("file") != expected_name):
            raise ValueError("rendered slide identity/order does not match the spec")
        if page.get("sha256") != sha256(rendered_dir / expected_name):
            raise ValueError(f"preview changed after rendering: {expected_name}")
    return {"spec_sha256": manifest["spec_sha256"], "pptx": pptx,
            "assets": assets, "slides": pages, "manifest_sha256": sha256(manifest_path)}


def create_critic(args):
    # Imported only after local validation; --dry-run never imports PaperBanana.
    from paperbanana.agents.critic import CriticAgent
    from paperbanana.core.config import Settings
    from paperbanana.core.types import DiagramType
    from paperbanana.core.utils import find_prompt_dir
    from paperbanana.providers.registry import ProviderRegistry

    class StrictCriticAgent(CriticAgent):
        def _parse_response(self, response):
            # Validate before the core parser can coerce strings/bools, clamp
            # scores, or turn missing suggestions into a positive evaluation.
            validate_raw_response(response)
            return super()._parse_response(response)

    settings = Settings()
    if args.vlm_provider:
        settings.vlm_provider = args.vlm_provider
    if args.vlm_model:
        settings.vlm_model = args.vlm_model
        # Provider-specific environment settings otherwise override VLM_MODEL.
        model_field = {"gemini": "google_vlm_model", "openai": "openai_vlm_model",
                       "openai_local": "openai_vlm_model", "bedrock": "bedrock_vlm_model",
                       "ollama": "ollama_model", "litellm": "litellm_model"}.get(
                           settings.vlm_provider.lower())
        if model_field:
            setattr(settings, model_field, args.vlm_model)
    provider = ProviderRegistry.create_vlm(settings)
    critic = StrictCriticAgent(provider, prompt_dir=settings.prompt_dir or find_prompt_dir())
    return critic, provider, DiagramType.SLIDE


def validate_raw_response(response: str) -> None:
    def invalid_constant(value):
        raise ValueError(f"non-finite JSON number: {value}")

    if not isinstance(response, str):
        raise ValueError("Critic response must be a JSON string")
    data = json.loads(response, parse_constant=invalid_constant)
    if not isinstance(data, dict) or "critic_suggestions" not in data:
        raise ValueError("Critic response must include critic_suggestions")
    suggestions = data["critic_suggestions"]
    if not isinstance(suggestions, list) or not all(isinstance(item, str) and item.strip()
                                                   for item in suggestions):
        raise ValueError("Critic response contains invalid critic_suggestions")
    score = data.get("score")
    if score is not None and (isinstance(score, bool) or not isinstance(score, (int, float))
                              or not math.isfinite(score) or not 0 <= score <= 10):
        raise ValueError("Critic response score must be a finite number from 0 to 10")
    revised = data.get("revised_description")
    if revised is not None and not isinstance(revised, str):
        raise ValueError("Critic response revised_description must be a string or null")
    if not suggestions and score is None:
        raise ValueError("Critic response contains no usable evaluation evidence")


def unreviewed(context: dict, error: str, detail: str) -> dict:
    return {"slide_id": context["slide_id"], "status": "unreviewed",
            "error": error, "detail": detail, "score": None, "summary": "Review incomplete.",
            "raw_suggestions": [], "suggestions": []}


def interpret_result(context: dict, result) -> dict:
    suggestions = getattr(result, "critic_suggestions", None)
    if not isinstance(suggestions, list) or not all(isinstance(item, str) and item.strip()
                                                   for item in suggestions):
        raise ValueError("Critic returned invalid critic_suggestions")
    score = getattr(result, "score", None)
    if score is not None and (isinstance(score, bool) or not isinstance(score, (int, float))
                              or not math.isfinite(score) or not 0 <= score <= 10):
        raise ValueError("Critic returned an invalid score")
    # The public core can turn JSON parse failure into empty, unscored feedback.
    if not suggestions and score is None:
        raise ValueError("Critic returned no usable evaluation evidence")
    return {
        "slide_id": context["slide_id"],
        "status": "needs-revision" if suggestions else "reviewed",
        "score": score,
        "summary": "; ".join(suggestions[:3]) if suggestions else "Automated review returned no suggestions.",
        "raw_suggestions": suggestions,
        "suggestions": map_suggestions(context["slide_id"], context["element_ids"], suggestions),
        "revised_description": getattr(result, "revised_description", None),
    }


async def review_slides(critic, contexts: list[dict], diagram_type) -> list[dict]:
    reviews = []
    for context in contexts:
        try:
            result = await critic.run(
                image_path=context["preview_png"],
                description=context["description"],
                source_context=context["source_context"],
                caption=context["title"],
                diagram_type=diagram_type,
                user_feedback="Prefix each suggestion with the affected element ID when identifiable; "
                              "keep other suggestions without inventing an element ID.",
            )
            reviews.append(interpret_result(context, result))
        except Exception as exc:
            # Provider exception bodies may contain request data or credentials.
            reviews.append(unreviewed(context, type(exc).__name__,
                                      "Critic call or response validation failed."))
    return reviews


def main(argv=None) -> int:
    args = parse_args(argv)
    output_path = pathlib.Path(args.output).resolve()
    spec_path = pathlib.Path(args.spec).resolve()
    rendered_dir = pathlib.Path(args.rendered_dir).resolve()
    spec, read_error = None, None
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except Exception as exc:
        read_error = exc
    try:
        check_output_path(output_path, spec_path, rendered_dir, spec)
    except Exception as exc:
        print(f"Unsafe review output ({type(exc).__name__}): {exc}", file=sys.stderr)
        return 1

    def save_report(payload):
        try:
            # Recheck aliases immediately before every write, including errors.
            check_output_path(pathlib.Path(args.output), spec_path, rendered_dir, spec)
            write_output(args.output, payload)
        except Exception as exc:
            print(f"Review report was not written ({type(exc).__name__}): {exc}", file=sys.stderr)
            return False
        return True

    contexts = []
    inputs = {}
    provider_info = None
    try:
        if read_error:
            raise read_error
        contexts = [build_slide_context(slide, rendered_dir, index + 1)
                    for index, slide in enumerate(spec["slides"])]
        if not contexts or len({c["slide_id"] for c in contexts}) != len(contexts):
            raise ValueError("spec must contain nonempty slides with unique IDs")
        if args.dry_run:
            saved = save_report({"status": "dry-run", "reviewed_at": utc_now(),
                                 "alignment": "not-verified", "slides": contexts})
            return 0 if saved else 1
        inputs = verify_render_inputs(spec_path, rendered_dir, contexts)
    except Exception as exc:
        save_report({
            "status": "unreviewed", "error": type(exc).__name__, "detail": str(exc),
            "reviewed_at": utc_now(), "inputs": inputs,
            "slides": [unreviewed(c, type(exc).__name__, "Render inputs could not be verified.")
                       for c in contexts],
        })
        return 1

    try:
        critic, provider, diagram_type = create_critic(args)
        reviews = asyncio.run(review_slides(critic, contexts, diagram_type))
        provider_info = {"name": provider.name, "model": provider.model_name}
        # Detect changes during the review instead of attaching it to a new build.
        if verify_render_inputs(spec_path, rendered_dir, contexts) != inputs:
            raise ValueError("render inputs changed during review")
    except Exception as exc:
        reviews = [unreviewed(c, type(exc).__name__,
                             "Critic setup failed or render inputs changed during review.")
                   for c in contexts]

    failed = any(item["status"] == "unreviewed" for item in reviews)
    needs_revision = any(item["status"] == "needs-revision" for item in reviews)
    scores = [review["score"] for review in reviews if isinstance(review.get("score"), (int, float))]
    payload = {
        "status": "unreviewed" if failed else "needs-revision" if needs_revision else "reviewed",
        "score": min(scores) if scores else None,
        "summary": f"{len(reviews)} slide results; "
                   f"{sum(1 for review in reviews if review['status'] == 'unreviewed')} unreviewed",
        "suggestions": [item for review in reviews for item in review.get("suggestions", [])],
        "reviewed_at": utc_now(),
        "provider": provider_info,
        "inputs": inputs,
        "slides": reviews,
    }
    saved = save_report(payload)
    return 1 if failed or not saved else 0


if __name__ == "__main__":
    sys.exit(main())
