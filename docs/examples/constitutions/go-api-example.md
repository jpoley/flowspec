# Go API Constitution Example

## Overview

This example shows how a **Medium** tier constitution template is customized for a Go REST API project:

- **Project Type**: REST API microservice
- **Language**: Go 1.21+
- **Framework**: Chi router (or Gin/Echo)
- **Testing**: Go's built-in testing + testify
- **Linting**: golangci-lint
- **Dependency Management**: Go modules
- **CI/CD**: GitHub Actions

## Detection Process

When `specify init` detects this project:

1. **Language Detection**: Finds `go.mod` → Go
2. **Version Detection**: Parses `go 1.21` from go.mod
3. **Framework Detection**: Scans imports for `chi`, `gin`, or `echo`
4. **Linter Detection**: Finds `.golangci.yml` → golangci-lint
5. **CI Detection**: Finds `.github/workflows/` → GitHub Actions

## Before: Template (constitution-medium.md)

```markdown
## Technology Stack
<!-- SECTION:TECH_STACK:BEGIN -->
<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->
[LANGUAGES_AND_FRAMEWORKS]

### Linting & Formatting
<!-- NEEDS_VALIDATION: Detected linting tools -->
[LINTING_TOOLS]
<!-- SECTION:TECH_STACK:END -->
```

## After: Customized Constitution

```markdown
## Technology Stack
<!-- SECTION:TECH_STACK:BEGIN -->
### Languages & Frameworks
- **Language**: Go 1.21+
- **HTTP Router**: Chi (github.com/go-chi/chi/v5)
- **Database**: PostgreSQL via pgx/v5
- **ORM**: sqlc (type-safe SQL) or GORM
- **Dependency Management**: Go modules
- **Minimum Go Version**: 1.21 (for generic improvements)

### Testing
- **Framework**: Go's built-in `testing` package
- **Assertions**: testify/assert and testify/require
- **Mocking**: testify/mock or gomock
- **Table-Driven Tests**: Encouraged for multiple cases
- **Coverage Target**: 80%

### Code Quality
- **Linter**: golangci-lint (30+ linters enabled)
- **Formatter**: gofmt (enforced via golangci-lint)
- **Static Analysis**: go vet, staticcheck, gosec
- **Import Ordering**: gci or goimports
- **Pre-commit**: golangci-lint run --fast

### Build & CI/CD
- **Build Tool**: Go's built-in toolchain (`go build`)
- **CI Platform**: GitHub Actions
- **Go Versions Tested**: 1.21, 1.22
- **Container Base**: distroless/static-debian12
- **Container Registry**: ghcr.io
- **Binary Artifacts**: Multi-platform (linux/amd64, linux/arm64)
<!-- SECTION:TECH_STACK:END -->
```

## What Was Detected

The LLM detected:

- ✅ Go 1.21+ from `go.mod`: `go 1.21`
- ✅ Chi router from imports: `github.com/go-chi/chi/v5`
- ✅ PostgreSQL driver from imports: `github.com/jackc/pgx/v5`
- ✅ golangci-lint from `.golangci.yml`
- ✅ GitHub Actions from `.github/workflows/ci.yml`

## What Needed Validation

User needed to confirm/customize:

- Database choice (PostgreSQL vs MySQL vs MongoDB)
- ORM approach (sqlc vs GORM vs raw SQL)
- Coverage target (80% is suggested)
- Multi-platform builds (amd64 vs arm64)
- Container base image (distroless vs alpine)

## Related Examples

- [Python FastAPI Example](python-fastapi-example.md) - Similar API patterns
- [TypeScript React Example](typescript-react-example.md) - Frontend comparison
- [Rust CLI Example](rust-cli-example.md) - Systems language approach
