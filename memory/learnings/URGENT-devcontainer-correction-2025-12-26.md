# Devcontainer DHI Authentication - Corrected Solution

## Problem Statement
Devcontainers failed to build with:
```
Error: unauthorized: Authentication failed
```
When pulling `dhi.io/python:3.13-alpine3.22-dev`

## Root Cause
DHI (Docker Hardened Images) requires authentication via `docker login dhi.io` using Docker Hub credentials. The registry was not configured in `~/.docker/config.json`.

## CRITICAL LEARNING
**DHI is a CORE REQUIREMENT - never replace it with standard images.**

DHI provides:
- 95%+ CVE reduction
- SLSA Level 3 provenance
- Signed attestations
- Supply chain security

## Correct Solution (Implemented)

### Architecture
1. **CI/CD** builds the image using DHI (auth via GitHub secrets)
2. **Pre-built image** pushed to Docker Hub as `jpoley/flowspec-agents:latest`
3. **Developers** use the pre-built image (no DHI auth needed)
4. **Maintainers** who need to rebuild locally run `docker login dhi.io` first

### Changes Made
1. Updated `.devcontainer/devcontainer.json`:
   - Changed from `"build": {"dockerfile": "Dockerfile"}` to `"image": "jpoley/flowspec-agents:latest"`
   - Added comments explaining how to rebuild locally

2. Updated `.devcontainer/README.md`:
   - Added "Building the Image Locally (Maintainers)" section
   - Documents DHI auth requirements

### Dockerfile (Unchanged)
The Dockerfile keeps DHI base image - this is correct:
```dockerfile
FROM dhi.io/python:3.13-alpine3.22-dev
```

### CI Workflow (Already Correct)
`docker-publish.yml` already handles DHI auth:
```yaml
- name: Log in to Docker Hardened Images (DHI) registry
  uses: docker/login-action@v3
  with:
    registry: dhi.io
    username: ${{ secrets.DOCKERHUB_USER }}
    password: ${{ secrets.DOCKERHUB_SECRET }}
```

## For Maintainers Rebuilding Locally
```bash
# One-time: Authenticate to DHI with Docker Hub creds
docker login dhi.io

# Build
cd .devcontainer
docker build -t jpoley/flowspec-agents:local .
```

## Key Insight
DHI became FREE on Dec 17, 2025, but still requires authentication. Same Docker Hub credentials work for dhi.io registry.
