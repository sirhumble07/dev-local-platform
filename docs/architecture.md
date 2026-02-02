# Architecture — DevOps Local Platform

## Overview
This repository contains a local-first DevOps platform designed to mirror real production systems. It runs entirely via `docker compose` and includes:

- FastAPI application (`app`) exposing `/`, `/health`, `/metrics`, `/version`
- Nginx reverse proxy (`nginx`) routing external traffic to the app
- Prometheus for metrics scraping and alerting
- Alertmanager to manage alert routes and receivers
- Grafana for dashboards and visualization

All services run on a Docker bridge network `devops` and communicate via service DNS names (e.g., `http://app:8000`). Containers are treated as immutable artifacts built in CI and deployed by CD.

## CI/CD Artifact Flow
- CI (Pull Request): lint → test → build image → save image artifact → security scan (SBOM & Trivy)
  - Security job fails the PR if HIGH/CRITICAL vulnerabilities are found (enforced by the CI step exit codes). This allows branch protection to block merges.
- CD (main branch push): build → push image to GitHub Container Registry (GHCR) → simulate deployment
  - The CD job logs in to GHCR, pushes the same image, and in the simulation runs `docker compose up` in the runner to validate health checks and perform smoke tests.

This follows "build once, deploy many": images built in CI are the exact artifacts considered by CD.

## Secrets & Authentication
- Local secret pattern: `.env` (never committed). Use `.env.example` for defaults only.
- CI secrets:
  - `GITHUB_TOKEN` (used by Actions for GHCR by default)
  - `COSIGN_PRIVATE_KEY` & `COSIGN_PASSWORD` (optional for signing images)

## Observability
- App metrics exposed at `/metrics` (Prometheus format).
- Prometheus scrapes `app:8000` and is configured with alerting/rules.
- Alertmanager receives alerts from Prometheus and forwards to receivers (e.g., webhook, PagerDuty) per `monitoring/alertmanager/config.yml`.
- Grafana is auto-provisioned with a Prometheus datasource and a basic dashboard for HTTP rates and latency.

## How to move to Kubernetes / Cloud
- Swap `docker compose` with Kubernetes manifests (Deployment/Service/Ingress) or Helm charts.
- Use a registry (GHCR, ECR, ACR) for image distribution across clusters.
- Use managed Prometheus (or kube-prometheus stack) and Alertmanager, and route alerts to PagerDuty/Teams/Slack.
- Use ArgoCD/Flux or your cloud provider's deployment services for CD.
