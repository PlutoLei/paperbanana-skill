"""Shared source-asset checks for editable rendering and review."""

import hashlib
from pathlib import Path


def source_image_paths(spec, spec_path: Path) -> list[Path]:
    """Find declared inputs without requiring valid hashes or a valid schema.

    Output collision checks must still protect images when validation fails
    and the caller is about to write an error report.
    """
    base_dir = spec_path.resolve().parent
    paths = []
    pending = [spec]
    while pending:
        node = pending.pop()
        if isinstance(node, dict):
            if node.get("type") == "image" and isinstance(node.get("path"), str) and node["path"]:
                paths.append(base_dir / node["path"])
            pending.extend(node.values())
        elif isinstance(node, list):
            pending.extend(node)
    return paths


def collect_assets(spec: dict, spec_path: Path) -> list[dict]:
    """Return ordered image inputs, including images nested in layout groups.

    Resolve paths exactly as the renderer does, relative to the spec. Checking
    against the declared digest prevents an edited file from being associated
    with a spec which still describes the old asset.
    """
    base_dir = spec_path.resolve().parent
    assets = []

    def visit(slide_id: str, elements: list[dict]) -> None:
        for element in elements:
            if element.get("type") == "image":
                asset_path = element.get("path")
                if not isinstance(asset_path, str) or not asset_path:
                    raise ValueError(f"image path missing: {slide_id}/{element.get('id')}")
                source = (base_dir / asset_path).resolve()
                actual = hashlib.sha256(source.read_bytes()).hexdigest()
                if actual != element.get("sha256"):
                    raise ValueError(f"image asset does not match spec: {slide_id}/{element['id']}")
                assets.append({"slide_id": slide_id, "element_id": element["id"],
                               "path": asset_path, "sha256": actual})
            if element.get("type") == "group":
                visit(slide_id, element.get("children", []))

    for slide in spec["slides"]:
        visit(slide["id"], slide.get("elements", []))
    return assets
