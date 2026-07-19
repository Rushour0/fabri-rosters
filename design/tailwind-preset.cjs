// Shared fabri Tailwind preset — see ../DESIGN.md. Copied verbatim into each app
// (the gallery and Studio live in separate repos, so this is a copied preset,
// not an npm package). Colors reference CSS variables defined in theme.css so
// light/dark theming via :root[data-theme] works with the same class names.
//
// Semantic class names (intentionally avoid Tailwind's `border`/`text` collisions):
//   bg-bg  bg-surface  bg-surface-2      surfaces
//   border-line  border-line-2          hairlines
//   text-ink  text-ink-dim  text-ink-faint   text tiers
//   text-accent  bg-accent  bg-accent-soft   THE accent (one focal point/view)
//   text-ok / text-err                    status
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        "surface-2": "var(--surface-2)",
        line: "var(--border)",
        "line-2": "var(--border-2)",
        ink: "var(--text)",
        "ink-dim": "var(--text-dim)",
        "ink-faint": "var(--text-faint)",
        accent: {
          DEFAULT: "var(--accent)",
          soft: "var(--accent-soft)",
        },
        ok: "var(--ok)",
        err: "var(--err)",
      },
      fontFamily: {
        sans: [
          "-apple-system", "BlinkMacSystemFont", '"Segoe UI"', "Roboto",
          "Helvetica", "Arial", "sans-serif",
        ],
        mono: [
          "ui-monospace", '"SF Mono"', "Menlo", "Consolas",
          '"Liberation Mono"', "monospace",
        ],
      },
      borderRadius: {
        DEFAULT: "10px",
        card: "10px",
        pill: "999px",
      },
      boxShadow: {
        card: "0 8px 24px rgba(0, 0, 0, 0.28)",
      },
      transitionTimingFunction: {
        fabri: "cubic-bezier(0.32, 0.72, 0, 1)",
      },
      maxWidth: {
        content: "1120px",
        prose: "760px",
      },
      letterSpacing: {
        eyebrow: "0.14em",
      },
      fontSize: {
        eyebrow: ["0.75rem", { lineHeight: "1.2", letterSpacing: "0.14em" }],
        meta: ["0.72rem", { lineHeight: "1.4" }],
      },
    },
  },
};
