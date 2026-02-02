# Incident Response — DevOps Local Platform

This document standardizes how to run incident simulations and real incident responses.

## Simulation: App crash
1. Simulate crash locally: docker compose exec app pkill -f uvicorn || true (or modify code to raise an exception).
2. Observe Prometheus alert (InstanceDown) and check Alertmanager receiver.
3. Follow runbook steps for InstanceDown to recover.

## Simulation: Bad configuration
1. Introduce a bad config in `.env` (e.g., BAD_ENV=true) and restart the compose stack.
2. Observe application behavior and alerts (errors or increased latency).
3. Revert config and validate with health checks and smoke tests.

## Communication & Postmortem
- Open an incident channel and include: title, impact, start time, services affected, severity.
- After resolution, prepare a postmortem: summary, timeline, root cause, fixes, and owners.
- Archive and link artifacts (logs, graphs, commits, PRs) for learning.
