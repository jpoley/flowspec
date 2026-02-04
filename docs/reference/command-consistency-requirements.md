# Flow Command Consistency Requirements

**Status:** Draft
**Created:** 2026-02-03
**Related Task:** task-605

## Overview

All `/flow:*` commands MUST consistently implement three core behaviors:

1. **Produce artifacts** in standardized locations
2. **Integrate with backlog** for task tracking
3. **Log decisions** for auditability

Currently, only 5 of 23 commands fully implement all three requirements.

## Required Behaviors

### 1. Artifact Production

Every command that performs work MUST produce artifacts in `docs/` subdirectories:

| Command Type | Artifact Location | Example |
|--------------|-------------------|---------|
| Assessment | `docs/assess/` | `docs/assess/{feature}-assessment.md` |
| Specification | `docs/prd/` | `docs/prd/{feature}-prd.md` |
| Research | `docs/research/` | `docs/research/{feature}-research.md` |
| Planning | `docs/adr/` | `docs/adr/ADR-{number}-{title}.md` |
| Security | `docs/security/` | `docs/security/{feature}-scan.json` |
| QA | `docs/qa/` | `docs/qa/{feature}-test-plan.md` |

**Exception:** Utility commands (`reset`, `rigor`) may not produce artifacts.

### 2. Backlog Integration

Every command MUST:

- Read task context if task ID provided or inferable
- Update task status/notes on completion
- Create follow-up tasks if work generates new items

```bash
# Commands should accept task context
/flow:implement task-123

# And update on completion
backlog task edit 123 --append-notes "Completed via /flow:implement"
```

### 3. Decision Logging

Every command that makes decisions MUST log to `.flowspec/logs/decisions/`:

```
.flowspec/logs/decisions/
├── {date}-{command}-{feature}.md
└── ...
```

**Decision log format:**
```markdown
# Decision: {Title}

**Date:** YYYY-MM-DD HH:MM
**Command:** /flow:{command}
**Task:** task-{id} (if applicable)
**Actor:** @{user|agent}

## Context
{Why this decision was needed}

## Decision
{What was decided}

## Rationale
{Why this option was chosen}

## Alternatives Considered
- {Alternative 1}: {Why rejected}
- {Alternative 2}: {Why rejected}
```

## Current Compliance Audit

> **Note:** Line counts are from `.claude/commands/flow/*.md` files.

### Fully Compliant (3 requirements met)

| Command | Artifacts | Backlog | Decisions | Lines |
|---------|-----------|---------|-----------|-------|
| assess | ✅ | ✅ | ✅ | 301 |
| plan | ✅ | ✅ | ✅ | 433 |
| research | ✅ | ✅ | ✅ | 439 |
| specify | ✅ | ✅ | ✅ | 370 |
| custom | ✅ | ✅ | ✅ | 222 |

### Partially Compliant (1-2 requirements met)

| Command | Artifacts | Backlog | Decisions | Lines | Gap |
|---------|-----------|---------|-----------|-------|-----|
| validate | ✅ | ✅ | ❌ | 1735 | Add decision logging |
| build | ✅ | ✅ | ❌ | 149 | Add decision logging |
| intake | ✅ | ✅ | ❌ | 256 | Add decision logging |
| pre-pr | ❌ | ✅ | ✅ | 153 | Add artifact output |
| generate-prp | ✅ | ✅ | ❌ | 365 | Add decision logging |
| implement | ✅ | ✅ | ❌ | 108 | Add decision logging |
| review | ❌ | ✅ | ❌ | 122 | Add artifacts, decisions |
| submit-n-watch-pr | ❌ | ✅ | ❌ | 1037 | Add artifacts, decisions |

### Non-Compliant (0 requirements met or utility)

| Command | Type | Action |
|---------|------|--------|
| init | Utility | Exempt - setup command |
| reset | Utility | Exempt - config command |
| rigor | Utility | Exempt - validation only |
| gate | Utility | Exempt - validation only |
| map-codebase | Utility | Add artifact output |

### Security Commands (Move to ps/dev-guard)

| Command | Status |
|---------|--------|
| security_fix | Move to separate package |
| security_report | Move to separate package |
| security_triage | Move to separate package |
| security_web | Move to separate package |
| security_workflow | Move to separate package |

## Implementation Priority

### P1 - High Impact (Core workflow)

1. **implement** - Add decision logging
2. **review** - Add artifact output + decision logging
3. **submit-n-watch-pr** - Add artifact output + decision logging
4. **validate** - Add decision logging

### P2 - Medium Impact

5. **build** - Add decision logging
6. **intake** - Add decision logging
7. **generate-prp** - Add decision logging

### P3 - Low Impact (Utility)

8. **map-codebase** - Add artifact output (optional)
9. **pre-pr** - Add artifact output (optional)

## Command Simplification Target

Commands should be **<200 lines each** for maintainability.

| Command | Current | Target | Reduction |
|---------|---------|--------|-----------|
| validate | 1735 | 200 | -87% |
| submit-n-watch-pr | 1037 | 300 | -71% |
| security_workflow | 647 | Move | N/A |
| security_fix | 532 | Move | N/A |

## Standard Command Template

All commands should follow this structure:

```markdown
---
description: {One-line description}
mode: agent
loop: inner|outer|both
---

# /flow:{command}

{2-3 sentence overview}

## Prerequisites
- {Required state or artifacts}

## Inputs
- Task ID (optional): Links to backlog task
- {Other inputs}

## Outputs
- **Artifact:** `docs/{type}/{feature}-{artifact}.md`
- **Decision Log:** `.flowspec/logs/decisions/{date}-{command}.md`
- **Backlog Update:** Task status/notes updated

## Workflow
1. {Step 1}
2. {Step 2}
3. Log decision to `.flowspec/logs/decisions/`
4. Update backlog task (if provided)

## Examples
{Minimal examples}
```

## Acceptance Criteria for Compliance

- [ ] All core commands (assess, specify, plan, implement, validate, review) log decisions
- [ ] All commands that produce work output artifacts to `docs/` subdirectories
- [ ] All commands accept optional task ID and update backlog on completion
- [ ] No command exceeds 300 lines (excluding security commands being moved)
- [ ] Security commands moved to `ps/dev-guard`

## References

- [everything-claude-code](https://github.com/affaan-m/everything-claude-code) - Reference implementation
- Command locations: `.claude/commands/flow/*.md`
