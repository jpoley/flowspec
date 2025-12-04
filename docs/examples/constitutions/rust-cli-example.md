# Rust CLI Constitution Example

## Overview

This example shows how a **Medium** tier constitution template is customized for a Rust CLI tool project:

- **Project Type**: Command-line application
- **Language**: Rust 1.75+ (2021 edition)
- **CLI Framework**: clap v4 (derive API)
- **Testing**: Rust's built-in testing + assert_cmd
- **Linting**: clippy + rustfmt
- **Dependency Management**: Cargo
- **CI/CD**: GitHub Actions

## Detection Process

When `specify init` detects this project:

1. **Language Detection**: Finds `Cargo.toml` → Rust
2. **Edition Detection**: Parses `edition = "2021"` from Cargo.toml
3. **CLI Detection**: Finds `clap` in dependencies
4. **Linter Detection**: Checks for `clippy.toml` or cargo-clippy
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
- **Language**: Rust 1.75+ (2021 edition)
- **CLI Framework**: clap 4.4+ (derive API)
- **Configuration**: serde + toml or yaml
- **Error Handling**: anyhow for applications, thiserror for libraries
- **Async Runtime**: tokio (if needed)
- **HTTP Client**: reqwest (if needed)

### Testing
- **Framework**: Built-in Rust test framework
- **CLI Testing**: assert_cmd + predicates
- **Snapshot Testing**: insta (for complex output)
- **Property Testing**: proptest or quickcheck
- **Coverage Target**: 80%

### Code Quality
- **Linter**: clippy (pedantic + restriction groups enabled)
- **Formatter**: rustfmt (2021 edition style)
- **Security Audit**: cargo-audit (check dependencies)
- **Unused Dependencies**: cargo-udeps
- **Pre-commit**: cargo fmt + cargo clippy

### Build & CI/CD
- **Build Tool**: Cargo
- **CI Platform**: GitHub Actions
- **Rust Versions Tested**: stable, beta
- **Target Platforms**: x86_64-unknown-linux-gnu, x86_64-apple-darwin, x86_64-pc-windows-msvc
- **Release**: cargo-dist for cross-platform binaries
- **Container Base**: gcr.io/distroless/cc-debian12 (if containerized)
<!-- SECTION:TECH_STACK:END -->
```

## What Was Detected

The LLM detected:

- ✅ Rust 1.75+ from `Cargo.toml`: `rust-version = "1.75"`
- ✅ 2021 edition from `Cargo.toml`: `edition = "2021"`
- ✅ clap from `[dependencies]`: `clap = { version = "4.4", features = ["derive"] }`
- ✅ clippy config from `clippy.toml` or `Cargo.toml`
- ✅ GitHub Actions from `.github/workflows/ci.yml`

## What Needed Validation

User needed to confirm/customize:

- CLI framework (clap vs structopt vs argh)
- Async requirements (tokio vs async-std vs none)
- Error handling strategy (anyhow vs thiserror)
- Cross-compilation targets (Linux/Mac/Windows)
- Release automation tool (cargo-dist vs manual)

## Related Examples

- [Python FastAPI Example](python-fastapi-example.md) - Web API comparison
- [TypeScript React Example](typescript-react-example.md) - Frontend comparison
- [Go API Example](go-api-example.md) - Systems language comparison
