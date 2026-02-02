#!/usr/bin/env bash
set -euo pipefail

# Stops and removes the docker compose stack and its volumes
# Usage: ./scripts/stop-stack.sh

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

echo "Stopping docker compose stack and removing volumes..."
docker compose down -v --remove-orphans

echo "Done."