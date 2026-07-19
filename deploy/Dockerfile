# A one-container public Fabri Studio demo.
# Build context is the REPO ROOT (so PaaS like Coolify, which build from the
# repo root, work with Dockerfile location deploy/Dockerfile):
#   docker build -f deploy/Dockerfile -t fabri-studio-demo .
#   docker run -p 8080:8080 -e OPENAI_API_KEY=sk-... fabri-studio-demo
# Then open http://localhost:8080 — type a request, answer its question, watch
# it finish (with the real cost shown). See deploy/README.md for hosting + the
# $5 spend cap.
FROM python:3.12-slim

# Full install: sqlite-vec (memory backend the agencies use) + embeddings
# (sentence-transformers, so memory retrieval + self-improvement actually work)
# + bm25 (hybrid retrieval). This pulls torch, so the image is large — fine for
# an always-on host; agencies get the full self-improving behavior.
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

RUN pip install "fabri[sqlite,embeddings,bm25]>=0.15.1"

WORKDIR /app
COPY deploy/studio-demo.yaml /app/studio-demo.yaml

# fabri writes per-run workspaces + a sqlite memory db under the working dir.
RUN mkdir -p /app/.fabri && useradd -m demo && chown -R demo /app
USER demo

EXPOSE 8080
# Bind 0.0.0.0 so the container is reachable; honor the platform's $PORT.
CMD ["sh", "-c", "fabri studio --config /app/studio-demo.yaml --host 0.0.0.0 --port ${PORT:-8080}"]
