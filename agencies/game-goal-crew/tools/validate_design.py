"""Validate a game design.json against the engines/web freeform playable-ad schema.

Mirrors the HtmlDesign contract in ludexel-app
engines/web/tools/authoring_html/author.py so a design that passes here is a
valid input for the freeform authoring pipeline. Standard fabri custom-tool
contract: JSON object on stdin, JSON object on stdout; paths jailed to
$FABRI_SANDBOX_ROOT.
"""

import json
import os
import re
import sys
from pathlib import Path

_SLUG = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_MECHANICS = {"launch", "match", "drop"}
_DIFFICULTIES = {"easy", "medium", "hard"}
# field -> (min_len, max_len)
_STR_BOUNDS = {
    "game_title": (1, 100),
    "setting": (10, 800),
    "style": (3, 300),
    "palette": (3, 300),
}


def check(design: dict) -> list[str]:
    failures: list[str] = []
    slug = design.get("slug", "")
    if not isinstance(slug, str) or not _SLUG.match(slug) or len(slug) > 64:
        failures.append(
            "slug must match ^[a-z0-9]+(_[a-z0-9]+)*$ and be 1-64 chars"
        )
    if design.get("mechanic") not in _MECHANICS:
        failures.append(f"mechanic must be one of {sorted(_MECHANICS)}")
    if design.get("difficulty") not in _DIFFICULTIES:
        failures.append(f"difficulty must be one of {sorted(_DIFFICULTIES)}")
    for field, (lo, hi) in _STR_BOUNDS.items():
        value = design.get(field)
        if not isinstance(value, str) or not (lo <= len(value) <= hi):
            failures.append(f"{field} must be a string {lo}-{hi} chars")
    return failures


def _sandbox_path(value: str) -> Path:
    root = Path(os.environ.get("FABRI_SANDBOX_ROOT", ".")).resolve()
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path escapes FABRI_SANDBOX_ROOT")
    return path


def main() -> None:
    args = json.loads(sys.stdin.read())
    design_path = args.get("design_path")
    try:
        path = _sandbox_path(design_path)
        if not path.is_file():
            print(json.dumps({"ok": False, "failures": [f"missing design file: {design_path}"]}))
            raise SystemExit(1)
        try:
            design = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(json.dumps({"ok": False, "failures": [f"design is not valid JSON: {str(exc)[:120]}"]}))
            raise SystemExit(1)
        if not isinstance(design, dict):
            print(json.dumps({"ok": False, "failures": ["design.json must be a JSON object"]}))
            raise SystemExit(1)
        failures = check(design)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - never leak host paths
        print(json.dumps({
            "ok": False,
            "failures": [f"{type(exc).__name__} while validating {design_path}"],
        }))
        raise SystemExit(1)
    print(json.dumps({"ok": not failures, "failures": failures}))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
