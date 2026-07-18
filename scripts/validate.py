from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_AGENCY_KEYS = ("name", "title", "tagline", "category", "deliverable", "entry")
REQUIRED_INDEX_AGENCY_KEYS = (*REQUIRED_AGENCY_KEYS, "agents", "tools", "max_cost_usd", "provider", "self_improving", "cogs_reported", "path")
REQUIRED_INDEX_ROSTER_KEYS = ("name", "title", "tagline", "positioning", "members", "path")


def read_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as file:
        return tomllib.load(file)


def validate_agency(path: Path) -> None:
    data = read_toml(path)
    agency = data.get("agency")
    if not isinstance(agency, dict):
        raise ValueError(f"{path}: missing [agency] table")
    missing = [key for key in REQUIRED_AGENCY_KEYS if not agency.get(key)]
    if missing:
        raise ValueError(f"{path}: missing required agency fields: {', '.join(missing)}")
    cogs = agency.get("cogs")
    if not isinstance(cogs, dict) or not isinstance(cogs.get("max_cost_usd"), (int, float)):
        raise ValueError(f"{path}: missing [agency.cogs].max_cost_usd")
    entry = agency["entry"]
    if not isinstance(entry, str) or not (path.parent / entry).is_file():
        raise ValueError(f"{path}: entry file does not exist: {entry}")


def validate_index() -> tuple[int, int]:
    index_path = REPO_ROOT / "index.json"
    if not index_path.is_file():
        raise ValueError("index.json: file is missing")
    data = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("index.json: root must be an object")
    agencies = data.get("agencies")
    rosters = data.get("rosters")
    if not isinstance(agencies, list) or not isinstance(rosters, list):
        raise ValueError("index.json: agencies and rosters must be arrays")
    for kind, records, keys in (("agency", agencies, REQUIRED_INDEX_AGENCY_KEYS), ("roster", rosters, REQUIRED_INDEX_ROSTER_KEYS)):
        for record in records:
            if not isinstance(record, dict):
                raise ValueError(f"index.json: {kind} record must be an object")
            missing = [key for key in keys if key not in record]
            if missing:
                raise ValueError(f"index.json: {kind} record missing keys: {', '.join(missing)}")
    return len(agencies), len(rosters)


def main() -> None:
    try:
        paths = sorted((REPO_ROOT / "agencies").glob("*/agency.toml"))
        for path in paths:
            validate_agency(path)
        agency_count, roster_count = validate_index()
    except (OSError, ValueError, json.JSONDecodeError, tomllib.TOMLDecodeError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(f"Validation passed: {len(paths)} agency manifests; index has {agency_count} agencies and {roster_count} rosters.")


if __name__ == "__main__":
    main()
