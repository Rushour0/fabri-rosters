# fabri Roster Registry

![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)

**fabri is an open-source engine for self-improving AI agencies you build products on.** Each agency retains a memory collection and grows its prompt from its own traces, making future runs cheaper and more reliable. Every agency is COGS-first: it declares a `max_cost_usd` ceiling and reports its real per-run cost. It is an open engine you embed, not a dashboard you rent.

This repository is an installable catalog of fabri agencies. Browse the [live gallery](https://rushour0.github.io/fabri-rosters/) or follow the [demo walkthrough](DEMO.md). Each directory under `agencies/` is a complete agency package consumable by `fabri new agency --from`.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/bug-triage-crew <dest-name>
fabri company compile companies/acme-eng/company.toml --dest <dest-dir>
```

Companies compiled with Fabri 0.18.3+ have an institutional-memory collection
at `<run-dir>/.fabri/<memory_namespace>.db`. The root manager learns from every
company task and retrieves durable decisions and insights on later runs; leaf
agencies keep their own specialized collections.

## Layout

- `agencies/` — installable agencies
- `companies/` — multi-level company definitions
- `rosters/` — curated collections
- `site/` — static gallery
- `scripts/` — catalog build and validation tools
- `templates/` — copy-me starting points

## Run an agency from Slack, GitHub, or Linear

Every entry in this catalog can be run from a connected workspace, not only from
Studio. Connect the workspace in Studio's **Settings** tab, then:

| Where | What you type | What comes back |
|---|---|---|
| Slack | `@fabri run <name> <task>` | the result in-thread, with its cost |
| Slack | `@fabri list` | the entries you can run |
| GitHub | `/fabri run <name> <task>` in an issue or PR comment | a comment on the same thread |
| Linear | label an issue `fabri:<name>` | a comment on the issue |

`<name>` is the entry's `name` in `index.json` — for example
`competitor-teardown-crew` or `escalation-brief-crew`. On Linear the issue
itself is the task, so no extra text is needed.

Runs started this way are capped: one at a time per workspace, a daily run and
spend limit per workspace, and a per-run ceiling that is the lower of the entry's
own `max_cost_usd` and the surface cap. An agent started from a webhook cannot
stop to ask a human a question, because there is nowhere to ask — in Slack it
can, and it will ask in the thread.

## Add an agency

Add a directory under `agencies/` containing `agency.toml`, an `agent.openai.yaml` entrypoint, specialist configurations, and a `workspace/`. Then regenerate and check the catalog:

```sh
python3 scripts/build_index.py
python3 scripts/validate.py
```

The generated `index.json` is the registry manifest. Curated collections live under `rosters/`.
