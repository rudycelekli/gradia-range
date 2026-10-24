FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY sim /opt/sim
ENV RANGE_REPO_URL=https://github.com/twentyhq/twenty
ENV RANGE_REVISION=c13b414b7a5a8a0a9c4f967be40bfa2c5a3a175e
RUN git init /workspace/repo \
    && git -C /workspace/repo remote add origin "$RANGE_REPO_URL" \
    && git -C /workspace/repo fetch --depth 1 origin "$RANGE_REVISION" \
    && git -C /workspace/repo checkout --detach FETCH_HEAD \
    && find /workspace/repo \\( -name .env -o -name id_rsa -o -name id_ed25519 -o -name '*.pem' -o -name credentials.json \\) -type f -print > /opt/sim/stripped.txt \
    && find /workspace/repo \\( -name .env -o -name id_rsa -o -name id_ed25519 -o -name '*.pem' -o -name credentials.json \\) -type f -delete
WORKDIR /workspace/repo
