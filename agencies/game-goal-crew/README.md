# Game Goal Crew

Turns a chosen concept into a validated engines/web `freeform` game spec plus a goal contract.

The goal_framer writes `goal.md` (a one-line fun promise + 3-5 acceptance criteria), then the design_speccer writes `design.json` and runs it through the `validate_design` gate — the crew finishes only when validation returns `ok=true`, fixing any named failures and re-validating first.

Deliverable: A schema-valid `design.json` (engines/web freeform input) plus a `goal.md` with a one-line fun promise and 3-5 acceptance criteria.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/game-goal-crew game-goal-crew
```
