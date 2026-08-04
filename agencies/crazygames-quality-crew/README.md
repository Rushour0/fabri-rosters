# CrazyGames Quality Crew

Audits a built HTML game against the published
[CrazyGames quality guidelines](https://docs.crazygames.com/requirements/quality/)
and returns **SHIP** or **BLOCK** before a human reviewer ever sees it.

## Why this exists

A real submission — *Choose One Curse*, 2026-08-01 — was rejected with exactly
this, and nothing else:

> The overall quality of the game does not yet meet the expectations of our platform.

Reviewers do not enumerate. That single sentence has to be turned back into a
list of specific, fixable things, and the cheapest place to do that is before the
upload rather than after the rejection. This crew is that list.

It is deliberately harsher than the feedback will be. A gate that passes
everything is worth nothing.

## Shape

Artifact crew. Four specialists, split so each owns one section of the published
guidelines and nothing else — an auditor that owns everything grades on vibes.

| Agent | Owns | Looks for |
|---|---|---|
| `onboarding_auditor` | ON, GP | Can a new player start and learn without being taught? Menus between load and play, controls never shown, instructions that appear only mid-game. |
| `aesthetic_auditor` | AQ, RK | Graphics, **audio**, visual consistency, restricted keys. Checks for silence first and explicitly. |
| `engagement_auditor` | FN, UQ | The core loop, pacing, repetition, device fit, whether it is distinguishable from what is already on the platform. |
| `verdict_writer` | — | Writes `crazygames-audit.md`, applies the verdict rule, drops any finding whose criterion ID is not real. |

The director keeps the harsher reading where auditors disagree. The gate is
cheap; a rejection is not.

## The criteria are a file, not a memory

`workspace/crazygames-quality-criteria.md` holds every criterion transcribed
verbatim, with stable IDs (`ON-1`, `AQ-4`, `FN-8`, …). Every agent reads it at the
start of every run, and every finding must cite an ID from it.

This is the load-bearing design decision. A model asked to "audit against
CrazyGames quality standards" from memory will confidently invent plausible rules,
and sending a creator to fix a rule nobody published is worse than missing one —
it costs real work and buys nothing. The `verdict_writer` drops uncited findings
and says in the report that it dropped them.

When the published guidelines change, re-transcribe that file and update its date.
Do not paraphrase: reviewers quote the wording, so the audit should too.

## Verdict rule

- Any **BLOCK** ⇒ BLOCK.
- Three or more **WARN** ⇒ BLOCK.

The second rule is the point. "Overall quality" is a judgement about accumulation,
and a game can fail it without any single criterion being catastrophic. An
absent-entirely criterion — no audio at all, no onboarding at all — is BLOCK
rather than WARN, because "present but weak" and "missing" are different failures
and only one of them is a rounding error.

## Inputs and output

Reads, relative to the shared `studio/` directory:

- `crazygames-quality-criteria.md` — copied from this agency's `workspace/`
- `build/<slug>/index.html` — the built game

Writes `crazygames-audit.md`: the verdict, one plain-language paragraph, a BLOCK
table and a WARN table (criterion ID, the criterion quoted verbatim, what the game
does instead, the fix), NOTEs that do not affect the verdict, and a
**"What this audit could not check"** section.

That last section is not a hedge. This is a static source review with no browser,
so button delays, response feel, and audio levels are genuinely out of reach.
Naming them keeps the passing verdicts honest — and marks exactly where a runtime
gate would have to take over.

## Run it

```sh
fabri new agency --from gh:Rushour0/fabri-rosters/agencies/crazygames-quality-crew crazygames-quality-crew
cd crazygames-quality-crew
# put the game at studio/build/<slug>/index.html, and the criteria at studio/
fabri --config agent.openai.yaml run "Audit the game with slug choose_one_curse."
```

Needs `OPENAI_API_KEY`. Budget: `max_cost_usd = 0.60` for the crew,
`0.15` per specialist.

## Where it belongs in the pipeline

After the deploy gate, before release. The
[Deployable HTML Verify Crew](../deployable-html-verify-crew/) answers *"does it
boot and obey the contract?"* and the [Game QA Crew](../game-qa-crew/) answers
*"is it playable against its own design?"*. Neither asks the question that
actually got a game rejected: *"would this platform's reviewer take it?"*
