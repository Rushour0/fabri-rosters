import { useEffect, useState } from "react";
import { Github, Moon, Sun } from "lucide-react";

type Theme = "dark" | "light";

function readTheme(): Theme {
  const t = document.documentElement.dataset.theme;
  return t === "light" ? "light" : "dark";
}

export function TopBar() {
  const [theme, setTheme] = useState<Theme>(readTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem("fabri-theme", theme);
    } catch {
      /* ignore */
    }
  }, [theme]);

  return (
    <header className="sticky top-0 z-20 border-b border-line bg-bg/80 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-content items-center justify-between px-5">
        <a href="#top" className="font-mono text-sm font-semibold tracking-tight text-ink">
          fabri
        </a>
        <nav className="flex items-center gap-1 text-sm text-ink-dim">
          <a
            href="#benchmarks"
            className="rounded-md px-3 py-1.5 transition-colors ease-fabri hover:bg-surface-2 hover:text-ink"
          >
            Benchmarks
          </a>
          <a
            href="https://fabri.rushour0.com"
            target="_blank"
            rel="noreferrer"
            className="rounded-md px-3 py-1.5 transition-colors ease-fabri hover:bg-surface-2 hover:text-ink"
          >
            Live demo
          </a>
          <a
            href="https://github.com/Rushour0/fabri-rosters"
            target="_blank"
            rel="noreferrer"
            aria-label="GitHub repository"
            className="rounded-md p-2 transition-colors ease-fabri hover:bg-surface-2 hover:text-ink"
          >
            <Github size={17} aria-hidden />
          </a>
          <button
            type="button"
            onClick={() => setTheme((t) => (t === "dark" ? "light" : "dark"))}
            aria-label={theme === "dark" ? "Switch to light theme" : "Switch to dark theme"}
            className="rounded-md p-2 transition-colors ease-fabri hover:bg-surface-2 hover:text-ink"
          >
            {theme === "dark" ? <Sun size={17} aria-hidden /> : <Moon size={17} aria-hidden />}
          </button>
        </nav>
      </div>
    </header>
  );
}
