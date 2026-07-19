import { useState } from "react";
import { Check, Copy } from "lucide-react";
import type { Agency } from "../types";

function installCommand(a: Agency): string {
  return `fabri new agency --from gh:Rushour0/fabri-rosters/${a.path} ${a.name}`;
}

export function AgencyCard({ agency }: { agency: Agency }) {
  const [copied, setCopied] = useState(false);
  const cmd = installCommand(agency);

  const copy = () => {
    const done = () => {
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1400);
    };
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(cmd).then(done, done);
    } else {
      done();
    }
  };

  const cost = agency.max_cost_usd != null ? `$${agency.max_cost_usd}/run` : "no cap set";

  return (
    <article className="group flex flex-col gap-2.5 rounded-card border border-line bg-surface p-4 transition-[transform,border-color,box-shadow] duration-200 ease-fabri hover:-translate-y-0.5 hover:border-line-2 hover:shadow-card">
      <div className="flex flex-wrap items-center gap-2">
        <span className="rounded-md bg-surface-2 px-2 py-0.5 text-meta font-medium text-ink-dim">
          {agency.category || "Uncategorized"}
        </span>
        {agency.self_improving && (
          <span className="rounded-md bg-accent-soft px-2 py-0.5 text-meta font-medium text-accent">
            Self-improving
          </span>
        )}
      </div>

      <h3 className="text-[1.05rem] font-semibold leading-snug text-ink">
        {agency.title || agency.name}
      </h3>
      {agency.tagline && <p className="text-sm leading-relaxed text-ink-dim">{agency.tagline}</p>}

      <p className="font-mono text-meta text-ink-faint">
        {agency.agents ?? "?"} agents · {agency.tools ?? "?"} tools · {cost}
      </p>

      <div className="mt-auto pt-2">
        <p className="mb-1 text-[0.68rem] font-medium uppercase tracking-wider text-ink-faint">
          Install
        </p>
        <button
          type="button"
          onClick={copy}
          aria-label={`Copy install command for ${agency.title || agency.name}`}
          className="flex w-full items-center gap-2 rounded-md border border-line bg-surface-2 px-2.5 py-2 text-left font-mono text-[0.72rem] text-ink-dim transition-colors ease-fabri hover:border-line-2 hover:text-ink"
        >
          <span className="min-w-0 flex-1 truncate">{cmd}</span>
          {copied ? (
            <span className="flex shrink-0 items-center gap-1 text-ok">
              <Check size={13} aria-hidden /> Copied
            </span>
          ) : (
            <Copy size={13} aria-hidden className="shrink-0 opacity-60 group-hover:opacity-100" />
          )}
        </button>
      </div>
    </article>
  );
}
