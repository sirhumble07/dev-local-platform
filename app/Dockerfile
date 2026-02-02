# syntax=docker/dockerfile:1
ARG BUILD_DATE="unset"
ARG VCS_REF="unset"
FROM python:3.11-slim-bullseye AS builder
LABEL stage=builder \
      org.opencontainers.image.title="devops-local-platform" \
      org.opencontainers.image.description="Local DevOps platform for teaching and testing CI/CD locally" \
      org.opencontainers.image.revision="$VCS_REF" \
      org.opencontainers.image.created="$BUILD_DATE"
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build deps only in the builder stage
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt \
    # Generate a lightweight SBOM using pip-licenses for quick local auditing (kept out of runtime image unless explicitly copied)
    && python -m pip install --no-cache-dir pip-licenses==4.0.2 \
    && mkdir -p /sbom \
    && pip-licenses --format=json --output-file /sbom/pip-licenses.json

FROM python:3.11-slim-bullseye AS runtime
LABEL maintainer="devops-local-platform <devnull@example.com>"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/install/bin:$PATH

# Runtime dependencies (tini for PID 1 handling, curl for healthcheck)
RUN apt-get update \
    && apt-get install -y --no-install-recommends tini curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN groupadd --system app && useradd --system --gid app --create-home --home-dir /home/app app

COPY --from=builder /install /install
# Copy SBOM into the runtime image to make it easy for local scanners to inspect image contents
COPY --from=builder /sbom/pip-licenses.json /app/sbom.json
COPY . /app
WORKDIR /app
# Ensure files are not world-writable and decrease attack surface
RUN chown -R app:app /app /install \
    && chmod -R go-w /app /install

USER app
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
