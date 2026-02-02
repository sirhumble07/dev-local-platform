# devops-local-platform — Local-first DevOps workshop

This repository provides a local-first DevOps platform running with Docker Compose test modern CI/CD and monitoring practices.

See `docs/` for architecture, runbooks, and incident-response guides.

## How to run & verify locally (quick commands) 🔧

1. Create a virtualenv and install deps:
   - python -m venv .venv && source .venv/bin/activate
   - pip install -r app/requirements.txt

2. Run tests:
   - cd devops-local-platform
   - pytest app/test_app.py

3. Run full stack locally with Docker Compose (recommended):
   - cp .env.example .env && edit the `.env` file if needed
   - docker compose up --build

   Or use the helper script (waits for health checks):
   - ./scripts/start-stack.sh [timeout_seconds]

4. Verify services:
   - Nginx / App: http://localhost:8080/ → root, /health, /metrics
   - Prometheus: http://localhost:9090/
   - Grafana: http://localhost:3000/ (default: admin/admin)
   - Alertmanager: http://localhost:9093/

5. Stop the stack:
   - docker compose down -v
   - or use the helper script: ./scripts/stop-stack.sh

5. Build and scan locally (requires Docker):
   - ./scripts/scan-image.sh devops-local-app:local

6. CI / CD notes:
   - CI runs lint → tests → build → security scans. The `security` job (SBOM + Trivy) will fail the PR if HIGH/CRITICAL vulnerabilities are detected — configure branch protection rules to require the `security` job as a status check to block merges.
   - CD pushes images to GitHub Container Registry (GHCR) on merges to `main`. To enable push, ensure `GITHUB_TOKEN` has package write permissions for your repository.

## Security & Secrets
- Do NOT commit secrets. Use environment variables and repository secrets in GitHub Actions. Common secrets for this repo:
  - `GITHUB_TOKEN` (used by GitHub Actions to authenticate to GHCR)
  - `COSIGN_PRIVATE_KEY` & `COSIGN_PASSWORD` (optional for image signing)

## Observability & Alerts
- Prometheus alerting rules are in `monitoring/prometheus.rules.yml` and will be loaded by Prometheus.
- Alertmanager config (receiver webhook) is in `monitoring/alertmanager/config.yml`.
- Example runbooks are stored in `docs/runbook.md` and `docs/incident-response.md`.
