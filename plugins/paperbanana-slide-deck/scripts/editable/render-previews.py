#!/usr/bin/env python3
"""Build an editable spec and render its PPTX into verifiable local previews.

Requires Bun plus the plugin dependencies, LibreOffice and Poppler. No model
service is called. The manifest records which spec, PPTX and pages belong to
one render; it is an integrity record, not scientific or security attestation.
"""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from uuid import uuid4

_INPUT_SPEC = importlib.util.spec_from_file_location(
    "paperbanana_render_inputs", Path(__file__).resolve().with_name("render_inputs.py"))
_INPUTS = importlib.util.module_from_spec(_INPUT_SPEC)
_INPUT_SPEC.loader.exec_module(_INPUTS)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_name(name: str) -> bool:
    return name in {"deck.pptx", "deck.pdf", "render-manifest.json"} or bool(
        re.fullmatch(r"slide-\d+\.png", name))


def check_destination(output: Path) -> None:
    if output.is_symlink():
        raise ValueError("output directory must not be a symlink")
    if output.exists():
        if not output.is_dir():
            raise ValueError("output path is not a directory")
        for item in output.iterdir():
            if item.is_symlink() or not item.is_file() or not generated_name(item.name):
                raise ValueError(f"output directory contains an unrelated item: {item.name}")


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)


def publish_bundle(stage: Path, output: Path, names: list[str]) -> None:
    """Swap complete generations; retain a recovery copy if rollback itself fails."""
    bundle = stage / "bundle"
    bundle.mkdir()
    for name in names:
        (stage / name).rename(bundle / name)
    check_destination(output)
    backup = output.with_name(f".{output.name}.backup-{uuid4().hex}")
    previous = output.exists()
    if previous:
        os.replace(output, backup)
    try:
        os.replace(bundle, output)
    except BaseException:
        if previous:
            try:
                os.replace(backup, output)
            except OSError as exc:
                # This directory is outside TemporaryDirectory, so cleanup
                # cannot erase the only complete copy after an I/O failure.
                raise RuntimeError(f"Publication and rollback failed; previous output is at {backup}") from exc
        raise
    if previous:
        try:
            shutil.rmtree(backup)
        except OSError:
            print(f"Render published; previous-output backup remains at {backup}", file=sys.stderr)


def render(spec_path: Path, output: Path) -> dict:
    check_destination(output)
    spec_path = spec_path.resolve()
    spec_bytes = spec_path.read_bytes()
    spec_hash = hashlib.sha256(spec_bytes).hexdigest()
    spec = json.loads(spec_bytes)
    for source in [spec_path, *_INPUTS.source_image_paths(spec, spec_path)]:
        if source.resolve().is_relative_to(output.resolve()):
            raise ValueError("output directory must not contain the spec or any source image")
    assets = _INPUTS.collect_assets(spec, spec_path)
    slide_ids = [slide["id"] for slide in spec["slides"]]
    if not slide_ids or len(set(slide_ids)) != len(slide_ids):
        raise ValueError("spec must contain nonempty slides with unique IDs")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Work beside the destination so publishing uses same-filesystem replaces.
    # An isolated LibreOffice profile avoids another open Office process.
    with tempfile.TemporaryDirectory(prefix=".paperbanana-render-", dir=output.parent) as temp:
        stage = Path(temp)
        deck = stage / "deck.pptx"
        renderer = Path(__file__).resolve().with_name("render-editable-pptx.ts")
        run(["bun", str(renderer), str(spec_path), str(deck)])
        profile = (stage / "office-profile").as_uri()
        run(["soffice", f"-env:UserInstallation={profile}", "--headless", "--convert-to", "pdf",
             "--outdir", str(stage), str(deck)])
        pdf = stage / "deck.pdf"
        if not pdf.is_file():
            raise ValueError("LibreOffice produced no deck.pdf")
        run(["pdftoppm", "-png", "-r", "150", str(pdf), str(stage / "page")])
        raw_pages = sorted(stage.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
        page_numbers = [int(p.stem.split("-")[-1]) for p in raw_pages]
        if page_numbers != list(range(1, len(slide_ids) + 1)):
            raise ValueError("rendered page count/order does not match the spec")
        pages = []
        for index, (slide_id, page) in enumerate(zip(slide_ids, raw_pages), 1):
            normalized = stage / f"slide-{index:02d}.png"
            page.rename(normalized)
            pages.append({"slide_id": slide_id, "index": index,
                          "file": normalized.name, "sha256": sha256(normalized)})
        if sha256(spec_path) != spec_hash:
            raise ValueError("spec changed while rendering; previous output was preserved")
        if _INPUTS.collect_assets(spec, spec_path) != assets:
            raise ValueError("image assets changed while rendering; previous output was preserved")
        manifest = {
            "schema_version": 2, "rendered_at": datetime.now(timezone.utc).isoformat(),
            "spec_sha256": spec_hash,
            "assets": assets,
            "pptx": {"file": "deck.pptx", "sha256": sha256(deck)},
            "slides": pages,
        }
        (stage / "render-manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        names = ["deck.pptx", "deck.pdf", *[p["file"] for p in pages], "render-manifest.json"]
        publish_bundle(stage, output, names)
        return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help="Path to slide-spec.json")
    parser.add_argument("--output-dir", required=True, help="Dedicated generated-preview directory")
    args = parser.parse_args(argv)
    try:
        # Keep the final component unresolved so symlinks are rejected.
        output = Path(args.output_dir).absolute()
        manifest = render(Path(args.spec), output)
    except Exception as exc:
        print(f"Render failed ({type(exc).__name__}): {exc}", file=sys.stderr)
        return 1
    print(f"Rendered {len(manifest['slides'])} slides: {output / 'render-manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
