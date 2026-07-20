# Game Idea Crew

Turns a theme or brief into three distinct freeform playable-ad game concepts, one per mechanic where possible. The only allowed mechanics are `launch`, `drop`, and `match`.

Input: a theme or brief.
Output: `concepts.md` written into the shared studio workspace — three concepts, each with a working title, its mechanic (launch|drop|match), a one-line hook, and why it suits a ~10-second playable ad.

Cost ceiling: `max_cost_usd = 0.20` (openai).

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/game-idea-crew game-idea-crew
```
