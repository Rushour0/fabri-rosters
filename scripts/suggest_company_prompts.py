#!/usr/bin/env python3
"""Open reviewable prompt-suggestion issues from durable company memory.

The public deployment runs this helper in watch mode. It is deliberately
opt-in: without ``GITHUB_TOKEN`` it exits before reading or publishing memory.
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import tempfile
import time
from pathlib import Path

import yaml

from fabri.company import compile_company


_LOG = logging.getLogger("fabri-rosters.prompt-improvement")


def suggest_company_prompts(
    catalog_root: Path,
    memory_root: Path,
    repository: str,
) -> int:
    """Submit prompt suggestions for company roots with promoted lessons."""
    company_files = sorted((catalog_root / "companies").glob("*/company.toml"))
    failures = 0
    with tempfile.TemporaryDirectory(prefix="fabri-prompt-suggestions-") as temp:
        compile_root = Path(temp)
        for company_file in company_files:
            company_slug = company_file.parent.name
            try:
                root_config = compile_company(
                    company_file,
                    compile_root / company_slug,
                    run_from=memory_root,
                )
                # Root node ids such as "ceo" recur across companies. Give the
                # suggestion a company-qualified agent name so issue dedup keys
                # cannot collide, without changing the runtime company config.
                config = yaml.safe_load(root_config.read_text())
                config["agent"]["name"] = f"{company_slug}-{config['agent']['name']}"
                suggestion_config = root_config.with_name("prompt-suggestion.yaml")
                suggestion_config.write_text(
                    yaml.safe_dump(config, sort_keys=False, allow_unicode=True)
                )
                result = subprocess.run(
                    [
                        "fabri",
                        "repo",
                        "suggest-prompt",
                        "--config",
                        str(suggestion_config),
                        "--provider",
                        "github",
                        "--repo",
                        repository,
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
            except (OSError, ValueError) as exc:
                failures += 1
                _LOG.warning("could not prepare %s: %s", company_slug, exc)
                continue
            if result.returncode:
                failures += 1
                _LOG.warning(
                    "prompt suggestion failed for %s: %s",
                    company_slug,
                    result.stderr.strip(),
                )
            else:
                _LOG.info("%s: %s", company_slug, result.stdout.strip())
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog-root", type=Path, default=Path("/app/rosters"))
    parser.add_argument("--memory-root", type=Path, default=Path("/app"))
    parser.add_argument("--repo", default="Rushour0/fabri-rosters")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval-seconds", type=int, default=24 * 60 * 60)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if not os.environ.get("GITHUB_TOKEN"):
        _LOG.info("GITHUB_TOKEN is not set; automatic prompt suggestions are disabled")
        return 0

    while True:
        failures = suggest_company_prompts(args.catalog_root, args.memory_root, args.repo)
        if not args.watch:
            return 1 if failures else 0
        time.sleep(max(60, args.interval_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
