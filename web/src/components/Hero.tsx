import { ArrowRight, BookOpen } from "lucide-react";

export function Hero({ agencyCount, companyCount }: { agencyCount: number; companyCount: number }) {
  const scrollToAgencies = (e: React.MouseEvent) => {
    e.preventDefault();
    document.getElementById("agencies")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <section className="relative overflow-hidden">
      {/* Subtle blue glow behind the headline — static, no motion. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10"
        style={{
          background:
            "radial-gradient(48rem 28rem at 18% 12%, var(--accent-soft), transparent 70%)",
        }}
      />
      <div className="mx-auto max-w-content px-5 pt-20 pb-16 sm:pt-28 sm:pb-20">
        <div className="max-w-prose">
          <p className="text-eyebrow font-medium uppercase text-accent-2">
            Open engine for agent companies
          </p>
          <h1 className="mt-4 text-4xl font-semibold leading-[1.05] tracking-tight text-ink sm:text-5xl md:text-6xl">
            Hire a company of AI agents.
          </h1>
          <p className="mt-5 text-lg leading-relaxed text-ink-dim">
            Small, self-improving, COGS-instrumented agencies that run in your tools — they get
            cheaper and better every run, on an open engine you can fork and own.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <a
              href="#agencies"
              onClick={scrollToAgencies}
              className="inline-flex items-center gap-2 rounded-lg bg-accent px-4 py-2.5 text-sm font-semibold text-white shadow-[0_6px_20px_-6px_var(--accent)] transition-transform ease-fabri hover:-translate-y-0.5"
            >
              Browse the roster
              <ArrowRight size={16} aria-hidden />
            </a>
            <a
              href="https://fabri.rushour0.com"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 rounded-lg border border-line-2 px-4 py-2.5 text-sm font-medium text-ink transition-colors ease-fabri hover:bg-surface-2"
            >
              Try the live demo
              <ArrowRight size={15} aria-hidden />
            </a>
            <a
              href={`${import.meta.env.BASE_URL}study.html`}
              className="inline-flex items-center gap-1.5 rounded-lg border border-line-2 px-4 py-2.5 text-sm font-medium text-ink transition-colors ease-fabri hover:bg-surface-2"
            >
              <BookOpen size={15} aria-hidden />
              Read the study pack
            </a>
          </div>

          <p className="mt-6 font-mono text-meta text-ink-faint">
            {agencyCount} agencies · {companyCount} companies · open source
          </p>
        </div>
      </div>
    </section>
  );
}
