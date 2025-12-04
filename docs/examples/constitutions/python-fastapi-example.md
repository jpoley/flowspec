# Python FastAPI Constitution Example

## Overview

This example shows how a **Light** tier constitution template is customized for a Python FastAPI project:

- **Project Type**: REST API service
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Testing**: pytest with coverage
- **Linting**: ruff (check + format)
- **CI/CD**: GitHub Actions

## Detection Process

When `specify init` detects this project:

1. **Language Detection**: Finds `pyproject.toml` or `requirements.txt` → Python
2. **Framework Detection**: Finds `from fastapi import` → FastAPI
3. **Test Framework**: Finds `pytest.ini` or `[tool.pytest]` → pytest
4. **Linter Detection**: Finds `[tool.ruff]` in pyproject.toml → ruff
5. **CI Detection**: Finds `.github/workflows/` → GitHub Actions

## Before: Template (constitution-light.md)

```markdown
## Technology Stack
<!-- SECTION:TECH_STACK:BEGIN -->
<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->
[LANGUAGES_AND_FRAMEWORKS]
<!-- SECTION:TECH_STACK:END -->
```

## After: Customized Constitution

```markdown
## Technology Stack
<!-- SECTION:TECH_STACK:BEGIN -->
### Languages & Frameworks
- **Language**: Python 3.11+
- **Web Framework**: FastAPI 0.104+
- **ASGI Server**: Uvicorn
- **Dependency Management**: uv (preferred) or pip

### Testing
- **Framework**: pytest
- **Coverage**: pytest-cov
- **Async Testing**: pytest-asyncio
- **Fixtures**: Factory pattern with pytest fixtures

### Code Quality
- **Linter**: ruff check
- **Formatter**: ruff format
- **Type Checking**: mypy (strict mode recommended)
- **Pre-commit**: Automated ruff + mypy checks

### CI/CD
- **Platform**: GitHub Actions
- **Python Versions**: 3.11, 3.12
- **Coverage Target**: 80%
- **Build Artifacts**: Docker image (ghcr.io)
<!-- SECTION:TECH_STACK:END -->
```

## What Was Detected

The LLM detected:

- ✅ Python 3.11+ from `pyproject.toml`: `requires-python = ">=3.11"`
- ✅ FastAPI from imports in source files
- ✅ pytest from `pyproject.toml` or `pytest.ini`
- ✅ ruff from `[tool.ruff]` configuration
- ✅ GitHub Actions from `.github/workflows/ci.yml`

## What Needed Validation

User needed to confirm/customize:

- Coverage target (80% is suggested, may need adjustment)
- Python version strategy (3.11+ vs 3.11 only)
- Docker image registry (ghcr.io vs dockerhub)
- Whether to use uv vs pip (project preference)

## Additional Customizations

Based on project specifics, you might also customize:

### Quality Standards
```markdown
### Code Standards
<!-- SECTION:QUALITY:BEGIN -->
- Type hints required on all function signatures
- Docstrings for public APIs (Google style)
- Pydantic models for all request/response validation
- Async/await for all I/O operations
- SQLAlchemy for database access (when applicable)
<!-- SECTION:QUALITY:END -->
```

### Testing Requirements
```markdown
### Testing Standards
<!-- SECTION:TESTING:BEGIN -->
- Unit tests for business logic functions
- Integration tests for API endpoints
- Parameterized tests for edge cases
- Fixtures for database setup/teardown
- Mock external API calls
- Coverage target: 80% overall, 100% for critical paths
<!-- SECTION:TESTING:END -->
```

## Commands to Run

After customization, verify with:

```bash
# Validate constitution
specify constitution validate

# Test that linting/formatting works
ruff check .
ruff format .

# Test that tests run
pytest tests/ -v --cov=src

# Test CI locally (if act is installed)
act -j test
```

## Related Examples

- [Go API Example](go-api-example.md) - Similar patterns for Go
- [TypeScript React Example](typescript-react-example.md) - Frontend comparison
- [Rust CLI Example](rust-cli-example.md) - Systems language approach
