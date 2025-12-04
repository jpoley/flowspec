# Constitution Customization Examples

This directory contains real-world examples of how constitution templates are customized for different technology stacks using LLM-assisted detection and customization.

## Overview

When you run `specify init`, the CLI:

1. **Detects** your project's technology stack
2. **Selects** an appropriate constitution template (Light/Medium/Heavy)
3. **Customizes** the template with detected values
4. **Marks** sections that need manual validation

These examples show the before/after process for common project types.

## Available Examples

| Example | Language | Use Case | Complexity |
|---------|----------|----------|------------|
| [Python FastAPI](python-fastapi-example.md) | Python 3.11+ | REST API service | Medium |
| [TypeScript React](typescript-react-example.md) | TypeScript 5+ | Web application (SPA) | Medium |
| [Go API](go-api-example.md) | Go 1.21+ | Microservice API | Medium |
| [Rust CLI](rust-cli-example.md) | Rust 1.75+ | Command-line tool | Medium |

## How to Use These Examples

### 1. Find a Similar Project

Choose the example that most closely matches your project:

- **Backend API**: Python FastAPI or Go API
- **Frontend Web App**: TypeScript React
- **CLI Tool**: Rust CLI

### 2. Review the Detection Process

Each example shows:
- What files the LLM scans
- How technology choices are detected
- Which configuration files are parsed

### 3. Compare Before/After

See how the template transforms:

**Before** (template with markers):
```markdown
<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->
[LANGUAGES_AND_FRAMEWORKS]
```

**After** (customized for your stack):
```markdown
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+
- **Testing**: pytest with coverage
```

### 4. Understand What Needs Validation

Not everything can be auto-detected:

- Coverage targets (70% vs 80% vs 90%)
- Package manager preferences (npm vs pnpm vs bun)
- Deployment targets (Vercel vs self-hosted)
- Security requirements (based on compliance needs)

### 5. Apply Patterns to Your Project

Use the examples as templates:

- Copy relevant sections to your constitution
- Adjust values to match your project
- Remove `NEEDS_VALIDATION` markers after review

## Example Structure

Each example follows this format:

1. **Overview**: Project type and key technologies
2. **Detection Process**: How the LLM identifies your stack
3. **Before/After**: Template transformation
4. **What Was Detected**: Automatically identified values
5. **What Needed Validation**: Manual customization points
6. **Related Examples**: Links to similar examples

## Common Patterns Across Examples

### Technology Stack Section

All examples customize the `TECH_STACK` section:

```markdown
## Technology Stack
<!-- SECTION:TECH_STACK:BEGIN -->
### Languages & Frameworks
- **Language**: <detected-language>
- **Framework**: <detected-framework>

### Testing
- **Framework**: <detected-test-framework>
- **Coverage Target**: <suggested-percentage>

### Code Quality
- **Linter**: <detected-linter>
- **Formatter**: <detected-formatter>

### CI/CD
- **Platform**: <detected-ci-platform>
<!-- SECTION:TECH_STACK:END -->
```

## When to Use Each Example

### Python FastAPI Example
**Use when:**
- Building REST APIs in Python
- Using FastAPI, Flask, or Django
- pytest for testing
- ruff or flake8 for linting

**Good for:**
- Microservices
- Backend APIs
- Data processing services

### TypeScript React Example
**Use when:**
- Building web applications
- Using React, Next.js, or Vue
- Jest or Vitest for testing
- ESLint + Prettier

**Good for:**
- Single-page applications
- Server-side rendered apps
- Admin dashboards
- Customer-facing web apps

### Go API Example
**Use when:**
- Building high-performance APIs
- Using Go with Chi, Gin, or Echo
- Go's built-in testing
- golangci-lint

**Good for:**
- Microservices
- High-throughput APIs
- Systems programming
- Cloud-native applications

### Rust CLI Example
**Use when:**
- Building command-line tools
- Using Rust with clap
- cargo test and clippy
- Cross-platform binaries

**Good for:**
- CLI tools
- System utilities
- Performance-critical applications
- Tools distributed as binaries

## Multi-Language Projects

For projects with multiple languages:

1. **Choose the primary language example** (e.g., TypeScript for Next.js + Python API)
2. **Merge relevant sections** from both examples
3. **Create separate standards sections** for each language

Example:
```markdown
## Technology Stack

### Frontend (TypeScript)
- Language: TypeScript 5+
- Framework: Next.js 14
- Testing: Jest + React Testing Library

### Backend (Python)
- Language: Python 3.11+
- Framework: FastAPI
- Testing: pytest
```

## Related Documentation

- [Constitution Templates Overview](../../guides/constitution-validation.md)
- [Constitution Validation Guide](../../guides/constitution-validation.md)
- [Light Constitution Template](../../../templates/constitutions/constitution-light.md)
- [Medium Constitution Template](../../../templates/constitutions/constitution-medium.md)
- [Heavy Constitution Template](../../../templates/constitutions/constitution-heavy.md)

## Questions?

See the [Constitution Validation Guide](../../guides/constitution-validation.md) or open an issue.
