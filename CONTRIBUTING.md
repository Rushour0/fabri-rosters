# Contributing

## Add an agency

Create `agencies/<name>/` using `templates/agency/` as a starting point. Keep the placeholder contract intact: `__AGENCY_ROOT__`, `__AGENCY_SLUG__`, and `__RUN_FROM__` are replaced during installation. Add `agency.toml` with `name`, `title`, `tagline`, `category`, `deliverable`, and `entry`; `[agency.stats]` with `agents` and `tools`; `[agency.cogs]` with `max_cost_usd` and `provider`; and `[agency.wedge]`.

Regenerate and validate the catalog before opening a PR:

```sh
python3 scripts/build_index.py
python3 scripts/validate.py
```

CI runs the same checks.

## Add a company

Add `companies/<name>/company.toml` with top-level `[[node]]` entries using `id` and `report_to`. Leaf nodes use `agency` paths relative to `company.toml`. Validate the compiled organization with:

```sh
fabri company compile companies/<name>/company.toml --dest <dest-dir>
```
