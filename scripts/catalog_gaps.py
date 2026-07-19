#!/usr/bin/env python3
"""Report catalog gaps for the growth loop (see grow_catalog.md).

Reads the built index.json and prints, deterministically:
  - agency count per category (the schema's four categories),
  - the most under-represented category (the suggested next target),
  - every existing agency + company slug (so the loop can dedupe).

Offline and side-effect free — the loop uses it to pick what to generate next.

Usage:
    python3 scripts/catalog_gaps.py          # human-readable
    python3 scripts/catalog_gaps.py --json   # machine-readable
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX = REPO_ROOT / "index.json"

# The fixed category enum (mirrors schema/agency.schema.json).
CATEGORIES = (
    "Engineering & Product",
    "Growth & Marketing",
    "Support & Ops",
    "Research",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    data = json.loads(INDEX.read_text())
    agencies = data.get("agencies", [])
    companies = data.get("companies", [])

    counts = Counter(a.get("category", "?") for a in agencies)
    # Fill zero-count categories so an empty category wins as the gap.
    per_category = {cat: counts.get(cat, 0) for cat in CATEGORIES}
    # Suggested target: fewest agencies, ties broken by the enum order above.
    target = min(CATEGORIES, key=lambda c: (per_category[c], CATEGORIES.index(c)))

    agency_slugs = sorted(a.get("name", "") for a in agencies)
    company_slugs = sorted(c.get("name", "") for c in companies)

    if args.json:
        print(json.dumps({
            "per_category": per_category,
            "suggested_category": target,
            "agency_slugs": agency_slugs,
            "company_slugs": company_slugs,
            "agency_count": len(agencies),
            "company_count": len(companies),
        }, indent=2))
        return 0

    print(f"agencies: {len(agencies)}  companies: {len(companies)}\n")
    print("per category:")
    for cat in sorted(CATEGORIES, key=lambda c: per_category[c]):
        print(f"  {per_category[cat]:>2}  {cat}")
    print(f"\nsuggested next target category: {target}\n")
    print("existing agency slugs (dedupe against these):")
    print("  " + ", ".join(agency_slugs))
    print("\nexisting company slugs:")
    print("  " + ", ".join(company_slugs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
