# VS Code Copilot Agents

This directory contains agent definitions for VS Code Copilot Chat, automatically generated from Claude Code commands.

## Purpose

VS Code Copilot supports custom agents (`.agent.md` files) that provide specialized AI assistance. This directory bridges Flowspec's Claude Code commands to VS Code Copilot, enabling the same workflow capabilities in both environments.

## File Naming Convention

Files follow the pattern: `{namespace}-{command}.agent.md`

- `flow-*` - Workflow orchestration agents (assess, specify, plan, implement, validate, operate)
- `speckit-*` - Specification toolkit agents (clarify, configure, tasks)
- `dev-*` - Developer tooling agents (debug, refactor, cleanup)
- `qa-*` - Quality assurance agents (test, review, verify)
- `sec-*` - Security agents (scan, triage, fix, report)
- `ops-*` - Operations agents (monitor, respond, scale, deploy)
- `arch-*` - Architecture agents (decide, model, design)
- `pm-*` - Product management agents (assess, define, discover)

## Sync Process

Agents are generated from Claude Code commands via:

```bash
# Generate/update all agents
./scripts/bash/sync-copilot-agents.sh

# Preview changes without writing
./scripts/bash/sync-copilot-agents.sh --dry-run

# Validate agents match source commands (CI check)
./scripts/bash/sync-copilot-agents.sh --validate

# Generate for specific role only
./scripts/bash/sync-copilot-agents.sh --role dev
```

### Automatic Sync (Pre-commit Hook)

The `pre-commit-agent-sync.sh` hook automatically syncs agents when command files change during commits.

## Source of Truth

- **Claude Code commands**: `.claude/commands/**/*.md` (symlinks to templates)
- **Templates**: `templates/commands/**/*.md` (authoritative source)
- **Generated**: `.github/agents/*.agent.md` (this directory)

**Never edit files in this directory directly.** Changes will be overwritten on next sync.

## CI/CD Validation

The validate-commands.yml workflow checks:
1. All symlinks in `.claude/commands/` resolve correctly
2. Agent sync produces no drift (`--validate` flag)
3. Required template files exist

## VS Code Integration

To use agents in VS Code:
1. Install GitHub Copilot Chat extension
2. Open command palette (Ctrl+Shift+P / Cmd+Shift+P)
3. Select "Copilot: Select Agent"
4. Choose from flowspec agents

Agents are also accessible via `@agent-name` mentions in Copilot Chat.

## Related Documentation

- [Command Structure](../../docs/architecture/command-single-source-of-truth.md)
- [Agent Sync Design](../../build-docs/design/git-hook-agent-sync-design.md)
- [Workflow Configuration](../../flowspec_workflow.yml)
