import type { Company } from "../types";

function memberName(m: string | { name?: string; title?: string }): string {
  return typeof m === "string" ? m : m.name || m.title || "agency";
}

export function CompanyCard({ company }: { company: Company }) {
  const members = company.member_agencies || company.members || [];
  const nodeCount = company.node_count ?? members.length;
  const crewWord = members.length === 1 ? "crew" : "crews";

  return (
    <article className="flex flex-col gap-2.5 rounded-card border border-line bg-surface p-4 transition-[transform,border-color,box-shadow] duration-200 ease-fabri hover:-translate-y-0.5 hover:border-line-2 hover:shadow-card">
      <h3 className="text-[1.05rem] font-semibold leading-snug text-ink">
        {company.title || company.name || "Untitled company"}
      </h3>
      {company.positioning && (
        <p className="text-sm leading-relaxed text-ink-dim">{company.positioning}</p>
      )}
      <p className="font-mono text-meta text-ink-faint">
        {nodeCount} agents across {members.length} {crewWord}
      </p>
      {members.length > 0 && (
        <ul className="mt-1 flex flex-wrap gap-1.5">
          {members.map((m, i) => (
            <li
              key={i}
              className="rounded-pill bg-surface-2 px-2 py-0.5 text-[0.72rem] text-ink-dim"
            >
              {memberName(m)}
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}
