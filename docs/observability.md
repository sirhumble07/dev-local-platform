# Observability — Principles and Implementation

This repo implements a minimal observability stack: Prometheus (scraping metrics) + Alertmanager (routing alerts) + Grafana (dashboards).

## RED metrics
- R: Rate — requests per second (traffic) measured with counters like `http_requests_total`.
- E: Errors — error rates (e.g. percentage of 5xx responses).
- D: Duration — latency quantiles (p95, p99) derived from histograms like `http_request_duration_seconds_bucket`.

These metrics are exposed by the app and scraped by Prometheus. The default dashboard shows request rate and p95 latency.

## What to alert on
- Service down (`up == 0`) — critical. Immediate action required.
- Sustained high error rate (e.g., >5% 5xx for 2 minutes) — warning → investigate.
- High latency (p95 > threshold) — warning → investigate performance regressions.

## What NOT to alert on
- Individual 4xx responses (client errors) — usually not actionable.
- Low severity noise and transient blips that resolve quickly.

## Prometheus rules
See `monitoring/prometheus.rules.yml` for examples of rules implemented (InstanceDown, HighErrorRate, HighLatencyP95).

## Alert routing
- Alertmanager (`monitoring/alertmanager/config.yml`) contains receivers and routing configuration.
- For local testing, configure webhook receivers (e.g., `webhook.site`) to see alert payloads.

## Grafana alerts
- For richer alerting workflows and silences, integrate Grafana alerting with Prometheus as a data source.
- Grafana provisioning is in `monitoring/grafana/provisioning` and dashboards are loaded from `monitoring/grafana/dashboards`.
