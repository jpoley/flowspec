# Memory Directory - Modular CLAUDE.md Components

This directory contains modular components imported by the root `CLAUDE.md` using `@import` syntax.

## Purpose

Breaking CLAUDE.md into modular components:
- Reduces duplication across projects
- Improves maintainability (single source of truth)
- Makes updates easier (change once, use everywhere)
- Keeps CLAUDE.md focused and scannable

## Structure

| File | Description | Imported By |
|------|-------------|-------------|
| `code-standards.md` | Python, testing, and commit standards | `CLAUDE.md` |
| `critical-rules.md` | Non-negotiable development rules (PR workflow, DCO, worktrees) | `CLAUDE.md` |
| `claude-hooks.md` | Documentation for all Claude Code hooks | `CLAUDE.md` |
| `mcp-configuration.md` | MCP server list, health checks, troubleshooting | `CLAUDE.md` |
| `constitution.md` | Project-specific core principles (template) | Project customization |
| `flowspec_workflow.yml` | Workflow configuration | `/flowspec` commands |
| `flowspec_workflow.schema.json` | Workflow config JSON schema | Validation |
| `WORKFLOW_DESIGN_SPEC.md` | Workflow system design spec | Reference |
| `decisions/` | JSONL decision logs (one file per task) | All workflow commands |

## Using @import Syntax

In CLAUDE.md or other markdown files, import modular components:

```markdown
@import memory/critical-rules.md
@import memory/code-standards.md
```

Claude Code will automatically inline the content when loading the file.

## Adding New Modules

1. Create a new `.md` file in this directory
2. Add descriptive content following existing patterns
3. Add an `@import` statement in `CLAUDE.md` at the appropriate location
4. Update this README with the new module
5. Test that imports load correctly

## Guidelines for Modular Files

- **Single responsibility**: Each file covers one logical topic
- **Self-contained**: Files should make sense independently
- **No circular imports**: Don't import files that import back
- **Clear headers**: Use `# Title` format for main heading
- **Consistent formatting**: Follow existing markdown style

## Benefits Achieved

- **Original CLAUDE.md**: 486 lines
- **Modular CLAUDE.md**: 211 lines (56% reduction)
- **Extracted content**: 292 lines across 4 modular files
- **Result**: More maintainable, less duplication, easier to scan

## Decision Logging

The `memory/decisions/` directory contains JSONL decision logs for all workflow tasks. Each task gets its own `.jsonl` file.

### Directory Structure

```
memory/decisions/
├── README.md           # Decision log documentation
├── task-541.jsonl      # Decision log for task-541
├── task-542.jsonl      # Decision log for task-542
└── ...                 # One file per task
```

### What Gets Logged

All significant decisions made during workflow execution:
- Technology choices (library, framework, pattern selection)
- Architecture changes and trade-offs
- Design pattern decisions
- Security approach choices
- Performance trade-offs
- Breaking changes

### How to Log Decisions

Use the helper script:

```bash
./scripts/bash/rigor-decision-log.sh \
  --task task-542 \
  --phase execution \
  --decision "Selected JSONL format for decision logs" \
  --rationale "Append-only, git-friendly, streaming-compatible" \
  --actor "@backend-engineer" \
  --alternatives "SQLite,Plain text,YAML"
```

### JSONL Schema

Each line is a valid JSON object with required and optional fields. See `memory/decisions/README.md` for:
- Full schema definition
- Query examples (using `jq`)
- Best practices for decision logging
- Integration with rigor rules (EXEC-003, VALID-001)

### Why JSONL?

- **Append-only**: Safe for concurrent writes
- **Git-friendly**: Line-based format shows clear diffs
- **Streaming-compatible**: Process one entry at a time
- **Queryable**: Standard `jq` tool for filtering and analysis
- **Version-controlled**: Full decision history in git

## Maintenance

When updating imported content:
1. Edit the modular file (e.g., `memory/critical-rules.md`)
2. Changes automatically apply to all files that import it
3. Test that imports still work correctly
4. Commit both the module and any dependent files
