# Deployable HTML Verify Crew

The deployability gate for the Playable Ad Studio. It boot-smokes a self-contained HTML
"playable ad" game at `build/<slug>/index.html` against the engines/web **frozen boot-smoke
contract** — exactly one `<canvas>`, no external/remote resources, no forbidden
network/storage/eval APIs, and the `window.__smokeReady` boot hook — a direct port of the
engines/web contract. If it passes, the game is deployable into the engines/web `freeform`
genre; if it fails, the crew translates the problems into concrete, ordered repair
instructions for the builder.

The custom `verify_playable_ad` tool runs the boot-smoke and returns `{ok, problems}`; the
`verifier` records the raw verdict to `verify.json` and the `repair_advisor` writes actionable
fixes to `qa-report.md`.

Deliverable: a recorded pass/fail verdict (`verify.json`) plus, on failure, ordered repair
instructions for the builder.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/deployable-html-verify-crew deployable-html-verify-crew
```
