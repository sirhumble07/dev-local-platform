#!/usr/bin/env bash
set -euo pipefail

TAG=${1:-devops-local-app:local}
DOCKERFILE_PATH="app/Dockerfile"

echo "Building image: $TAG"
docker build -t "$TAG" -f "$DOCKERFILE_PATH" app

if command -v trivy >/dev/null 2>&1; then
  echo "Trivy detected — running vulnerability scan (HIGH,CRITICAL)"
  trivy image --severity HIGH,CRITICAL --exit-code 1 "$TAG" || {
    echo "Vulnerabilities detected by Trivy"
    exit 1
  }
else
  echo "Trivy not found. To install: https://aquasecurity.github.io/trivy/latest/"
  echo "Showing SBOM embedded in image (/app/sbom.json):"
  docker run --rm "$TAG" cat /app/sbom.json || echo "No SBOM found in image"
fi

echo "Image build and local scan complete."
