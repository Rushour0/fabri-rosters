# Deploy a public Fabri Studio demo

A one-container web app anyone (non-technical included) can use in a browser:
they type a request, the agent asks a clarifying question, they answer, and it
finishes — with the **real cost shown**. No install, no terminal, no API key for
the visitor.

This runs on **your** OpenAI key. Two layers keep the bill small:

1. **Per-run ceiling** — `studio-demo.yaml` sets `max_cost_usd: 0.03`; fabri ends
   any run that would cross it. The model is `gpt-4o-mini` (a full run is
   typically a fraction of a cent).
2. **The real cap (do this): set a hard spend limit on the OpenAI side.** Create a
   dedicated **project + API key** for the demo at platform.openai.com, then set a
   **monthly usage limit of $5** on that project (Settings → Limits). When the
   project hits $5, the key stops working — a hard ceiling no amount of traffic can
   exceed. Use that key as `OPENAI_API_KEY` below.

> ⚠️ There is **no login** by default — anyone with the URL can run the demo (on
> your capped key). That's fine for a small share; before posting it widely, add a
> gate (a password page / your host's access control) or keep the $5 cap tight.

---

## Option A — Docker (any host, or local)

```bash
docker build -f deploy/Dockerfile -t fabri-studio-demo .
docker volume create fabri-data
docker run -p 8080:8080 \
  -v fabri-data:/app/.fabri \
  -e OPENAI_API_KEY=sk-proj-… \
  fabri-studio-demo
# open http://localhost:8080
```

## Option B — Fly.io (one command, free-tier friendly)

```bash
cd deploy
fly launch --copy-config --name fabri-studio-demo --no-deploy
fly volumes create fabri_data --region iad --size 1
fly deploy
fly secrets set OPENAI_API_KEY=sk-proj-…                   # the $5-capped key
# fly open
```

## Option C — Render / Railway / any container host

Point the service at `deploy/Dockerfile`, expose the port it sets via `$PORT`,
add `OPENAI_API_KEY` as a secret, and mount persistent storage at `/app/.fabri`.

## Automatic prompt suggestions (optional)

The container checks company memory once per day for `strategic` lessons that
have recurred across at least three sessions. To open/update deduplicated,
reviewable prompt-suggestion issues in this repository, add a `GITHUB_TOKEN`
with Issues write access. With no token, the helper exits and no company context
leaves the deployment.

```sh
docker run -p 8080:8080 \
  -v fabri-data:/app/.fabri \
  -e OPENAI_API_KEY=sk-proj-… \
  -e GITHUB_TOKEN=github_pat_… \
  fabri-studio-demo
```

Only promoted guidelines and the current manager prompt are sent to GitHub;
raw tasks and transcripts are not. Leave this disabled for deployments whose
company memory may contain confidential context.

---

## What the visitor sees

1. A chat box — they type e.g. *"Plan a 3-day trip to Lisbon."*
2. The agent asks one clarifying question (budget? travelling with kids?) — it
   pops in the **Questions** tab and inline in the conversation.
3. They answer; the run resumes and returns a short plan, and the **cost panel**
   shows what it cost (usually < $0.01).

## Swap the demo agent

Replace `studio-demo.yaml` with any agency from this catalog, or serve a whole
company for the org-chart view:

```dockerfile
# in the Dockerfile CMD, instead of --config:
fabri studio --company /app/acme-eng/company.toml --host 0.0.0.0 --port ${PORT:-8080}
```

(Companies cost more per run — keep the $5 OpenAI cap on.)
