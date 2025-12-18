# ADR-013: Adopt Docker Hardened Images (DHI) for Development Containers

## Status

**Accepted** - Implemented December 2024

## Context

### Problem Statement

The Flowspec development container needed a more secure base image. The original plan (ADR-012) proposed migrating from Debian Bullseye to Bookworm, but this would only provide incremental security improvements while retaining CVE exposure from Debian's larger package footprint.

### Docker Hardened Images (DHI)

Docker introduced Hardened Images in 2024, providing:
- **95%+ CVE reduction** compared to standard images
- **SLSA Build Level 3** provenance attestations
- **Complete SBOM** (Software Bill of Materials)
- **Apache 2.0 license** - free for all use cases
- **Same Docker Hub authentication** - no additional accounts required

## Decision

**Adopt Docker Hardened Images (DHI) using Alpine base instead of Debian Bookworm.**

Specifically:
- Base image: `dhi.io/python:3.13-alpine3.22-dev`
- Registry: `dhi.io` (authenticated via Docker Hub credentials)
- CI/CD: Updated GitHub Actions workflow to authenticate with DHI registry

## Options Considered

### Option 1: Debian Bookworm (from ADR-012)

**Approach**: `mcr.microsoft.com/devcontainers/python:3.11-bookworm`

**Pros**:
- Microsoft maintained
- Drop-in replacement for Bullseye
- Familiar Debian environment

**Cons**:
- Still contains CVEs (reduced but not eliminated)
- Larger image size (~1.5GB)
- No SLSA provenance attestations
- No guaranteed SBOM

**Verdict**: Superseded by DHI option.

### Option 2: Docker Hardened Images Alpine (SELECTED)

**Approach**: `dhi.io/python:3.13-alpine3.22-dev`

**Pros**:
- **Zero CVEs** - 95%+ reduction guaranteed
- **SLSA Level 3 provenance** - cryptographic build attestations
- **Complete SBOM** - full dependency transparency
- **Smaller image** - Alpine base is ~100MB vs ~1GB
- **Free license** - Apache 2.0, no restrictions
- **Python 3.13** - latest Python version
- **Dev variant** - includes gcc, make, git, headers for building packages

**Cons**:
- Requires DHI registry authentication in CI/CD
- Alpine musl libc vs glibc (rarely an issue for Python)
- Some packages may need Alpine-specific installation

**Verdict**: **SELECTED** - Superior security with acceptable tradeoffs.

### Option 3: Chainguard Images

**Approach**: Use Chainguard's hardened images

**Pros**:
- Zero CVE guarantee
- Minimal attack surface

**Cons**:
- Requires paid subscription for most images
- Different registry and authentication
- Less familiar ecosystem

**Verdict**: DHI provides similar security guarantees with free licensing.

## Implementation

### Dockerfile Changes

```dockerfile
# Before (standard Python Alpine)
FROM python:3.13-alpine

# After (Docker Hardened Image)
FROM dhi.io/python:3.13-alpine3.22-dev
```

### CI/CD Changes

Added DHI registry authentication to `.github/workflows/docker-publish.yml`:

```yaml
- name: Log in to Docker Hardened Images (DHI) registry
  uses: docker/login-action@v3
  with:
    registry: dhi.io
    username: ${{ secrets.DOCKERHUB_USER }}
    password: ${{ secrets.DOCKERHUB_SECRET }}
```

### Local Build Requirements

```bash
# Authenticate to DHI registry (uses Docker Hub credentials)
docker login dhi.io

# Build the image
docker build -t jpoley/flowspec-agents:latest .devcontainer/
```

## Consequences

### Positive

- **Zero CVE baseline** - Eliminates entire class of vulnerability concerns
- **Supply chain security** - SLSA Level 3 provenance provides build integrity
- **Transparency** - Complete SBOM for dependency auditing
- **Compliance** - Meets stringent security requirements
- **Smaller images** - Faster pulls, reduced storage
- **Latest Python** - Python 3.13 with newest features

### Negative

- **Registry authentication** - CI/CD and local builds require DHI login
- **Alpine learning curve** - Different package manager (apk vs apt)
- **musl libc** - Rare compatibility issues with some native packages

### Neutral

- **Cost** - DHI is free (Apache 2.0 license)
- **Performance** - No significant difference from standard images

## Security Benefits

| Metric | Standard Image | DHI Image |
|--------|---------------|-----------|
| CVE Count | 50-200+ | 0-5 |
| SLSA Level | None | Level 3 |
| SBOM | Not guaranteed | Included |
| Provenance | None | Cryptographic |

## Verification

```bash
# Verify SBOM attestation
cosign verify-attestation --type spdxjson \
  --certificate-identity-regexp '^https://github\.com/jpoley/flowspec/' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  jpoley/flowspec-agents:latest

# Verify provenance attestation
cosign verify-attestation --type slsaprovenance \
  --certificate-identity-regexp '^https://github\.com/jpoley/flowspec/' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  jpoley/flowspec-agents:latest
```

## References

- [Docker Hardened Images](https://www.docker.com/products/hardened-images/)
- [DHI Quickstart Guide](https://docs.docker.com/dhi/get-started/)
- [SLSA Framework](https://slsa.dev/)
- [ADR-012: Bookworm Migration (Superseded)](ADR-012-docker-base-image-bookworm.md)

## Related Changes

- `.devcontainer/Dockerfile` - Updated base image to DHI
- `.devcontainer/README.md` - Added DHI documentation
- `.github/workflows/docker-publish.yml` - Added DHI registry authentication
