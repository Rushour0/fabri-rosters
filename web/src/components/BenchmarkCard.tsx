import type { BenchmarkRecord } from "../types";

function formatPercent(value?: number): string {
  return value == null ? "—" : `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })}%`;
}

function formatCurrency(value?: number): string {
  return value == null
    ? "—"
    : value.toLocaleString(undefined, { style: "currency", currency: "USD", maximumFractionDigits: 2 });
}

function formatNumber(value?: number): string {
  return value == null ? "—" : value.toLocaleString();
}

export function BenchmarkCard({ record }: { record: BenchmarkRecord }) {
  const quality = record.quality;
  const cost = record.cost;

  return (
    <article className="flex flex-col gap-2.5 rounded-card border border-line bg-surface p-4 transition-[transform,border-color,box-shadow] duration-200 ease-fabri hover:-translate-y-0.5 hover:border-line-2 hover:shadow-card">
      <div className="flex flex-wrap items-center gap-2">
        {record.subject_type && (
          <span className="rounded-md bg-surface-2 px-2 py-0.5 text-meta font-medium text-ink-dim">
            {record.subject_type}
          </span>
        )}
        {record.control_memory_free && (
          <span className="rounded-md bg-surface-2 px-2 py-0.5 text-meta font-medium text-ink-dim">
            Verified no-memory control
          </span>
        )}
      </div>

      <div>
        <h3 className="text-[1.05rem] font-semibold leading-snug text-ink">
          {record.subject || "Untitled benchmark"}
        </h3>
        <p className="mt-1 text-sm leading-relaxed text-ink-dim">
          {[record.benchmark, record.date].filter(Boolean).join(" · ")}
        </p>
      </div>

      <div className="border-t border-line pt-2.5">
        <p className="text-[0.68rem] font-medium uppercase tracking-wider text-ink-faint">
          Quality (corrected)
        </p>
        <p className="mt-1 text-sm text-ink">
          memory {formatPercent(quality?.memory_corrected_pct)} · control {formatPercent(quality?.control_corrected_pct)}
        </p>
        <p className="mt-1 text-meta text-ink-faint">
          Raw: memory {formatPercent(quality?.memory_raw_pct)} · control {formatPercent(quality?.control_raw_pct)}
        </p>
      </div>

      <div>
        <p className="text-[0.68rem] font-medium uppercase tracking-wider text-ink-faint">Cost</p>
        <p className="mt-1 text-sm text-ink">{cost?.verdict || "No verdict reported"}</p>
        <dl className="mt-1.5 flex flex-wrap gap-x-3 gap-y-1 text-meta text-ink-dim">
          <div>
            <dt className="sr-only">Clean pairs</dt>
            <dd>{formatNumber(cost?.clean_pairs)} clean pairs</dd>
          </div>
          <div>
            <dt className="sr-only">Memory cheaper pairs</dt>
            <dd>{formatNumber(cost?.memory_cheaper_pairs)} memory-cheaper pairs</dd>
          </div>
          <div>
            <dt className="sr-only">Sign test p-value</dt>
            <dd>p = {formatNumber(cost?.sign_test_p)}</dd>
          </div>
        </dl>
      </div>

      <div className="mt-auto flex flex-wrap items-center justify-between gap-2 border-t border-line pt-2.5">
        <p className="font-mono text-meta text-ink-faint">
          {formatCurrency(record.spend_usd)} spend · {formatNumber(record.replicas)} replicas
        </p>
        {record.report_url && (
          <a
            href={record.report_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-ink-dim underline-offset-4 hover:text-ink hover:underline"
          >
            Read report
          </a>
        )}
      </div>
    </article>
  );
}
