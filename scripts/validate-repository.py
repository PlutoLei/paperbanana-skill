#!/usr/bin/env python3
"""Check skill metadata and packaged local Markdown/HTML references, without network."""
import argparse
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml


def validate(root: Path) -> list[str]:
    errors = []
    ignored = {".git", "node_modules", ".venv", "__pycache__", ".claude"}
    for current, directories, names in os.walk(root):
        directories[:] = [d for d in directories if d not in ignored and not (Path(current) / d).is_symlink()]
        for name in sorted(names):
            file = Path(current) / name
            if file.is_symlink():
                continue
            relative = file.relative_to(root)
            if name in {"marketplace.json", "plugin.json"} and ".claude-plugin" in file.parts:
                try:
                    json.loads(file.read_text())
                except (ValueError, OSError) as exc:
                    errors.append(f"{relative}: invalid manifest: {exc}")
            if file.suffix != ".md":
                continue
            text = file.read_text()
            if name == "SKILL.md":
                match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
                try:
                    if not match:
                        raise ValueError("missing YAML frontmatter")
                    data = yaml.safe_load(match.group(1))
                    if not isinstance(data, dict):
                        raise ValueError("frontmatter must be a mapping")
                    for key in ("name", "description"):
                        if not isinstance(data.get(key), str) or not data[key].strip():
                            raise ValueError(f"{key} must be a nonempty string")
                except (yaml.YAMLError, ValueError) as exc:
                    errors.append(f"{relative}: {exc}")
            # Fenced examples are instructions, not references in this document.
            prose = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*(?:\n|$)", "", text)
            links = re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", prose)
            links += re.findall(r"(?:src|href)=[\"']([^\"']+)[\"']", prose)
            for raw in links:
                target = raw.strip().split(' "', 1)[0].strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                path = (file.parent / unquote(parsed.path)).resolve()
                if not path.is_relative_to(root):
                    errors.append(f"{relative}: reference leaves bundle: {target}")
                elif not path.exists():
                    errors.append(f"{relative}: missing local reference: {target}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    failures = validate(Path(args.root).resolve())
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        raise SystemExit(1)
    print("Skill YAML, plugin JSON and local document references are valid.")
