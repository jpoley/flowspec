# Security Tasks Parallel Execution Plan

## CRITICAL: Single Host, Multiple Subagents

**ALL tasks execute on muckross using parallel SUBAGENTS, NOT multiple hosts.**

Other hosts (galway, kinsale, adare) are busy with other work streams.

## Execution Model

```
muckross (this host)
    ├── Subagent 1: Task A
    ├── Subagent 2: Task B
    ├── Subagent 3: Task C
    └── (parallel Task tool calls)
```

## Task Dependencies (21 remaining after task-220)

### Wave 1: Foundation (No dependencies) - 3 parallel subagents
| Subagent | Task | Duration | Files |
|----------|------|----------|-------|
| 1 | task-217 (Config System) | 2h | `src/specify_cli/config/security_config.py` |
| 2 | task-258 (ADR-008 Impl) | 2h | MCP server docs |
| 3 | task-212 (Triage Engine) | 3h | `.claude/skills/security-triage.md` |

### Wave 2: Core Skills (Depends on Wave 1) - 3 parallel subagents
| Subagent | Task | Depends On | Files |
|----------|------|------------|-------|
| 1 | task-213 (Fix Generator) | task-212 | `.claude/skills/security-fixer.md` |
| 2 | task-214 (Report Gen) | task-212 | `.claude/skills/security-reporter.md` |
| 3 | task-221 (Personas) | task-212, task-217 | `.claude/skills/security-triage-*.md` |

### Wave 3: Extensions (Depends on Wave 1-2) - up to 6 parallel subagents
| Subagent | Task | Depends On |
|----------|------|------------|
| 1 | task-223 (Custom Rules) | task-217 |
| 2 | task-252 (Policy Engine) | task-217 |
| 3 | task-224 (MCP Server) | task-258 |
| 4 | task-222 (Playwright DAST) | none |
| 5 | task-225 (CodeQL) | none |
| 6 | task-226 (AFL++) | none |

### Wave 4: Integration (Bottleneck) - 1 subagent
| Subagent | Task | Depends On |
|----------|------|------------|
| 1 | task-216 (Workflow Integration) | task-212, task-213, task-214 |

### Wave 5: Operations - 4 parallel subagents
| Subagent | Task | Depends On |
|----------|------|------------|
| 1 | task-248 (CI/CD Pipeline) | task-216 |
| 2 | task-251 (Pre-commit) | task-212 |
| 3 | task-250 (Observability) | task-212 |
| 4 | task-253 (DORA Metrics) | task-250 (soft) |

### Wave 6: Quality - 4 parallel subagents
| Subagent | Task | Depends On |
|----------|------|------------|
| 1 | task-218 (Documentation) | ALL previous |
| 2 | task-219 (Test Suite) | task-212, task-213, task-214 |
| 3 | task-280 (Benchmark) | task-212 |
| 4 | task-254 (Docker Image) | task-248 |

## File Conflicts (CANNOT run in same wave)

| Conflict Group | Tasks | Reason |
|----------------|-------|--------|
| Config files | task-217, task-223, task-252 | Same `security_config.py` |
| Triage skill | task-212, task-221 | task-221 extends task-212 |
| Metrics | task-250, task-253 | Related metrics files |

## Execution Commands

### Wave 1 (Launch 3 subagents in parallel)
```
Use Task tool with 3 parallel invocations:
- Subagent 1: task-217
- Subagent 2: task-258
- Subagent 3: task-212
```

### Wave 2 (After Wave 1 completes)
```
Use Task tool with 3 parallel invocations:
- Subagent 1: task-213
- Subagent 2: task-214
- Subagent 3: task-221
```

## Time Estimate

| Strategy | Time |
|----------|------|
| Sequential (1 task at a time) | ~50 hours |
| Parallel subagents (3-6 per wave) | ~15-20 hours |

## Host Assignment

**ALL tasks: @muckross (this host)**

No other hosts involved. Galway, kinsale, adare have their own work streams.
