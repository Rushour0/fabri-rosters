"""Validate a game design.json against the engines/web freeform playable-ad schema.

Mirrors the HtmlDesign contract in ludexel-app
engines/web/tools/authoring_html/author.py — including its ``extra="forbid"`` —
so a design that passes here is a valid input for the freeform authoring
pipeline. Standard fabri custom-tool contract: one JSON object on stdin, one
JSON object on stdout matching output_schema; paths are jailed to
$FABRI_SANDBOX_ROOT and the tool refuses to run without it.
"""

import json
import math  # noqa: F401 - kept for parity with the verify tool's numeric guards
import os
import re
import sys
from pathlib import Path

_SLUG = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_MECHANICS = {"launch", "match", "drop"}
_DIFFICULTIES = {"easy", "medium", "hard"}
_ALLOWED_KEYS = {"slug", "game_title", "mechanic", "setting", "style", "palette", "difficulty"}
# field -> (min_len, max_len)
_STR_BOUNDS = {
    "game_title": (1, 100),
    "setting": (10, 800),
    "style": (3, 300),
    "palette": (3, 300),
}
_MAX_BYTES = 64_000  # a design is small JSON; refuse anything pathological.


def check(design: dict) -> list[str]:
    failures: list[str] = []
    # extra="forbid" parity: exactly the seven schema keys, no more, no less.
    extra = set(design) - _ALLOWED_KEYS
    missing = _ALLOWED_KEYS - set(design)
    if extra:
        failures.append(f"unexpected keys (forbidden): {sorted(extra)}")
    if missing:
        failures.append(f"missing required keys: {sorted(missing)}")
    slug = design.get("slug", "")
    # fullmatch, not match: match() would accept a trailing newline before $.
    if not isinstance(slug, str) or not _SLUG.fullmatch(slug) or len(slug) > 64:
        failures.append("slug must match ^[a-z0-9]+(_[a-z0-9]+)*$ and be 1-64 chars")
    if design.get("mechanic") not in _MECHANICS:
        failures.append(f"mechanic must be one of {sorted(_MECHANICS)}")
    if design.get("difficulty") not in _DIFFICULTIES:
        failures.append(f"difficulty must be one of {sorted(_DIFFICULTIES)}")
    for field, (lo, hi) in _STR_BOUNDS.items():
        value = design.get(field)
        if not isinstance(value, str) or not (lo <= len(value) <= hi):
            failures.append(f"{field} must be a string {lo}-{hi} chars")
    return failures


def _sandbox_root() -> Path:
    root = os.environ.get("FABRI_SANDBOX_ROOT")
    if not root:
        raise ValueError("FABRI_SANDBOX_ROOT is not set")
    return Path(root).resolve()


def _sandbox_path(value: str) -> Path:
    root = _sandbox_root()
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path escapes FABRI_SANDBOX_ROOT")
    return path


def _run(args: dict) -> tuple[bool, list[str]]:
    design_path = args.get("design_path")
    if not isinstance(design_path, str) or not design_path:
        return False, ["design_path must be a non-empty string"]
    path = _sandbox_path(design_path)
    if not path.is_file():
        return False, [f"missing design file: {design_path}"]
    if path.stat().st_size > _MAX_BYTES:
        return False, [f"design file exceeds {_MAX_BYTES} bytes"]
    try:
        design = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, [f"design is not valid JSON: {str(exc)[:120]}"]
    if not isinstance(design, dict):
        return False, ["design.json must be a JSON object"]
    failures = check(design)
    return not failures, failures


def main() -> None:
    # Parse INSIDE the guard so malformed stdin still yields schema-shaped JSON.
    args_repr = "<stdin>"
    try:
        args = json.loads(sys.stdin.read())
        if not isinstance(args, dict):
            raise ValueError("tool input must be a JSON object")
        args_repr = str(args.get("design_path"))
        ok, failures = _run(args)
    except Exception as exc:  # noqa: BLE001 - never leak host paths / tracebacks
        print(json.dumps({"ok": False, "failures": [f"{type(exc).__name__} while validating {args_repr}"]}))
        raise SystemExit(1)
    print(json.dumps({"ok": ok, "failures": failures}))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
