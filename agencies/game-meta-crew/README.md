# Game Meta Crew

Writes the engines/web `freeform` catalog metadata for a finished playable-ad game.

The meta_writer reads `studio/design.json` and writes `build/<slug>/_meta.toml` in the exact freeform format the catalog reads (`name`, `platform = "web"`, `genre = "freeform"`, `description`, `vibes = ["playable-ad", <mechanic>, "freeform"]`, `hidden = false`). The copy_polisher then sharpens the description into one vivid, honest sentence and writes a short store blurb to `store-blurb.md`.

Deliverable: A catalog-exact `build/<slug>/_meta.toml` (engines/web freeform format) plus a short, polished store blurb.

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/game-meta-crew game-meta-crew
```
