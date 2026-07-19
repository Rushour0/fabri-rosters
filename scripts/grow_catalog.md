# Catalog-growth loop — per-iteration recipe

A repeatable recipe for adding **one** new agency (or company) to the catalog per
iteration, gated so nothing broken lands. Driven by a `/loop` task (self-paced):
each firing runs this recipe once and opens **one gated PR**. Merged PRs → `main`
→ the gallery (Pages) and the Coolify demo redeploy automatically.

**Never commit generated entries straight to `main`.** Every iteration ends in a
PR a human reviews and merges.

## Guardrails (check before generating)

1. **Cap open bot PRs.** If there are already **≥ 3** open PRs labeled
   `catalog-bot`, stop this iteration — let the queue drain first.
   ```bash
   gh pr list --repo Rushour0/fabri-rosters --label catalog-bot --state open --json number | jq length
   ```
2. **Dedupe.** The new slug must not collide with any existing agency/company
   slug (see `scripts/catalog_gaps.py` output).
3. **One entry per iteration**, one PR per entry.

## Steps

### 1. Pick the gap
```bash
python3 scripts/catalog_gaps.py
```
Take `suggested next target category` (the thinnest category) unless it's already
covered by an open bot PR — then take the next thinnest. Invent a concrete,
non-duplicate agency idea in that category with a real deliverable (not a vague
"assistant"). Choose a kebab-case `<slug>` ending in a role noun (…-crew,
…-writer, …-brief), consistent with existing slugs.

### 2. Generate the entry (delegate to codex)
Use `codex exec` (see the `codex-exec` skill) driven by the `fabri-agency-builder`
+ `hermes-new-agency-brief` skills. Copy `templates/agency/` to
`agencies/<slug>/` and fill it in, **keeping the placeholders**
`__AGENCY_ROOT__`, `__AGENCY_SLUG__`, `__RUN_FROM__` intact (the installer
substitutes them). The entry must satisfy `schema/agency.schema.json`:

- `agency.toml` — `[agency]` with `name,title,tagline,category,deliverable,
  entry`; `[agency.stats]` `agents,tools`; `[agency.cogs]` `max_cost_usd,provider`;
  `[agency.wedge]` `self_improving,cogs_reported`. `category` MUST be one of the
  four enum values. `entry` MUST point at a real file in the dir.
- `agent.openai.yaml` (manager) + one `*.openai.yaml` per specialist, wired via
  `tools.agents[]`, `sandbox_root: __AGENCY_ROOT__/workspace`, memory
  `collection: __AGENCY_SLUG__…`, `sqlite_path: __RUN_FROM__/.fabri/__AGENCY_SLUG__.db`.
- `README.md` + a `workspace/` dir (with `.gitignore` + `README.md`).

`stats.agents`/`stats.tools` must match what the YAML actually declares. Keep
`max_cost_usd` modest (≤ 0.50). For a **company** instead, add
`companies/<slug>/company.toml` composing existing agency slugs (exactly one root
node with `report_to = ""`; every `agency = "../../agencies/<slug>"` must exist).

### 3. Gate (all must pass — no PR otherwise)
```bash
python3 scripts/build_index.py        # regenerate index.json from the TOML sources
python3 scripts/validate.py           # schema + reference checks
fabri new agency "ci-<slug>" --from "./agencies/<slug>" --dest "/tmp/ci-<slug>"
fabri --config "/tmp/ci-<slug>/ci-<slug>/agent.openai.yaml" run --dry-run "smoke"
```
(For a company: `fabri company compile companies/<slug>/company.toml --dest
/tmp/ci-<slug>` then a dry-run of the compiled root.) If any step fails, **discard
the changes** (`git checkout -- . && git clean -fd agencies/<slug>`) and either
retry a different idea or end the iteration. Do not open a broken PR.

### 4. Open the gated PR
```bash
git checkout -b catalog/<slug>
git add agencies/<slug> index.json          # (or companies/<slug>)
git commit -m "catalog: add <slug> (<Category>)"
git push -u origin catalog/<slug>
gh pr create --repo Rushour0/fabri-rosters --label catalog-bot \
  --title "catalog: add <slug>" \
  --body "Auto-generated <Category> agency. Gates passed: build_index + validate + fabri dry-run. Review the prompts/deliverable before merging."
```
The repo's `ci.yml` re-runs validate + dry-run on the PR, so the gate is enforced
server-side too. Nothing goes live until a human merges.

> First run: create the `catalog-bot` label once —
> `gh label create catalog-bot -c "#d7a13b" -d "Auto-generated catalog entries" --repo Rushour0/fabri-rosters`
