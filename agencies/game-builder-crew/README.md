# Game Builder Crew

Reads a game `design.json` from the shared studio and writes a complete,
self-contained HTML "playable ad" game for the engines/web `freeform` genre.

Deliverable: A self-contained `build/<slug>/index.html` playable-ad game
(Canvas2D) that obeys the frozen self-contained-game contract — one file, one
`<canvas>`, the `/*__SPRITES__*/` marker, `window.__smokeReady = true` in the
rAF loop, and no forbidden network/storage/eval tokens.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/game-builder-crew game-builder-crew
```
