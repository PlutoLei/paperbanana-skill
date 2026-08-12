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
import json
import pathlib
import sys
from datetime import datetime, timezone


def map_suggestions(slide_id: str, element_ids: list[str], suggestions: list[str]) -> list[str]:
    mapped = []
    for suggestion in suggestions:
        owner = next((element_id for element_id in element_ids
                      if suggestion.startswith(f"{element_id}:")), "unmapped")
        mapped.append(f"{slide_id}/{owner}: {suggestion.split(':', 1)[-1].strip()}")
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
                        help="Directory holding slide-NN.png previews")
    parser.add_argument("--output", required=True, help="Path for the review JSON")
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


def main(argv=None) -> int:
    args = parse_args(argv)
    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
    rendered_dir = pathlib.Path(args.rendered_dir)
    contexts = [build_slide_context(slide, rendered_dir, index + 1)
                for index, slide in enumerate(spec["slides"])]

    if args.dry_run:
        write_output(args.output, {
            "status": "dry-run",
            "reviewed_at": utc_now(),
            "slides": contexts,
        })
        return 0

    try:
        # PaperBanana is imported only here so the mapping unit tests and
        # --dry-run never require the package.
        from paperbanana.agents.critic import CriticAgent
        from paperbanana.core.types import DiagramType
    except Exception as exc:
        write_output(args.output, {
            "status": "unreviewed",
            "error": type(exc).__name__,
            "detail": str(exc),
            "reviewed_at": utc_now(),
            "slides": [],
        })
        return 1

    critic_kwargs = {}
    if args.vlm_provider:
        critic_kwargs["vlm_provider"] = args.vlm_provider
    if args.vlm_model:
        critic_kwargs["vlm_model"] = args.vlm_model
    try:
        critic = CriticAgent(**critic_kwargs)
    except Exception as exc:
        write_output(args.output, {
            "status": "unreviewed",
            "error": type(exc).__name__,
            "detail": str(exc),
            "reviewed_at": utc_now(),
            "slides": [],
        })
        return 1

    reviews = []
    failed = False
    for context in contexts:
        try:
            result = critic.run(
                image_path=context["preview_png"],
                description=context["description"],
                source_context=context["source_context"],
                diagram_type=DiagramType.SLIDE,
            )
        except Exception as exc:
            reviews.append({
                "slide_id": context["slide_id"],
                "status": "unreviewed",
                "error": type(exc).__name__,
                "detail": str(exc),
                "score": None,
                "summary": "",
                "suggestions": [],
            })
            failed = True
            continue
        raw_suggestions = list(getattr(result, "suggestions", None) or [])
        reviews.append({
            "slide_id": context["slide_id"],
            "status": str(getattr(result, "status", "reviewed")),
            "score": getattr(result, "score", None),
            "summary": str(getattr(result, "summary", "")),
            "suggestions": map_suggestions(
                context["slide_id"], context["element_ids"], raw_suggestions),
        })

    scores = [review["score"] for review in reviews if isinstance(review.get("score"), (int, float))]
    payload = {
        "status": "unreviewed" if failed else "reviewed",
        "score": min(scores) if scores else None,
        "summary": f"{len(reviews)} slides reviewed; "
                   f"{sum(1 for review in reviews if review['status'] == 'unreviewed')} unreviewed",
        "suggestions": [item for review in reviews for item in review.get("suggestions", [])],
        "reviewed_at": utc_now(),
        "slides": reviews,
    }
    write_output(args.output, payload)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
