# Migration Guide: specify to specflow

This guide helps you migrate from the old `specify` CLI command to the new `specflow` command.

## Why the Rename?

The CLI has been renamed from `specify` to `specflow` to:
- Establish clear branding identity for JP Spec Kit
- Avoid conflicts with generic "specify" terms
- Improve discoverability on PyPI and in search engines

## Quick Migration

### 1. Update Your Installation

```bash
# Remove old CLI (if installed)
uv tool uninstall specify-cli 2>/dev/null || true

# Install new CLI
uv tool install specflow-cli --from git+https://github.com/jpoley/jp-spec-kit.git
```

### 2. Update Your Commands

Simply replace `specify` with `specflow` in all commands:

| Old Command | New Command |
|-------------|-------------|
| `specify init` | `specflow init` |
| `specify workflow validate` | `specflow workflow validate` |
| `specify dev-setup` | `specflow dev-setup` |
| `specify security scan` | `specflow security scan` |
| `specify upgrade` | `specflow upgrade` |

## Deprecation Timeline

The old `specify` command will continue to work during the transition period:

| Phase | Timeline | `specify` Command Behavior |
|-------|----------|---------------------------|
| **Soft Launch** | Now - Month 2 | Works with deprecation warning |
| **Hard Deprecation** | Month 4-6 | Fails with migration guide |
| **Removal** | v2.0.0+ | Command removed completely |

## Automatic Script Migration

### Bash Scripts

```bash
# Find and replace in your scripts
find . -name "*.sh" -exec sed -i 's/\bspecify\b/specflow/g' {} +

# Or use this more targeted approach for common patterns:
find . -name "*.sh" -exec sed -i \
  -e 's/uv run specify/uv run specflow/g' \
  -e 's/specify init/specflow init/g' \
  -e 's/specify workflow/specflow workflow/g' \
  -e 's/specify security/specflow security/g' \
  -e 's/specify dev-setup/specflow dev-setup/g' \
  {} +
```

### CI/CD Workflows (GitHub Actions)

```yaml
# Old
- run: uv run specify workflow validate

# New
- run: uv run specflow workflow validate
```

### Shell Aliases

Update your shell configuration (`.bashrc`, `.zshrc`):

```bash
# Old alias (remove or update)
# alias specify='...'

# New aliases
alias jp='specflow'
alias jps='specflow security scan'
alias jpw='specflow workflow validate'
```

## What Stays the Same

The following have NOT changed:

- **Internal package name**: `specify_cli` (Python import paths unchanged)
- **Slash commands**: `/jpspec:specify`, `/speckit:*`, etc.
- **Directory names**: `.specify/` configuration directory
- **File names**: `*-specify-*` rule files for AI agents

## Package Name Change

| Component | Old Name | New Name |
|-----------|----------|----------|
| PyPI Package | `specify-cli` | `specflow-cli` |
| CLI Command | `specify` | `specflow` |
| Version | 0.2.x | 1.0.0+ |

## Troubleshooting

### "specify: command not found"

The old command may have been removed. Install the new CLI:

```bash
uv tool install specflow-cli --from git+https://github.com/jpoley/jp-spec-kit.git
```

### Deprecation Warning Appears

This is expected behavior during the transition period. Update your scripts to use `specflow` to suppress the warning.

### Scripts Still Using Old Command

Search your codebase for remaining references:

```bash
# Find all references to old command
grep -r "specify " --include="*.sh" --include="*.yml" --include="*.yaml" .
grep -r "specify-cli" --include="*.sh" --include="*.yml" --include="*.yaml" .
```

## Need Help?

- Open an issue: https://github.com/jpoley/jp-spec-kit/issues
- Check documentation: https://github.com/jpoley/jp-spec-kit/blob/main/docs/
