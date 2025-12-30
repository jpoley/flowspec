# Flowspec Backlog Simplification Analysis

**Date**: 2025-12-29
**Version**: v0.3.013
**Open Tasks**: 86
**Goal**: Streamline to a focused, maintainable tool

---

## Executive Summary

Flowspec has accumulated significant backlog debt with 86 open tasks, many of which are speculative infrastructure that adds complexity without clear user value. This analysis recommends:

- **Finish**: 3 tasks (already 80%+ complete)
- **Keep**: 5 tasks (clear value, reasonable effort)
- **Close**: 78 tasks (over-engineering, nice-to-have, or duplicate)

**Result**: 90% backlog reduction, focused roadmap

---

## What's Working (Core Value)

Flowspec already delivers significant value:

| Capability | Status | Value |
|------------|--------|-------|
| `flowspec init` | Working | Bootstrap AI-assisted projects |
| 15+ CLI commands | Working | quality, gate, workflow, memory, hooks |
| 20+ AI skills | Working | Security, architecture, workflow, QA |
| 7 command namespaces | Working | /flow, /spec, /arch, /dev, /ops, /qa, /sec |
| Task Memory | 90% complete | Persistent context across sessions |
| Rigor Rules | Documented | Workflow quality gates |
| Backlog.md integration | Working | Task management |
| Security scanning | Working | Trivy, Semgrep, custom rules |

**The tool works. It doesn't need 86 more features.**

---

## TIER 1: COMPLETE (High Value, Low Effort)

These tasks are nearly done and should be marked complete:

### task-368: Task Memory (Mark Done)
- **Status**: 90% complete (2,864 LOC implemented)
- **Missing**: AC #8 - backlog hook integration
- **Action**: Mark Done with note that manual workflow works
- **Workaround documented**: `backlog task edit && flowspec memory init`

### task-432: DCO Sign-off Enforcement
- **Status**: Already in critical-rules.md
- **Action**: Verify hooks enforce it, mark Done

### task-551: Rigor Rules in Critical Rules (Already Done)
- **Status**: Completed via PR #1081
- **Action**: Already marked Done

---

## TIER 2: KEEP (Medium Value, Reasonable Effort)

These 5 tasks have clear value and should remain open:

| Task | Description | Rationale |
|------|-------------|-----------|
| task-171 | Library doc MCP replacement | Useful if Context7 breaks |
| task-283 | Archive hook for workflow | Clean maintenance |
| task-284 | Archive documentation | Operational docs |
| task-468 | Prompt naming convention | One-time cleanup |
| task-435 | flowspec remove command | Clean uninstall |

---

## TIER 3: CLOSE AS WON'T DO

### Category A: Agent Event System (30 tasks)

**Tasks**: 485-540 (task-485 through task-540)

**What it is**: JSON Schema for 60 event types, 11 namespaces, action registry with 55 actions, event router, JSONL writer, query CLI.

**Why close**:
- Classic over-engineering - building infrastructure nobody asked for
- Massive maintenance burden (30 tasks = months of work)
- Flowspec works fine without sophisticated eventing
- No users requesting this capability
- Adds complexity to an already working system

**Specific tasks to close**:
```
task-485, task-486, task-487, task-504, task-507, task-508, task-509,
task-510, task-511, task-512, task-513, task-530, task-531, task-533,
task-534, task-535, task-536, task-537, task-538, task-539, task-540,
task-553, task-554, task-555
```

---

### Category B: Git Workflow Automation (15 tasks)

**Tasks**: 505-527

**What it is**: Custom worktree automation, GPG key management, container orchestration, pre-commit quality gates, local PR approval workflow.

**Why close**:
- Reinventing existing tools (git hooks, pre-commit, GitHub Actions)
- Container orchestration belongs in nanofuse, not flowspec
- GPG signing is already handled by git config
- Local PR approval is what GitHub is for
- These are platform features, not SDD features

**Specific tasks to close**:
```
task-505, task-506, task-514, task-515, task-516, task-517, task-518,
task-519, task-520, task-521, task-522, task-523, task-524, task-525,
task-526, task-527, task-528, task-529
```

---

### Category C: Role-Based Commands (5 tasks)

**Tasks**: 361-367

**What it is**: Role selection during init (PM, Dev, Sec, QA, All), role-to-command filtering, VSCode role integration.

**Why close**:
- Adds onboarding complexity without clear benefit
- Users can already use any command they want
- Role filtering is restriction, not empowerment
- Maintenance burden for minimal value
- Most users are "All" anyway

**Specific tasks to close**:
```
task-361, task-363, task-364, task-365, task-367
```

---

### Category D: Rigor Rules Integration (8 tasks)

**Tasks**: 546-550, 552

**What it is**: Integrate rigor rules into flow commands, add freeze command, workflow status tracking.

**Why close**:
- Rigor rules already documented in critical-rules.md
- Integration is polish, not core functionality
- `/flow:assess` and `/flow:plan` already reference rules via CLAUDE.md
- Adding more automation adds more maintenance

**Specific tasks to close**:
```
task-546, task-547, task-548, task-549, task-550, task-552
```

---

### Category E: Claude-Improves (11 of 12 tasks)

**Tasks**: 469-484 (keep 468)

**What it is**: CLAUDE.md scaffolding, template placeholders, VSCode extensions, symlinks, agents, MCP templates, CI checks, deployment reports.

**Why close**:
- Many are perfectionism, not user-facing improvements
- Template system already works
- VSCode integration is nice-to-have
- CI parity check is over-engineering
- Keep only task-468 (naming convention cleanup)

**Specific tasks to close**:
```
task-469, task-471, task-472, task-474, task-475, task-476, task-478,
task-479, task-481, task-484, task-293, task-294
```

---

### Category F: Documentation Tasks (3 tasks)

**Tasks**: 087, 134

**What it is**: Production case studies, diagram integration.

**Why close**:
- Case studies require real external users (we don't have them yet)
- Diagrams are polish, not functionality
- Documentation should follow usage, not precede it

**Specific tasks to close**:
```
task-087, task-134
```

---

### Category G: Miscellaneous Nice-to-Have (12 tasks)

**Why close**: Low priority, polish, or superseded

| Task | Description | Reason to Close |
|------|-------------|-----------------|
| task-079 | Stack selection during init | Complex, unclear value |
| task-084 | Spec quality metrics command | Metrics without users |
| task-168 | macOS CI matrix testing | Low priority |
| task-196 | Output style experiments | Polish |
| task-197 | Custom statusline | Polish |
| task-285 | CI check for stale Done tasks | Over-engineering |
| task-402 | Upstream backlog hook contrib | External dependency |
| task-429 | ASCII logo for CLI | Already have logo |
| task-430 | flowspec-cli replace specify | init already works |
| task-438 | GitHub setup docs | Docs follow usage |
| task-444 | CI validation post-Bookworm | Already working |
| task-445 | Post-migration monitoring | Already stable |

---

## Implementation Plan

### Phase 1: Mark Complete (Today)
```bash
# Task Memory - already implemented
backlog task edit task-368 -s Done --notes "90% complete, manual workflow documented. AC #8 deferred - requires upstream backlog hook support."

# DCO enforcement - already in rules
backlog task edit task-432 -s Done --notes "Enforced via critical-rules.md and DCO GitHub check."
```

### Phase 2: Close Won't Do Tasks (Today)

```bash
# Event System (24 tasks)
for id in 485 486 487 504 507 508 509 510 511 512 513 530 531 533 534 535 536 537 538 539 540 553 554 555; do
  backlog task edit task-$id -s Done --notes "Closed: Over-engineered event infrastructure. Flowspec works without it."
done

# Git Workflow Automation (18 tasks)
for id in 505 506 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529; do
  backlog task edit task-$id -s Done --notes "Closed: Reinvents existing tools (git hooks, pre-commit, GitHub Actions)."
done

# Role-Based Commands (5 tasks)
for id in 361 363 364 365 367; do
  backlog task edit task-$id -s Done --notes "Closed: Adds complexity without clear user value."
done

# Rigor Integration (6 tasks)
for id in 546 547 548 549 550 552; do
  backlog task edit task-$id -s Done --notes "Closed: Rules documented in critical-rules.md, integration is polish."
done

# Claude-Improves (13 tasks)
for id in 293 294 469 471 472 474 475 476 478 479 481 484; do
  backlog task edit task-$id -s Done --notes "Closed: Nice-to-have polish, not core functionality."
done

# Documentation (2 tasks)
for id in 087 134; do
  backlog task edit task-$id -s Done --notes "Closed: Requires real users first. Documentation follows usage."
done

# Miscellaneous (12 tasks)
for id in 079 084 168 196 197 285 402 429 430 438 444 445; do
  backlog task edit task-$id -s Done --notes "Closed: Low priority nice-to-have."
done
```

---

## Post-Cleanup State

### Before
- **Open Tasks**: 86
- **Complexity**: High (event systems, container orchestration, role management)
- **Focus**: Scattered across infrastructure and polish

### After
- **Open Tasks**: ~8
- **Complexity**: Low (clear, achievable goals)
- **Focus**: Core SDD workflow and maintenance

### Remaining Open Tasks
| Task | Priority | Description |
|------|----------|-------------|
| task-171 | Medium | Library doc MCP replacement |
| task-283 | Medium | Archive hook for workflow |
| task-284 | Medium | Archive documentation |
| task-435 | Medium | flowspec remove command |
| task-468 | High | Prompt naming convention |

---

## Principles Going Forward

1. **No speculative infrastructure** - Build only what users need today
2. **Prefer existing tools** - Don't reinvent git hooks, pre-commit, GitHub Actions
3. **Documentation follows usage** - Don't write case studies without users
4. **Simplicity over features** - A tool that does 5 things well beats one that does 50 poorly
5. **Maintenance burden matters** - Every feature is forever maintenance

---

## Appendix: Full Task Closure List

### Close as Done (Won't Do) - 80 tasks

**Event System**: 485, 486, 487, 504, 507, 508, 509, 510, 511, 512, 513, 530, 531, 533, 534, 535, 536, 537, 538, 539, 540, 553, 554, 555

**Git Workflow**: 505, 506, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529

**Role-Based**: 361, 363, 364, 365, 367

**Rigor Integration**: 546, 547, 548, 549, 550, 552

**Claude-Improves**: 293, 294, 469, 471, 472, 474, 475, 476, 478, 479, 481, 484

**Documentation**: 087, 134

**Miscellaneous**: 079, 084, 168, 196, 197, 285, 402, 429, 430, 438, 444, 445

### Keep Open - 5 tasks
171, 283, 284, 435, 468

### Mark Complete - 2 tasks
368, 432
