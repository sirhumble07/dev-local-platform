# Runbook — DevOps Local Platform

This runbook describes how to respond to common alerts and incidents in the local stack.

## Getting logs & status
- View service logs:
  - docker compose logs -f app
  - docker compose logs -f nginx
- Check health endpoints:
  - curl http://localhost:8080/health
- Check metrics in Prometheus: http://localhost:9090/targets and http://localhost:9090/graph

## Alert: InstanceDown (severity: critical)
1. Check Prometheus: confirm `up` metric for the target is 0.
2. Check container status: docker compose ps
3. Inspect logs: docker compose logs -f <service>
4. If the app crashed, restart the service: docker compose restart app
5. If restart fails, roll back to previous image (if known) or run local build and test before re-deploy.
6. Post-incident: capture logs, create a timeline, and file a follow-up in your issue tracker.

## Alert: HighErrorRate (5xx) (severity: warning)
1. Inspect recent requests and error counts in Grafana.
2. Tail the app logs to identify stack traces or exception patterns.
3. Check dependency health (databases, external APIs) and configuration errors.
4. If caused by a recent deploy, consider rolling back the deploy image or toggling feature flags.

## Alert: HighLatencyP95 (severity: warning)
1. Confirm increased latency in Prometheus graphs and check correlating resource usage.
2. Check for increased CPU, memory, or blocking calls in the app logs.
3. If caused by heavy load, scale horizontally (in k8s scale replicas) or identify hot paths in code and optimize.

## Escalation & Postmortem
- If you cannot remediate within the SLO window, escalate to on-call and open an incident channel.
- After resolution, write an incident report: summary, timeline, root cause, action items, and owners.
