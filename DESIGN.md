# fabri — Design System

> Single source of truth for the fabri UI surfaces (the **Roster gallery** and
> **Studio**). Both apps are React + Vite + Tailwind and consume the same tokens
> via `tailwind-preset.cjs` + a CSS-variable theme. This file is the taste
> contract every design change is checked against — no ad-hoc hexes, no off-scale
> spacing, no new aesthetic.

## Identity

**Restrained, warm-dark, editorial.** Slate-not-void backgrounds, a single gold
accent, generous hairlines, quiet motion. The reference bar is Linear / Vercel /
Stripe restraint — *not* a colorful marketing site. It should read as an
engineering product with taste, not a template.

**One deliberate accent.** Gold `--accent` (#d7a13b) means **"this is the one
thing to act on"** — the primary CTA, a pending question, a self-improving badge.
It is never decorative, never a gradient, never applied to more than one focal
point per view. Surfaces and body text own no hue.

**Anti-slop (hard rules).** No indigo/violet "AI purple" gradients. No
gradient/rainbow text. No emoji as iconography (use `lucide-react` / inline SVG).
No templated hero→3-card→CTA skeleton for its own sake. No untouched default
shadcn palette. Depth (hierarchy, flow, a11y) over surface polish.

## Color tokens

Themed via CSS variables on `:root` / `:root[data-theme="light"]`; dark is the
default. Tailwind reads them as semantic names (see preset).

| Token | Dark | Light | Use |
| --- | --- | --- | --- |
| `--bg` | `#0c0d10` | `#f7f6f3` | page background |
| `--surface` | `#131418` | `#ffffff` | card / raised panel |
| `--surface-2` | `#1a1c22` | `#f0efec` | input / hover / chip |
| `--border` | `#24262d` | `#e4e2dc` | hairline |
| `--border-2` | `#33363f` | `#d3d0c8` | emphasized edge / focus ring |
| `--text` | `#e8e9ec` | `#1c1c1e` | tier-1 body |
| `--text-dim` | `#9497a3` | `#5b5c63` | tier-2 labels, meta |
| `--text-faint`| `#7c7f8b` | `#85868f` | tier-3 chrome (keep AA-legible) |
| `--accent` | `#d7a13b` | `#b9822a` | THE accent — CTA / needs-you |
| `--accent-soft`| `rgba(215,161,59,.14)` | `rgba(185,130,42,.12)` | accent wash |
| `--ok` | `#5fbf8f` | `#2f8f63` | success |
| `--err` | `#e2695f` | `#e2695f` | error |

## Type

- Font: system stack — `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, …`.
  Mono: `ui-monospace, "SF Mono", Menlo, …` (install commands, code).
- Scale (rem): eyebrow `.75` (tracking `.14em`, uppercase), meta `.72`, label
  `.78`, body `.95–1.05`, h2 `1.5` (tracking `-.01em`), hero h1
  `clamp(2rem, 5vw, 3.2rem)` (tracking `-.02em`). Line-height 1.5 body, ~1.1 heads.

## Space · radius · shadow · motion

- Spacing: 4px base; Tailwind default scale (0.5rem gaps in cards, 1rem grid gap).
- Radius: `--radius: 10px` cards/panels; `5–6px` chips-with-corners; `999px` pills.
- Shadow (cards, on hover): `0 8px 24px rgba(0,0,0,.28)` dark / `…,.08` light.
- Motion: ease `cubic-bezier(0.32,0.72,0,1)`; durations **150–250ms**;
  purposeful only (hover lift, tab width). Respect `prefers-reduced-motion`.
  No looping/decorative animation.

## Layout

- Content max-width ~`1120px`; hero copy ~`620–760px`. Card grid
  `repeat(auto-fill, minmax(280px, 1fr))`, gap `1rem`.

## Components (conventions)

- **Card** — `--surface`, 1px `--border`, radius 10px; on hover lift + `--border-2`
  + shadow. Category tag (small, cornered), optional `Self-improving` badge in
  `--accent-soft`/`--accent`.
- **Filter chip** — pill; active = `--accent` text + `--border-2`; `aria-pressed`.
- **Install command** — mono, one line, click-to-copy → "Copied" for 1.4s.
  Keyboard-operable button, `aria-label`.
- **Company card** — title + positioning + "N agents across M crews" + member chips.

## Accessibility floor (every surface)

WCAG **AA** contrast (text ≥ 4.5:1, UI ≥ 3:1); a visible focus ring on every
interactive element; full keyboard nav with logical order; semantic HTML/ARIA;
`prefers-reduced-motion` honored. Hierarchy must read **in grayscale** — the eye
lands on the one primary action without relying on the gold.
