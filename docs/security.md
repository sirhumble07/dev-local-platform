# Security & CI gating

This project integrates SBOM generation and vulnerability scanning within CI to prevent known critical issues from reaching production.

## How it works
- The `build` job in CI builds the image and uploads it as an artifact.
- The `security` job loads that image, generates an SBOM (Syft) and runs Trivy against the image. The Trivy step is configured to fail if any HIGH or CRITICAL vulnerabilities are found.
- Because the `security` job runs on PRs (it requires the `build` job), you can configure GitHub branch protection rules to require the `security` job to pass before merges into `main` are allowed.

## Enforcing via Branch Protection
1. Go to your GitHub repo → Settings → Branches → Add rule for `main`.
2. Under "Require status checks to pass before merging", add the checks for the CI jobs you want to require (e.g., `lint`, `test`, `security`).
3. Save the rule.

## Image signing and provenance
- The CD workflow optionally signs images with `cosign` if `COSIGN_PRIVATE_KEY` is present as a secret.
- Image labels (`org.opencontainers.image.*`) and SBOM artifacts support provenance and auditing.

## GHCR (GitHub Container Registry)
- The CD pipeline pushes images to GHCR (registry: `ghcr.io/${{ github.repository_owner }}/devops-local-app`).
- To push images to GHCR, the GitHub Actions runner uses `${{ secrets.GITHUB_TOKEN }}` by default; ensure package write permissions are enabled under Actions > General > Workflow permissions or use a Personal Access Token.

## Local testing
- You can run `./scripts/scan-image.sh` locally to build the image and run Trivy (if installed); this mirrors the security scan run in CI.
