# CrazyGames quality guidelines — the checklist this crew audits against

Transcribed 2026-08-04 from <https://docs.crazygames.com/requirements/quality/>.

**This file is the source of truth for the audit, not the model's memory.** Every
finding must quote the criterion ID and text from this file. A finding that cannot
cite a line here is out of scope and must be dropped — inventing platform rules is
worse than missing one, because it sends a creator to fix something nobody asked for.

Re-transcribe this file when the published guidelines change, and note the date
above. Do not paraphrase the wording: reviewers quote it, and so should we.

---

## ON — Onboarding

| ID | Criterion |
|---|---|
| ON-1 | "Provide a simple onboarding phase where new users land directly" |
| ON-2 | "Implement the onboarding in gameplay" |
| ON-3 | "Focus on the core functionality so users can start playing, avoid explaining every single feature" |
| ON-4 | "Make the onboarding phase skippable" |
| ON-5 | Prioritize visuals; limit text usage |
| ON-6 | "Show the user how to control the game with a keyboard overlay or mouse gestures" |
| ON-7 | "Buttons are clearly labeled to indicate how to proceed" |
| ON-8 | "Buttons are not sized to encourage ads or other behaviors" |
| ON-9 | "Buttons do not have delays to confuse users or encourage other behaviors" |

## GP — General principles

| ID | Criterion |
|---|---|
| GP-1 | "There are clear goals that the player can reach" |
| GP-2 | "The game is easy to learn" |
| GP-3 | "The game is easy to understand — the language is correct and clear, well translated" |
| GP-4 | Game uses universal graphics prompts effectively |
| GP-5 | "The controls are consistent and intuitive throughout the game" |

## FN — Fun experience

| ID | Criterion |
|---|---|
| FN-1 | "The game responds quickly to the player's actions" |
| FN-2 | Challenge, strategy, and story are balanced and well-paced |
| FN-3 | "The display layout is comfortable and intuitive" |
| FN-4 | "The audio is comfortable and appropriate for the game" |
| FN-5 | Game designed for the user's device (desktop, optionally mobile) |
| FN-6 | "Various player segments can enjoy the game" |
| FN-7 | Game story/scenarios are interesting where applicable |
| FN-8 | "There are no overly repetitive or 'boring' tasks" |
| FN-9 | Game processes information quickly for smooth flow |
| FN-10 | Solo and multiplayer are equally prominent if both are offered |
| FN-11 | Solo play unavailability must be clearly explained |

## UQ — Uniqueness

| ID | Criterion |
|---|---|
| UQ-1 | Game should be easily modifiable for new content |
| UQ-2 | Major features/genre must not change post-submission |
| UQ-3 | "The game should be frequently maintained and updated" |
| UQ-4 | Game not easily confused with similar-named or similar-iconography games |
| UQ-5 | Non-IP owners cannot use common identifiers (e.g. "Chess" alone) |

## AQ — Aesthetic quality

| ID | Criterion |
|---|---|
| AQ-1 | Graphics: high resolution |
| AQ-2 | Graphics: consistent throughout |
| AQ-3 | Graphics: free of compression artifacts |
| AQ-4 | Audio: consistent levels |
| AQ-5 | Audio: appropriate volume |
| AQ-6 | Audio: complementary to the visuals |
| AQ-7 | Visual style remains consistent (no switching between realistic/cartoony, high/low resolution) |
| AQ-8 | "The game is clear about what it is. It isn't misleading" |
| AQ-9 | Name and imagery accurately reflect the actual gameplay experience |
| AQ-10 | Name/imagery changes only with significant updates or overhauls |

## RK — Restricted keys

| ID | Criterion |
|---|---|
| RK-1 | Control bindings should adapt to keyboard layout (AZERTY vs QWERTY) |
| RK-2 | Avoid `Escape` (closes fullscreen) |
| RK-3 | Avoid `Ctrl/Cmd + W` (closes the tab; exception: fullscreen mode) |

---

## Severity, and what BLOCK means

A rejection reads *"The overall quality of the game does not yet meet the
expectations of our platform"* — the reviewer does not enumerate. So the audit has
to be harsher than the feedback will be.

- **BLOCK** — a reviewer opening this game would plausibly reject on this alone.
  Any absent-entirely criterion (no audio at all, no onboarding at all) is BLOCK,
  not a warning: "present but weak" and "missing" are different failures.
- **WARN** — real, would not sink the submission by itself, compounds with others.
- **NOTE** — an observation with no criterion behind it. Never counts toward the
  verdict.

**Verdict rule: any BLOCK ⇒ BLOCK.** Three or more WARNs ⇒ BLOCK, because
"overall quality" is a judgement about the accumulation, and that is precisely the
rejection this crew exists to prevent.
