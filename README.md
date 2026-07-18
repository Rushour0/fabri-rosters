# fabri Roster Registry

**fabri is an open-source engine for self-improving AI agencies you build products on.** Each agency retains a memory collection and grows its prompt from its own traces, making future runs cheaper and more reliable. Every agency is COGS-first: it declares a `max_cost_usd` ceiling and reports its real per-run cost. It is an open engine you embed, not a dashboard you rent.

This repository is an installable catalog of fabri agencies. Each directory under `agencies/` is a complete agency package consumable by `fabri new agency --from`.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/bug-triage-crew <dest-name>
```

## Add an agency

Add a directory under `agencies/` containing `agency.toml`, an `agent.openai.yaml` entrypoint, specialist configurations, and a `workspace/`. Then regenerate and check the catalog:

```sh
python3 scripts/build_index.py
python3 scripts/validate.py
```

The generated `index.json` is the registry manifest. Curated collections live under `rosters/`.
