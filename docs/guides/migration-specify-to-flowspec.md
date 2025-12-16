# Migration Guide: specify-cli to flowspec-cli

This guide helps you migrate from `specify-cli` (package name `specify`) to `flowspec-cli` (command name `flowspec`).

## Overview

Starting with version 0.2.360, the CLI has been renamed:

| Before | After |
|--------|-------|
| Package: `specify-cli` | Package: `flowspec-cli` |
| Command: `specify` | Command: `flowspec` |
| Module: `specify_cli` | Module: `flowspec_cli` |
| Pytest plugin: `specify_ac` | Pytest plugin: `flowspec_ac` |

## Quick Migration

### 1. Update Installation

```bash
# Uninstall old package
pip uninstall specify-cli

# Install new package
pip install flowspec-cli

# Or with uv
uv tool uninstall specify-cli
uv tool install flowspec-cli
```

### 2. Update Command Usage

Replace all `specify` commands with `flowspec`:

```bash
# Before
specify init my-project --agent claude
specify dev-setup --force
specify workflow validate

# After
flowspec init my-project --agent claude
flowspec dev-setup --force
flowspec workflow validate
```

### 3. Update Scripts and CI/CD

Search and replace in your scripts:

```bash
# Find files containing 'specify' command references
grep -r "specify " scripts/ .github/

# Common replacements:
# - "specify init" -> "flowspec init"
# - "specify dev-setup" -> "flowspec dev-setup"
# - "specify workflow" -> "flowspec workflow"
# - "uv run specify" -> "uv run flowspec"
```

### 4. Update Python Imports

If you import from the CLI module directly:

```python
# Before
from specify_cli import main
from specify_cli.commands import init

# After
from flowspec_cli import main
from flowspec_cli.commands import init
```

### 5. Update pytest Plugin References

If you use the pytest plugin for acceptance criteria:

```python
# Before (pyproject.toml or pytest.ini)
pytest_plugins = ["specify_ac"]

# After
pytest_plugins = ["flowspec_ac"]
```

## Environment Variables

The following environment variable names remain unchanged:
- `SPECIFY_FEATURE` - Override feature detection for non-Git repos  
  _(This variable retains the old 'specify' naming for backward compatibility. It may be renamed to `FLOWSPEC_FEATURE` in a future release, but for now, please continue to use `SPECIFY_FEATURE`.)_
- `GITHUB_FLOWSPEC` - GitHub token for API requests

## Slash Commands

All slash commands remain unchanged:
- `/flow:specify`, `/flow:plan`, `/flow:implement`, etc.

## Breaking Changes

### Module Renaming

The internal module structure changed from `specify_cli` to `flowspec_cli`. If you have any direct imports or references to internal modules, update them:

| Old Path | New Path |
|----------|----------|
| `src/specify_cli/` | `src/flowspec_cli/` |
| `specify_cli.__version__` | `flowspec_cli.__version__` |
| `specify_cli.commands.*` | `flowspec_cli.commands.*` |

### pytest Coverage Paths

If you have coverage configurations:

```toml
# Before (pyproject.toml)
[tool.pytest.ini_options]
addopts = "--cov=src/specify_cli"

# After
[tool.pytest.ini_options]
addopts = "--cov=src/flowspec_cli"
```

## Verification

After migration, verify everything works:

```bash
# Check CLI is installed
flowspec --version

# Run dev-setup to ensure templates work
flowspec dev-setup --force

# Run tests
pytest tests/
```

## Troubleshooting

### Command Not Found

If `flowspec` command is not found after installation:

```bash
# Reinstall with force
uv tool install flowspec-cli --force

# Or add to PATH if using pip
pip show flowspec-cli  # Check installation location
```

### Import Errors

If you see `ModuleNotFoundError: No module named 'specify_cli'`:

1. Search for remaining references: `grep -r "specify_cli" .`
2. Update all imports to `flowspec_cli`
3. Update any shell scripts that reference the old module

### Old Package Still Installed

If both packages are installed:

```bash
pip uninstall specify-cli
pip install flowspec-cli --force-reinstall
```

## Timeline

- **v0.2.359**: Last version with `specify-cli` name
- **v0.2.360+**: New `flowspec-cli` name

## Need Help?

- Open an issue: https://github.com/jpoles1/flowspec/issues
- Check documentation: `docs/guides/`
