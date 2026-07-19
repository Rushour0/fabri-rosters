# Go live: fabri.rushour0.com — tiny box behind Cloudflare

The interactive Studio (a stateful Python server) can't run on Cloudflare
Workers/Pages, so we run the 727 MB container on a small always-on box and let
Cloudflare (which already hosts rushour0.com's DNS) front it with free TLS.

**~10 minutes. Three things only you can do:** a host box, a $5-capped OpenAI
key, and the Cloudflare DNS record.

---

## 0. Make a $5-capped OpenAI key (the real spend cap)

platform.openai.com → create a **new project** → **API key** in it → **Limits →
set a $5 monthly usage limit**. Copy the key (`sk-proj-…`). When the project hits
$5 the key stops — a hard ceiling. (The container also caps each run at $0.03.)

## 1. A small box with Docker

Any Ubuntu VM with Docker works. On DigitalOcean ($6/mo, "Docker on Ubuntu 24.04"
Marketplace image), or:

```bash
# on a fresh Ubuntu box:
curl -fsSL https://get.docker.com | sh
```

Note the box's public IP.

## 2. Build + run the container (on the box)

```bash
git clone https://github.com/Rushour0/fabri-rosters
cd fabri-rosters
docker build -f deploy/Dockerfile -t fabri-studio-demo .
docker run -d --name fabri-studio --restart unless-stopped \
  -p 80:8080 \
  -e OPENAI_API_KEY='sk-proj-…your-$5-capped-key…' \
  fabri-studio-demo
# check it: curl -s http://localhost/health   -> {"status":"ok"}
```

(Serves plain HTTP on port 80; Cloudflare adds TLS at the edge in step 3.)

## 3. Point fabri.rushour0.com at it (Cloudflare)

Cloudflare dashboard → rushour0.com → **DNS → Add record**:

| Type | Name  | Content (the box IP) | Proxy |
|------|-------|----------------------|-------|
| A    | fabri | `<your box IP>`      | **Proxied** (orange cloud) |

Then **SSL/TLS → Overview → set mode to "Flexible"** (Cloudflare terminates HTTPS
at the edge and talks HTTP to the box). For end-to-end TLS instead, run a Caddy/
nginx reverse proxy on the box with a cert and set mode "Full (strict)".

Open **https://fabri.rushour0.com** — type a request, answer its question, watch
it finish with the cost shown.

---

## Want me to drive it instead?

I can run most of this if you hand me the credentials in this session:

- `! doctl auth init` (paste a DigitalOcean token) → I provision the droplet + run the container.
- A **Cloudflare API token** (Zone → DNS → Edit on rushour0.com) → I add the DNS record.
- The **$5-capped OpenAI key** → I set it as the container env.

I can't do any of these without you providing them — they're your cloud, your key, and your domain.

## Updating later

```bash
cd fabri-rosters && git pull && docker build -f deploy/Dockerfile -t fabri-studio-demo . \
  && docker rm -f fabri-studio \
  && docker run -d --name fabri-studio --restart unless-stopped -p 80:8080 \
     -e OPENAI_API_KEY='sk-proj-…' fabri-studio-demo
```
