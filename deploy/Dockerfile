# A one-container public Fabri Studio demo.
#   docker build -t fabri-studio-demo deploy/
#   docker run -p 8080:8080 -e OPENAI_API_KEY=sk-... fabri-studio-demo
# Then open http://localhost:8080 — type a request, answer its question, watch
# it finish (with the real cost shown). See deploy/README.md for hosting + the
# $5 spend cap.
FROM python:3.12-slim

# fabri pulls a memory/embeddings stack; give pip room and keep the image lean.
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

RUN pip install "fabri>=0.15"

WORKDIR /app
COPY studio-demo.yaml /app/studio-demo.yaml

# fabri writes per-run workspaces + a sqlite memory db under the working dir.
RUN mkdir -p /app/.fabri && useradd -m demo && chown -R demo /app
USER demo

EXPOSE 8080
# Bind 0.0.0.0 so the container is reachable; honor the platform's $PORT.
CMD ["sh", "-c", "fabri studio --config /app/studio-demo.yaml --host 0.0.0.0 --port ${PORT:-8080}"]
