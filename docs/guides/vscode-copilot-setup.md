# VS Code Copilot Chat Setup Guide

This guide explains how to use flowspec commands in VS Code with GitHub Copilot Chat.

## Overview

Flowspec provides commands for both:
- **Claude Code CLI** - Uses `.claude/commands/` directory
- **VS Code Copilot Chat** - Uses `.github/agents/` directory

Both directories are kept in sync automatically, ensuring the same workflows work in both environments.

## Prerequisites

1. **VS Code** or **VS Code Insiders** installed
2. **GitHub Copilot** extension installed and authenticated
3. **GitHub Copilot Chat** extension installed

## Directory Structure

```
project/
├── .claude/commands/           # Claude Code slash commands
│   ├── flow/                   # /flow:* commands (symlinks)
│   └── speckit/                # /speckit:* commands (symlinks)
├── .github/agents/             # VS Code Copilot agents (auto-generated)
│   ├── flow-assess.agent.md
│   ├── flow-specify.agent.md
│   ├── flow-implement.agent.md
│   └── ...
└── templates/commands/         # Source templates (single source of truth)
```

## Using Copilot Chat Agents

### Option 1: @ Mention

Type `@` in Copilot Chat to see available agents:

```
@flow-specify Build a user authentication system with JWT tokens
```

Available agents include:
- `@flow-assess` - Evaluate SDD workflow suitability
- `@flow-specify` - Create feature specifications
- `@flow-plan` - Architecture planning
- `@flow-implement` - Implementation with code review
- `@flow-validate` - QA and security validation
- `@speckit-configure` - Configure workflow settings
- `@speckit-tasks` - Generate task breakdowns

### Option 2: Command Picker

1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Type "Copilot: Select Agent"
3. Choose from the flowspec agents list

### Option 3: Agent Handoffs

Some agents suggest follow-up agents. For example, after `@flow-assess` completes, it may suggest using `@flow-specify` next.

## Keeping Agents in Sync

### Automatic Sync (Pre-commit Hook)

If you modify command templates, the pre-commit hook automatically regenerates agents:

```bash
# The hook runs automatically on commit
git commit -m "Update flow-specify command"
# → pre-commit-agent-sync.sh runs
# → .github/agents/ files updated
```

### Manual Sync

To manually regenerate agents:

```bash
# Regenerate all agents
./scripts/bash/sync-copilot-agents.sh

# Preview changes without writing
./scripts/bash/sync-copilot-agents.sh --dry-run

# Force regeneration
./scripts/bash/sync-copilot-agents.sh --force
```

### Validate Sync

Check if agents match commands:

```bash
./scripts/bash/sync-copilot-agents.sh --validate
# Exit code 0 = in sync
# Exit code 2 = drift detected
```

## Troubleshooting

### Agents Not Appearing in Copilot Chat

1. **Verify `.github/agents/` exists** with `.agent.md` files
2. **Reload VS Code window** (`Ctrl+Shift+P` → "Developer: Reload Window")
3. **Check Copilot Chat is enabled** in VS Code settings

### Agent Content Outdated

Run the sync script to regenerate:

```bash
./scripts/bash/sync-copilot-agents.sh --force
```

### Sync Script Fails

1. **Check Python is available**: The script uses Python for YAML parsing
2. **Verify uv is installed**: `uv --version`
3. **Check template files exist**: `ls templates/commands/`

### Different Behavior in CLI vs VS Code

The agents are generated from the same templates, but there may be minor differences:
- CLI supports `{{INCLUDE:...}}` directives at runtime
- Agents have includes pre-resolved at generation time

If you notice differences, regenerate agents and verify the content matches.

## CI/CD Validation

PRs are automatically validated for agent sync drift:

```yaml
# .github/workflows/validate-agent-sync.yml
- Runs on PRs that modify command files
- Fails if .github/agents/ is out of sync
- Works on Linux, macOS, and Windows
```

## Best Practices

1. **Edit templates, not agents**: Always edit files in `templates/commands/`, not `.github/agents/`
2. **Let sync run automatically**: The pre-commit hook handles regeneration
3. **Verify after template changes**: Run `--validate` to confirm sync
4. **Don't commit partial changes**: Commit both template and agent changes together

## Related Documentation

- [README - Supported AI Agents](../../README.md#supported-ai-agents)
- [.github/agents/README](../../.github/agents/README.md)
- [Command Single Source of Truth](../architecture/command-single-source-of-truth.md)
