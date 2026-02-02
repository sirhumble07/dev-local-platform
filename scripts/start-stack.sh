#!/usr/bin/env bash
set -euo pipefail

# Starts the docker compose stack, waits for services to become healthy, and prints status.
# Usage: ./scripts/start-stack.sh [timeout_seconds]

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

TIMEOUT=${1:-120}

echo "Starting docker compose stack..."
docker compose up -d --build

echo "Waiting up to $TIMEOUT seconds for services to become healthy..."

start_ts=$(date +%s)
end_ts=$((start_ts + TIMEOUT))

check_ok() {
  local url=$1
  if curl -fsS "$url" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

# Services to check
declare -a checks=(
  "http://localhost:8080/health"
  "http://localhost:9090/-/ready || http://localhost:9090/"  # Prometheus readiness (varies)
  "http://localhost:3000/"  # Grafana
  "http://localhost:9093/"  # Alertmanager
)

while [ $(date +%s) -le $end_ts ]; do
  all_ok=true
  for expr in "${checks[@]}"; do
    # support fallbacks with '||'
    ok=false
    IFS='||' read -ra opts <<< "$expr"
    for opt in "${opts[@]}"; do
      url=$(echo "$opt" | xargs)
      if check_ok "$url"; then
        ok=true
        break
      fi
    done
    if ! $ok; then
      all_ok=false
      break
    fi
  done
  if $all_ok; then
    echo "All services are responding. Stack started successfully."
    docker compose ps
    exit 0
  fi
  sleep 2
done

echo "Timeout waiting for services. Dumping logs for diagnosis..."
docker compose ps
sleep 1
docker compose logs --no-color --tail=200
exit 1
