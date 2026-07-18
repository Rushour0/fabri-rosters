from __future__ import annotations

import json
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def read_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as file:
        return tomllib.load(file)


def flatten_agency(data: dict[str, object], path: str) -> dict[str, object]:
    agency = data["agency"]
    if not isinstance(agency, dict):
        raise ValueError(f"{path}: [agency] must be a table")
    item = {key: value for key, value in agency.items() if not isinstance(value, dict)}
    for table_name in ("stats", "cogs", "wedge"):
        table = agency.get(table_name, {})
        if not isinstance(table, dict):
            raise ValueError(f"{path}: [agency.{table_name}] must be a table")
        item.update(table)
    item["path"] = path
    return item


def flatten_roster(data: dict[str, object], path: str) -> dict[str, object]:
    roster = data["roster"]
    if not isinstance(roster, dict):
        raise ValueError(f"{path}: [roster] must be a table")
    item = dict(roster)
    item["path"] = path
    return item


def main() -> None:
    agencies = [
        flatten_agency(read_toml(path), path.parent.relative_to(REPO_ROOT).as_posix())
        for path in (REPO_ROOT / "agencies").glob("*/agency.toml")
    ]
    rosters = [
        flatten_roster(read_toml(path), path.parent.relative_to(REPO_ROOT).as_posix())
        for path in (REPO_ROOT / "rosters").glob("*/roster.toml")
    ]
    agencies.sort(key=lambda item: str(item["name"]))
    rosters.sort(key=lambda item: str(item["name"]))
    (REPO_ROOT / "index.json").write_text(
        json.dumps({"agencies": agencies, "rosters": rosters}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built index.json with {len(agencies)} agencies and {len(rosters)} rosters.")


if __name__ == "__main__":
    main()
