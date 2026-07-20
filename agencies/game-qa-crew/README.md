# Game QA Crew

Playtest-reviews a built HTML "playable ad" game (build/<slug>/index.html) against its design.json and goal.md, judging playability and quality — then returns a PASS/FAIL QA report with prioritized fixes. Static source review (no browser).

Deliverable: A qa-report.md with a PASS/FAIL verdict, severity-ranked findings mapped to acceptance criteria, and concrete fixes.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/game-qa-crew game-qa-crew
```
