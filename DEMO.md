# Demo — "fabri as a company"

A ~5-minute walkthrough of the three surfaces: a **catalog** of self-improving
agencies, a **human-in-the-loop** flow, and a **multi-level company** org chart
with live cost. Everything is real — real agents, real per-run COGS.

> Prereqs: `fabri >= 0.19.0, < 0.20` (`pip install -U 'fabri>=0.19.0,<0.20'` or run from a checkout), an
> `OPENAI_API_KEY`, and this repo cloned. `fabri` does **not** auto-load `.env` —
> export your key first: `export OPENAI_API_KEY=…`.

---

## 1. The Roster — browse the catalog (~30s)

```bash
python3 -m http.server 8899          # from the repo root
# open http://localhost:8899/site/index.html
```

A catalog of **self-improving agencies** — each shipped with a hard per-run cost
ceiling and a one-command install (`fabri new agency --from gh:…`), plus a
**Companies** section for the multi-level orgs. This is fabri's wedge on a page:
*self-improving + COGS-first + an open engine you build on* — not a governance
dashboard you rent.

**Hire one in one command:**

```bash
fabri new agency my-crew --from gh:Rushour0/fabri-rosters/agencies/bug-triage-crew
```

Each install gets its **own memory collection**, so it improves independently.

---

## 2. Human-in-the-loop — an agent asks, you answer, it resumes (~90s)

```bash
export OPENAI_API_KEY=…
fabri studio --config demo/refund-approver.yaml --port 8790
# open http://localhost:8790
```

1. In **Conversation**, submit:
   *"Customer #8842 requests a full refund on a 45-day-old $180 order, past our 30-day policy; they say it was defective."*
2. The live agent hits a decision it can't make and **asks a human**. It shows up
   in the **Questions** tab (a cross-run inbox) — *"…outside our 30-day policy…
   How should I proceed?"* with Approve / Deny / Escalate.
3. Answer it. The run **resumes and completes**, and the **COGS panel** shows the
   real cost (~$0.0002 on `gpt-4o-mini`).

The Questions inbox is the safety valve that makes an agency deployable
unattended: when it's unsure, it asks the right person and picks up where it left
off.

---

## 3. A whole company — multi-level org chart with live cost (~2m)

```bash
export OPENAI_API_KEY=…
fabri studio --company companies/acme-eng/company.toml --port 8792
# open http://localhost:8792  → "Company" tab
```

- **Acme Inc — 7 agents · 4 crews · $8/run ceiling.** The org chart is the real
  compiled structure: **Chief of Staff → { VP Engineering, VP Growth } → 4 crews**.
  A flat `company.toml` with `report_to` edges compiles to a nested tree of fabri
  agents — no new runtime.
- In **Conversation**, submit *"Give me a one-line status from each division."*
  Flip to **Company**: the nodes **light up with live status and real per-node
  cost**, and the header shows total spend (e.g. *spent $0.0084*).
- The Chief of Staff keeps a durable **company memory** across sessions. Every
  company task records a postmortem; durable decisions, facts, insights, and
  open loops are retrieved into later runs while credentials, personal data,
  and unverified claims are explicitly excluded.

Edit `companies/acme-eng/company.toml` (add a node, change `report_to`) and
re-serve to reshape the org — `fabri company compile` validates it's a tree and
rebuilds the whole thing.

---

## The one-line pitch

> Browse a catalog of small, self-improving agencies; hire one in a command; when
> it's unsure it asks the right human and resumes; compose several into a company
> with an org chart — and every run reports exactly what it cost.

## How this repo is laid out

- `agencies/<name>/` — installable agencies (`fabri new agency --from ...`)
- `companies/<name>/company.toml` — multi-level orgs (`fabri company compile ...`)
- `demo/refund-approver.yaml` — the HITL demo agent used in step 2
- `site/` — the gallery (static; reads `index.json`)
- `scripts/build_index.py` — regenerate `index.json` after adding an agency/company
