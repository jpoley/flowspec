# Backlog Task Review - December 31, 2025

> **Purpose**: Pragmatic review of all open tasks to clean up the backlog before new features.
> **Approach**: Ultra-think analysis with honest recommendations.

## Executive Summary

| Recommendation | Count | Action |
|----------------|-------|--------|
| **Abandon** | 45 | Close as "won't do" - over-engineered or obsolete |
| **Hold** | 12 | Keep but deprioritize - nice to have |
| **Finish** | 8 | Complete - high value, near done, or blocking |

**Key Finding**: The backlog is bloated with an over-engineered "Agent Event System" (30+ tasks) that represents speculative architecture. The core flowspec functionality works well without it.

---

## Task Review Table

| Task | Category | Related Tasks | Feature | Detail | % Done | Recommendation |
|------|----------|---------------|---------|--------|--------|----------------|
| **task-368** | Core | task-402 | Task Memory | Persistent context management across sessions | 90% | **FINISH** |
| **task-402** | Core | task-368 | Backlog Hooks | Upstream contribution for lifecycle events | 0% | **FINISH** |
| **task-432** | CI/CD | - | DCO Sign-off | Enforce commit signing for compliance | 0% | **FINISH** |
| **task-084** | CLI | - | Quality Metrics | `flowspec quality` command for spec scoring | 10% | **FINISH** |
| **task-435** | CLI | task-430 | Remove Command | `flowspec remove` to purge artifacts | 0% | **FINISH** |
| **task-171** | MCP | - | Library Docs MCP | Replace context7 for library documentation | 0% | **FINISH** |
| **task-168** | CI/CD | - | macOS CI Matrix | Add macOS to CI testing matrix | 0% | **FINISH** |
| **task-546** | Rigor | task-547 | Rigor in Assess | Add rigor rules to /flow:assess | 0% | **FINISH** |
| **task-087** | Docs | - | Case Studies | Production usage documentation | 0% | **HOLD** |
| **task-134** | Docs | - | Diagram Integration | Integrate Mermaid/Excalidraw docs | 0% | **HOLD** |
| **task-283** | Hooks | task-284 | Archive Hook | Post-workflow archive automation | 0% | **HOLD** |
| **task-284** | Docs | task-283 | Archive Docs | Documentation for archive-tasks.sh | 0% | **HOLD** |
| **task-196** | UX | task-197 | Output Styles | Experiment with phase output formatting | 0% | **HOLD** |
| **task-197** | UX | task-196 | Statusline | Custom statusline with workflow context | 0% | **HOLD** |
| **task-285** | CI/CD | - | Stale Task Check | CI check for stale Done tasks | 0% | **HOLD** |
| **task-429** | CLI | task-430 | ASCII Logo | Flowspec CLI branding | 0% | **HOLD** |
| **task-430** | CLI | task-429, 435 | Flowspec CLI | Replace specify init | 0% | **HOLD** |
| **task-438** | Docs | - | GitHub Setup Guide | User guide for GitHub features | 0% | **HOLD** |
| **task-547** | Rigor | task-546 | Rigor in Plan | Add rigor rules to /flow:plan | 0% | **HOLD** |
| **task-549** | Workflow | - | Freeze Command | /flow:freeze for task suspension | 0% | **HOLD** |
| **task-293** | Testing | task-294 | LLM Accuracy Tests | Constitution customization accuracy | 0% | **ABANDON** |
| **task-294** | Testing | task-293 | Constitution Tests | Constitution enforcement integration | 0% | **ABANDON** |
| **task-361** | Roles | task-364, 365, 367 | Role Selection | Role selection in init/reset | 0% | **ABANDON** |
| **task-363** | Roles | task-361 | Agent Sync Roles | Role-based agent generation | 0% | **ABANDON** |
| **task-364** | Roles | task-361 | Schema Roles | Add vscode_roles to schema | 0% | **ABANDON** |
| **task-365** | Roles | task-361 | Role CI | Role-based CI validation | 0% | **ABANDON** |
| **task-367** | Roles | task-361 | Role Namespaces | Create role-based command dirs | 0% | **ABANDON** |
| **task-444** | CI/CD | task-445 | Bookworm Migration | Validate CI post-migration | 0% | **ABANDON** |
| **task-445** | CI/CD | task-444 | Post-Migration | Monitoring and documentation | 0% | **ABANDON** |
| **task-468** | Prompts | task-469 | Naming Convention | Standardize prompt naming | 0% | **ABANDON** |
| **task-469** | Docs | task-468 | Agent Alignment | Document Copilot vs Claude alignment | 0% | **ABANDON** |
| **task-471** | Init | task-472 | CLAUDE.md Scaffold | Add CLAUDE.md to flowspec init | 0% | **ABANDON** |
| **task-472** | Init | task-471 | Placeholder Handling | Improve template placeholders | 0% | **ABANDON** |
| **task-474** | Init | - | VSCode Extensions | Populate extensions.json template | 0% | **ABANDON** |
| **task-475** | Init | - | GitHub Symlinks | Symlinks for GitHub prompts | 0% | **ABANDON** |
| **task-476** | Agents | - | Missing Agents | Create agents for non-speckit commands | 0% | **ABANDON** |
| **task-478** | Init | - | MCP Template | Add .mcp.json template | 0% | **ABANDON** |
| **task-479** | CI/CD | - | Template Parity CI | CI check for template-deployment parity | 0% | **ABANDON** |
| **task-481** | Init | - | Completeness Report | Deployment completeness report | 0% | **ABANDON** |
| **task-484** | Init | - | VSCode Python | VSCode settings for Python/FastAPI | 0% | **ABANDON** |
| **task-485** | Events | task-486-540 | Event Schema | Core event schema v1.1.0 | 0% | **ABANDON** |
| **task-486** | Events | task-485 | JSONL Writer | Event writer library | 0% | **ABANDON** |
| **task-487** | Events | task-485 | Event Router | Namespace dispatch routing | 0% | **ABANDON** |
| **task-504** | Events | task-485 | Event Query | CLI and API for event queries | 0% | **ABANDON** |
| **task-505** | Events | task-485 | Git Config Schema | Git workflow configuration | 0% | **ABANDON** |
| **task-506** | Events | task-505 | Config Loader | Configuration validation | 0% | **ABANDON** |
| **task-507** | Events | task-485 | Hook Events | Claude Code hook event emission | 0% | **ABANDON** |
| **task-508** | Events | task-485 | Backlog Events | Backlog operation events | 0% | **ABANDON** |
| **task-509** | Events | task-485 | Git Events | Git operation events | 0% | **ABANDON** |
| **task-510** | Events | task-485 | MCP Events | MCP server events | 0% | **ABANDON** |
| **task-511** | Events | task-485 | Action Registry | 55 action implementations | 0% | **ABANDON** |
| **task-512** | Events | task-511 | Action Decorators | Action helper system | 0% | **ABANDON** |
| **task-513** | Events | task-511 | Action Mapping | Action to event mapping | 0% | **ABANDON** |
| **task-514** | Events | task-511 | Followup Validation | Allowed followups validation | 0% | **ABANDON** |
| **task-515** | Git | task-517 | Worktree Creation | Git worktree automation | 0% | **ABANDON** |
| **task-516** | Git | task-515 | Worktree Cleanup | Worktree cleanup automation | 0% | **ABANDON** |
| **task-517** | Git | task-515 | Git Hook Framework | Local PR git hooks | 0% | **ABANDON** |
| **task-518** | Git | task-517 | Pre-Commit Lint | Lint quality gate | 0% | **ABANDON** |
| **task-519** | Git | task-517 | Pre-Commit Test | Test quality gate | 0% | **ABANDON** |
| **task-520** | Git | task-517 | Pre-Commit SAST | SAST quality gate | 0% | **ABANDON** |
| **task-521** | Git | task-517 | Local PR Approval | Local approval workflow | 0% | **ABANDON** |
| **task-522** | Security | task-523 | GPG Key Design | Agent GPG key management | 0% | **ABANDON** |
| **task-523** | Security | task-522 | GPG Generation | GPG key generation for agents | 0% | **ABANDON** |
| **task-524** | Security | task-523 | Auto Signing | Automated commit signing | 0% | **ABANDON** |
| **task-525** | Containers | task-526, 527 | Container Strategy | Container orchestration design | 0% | **ABANDON** |
| **task-526** | Containers | task-525 | Container Launch | Container launch automation | 0% | **ABANDON** |
| **task-527** | Containers | task-525 | Secret Injection | Runtime secret injection | 0% | **ABANDON** |
| **task-528** | Containers | task-525 | Resource Monitoring | Container resource monitoring | 0% | **ABANDON** |
| **task-529** | Containers | task-525 | Container Cleanup | Container cleanup automation | 0% | **ABANDON** |
| **task-530** | Events | task-485 | Decision Events | Decision event emission | 0% | **ABANDON** |
| **task-531** | Events | task-530 | Decision Query | Decision query utilities | 0% | **ABANDON** |
| **task-532** | Events | task-530 | Reversibility Tool | Reversibility assessment | 0% | **ABANDON** |
| **task-533** | Git | task-505 | Git State Machine | Git workflow state machine | 0% | **ABANDON** |
| **task-534** | Git | task-533 | State Recovery | State recovery utilities | 0% | **ABANDON** |
| **task-535** | Git | task-533 | Cleanup Orchestrator | Automated cleanup orchestration | 0% | **ABANDON** |
| **task-536** | Docs | task-485 | Event Architecture | Event system architecture docs | 0% | **ABANDON** |
| **task-537** | Testing | task-485 | Event Tests | Event system integration tests | 0% | **ABANDON** |
| **task-538** | Testing | task-485 | Event Benchmarks | Event system performance tests | 0% | **ABANDON** |
| **task-539** | Metrics | task-485 | DORA Dashboard | DORA metrics dashboard | 0% | **ABANDON** |
| **task-540** | Docs | task-485 | Event Runbooks | Operational runbooks | 0% | **ABANDON** |
| **task-548** | Rigor | - | Rigor in Operate | Add rigor rules to /flow:operate | 0% | **ABANDON** |
| **task-550** | Workflow | - | Status Tracking | Workflow status in commands | 0% | **ABANDON** |
| **task-552** | Docs | - | Rigor Troubleshoot | Rigor rules troubleshooting guide | 0% | **ABANDON** |
| **task-553** | Logging | task-554, 555 | Log Aggregation | Combine daily logs into summaries | 0% | **ABANDON** |
| **task-554** | Logging | task-553 | Log Analytics | Query logs for patterns | 0% | **ABANDON** |
| **task-555** | Logging | task-553 | Central Logging | Integrate with central logging | 0% | **ABANDON** |

---

## Abandon Tasks: Effort, Complexity & Value Analysis

> **Effort**: 1-10 (1=trivial, 10=massive)
> **Complexity**: 1-10 (1=simple, 10=very complex)
> **Value**: 1-10 (1=no user value, 10=critical user need)

**Sorted by Effort (lowest first):**

| Task | Feature | Effort | Complexity | Value | Notes |
|------|---------|--------|------------|-------|-------|
| **task-548** | Rigor in Operate | 1 | 1 | 0 | **OBSOLETE - command removed** |
| **task-474** | VSCode Extensions | 1 | 1 | 6 | Simple JSON, improves DX |
| **task-469** | Agent Alignment | 2 | 2 | 3 | Documentation only |
| **task-471** | CLAUDE.md Scaffold | 2 | 2 | 7 | Users expect this |
| **task-445** | Post-Migration | 2 | 3 | 2 | Unclear if needed |
| **task-475** | GitHub Symlinks | 2 | 2 | 4 | Minor convenience |
| **task-478** | MCP Template | 2 | 2 | 7 | Users need MCP setup |
| **task-484** | VSCode Python | 2 | 2 | 5 | Stack-specific settings |
| **task-552** | Rigor Troubleshoot | 2 | 2 | 3 | Docs for edge cases |
| **task-364** | Schema Roles | 2 | 3 | 3 | Part of role system |
| **task-363** | Agent Sync Roles | 3 | 4 | 3 | Already works without |
| **task-367** | Role Namespaces | 3 | 3 | 3 | Already exists |
| **task-444** | Bookworm Migration | 3 | 4 | 2 | CI works fine |
| **task-468** | Naming Convention | 3 | 3 | 4 | Reduces confusion |
| **task-472** | Placeholder Handling | 3 | 4 | 5 | Better UX |
| **task-481** | Completeness Report | 3 | 4 | 4 | Nice feedback |
| **task-514** | Followup Validation | 3 | 4 | 2 | Event system dep |
| **task-516** | Worktree Cleanup | 3 | 4 | 3 | Git does this |
| **task-518** | Pre-Commit Lint | 3 | 4 | 4 | Pre-commit exists |
| **task-530** | Decision Events | 3 | 4 | 2 | Event system dep |
| **task-540** | Event Runbooks | 3 | 3 | 1 | Docs for unused system |
| **task-361** | Role Selection | 4 | 5 | 4 | UX complexity |
| **task-365** | Role CI | 4 | 5 | 3 | CI already validates |
| **task-476** | Missing Agents | 4 | 4 | 5 | Agents work now |
| **task-479** | Template Parity CI | 4 | 5 | 4 | Catches drift |
| **task-505** | Git Config Schema | 4 | 5 | 2 | Event system dep |
| **task-506** | Config Loader | 4 | 5 | 2 | Event system dep |
| **task-507** | Hook Events | 4 | 5 | 3 | Hooks work without events |
| **task-508** | Backlog Events | 4 | 5 | 3 | Backlog works fine |
| **task-509** | Git Events | 4 | 5 | 2 | Git works fine |
| **task-510** | MCP Events | 4 | 5 | 2 | MCP works fine |
| **task-513** | Action Mapping | 4 | 5 | 2 | Event system dep |
| **task-515** | Worktree Creation | 4 | 5 | 3 | Git does this |
| **task-519** | Pre-Commit Test | 4 | 5 | 4 | CI runs tests |
| **task-520** | Pre-Commit SAST | 4 | 5 | 5 | CI runs SAST |
| **task-524** | Auto Signing | 4 | 5 | 4 | DCO is simpler |
| **task-529** | Container Cleanup | 4 | 5 | 2 | Out of scope |
| **task-531** | Decision Query | 4 | 5 | 2 | Event system dep |
| **task-536** | Event Architecture | 4 | 4 | 1 | Docs for unused system |
| **task-550** | Status Tracking | 4 | 5 | 5 | Workflow visibility |
| **task-553** | Log Aggregation | 4 | 5 | 4 | Nice to have |
| **task-293** | LLM Accuracy Tests | 5 | 6 | 3 | Over-testing |
| **task-486** | JSONL Writer | 5 | 6 | 2 | Event system dep |
| **task-504** | Event Query | 5 | 6 | 3 | Event system dep |
| **task-512** | Action Decorators | 5 | 6 | 2 | Event system dep |
| **task-521** | Local PR Approval | 5 | 6 | 3 | GitHub does this |
| **task-522** | GPG Key Design | 5 | 7 | 3 | Security theater |
| **task-523** | GPG Generation | 5 | 6 | 3 | Overkill |
| **task-526** | Container Launch | 5 | 6 | 2 | Out of scope |
| **task-527** | Secret Injection | 5 | 7 | 3 | Out of scope |
| **task-528** | Resource Monitoring | 5 | 6 | 2 | Out of scope |
| **task-532** | Reversibility Tool | 5 | 6 | 3 | Nice idea |
| **task-534** | State Recovery | 5 | 6 | 3 | Event system dep |
| **task-538** | Event Benchmarks | 5 | 6 | 1 | Tests for unused system |
| **task-554** | Log Analytics | 5 | 6 | 4 | Useful if logs grow |
| **task-294** | Constitution Tests | 6 | 7 | 3 | Over-testing |
| **task-487** | Event Router | 6 | 7 | 2 | Event system dep |
| **task-517** | Git Hook Framework | 6 | 7 | 4 | Pre-commit exists |
| **task-525** | Container Strategy | 6 | 8 | 2 | Out of scope |
| **task-535** | Cleanup Orchestrator | 6 | 7 | 3 | Over-engineered |
| **task-537** | Event Tests | 6 | 6 | 1 | Tests for unused system |
| **task-555** | Central Logging | 6 | 7 | 3 | Enterprise feature |
| **task-485** | Event Schema | 7 | 8 | 2 | Foundation of unused system |
| **task-533** | Git State Machine | 7 | 8 | 3 | Over-engineered |
| **task-539** | DORA Dashboard | 7 | 8 | 4 | Cool but overkill |
| **task-511** | Action Registry | 9 | 9 | 2 | **55 actions - massive** |

### Quick Filter: High Value, Low Effort (Worth Reconsidering)

| Task | Feature | Effort | Value | Delta | Consider? |
|------|---------|--------|-------|-------|-----------|
| **task-471** | CLAUDE.md Scaffold | 2 | 7 | +5 | **YES** |
| **task-478** | MCP Template | 2 | 7 | +5 | **YES** |
| **task-474** | VSCode Extensions | 1 | 6 | +5 | **YES** |
| **task-484** | VSCode Python | 2 | 5 | +3 | Maybe |
| **task-472** | Placeholder Handling | 3 | 5 | +2 | Maybe |
| **task-550** | Status Tracking | 4 | 5 | +1 | Maybe |
| **task-476** | Missing Agents | 4 | 5 | +1 | Maybe |
| **task-520** | Pre-Commit SAST | 4 | 5 | +1 | Maybe |

---

## Abandonment Justifications

### Event System Family (task-485 through task-540) - 30 tasks

**Reason**: Over-engineered speculative architecture.

This is a massive undertaking proposing:
- 60 event types across 11 namespaces
- JSON Schema definitions
- Event routing and dispatch
- Action registry with 55 actions
- DORA metrics dashboard
- Complex state machines

**Reality check**:
- Flowspec is a CLI tool that works well today
- The `/vibe` mode was just added for "less ceremony, more building"
- None of this infrastructure is needed for current features
- This represents weeks/months of work with unclear ROI
- The simpler `.flowspec/logs/` approach already provides event logging

**Impact of abandoning**: None. Current logging works fine.

---

### Role-Based System (task-361, 363, 364, 365, 367) - 5 tasks

**Reason**: Partially implemented, remainder is over-engineering.

- Role-based command namespaces (`flow/`, `spec/`, `dev/`, etc.) already exist
- VS Code agent sync already works
- CI validation for roles already exists and passes
- The "role selection during init" adds complexity users don't need
- Users naturally use commands relevant to their role without explicit selection

**Impact of abandoning**: None. Current namespace structure is sufficient.

---

### task-548 - Rigor Rules in /flow:operate

**Reason**: **Command was removed.**

The `/flow:operate` command and "Deployed" state were removed in PR #1082. This task references a command that no longer exists.

**Impact of abandoning**: None. Task is obsolete.

---

### task-293, task-294 - Constitution Testing

**Reason**: Over-testing a simplified system.

The constitution system has been simplified. Adding complex accuracy tests for LLM customization adds maintenance burden without proportional value. The constitution works - we don't need 90%+ accuracy metrics.

**Impact of abandoning**: Minor. Constitution works without formal accuracy testing.

---

### claude-improves Family (task-468, 469, 471, 472, 474, 475, 476, 478, 479, 481, 484) - 11 tasks

**Reason**: Micro-optimizations with diminishing returns.

These tasks represent incremental improvements to:
- Naming conventions (task-468)
- Template placeholders (task-472)
- VSCode settings (task-474, 484)
- Symlinks and scaffolding (task-471, 475)
- CI checks for parity (task-479)

While individually reasonable, collectively they represent polishing work that doesn't add user value. The current system works.

**Impact of abandoning**: Minor. Users don't notice these refinements.

---

### Git Workflow Family (task-515-521, 533-535) - 10 tasks

**Reason**: Building infrastructure GitHub already provides.

This proposes:
- Git worktree automation
- Local PR approval workflows
- Pre-commit quality gates (lint, test, SAST)
- Git state machines

GitHub Actions, pre-commit hooks, and standard git workflows already handle all of this. Building custom infrastructure duplicates existing solutions.

**Impact of abandoning**: None. Use GitHub's native features.

---

### Container Family (task-525-529) - 5 tasks

**Reason**: Out of scope for flowspec.

Container orchestration, secret injection, and resource monitoring are DevOps concerns, not spec-driven development concerns. This is scope creep.

**Impact of abandoning**: None. Use Docker/K8s native tooling.

---

### GPG/Security Family (task-522-524) - 3 tasks

**Reason**: Premature optimization for a non-existent problem.

Agent GPG key management and automated commit signing are security theater unless there's a specific compliance requirement. DCO sign-off (task-432) is the actual compliance need.

**Impact of abandoning**: None. Focus on DCO instead.

---

### Logging Family (task-553-555) - 3 tasks

**Reason**: YAGNI (You Ain't Gonna Need It).

Log aggregation, analytics, and central logging integration are enterprise features. Flowspec is a developer tool. The simple JSONL logging in `.flowspec/logs/` is sufficient.

**Impact of abandoning**: None. Current logging works.

---

### task-444, task-445 - Bookworm Migration

**Reason**: Already done or unnecessary.

CI is working on current infrastructure. If migration was needed, it's either done or not happening. These tasks have no clear deliverable.

**Impact of abandoning**: None.

---

## Recommended Action Plan

### Immediate (This Week)

1. **Close 45 "Abandon" tasks** with reason "won't do - backlog cleanup Dec 2025"
2. **Mark task-368 as Done** - 90% complete, AC#8 can be a future enhancement
3. **Implement task-432 (DCO)** - Keeps causing PR failures

### Near-Term (January)

4. **task-084** - Quality metrics command (practical user value)
5. **task-435** - Remove command (completes CLI lifecycle)
6. **task-171** - Library docs MCP (improves agent capability)
7. **task-168** - macOS CI (broader testing)
8. **task-546** - Rigor in assess (completes rigor integration)

### Backlog (When Needed)

9. Documentation tasks (task-087, 134, 284, 438)
10. UX improvements (task-196, 197, 429)
11. CLI consolidation (task-430)

---

## Post-Cleanup Backlog Projection

After cleanup:
- **To Do**: ~20 tasks (down from 80+)
- **Categories**: CLI, Documentation, CI/CD, MCP
- **Complexity**: Simple, achievable tasks
- **Time horizon**: All completable in Q1 2025

This cleanup removes ~60% of backlog bloat while preserving all meaningful work.
