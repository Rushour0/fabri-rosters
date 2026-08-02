import { useEffect, useMemo, useState } from "react";
import { TopBar } from "./components/TopBar";
import { Hero } from "./components/Hero";
import { AgencyCard } from "./components/AgencyCard";
import { BenchmarkCard } from "./components/BenchmarkCard";
import { CompanyCard } from "./components/CompanyCard";
import type { Catalog } from "./types";

const ALL = "All";

export default function App() {
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [active, setActive] = useState<string>(ALL);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}index.json`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load index.json (${res.status})`);
        return res.json();
      })
      .then((data: Catalog) =>
        setCatalog({
          agencies: data.agencies ?? [],
          companies: data.companies ?? [],
          benchmarks: data.benchmarks,
        }),
      )
      .catch((err: Error) => setError(err.message));
  }, []);

  const agencies = catalog?.agencies ?? [];
  const companies = catalog?.companies ?? [];
  const benchmarks = catalog?.benchmarks;
  const benchmarkRecords = benchmarks?.records ?? [];

  const categories = useMemo(() => {
    const set = new Set(agencies.map((a) => a.category || "Uncategorized"));
    return [ALL, ...Array.from(set).sort()];
  }, [agencies]);

  const visible = useMemo(
    () => (active === ALL ? agencies : agencies.filter((a) => (a.category || "Uncategorized") === active)),
    [agencies, active],
  );

  return (
    <div id="top" className="min-h-screen">
      <TopBar />
      <main>
        <Hero agencyCount={agencies.length} companyCount={companies.length} />

        <section
          id="agencies"
          aria-labelledby="agencies-heading"
          className="mx-auto max-w-content px-5 py-4 scroll-mt-16"
        >
          <div className="mb-5">
            <h2 id="agencies-heading" className="text-2xl font-semibold tracking-tight text-ink">
              Agencies
            </h2>
            <p className="mt-1 text-sm text-ink-dim">
              Hire one directly, or fork it as the starting point for your own.
            </p>
          </div>

          <div role="group" aria-label="Filter agencies by category" className="mb-6 flex flex-wrap gap-2">
            {categories.map((cat) => {
              const on = cat === active;
              return (
                <button
                  key={cat}
                  type="button"
                  aria-pressed={on}
                  onClick={() => setActive(cat)}
                  className={
                    "rounded-pill border px-3 py-1 text-sm transition-colors ease-fabri " +
                    (on
                      ? "border-line-2 bg-surface-2 text-accent"
                      : "border-line text-ink-dim hover:border-line-2 hover:text-ink")
                  }
                >
                  {cat}
                </button>
              );
            })}
          </div>

          {error ? (
            <p className="rounded-card border border-line bg-surface p-4 text-sm text-err">
              Could not load the roster: {error}
            </p>
          ) : visible.length === 0 ? (
            <p className="text-sm text-ink-dim">
              {catalog ? "No agencies match this filter." : "Loading the roster…"}
            </p>
          ) : (
            <div
              aria-live="polite"
              className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4"
            >
              {visible.map((a) => (
                <AgencyCard key={a.name} agency={a} />
              ))}
            </div>
          )}
        </section>

        {companies.length > 0 && (
          <section
            aria-labelledby="companies-heading"
            className="mx-auto max-w-content px-5 py-12"
          >
            <div className="mb-5">
              <h2 id="companies-heading" className="text-2xl font-semibold tracking-tight text-ink">
                Companies
              </h2>
              <p className="mt-1 text-sm text-ink-dim">
                Multi-level orgs: several agencies working together as one hire.
              </p>
            </div>
            <div className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4">
              {companies.map((c) => (
                <CompanyCard key={c.name} company={c} />
              ))}
            </div>
          </section>
        )}

        {benchmarkRecords.length > 0 && (
          <section
            id="benchmarks"
            aria-labelledby="benchmarks-heading"
            className="mx-auto max-w-content px-5 py-12 scroll-mt-14"
          >
            <div className="mb-5">
              <h2 id="benchmarks-heading" className="text-2xl font-semibold tracking-tight text-ink">
                Benchmarks
              </h2>
              {benchmarks?.headline && (
                <p className="mt-1 text-sm text-ink-dim">{benchmarks.headline}</p>
              )}
            </div>
            <div className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-4">
              {benchmarkRecords.map((record, index) => (
                <BenchmarkCard
                  key={`${record.subject ?? "benchmark"}-${record.date ?? index}-${index}`}
                  record={record}
                />
              ))}
            </div>
          </section>
        )}
      </main>

      <footer className="mt-8 border-t border-line">
        <div className="mx-auto flex max-w-content flex-wrap items-center justify-between gap-3 px-5 py-8 text-sm text-ink-dim">
          <p>
            Built on <span className="font-semibold text-ink">fabri</span> — an open engine for
            self-improving agencies.
          </p>
          <a
            href="https://github.com/Rushour0/fabri-rosters"
            target="_blank"
            rel="noreferrer"
            className="text-ink-dim underline-offset-4 hover:text-ink hover:underline"
          >
            GitHub
          </a>
        </div>
      </footer>
    </div>
  );
}
