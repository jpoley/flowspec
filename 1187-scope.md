# Issue #1187 Scope Analysis

## Summary

Feature request to consolidate flowspec configuration files into a single `.flowspec/` directory. This analysis evaluates what can and cannot be consolidated based on external tool constraints.

---

## Platform Convention Constraints

These directories have **hardcoded paths** that external tools depend on. They **cannot be relocated**.

### Claude Code (Anthropic)

| Directory | Purpose | Constraint |
|-----------|---------|------------|
| `.claude/commands/` | Slash commands (`/flow:*`, `/vibe`) | Claude Code looks here by convention |
| `.claude/skills/` | Model-invoked skills | Claude Code looks here by convention |
| `.claude/rules/` | Auto-loaded context rules | Claude Code looks here by convention |
| `.claude/agents/` | Agent definitions | Claude Code looks here by convention |
| `CLAUDE.md` | Project instructions | Claude Code looks here by convention |
| `memory/` | Persistent memory files | Claude Code convention (may vary) |

**Impact**: Moving `.claude/commands/flow/` to `.flowspec/commands/flow/` would break all `/flow:*` slash commands.

### GitHub

| Directory | Purpose | Constraint |
|-----------|---------|------------|
| `.github/workflows/` | GitHub Actions CI/CD | GitHub hardcoded path |
| `.github/ISSUE_TEMPLATE/` | Issue templates | GitHub hardcoded path |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR template | GitHub hardcoded path |
| `.github/CODEOWNERS` | Code ownership | GitHub hardcoded path |
| `.github/dependabot.yml` | Dependabot config | GitHub hardcoded path |

**Impact**: Moving workflows to `.flowspec/github/workflows/` means GitHub won't execute them.

### GitHub Copilot

| Directory | Purpose | Constraint |
|-----------|---------|------------|
| `.github/copilot-instructions.md` | Copilot context | GitHub Copilot hardcoded path |
| `.github/prompts/` | Copilot prompt files | GitHub Copilot convention |

**Impact**: Moving prompts to `.flowspec/` breaks Copilot integration.

### VSCode

| Directory | Purpose | Constraint |
|-----------|---------|------------|
| `.vscode/settings.json` | Workspace settings | VSCode hardcoded path |
| `.vscode/extensions.json` | Recommended extensions | VSCode hardcoded path |
| `.vscode/launch.json` | Debug configurations | VSCode hardcoded path |

**Impact**: Moving to `.flowspec/vscode/` means VSCode won't apply settings.

### Pre-commit

| File | Purpose | Constraint |
|------|---------|------------|
| `.pre-commit-config.yaml` | Pre-commit hooks config | Pre-commit hardcoded path |

**Impact**: Must remain in project root.

---

## What CAN Be Consolidated

These are flowspec-specific files with no external tool dependencies:

### Currently Consolidatable

| Current Location | Proposed Location | Notes |
|------------------|-------------------|-------|
| `flowspec_workflow.yml` | `.flowspec/workflow.yml` | State machine config |
| `.flowspec/logs/` | `.flowspec/logs/` | Already here |
| `.flowspec/hooks/` | `.flowspec/hooks/` | Already here |
| `.logs/` | `.flowspec/logs/` | Merge with existing |

### Template-Specific (in `templates/`)

| Current Location | Proposed Location | Notes |
|------------------|-------------------|-------|
| `templates/partials/` | `templates/.flowspec/partials/` | Internal references |
| `templates/constitutions/` | `templates/.flowspec/constitutions/` | Internal to flowspec |
| `templates/security-rules/` | `templates/.flowspec/security-rules/` | Semgrep rules |
| `templates/logs/` | `templates/.flowspec/logs/` | Log structure |

---

## What CANNOT Be Consolidated

### Hard Constraints (External Tools)

| Directory | Reason |
|-----------|--------|
| `.claude/commands/` | Claude Code slash command discovery |
| `.claude/skills/` | Claude Code skill discovery |
| `.claude/rules/` | Claude Code auto-loading |
| `.github/workflows/` | GitHub Actions execution |
| `.github/ISSUE_TEMPLATE/` | GitHub issue creation |
| `.vscode/` | VSCode workspace settings |
| `CLAUDE.md` | Claude Code project instructions |

### Soft Constraints (Convention/Expectation)

| Directory | Reason |
|-----------|--------|
| `memory/` | Claude Code memory convention |
| `backlog/` | Backlog.md MCP server expectation |
| `docs/` | Standard documentation location |

---

## Proposed Scoped Solution

Instead of full consolidation, create a **hybrid approach**:

### 1. Consolidate Flowspec-Only Files

```
.flowspec/
├── workflow.yml          # From flowspec_workflow.yml
├── hooks/                # Already here
├── logs/                 # Merge .logs/ into here
├── partials/             # Move from templates/partials/
├── constitutions/        # Move from templates/constitutions/
├── security-rules/       # Move from templates/security-rules/
└── rigor-config.yml      # Rigor rule overrides
```

### 2. Keep Platform-Required Directories

```
.claude/
├── commands/flow/        # Must stay - Claude Code
├── commands/vibe/        # Must stay - Claude Code
├── skills/               # Must stay - Claude Code
├── rules/                # Must stay - Claude Code
└── agents/               # Must stay - Claude Code

.github/
├── workflows/            # Must stay - GitHub Actions
├── ISSUE_TEMPLATE/       # Must stay - GitHub
└── prompts/              # Must stay - Copilot

.vscode/                  # Must stay - VSCode
```

### 3. Symlink Strategy (Optional)

For projects wanting a single "flowspec manifest", create symlinks:

```bash
# Example: Create a manifest listing all flowspec locations
cat > .flowspec/MANIFEST.md << 'EOF'
# Flowspec File Locations

Due to external tool constraints, flowspec files are in multiple locations:

- `.flowspec/` - Flowspec-specific configuration
- `.claude/commands/flow/` - Slash commands (Claude Code requirement)
- `.claude/skills/` - Skills (Claude Code requirement)
- `.github/workflows/` - CI/CD (GitHub requirement)
EOF
```

---

## Migration Considerations

### Breaking Changes

If any consolidation is done:
1. Existing projects need migration tooling
2. Documentation must be updated
3. `flowspec init` must generate new structure
4. `flowspec upgrade` command needed for existing projects

### Version Strategy

- Flowspec 0.4.x: Current structure
- Flowspec 0.5.0: Consolidated structure (breaking change)
- Migration guide required

---

## Recommendation

**Scope down the feature request to:**

1. ✅ Consolidate `flowspec_workflow.yml` → `.flowspec/workflow.yml`
2. ✅ Consolidate `.logs/` → `.flowspec/logs/`
3. ✅ Move flowspec-internal templates to `.flowspec/`
4. ❌ Do NOT move `.claude/`, `.github/`, `.vscode/`
5. 📄 Create `.flowspec/MANIFEST.md` documenting all locations

This provides the organizational benefits without breaking external tool integrations.

---

## References

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [VSCode Workspace Settings](https://code.visualstudio.com/docs/getstarted/settings)
