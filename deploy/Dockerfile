# A one-container public Fabri Studio serving THIS whole roster (catalog mode):
# visitors browse the agencies + companies and run any of them in the browser.
# Build context is the REPO ROOT (Coolify builds from the repo root with
# Dockerfile location deploy/Dockerfile):
#   docker build -f deploy/Dockerfile -t fabri-studio-demo .
#   docker run -p 8080:8080 -e OPENAI_API_KEY=sk-... fabri-studio-demo
# See deploy/README.md for hosting + the $5 spend cap.
FROM python:3.12-slim

# Full install so agencies self-improve: sqlite-vec (memory backend) + embeddings
# (sentence-transformers) + bm25. CRITICAL: install CPU-only torch FIRST — the
# default `pip install torch` pulls ~5-7GB of CUDA/nvidia libs (useless on a CPU
# box, and it blows small disks). CPU torch is ~200MB and satisfies
# sentence-transformers, so the [embeddings] extra won't re-pull the CUDA build.
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
# Cache-bust the fabri install whenever a new version publishes: the PyPI
# metadata JSON changes on each release, so this ADD's content changes and Docker
# invalidates the pip layer below. Without it, the layer stays cached at an old
# fabri version and redeploys silently ship a stale Studio (which is exactly what
# happened — the demo kept serving a pre-blue build). --upgrade for good measure.
ADD https://pypi.org/pypi/fabri/json /tmp/fabri-pypi.json
RUN pip install --upgrade "fabri[sqlite,embeddings,bm25]>=0.19.0,<0.20"

WORKDIR /app
# Bundle the roster so `--catalog` can pre-install/compile every entry at startup.
COPY index.json /app/rosters/index.json
COPY agencies /app/rosters/agencies
COPY companies /app/rosters/companies
COPY deploy/studio-demo.yaml /app/studio-demo.yaml
COPY scripts/suggest_company_prompts.py /app/scripts/suggest_company_prompts.py

# fabri writes per-run workspaces + a sqlite memory db under the working dir.
RUN mkdir -p /app/.fabri && useradd -m demo && chown -R demo /app
USER demo

EXPOSE 8080
# Serve the whole roster (catalog mode). Company memory and run history live on
# /app/.fabri. Prompt suggestions are opt-in: the helper exits immediately
# unless GITHUB_TOKEN is configured.
CMD ["sh", "-c", "python /app/scripts/suggest_company_prompts.py --watch & exec fabri studio --catalog /app/rosters --home-root /app/.fabri/serve --host 0.0.0.0 --port ${PORT:-8080}"]
