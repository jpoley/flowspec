# Flowspec Backlog Simplification - Detailed Analysis

**Date**: 2025-12-29
**Current Version**: v0.3.013
**Open Tasks**: 86

---

## ALREADY DONE - Just Archive These

These tasks are complete but not marked done. Archive immediately.

### task-368: Task Memory
**Status**: 90% complete, all code shipped
**Evidence**: 2,864 LOC in `src/flowspec_cli/memory/`, 11 CLI commands working
**Missing AC #8**: "Integration with backlog.md task lifecycle events" - requires upstream backlog CLI to support hooks, which is external dependency (task-402)
**Decision**: MARK DONE. Workaround (manual `flowspec memory init`) is documented and works. The feature delivers value today.

### task-432: DCO Sign-off Enforcement
**Status**: Already enforced
**Evidence**: GitHub DCO app is configured, `critical-rules.md` documents requirement, all PRs already require DCO
**Decision**: MARK DONE. Nothing to implement - it's already working.

### task-551: Rigor Rules Reference
**Status**: Completed in PR #1081
**Decision**: Already marked Done. Archive it.

---

## WON'T DO - Agent Event System (24 tasks)

**Tasks**: 485, 486, 487, 504, 507, 508, 509, 510, 511, 512, 513, 530, 531, 533, 534, 535, 536, 537, 538, 539, 540, 553, 554, 555

### What This System Would Build

A complete event sourcing infrastructure:
- JSON Schema for 60 event types across 11 namespaces (lifecycle, activity, coordination, hook, git, task, container, decision, system, action, security)
- JSONL event writer with daily rotation and async writes
- Event router with namespace dispatch
- Action registry with 55 registered actions across 18 categories
- Event query CLI and API
- State machine for git workflows
- DORA metrics dashboard
- Performance benchmarks
- Operational runbooks

### Why We Won't Do This

**1. No User Need**
Nobody has asked for event sourcing. Flowspec users want to run `/flow:specify` and get a PRD, not emit `lifecycle.session_start` events to a JSONL file. This is infrastructure for infrastructure's sake.

**2. Massive Scope Creep**
This is 24 tasks representing 2-3 months of work. The event system alone (tasks 485-487) would take a week. The action registry (task-511) defines 55 actions - that's a product unto itself.

**3. Wrong Abstraction Level**
Flowspec is a CLI tool that bootstraps projects and runs AI agent workflows. It is NOT:
- An event bus
- A state machine runtime
- A metrics platform
- A container orchestrator

These are platform concerns that belong in dedicated tools (Kafka, Temporal, Prometheus, Kubernetes).

**4. Maintenance Burden**
Every event type is a contract. 60 event types = 60 things to maintain, version, and keep backward compatible. The action registry with 55 actions means 55 interfaces to document and test.

**5. The Logging We Have Works**
`.flowspec/logs/` already captures events via simple hooks. `hooks.py` emits to JSONL. Adding 11 namespaces doesn't make it more useful - it makes it harder to parse.

### Specific Task Rejections

| Task | What It Does | Why Not |
|------|--------------|---------|
| task-485 | JSON Schema for 60 event types | 60 event types is absurd for a CLI tool. We emit maybe 5 event types in practice. |
| task-486 | JSONL writer with async, daily rotation | We have sync writes that work fine. Daily rotation for a CLI that runs for seconds? |
| task-487 | Event router with namespace dispatch | Routing events to 11 namespaces nobody will query. Complexity for complexity. |
| task-504 | Event query CLI | Who is querying events? For what purpose? No use case defined. |
| task-507 | Claude Code hooks emit events | Hooks already emit to JSONL. Adding "events" layer is abstraction theater. |
| task-508 | Backlog operations emit events | Backlog.md has its own audit trail. Duplicating it is waste. |
| task-509 | Git operations emit events | Git has reflog. We don't need another git event system. |
| task-510 | MCP server emits events | MCP calls are already logged by Claude Code. Redundant. |
| task-511 | 55-action registry | Defining 55 actions across 18 categories. This is a framework, not a feature. |
| task-512 | Action decorators and helpers | Building a decorator system for actions nobody will register. |
| task-513 | Action to event mapping | Mapping 55 actions to 60 events. Combinatorial complexity explosion. |
| task-530 | Decision event emission | Decisions should go in task memory markdown, not event streams. |
| task-531 | Decision query utilities | Querying decisions from events when they're in markdown files. |
| task-533 | Git workflow state machine | Git already has state. Branches ARE state. Adding another layer is wrong. |
| task-534 | State recovery utilities | Recovering state from events when git history exists. Pointless. |
| task-535 | Automated cleanup orchestrator | Cleaning up what? Event files that shouldn't exist? |
| task-536 | Event system architecture docs | Documenting a system we won't build is waste. |
| task-537 | Event system integration tests | Testing infrastructure that delivers no user value. |
| task-538 | Event system performance benchmarks | Benchmarking event writes for a CLI tool. Absurd. |
| task-539 | DORA metrics dashboard | DORA metrics require deployment frequency data. A CLI doesn't deploy. |
| task-540 | Operational runbooks for events | Runbooks for a system that shouldn't exist. |
| task-553 | Log aggregation and summaries | Aggregating logs nobody reads into summaries nobody wants. |
| task-554 | Log analytics for patterns | Pattern analysis on CLI logs. What patterns? |
| task-555 | Central logging integration | Shipping CLI logs to central systems. For a local dev tool. |

---

## WON'T DO - Git Workflow Automation (18 tasks)

**Tasks**: 505, 506, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529

### What This System Would Build

- Git workflow configuration schema (YAML)
- Configuration loader with validation
- Worktree creation/cleanup automation
- Git hook framework with centralized dispatcher
- Pre-commit quality gates (lint, test, SAST)
- Local PR approval workflow (approve PRs without GitHub)
- Agent GPG key management system
- Automated commit signing
- Container orchestration for isolated task execution
- Container resource monitoring and cleanup

### Why We Won't Do This

**1. Reinventing Existing Tools**

| What We'd Build | What Already Exists |
|-----------------|---------------------|
| Git hook framework (task-517) | [pre-commit](https://pre-commit.com/) - 50k+ GitHub stars, battle-tested |
| Pre-commit lint/test/SAST (task-518-520) | pre-commit hooks for ruff, pytest, bandit, semgrep |
| Worktree automation (task-515) | `git worktree add ../foo feature/foo` - one command, done |
| Container orchestration (task-525-529) | Docker, Kubernetes, or **nanofuse** (your other project) |
| GPG key management (task-522-524) | `git config user.signingkey` + gpg-agent, standard tooling |

**2. Wrong Project for Container Work**

task-525 through task-529 propose container orchestration, resource monitoring, and cleanup. This is literally what **nanofuse** is for. Flowspec is a CLI for SDD workflows. If we need isolated execution, we call out to nanofuse or Docker. We don't rebuild container orchestration in a Python CLI.

**3. Local PR Workflow Is Conceptually Wrong**

task-521 proposes "Local PR Approval Workflow" - approving PRs without GitHub.

This misunderstands what PRs are for:
- PRs exist for **collaboration** - team review, discussion, approval
- PRs trigger **CI** - tests run on GitHub Actions, not locally
- PRs create **audit trail** - who approved what, when
- Local approval has no witnesses, no CI, no history

If you're working solo and don't need review, just merge. Don't build fake approval ceremonies.

**4. GPG Key Management Is Already Solved**

task-522/523/524 propose:
- Key storage at `.flowspec/agent-keys/`
- Key registry file `keyring.txt`
- Automated key generation for agents

But:
- Git already handles signing: `git config commit.gpgsign true`
- GitHub verifies signatures via web flow
- Keyservers distribute public keys
- gpg-agent manages private keys

Flowspec should not become a PKI. Keys are OS-level concerns.

### Specific Task Rejections

| Task | What It Does | Why Not |
|------|--------------|---------|
| task-505 | YAML schema for git workflow config | Git config exists. `.gitconfig` is the schema. |
| task-506 | Configuration loader with validation | Loading config for features we won't build. |
| task-514 | Allowed followups validation | Validating workflow transitions that don't need validation. |
| task-515 | Worktree creation automation | `git worktree add` is already one command. Script adds nothing. |
| task-516 | Worktree cleanup automation | `git worktree remove` exists. |
| task-517 | Hook dispatcher framework | pre-commit.com does this with massive ecosystem. |
| task-518 | Pre-commit lint gate | `pre-commit run ruff` - already works. |
| task-519 | Pre-commit test gate | `pre-commit run pytest` - already works. |
| task-520 | Pre-commit SAST gate | `pre-commit run bandit` - already works. |
| task-521 | Local PR approval | PRs are for GitHub. Local approval is theater. |
| task-522 | GPG key management design | gpg-agent exists. Don't reinvent it. |
| task-523 | GPG key generation for agents | Agents don't need their own keys. User signs commits. |
| task-524 | Automated commit signing | `git config commit.gpgsign true` - done. |
| task-525 | Container orchestration design | This is nanofuse's job, not flowspec's. |
| task-526 | Container launch automation | Docker/podman already do this. |
| task-527 | Runtime secret injection | Docker secrets, Kubernetes secrets exist. |
| task-528 | Container resource monitoring | Docker stats, cAdvisor exist. |
| task-529 | Container cleanup automation | `docker system prune` exists. |

---

## WON'T DO - Role-Based Commands (5 tasks)

**Tasks**: 361, 363, 364, 365, 367

### What This Would Build

- Role selection during `flowspec init` (PM, Dev, Sec, QA, Ops, Arch, All)
- Role stored in `flowspec_workflow.yml`
- Commands filtered/hidden by role
- VSCode roles synced
- CI validates role-based access

### Why We Won't Do This

**1. Artificial Restriction That Hurts Users**

Role-based filtering **hides commands** from users:
- A developer can't run `/sec:scan`? Security is everyone's job.
- A QA person can't run `/arch:decide`? QA often finds architectural issues.
- A PM can't run `/dev:debug`? PMs troubleshoot demos.

Restricting access in a **local CLI tool** that runs on YOUR machine is paternalistic nonsense.

**2. Most Users Are "All" - Making Init Slower For No Benefit**

In practice:
- Solo developers wear all hats
- Small teams rotate responsibilities
- Even in large orgs, people cross-function

Adding a role selection prompt means:
- Extra step during init that 90% answer "All" to
- Configuration file bloat
- Edge cases when someone's role changes

**3. The Namespace IS The Role Indicator**

Commands are already organized:
- `/sec:*` - security commands
- `/arch:*` - architecture commands
- `/qa:*` - quality assurance commands

Users naturally use what they need. The namespace tells them what it's for. No filtering required.

**4. CI Role Validation Is Gatekeeping**

task-365 proposes CI validates role-based access. This means:
- PR fails if "wrong" person ran a command
- Debates about who has what role
- Time wasted on access control for a dev tool

This is corporate bureaucracy cosplay, not useful software.

### Specific Task Rejections

| Task | What It Does | Why Not |
|------|--------------|---------|
| task-361 | Role selection in init with 7 options | Extra prompt, everyone picks "All", wasted time. |
| task-363 | Sync script for role-based generation | Generating filtered command sets nobody wants. |
| task-364 | VSCode roles schema in workflow.yml | VSCode doesn't need role configuration. |
| task-365 | CI validates role-based workflows | Gatekeeping who can run dev commands. Hostile UX. |
| task-367 | Role-based command directories | Commands already organized by namespace. Redundant. |

---

## WON'T DO - Rigor Rules Integration (6 tasks)

**Tasks**: 546, 547, 548, 549, 550, 552

### What This Would Build

- Inject `{{INCLUDE:_rigor-rules.md}}` into assess/plan/operate commands
- Add `/flow:freeze` command for task suspension
- Add workflow status tracking to all commands
- Create troubleshooting guide

### Why We Won't Do This

**1. Rules Are Already Loaded via CLAUDE.md**

`memory/critical-rules.md` has a full Rigor Rules section. CLAUDE.md has `@import memory/critical-rules.md`. Agents see the rules. Adding `{{INCLUDE}}` to individual command templates is redundant.

**2. /flow:freeze Solves A Problem That Doesn't Exist**

task-549 proposes a freeze command for "task suspension."

What does "freeze" mean?
- Tasks are markdown files. They don't run.
- "Suspension" = set status to "Blocked" in backlog
- Git handles version control already

This is inventing a concept that maps to nothing real.

**3. Workflow Status Tracking Is Already There**

task-550 proposes adding status tracking to all commands.

But:
- Backlog.md tracks task status
- Git tracks branch/worktree status
- The agent knows what step it's on

Adding another status system creates three sources of truth.

**4. Troubleshooting Guide Needs Trouble First**

task-552 proposes a troubleshooting guide for rigor rules.

We don't have users hitting rigor rule problems. We don't know what they'd struggle with. Writing a troubleshooting guide before there's trouble is guessing.

Documentation should follow pain, not anticipate it.

### Specific Task Rejections

| Task | What It Does | Why Not |
|------|--------------|---------|
| task-546 | Add rigor include to assess.md | Rules already in CLAUDE.md via @import. Redundant. |
| task-547 | Add rigor include to plan.md | Same - already loaded via CLAUDE.md. |
| task-548 | Add rigor include to operate.md | Same - already loaded via CLAUDE.md. |
| task-549 | /flow:freeze command | "Freeze" is not a real workflow concept. Use backlog status. |
| task-550 | Workflow status tracking | Backlog + git already track status. Third system is noise. |
| task-552 | Rigor troubleshooting guide | No users, no trouble to document yet. |

---

## WON'T DO - Claude-Improves (11 of 12 tasks)

**Tasks**: 293, 294, 469, 471, 472, 474, 475, 476, 478, 479, 481, 484

### Keep task-468 (Prompt Naming Convention)

This is the ONE worth doing - standardizing `jpspec.*` vs `specflow.*` vs `speckit.*` prevents confusion. Simple cleanup.

### Why Close The Rest

| Task | What It Does | Why Not |
|------|--------------|---------|
| task-293 | LLM customization accuracy tests | Testing that LLMs follow prompts. Untestable - LLM outputs vary. |
| task-294 | Constitution enforcement integration tests | Testing config file loading. Already covered by existing tests. |
| task-469 | Document agent-prompt alignment | Internal documentation nobody will read. |
| task-471 | CLAUDE.md scaffolding in init | Users write their own CLAUDE.md. Auto-generated ones are ignored. |
| task-472 | Template placeholder handling | Current placeholders (`[PROJECT_NAME]`) work. No bugs reported. |
| task-474 | VSCode extensions.json template | Users install extensions themselves. Don't dictate their setup. |
| task-475 | Symlinks for GitHub Copilot prompts | GitHub Copilot prompts work differently than Claude. Not applicable. |
| task-476 | Missing agents for non-speckit commands | We have 20+ agents. More agents = more maintenance, not more value. |
| task-478 | .mcp.json template | MCP configuration is highly project-specific. Templates don't help. |
| task-479 | CI check for template-deployment parity | Over-engineering. If template and deploy diverge, we notice manually. |
| task-481 | Deployment completeness report | Reporting on a problem we've never had. |
| task-484 | VSCode Python/FastAPI settings | Users configure their own IDE. We don't own their settings. |

**Common Theme**: These tasks assume users want flowspec to configure their entire development environment. They don't. They want flowspec to help with SDD workflows. IDE settings, extensions, and MCP configs are user responsibility.

---

## WON'T DO - Documentation (2 tasks)

**Tasks**: 087, 134

### task-087: Production Case Studies

**What It Wants**: 3-5 case studies with quantitative metrics (time saved, rework %, test coverage, bugs caught), developer quotes, ROI calculations.

**Why Not**:
- **No external users to interview.** Case studies require third-party validation. We can't write our own testimonials.
- **Metrics require before/after data.** We'd need projects that started without flowspec and measured everything, then added flowspec and measured again. That data doesn't exist.
- **This is marketing, not engineering.** When we have real users, they'll write their own case studies. Until then, it's fiction.

### task-134: Integrate Diagrams

**What It Wants**: Excalidraw diagrams, PNG exports, navigation links, grammar checks.

**Why Not**:
- **Diagrams of what?** The workflow is 7 commands: assess → specify → research → plan → implement → validate → operate. That's a list, not a diagram.
- **CLI tools don't need visual documentation.** Users read `--help`, not architecture diagrams.
- **This is polish for polish's sake.** If something is confusing, we'll diagram it. Nothing is currently confusing enough to warrant this.

---

## WON'T DO - Miscellaneous (12 tasks)

| Task | What It Does | Why Not |
|------|--------------|---------|
| task-079 | Stack selection during init | 9 stack options, cleanup logic, CI workflows per stack. Massive complexity for "delete files you don't need." |
| task-084 | Spec quality metrics command | Metrics like what? Lines of spec? Acceptance criteria count? These don't correlate with quality. |
| task-168 | macOS CI matrix testing | CI runs on Linux. macOS works locally. GitHub Actions minutes are expensive. Low value. |
| task-196 | Output style experiments | Current rich console output works. Experiments without hypothesis are wasted time. |
| task-197 | Custom statusline with workflow context | Claude Code already supports statuslines. We'd be duplicating built-in functionality. |
| task-285 | CI check for stale Done tasks | Automating backlog hygiene in CI. If Done tasks pile up, archive them manually. |
| task-402 | Upstream backlog hook contribution | We don't control backlog.md project. External contribution has uncertain timeline. |
| task-429 | ASCII logo for CLI | `flowspec --help` already shows a logo. Look at it. It exists. |
| task-430 | flowspec-cli replace specify | `flowspec init` already works. Renaming adds confusion, not value. |
| task-438 | GitHub setup features user guide | Document what? `flowspec init` creates GitHub files. That's the guide. |
| task-444 | Validate CI post-Bookworm migration | Migration happened. CI passes. Validation complete. |
| task-445 | Post-migration monitoring | Nothing to monitor. Migration is done. System is stable. |

---

## KEEP OPEN (5 tasks)

These have clear value and reasonable scope:

| Task | Description | Why Keep |
|------|-------------|----------|
| task-171 | Library doc MCP replacement | Context7 may become unavailable or rate-limited. Need fallback strategy. |
| task-283 | Archive hook for workflow | Automatically archives Done tasks, keeping backlog clean without manual work. |
| task-284 | Archive documentation | Documents archive-tasks.sh behavior so future maintainers understand it. |
| task-435 | flowspec remove command | Clean uninstall is basic hygiene. Users should be able to remove what they installed. |
| task-468 | Prompt naming convention | One-time cleanup of jpspec/specflow/speckit naming confusion. Prevents ongoing confusion. |

---

## Execution Commands

### Mark Actually Done (2 tasks)

```bash
backlog task edit task-368 -s Done --notes "Complete. 2,864 LOC shipped, 11 CLI commands working. AC #8 (backlog hooks) deferred - requires upstream support."

backlog task edit task-432 -s Done --notes "Complete. DCO enforced via GitHub DCO app and critical-rules.md documentation."
```

### Close Won't Do - With Specific Reasons

```bash
# Event System
backlog task edit task-485 -s Done --notes "WONT DO: 60 event types for a CLI is over-engineering. Simple JSONL logging suffices."
backlog task edit task-486 -s Done --notes "WONT DO: Async JSONL writer with rotation unnecessary for CLI that runs seconds."
backlog task edit task-487 -s Done --notes "WONT DO: Event router with 11 namespaces adds complexity without user value."
backlog task edit task-504 -s Done --notes "WONT DO: Event query CLI has no use case. Nobody queries CLI event logs."
backlog task edit task-507 -s Done --notes "WONT DO: Hook events already logged. Additional event layer is redundant."
backlog task edit task-508 -s Done --notes "WONT DO: Backlog.md has its own audit trail. Duplicating is waste."
backlog task edit task-509 -s Done --notes "WONT DO: Git has reflog. Another git event system is pointless."
backlog task edit task-510 -s Done --notes "WONT DO: MCP calls logged by Claude Code. Redundant."
backlog task edit task-511 -s Done --notes "WONT DO: 55-action registry is a framework, not a feature. Too complex."
backlog task edit task-512 -s Done --notes "WONT DO: Action decorator system for actions nobody will register."
backlog task edit task-513 -s Done --notes "WONT DO: Mapping 55 actions to 60 events is combinatorial explosion."
backlog task edit task-530 -s Done --notes "WONT DO: Decisions belong in task memory markdown, not event streams."
backlog task edit task-531 -s Done --notes "WONT DO: Querying decisions from events when they're in markdown."
backlog task edit task-533 -s Done --notes "WONT DO: Git branches ARE state. Additional state machine is wrong abstraction."
backlog task edit task-534 -s Done --notes "WONT DO: Git history exists. State recovery from events is pointless."
backlog task edit task-535 -s Done --notes "WONT DO: Cleanup orchestrator for system that shouldn't exist."
backlog task edit task-536 -s Done --notes "WONT DO: Documentation for system we won't build."
backlog task edit task-537 -s Done --notes "WONT DO: Testing infrastructure that delivers no user value."
backlog task edit task-538 -s Done --notes "WONT DO: Benchmarking event writes for CLI tool is absurd."
backlog task edit task-539 -s Done --notes "WONT DO: DORA metrics for CLI. Deployment frequency of what?"
backlog task edit task-540 -s Done --notes "WONT DO: Runbooks for system that shouldn't exist."
backlog task edit task-553 -s Done --notes "WONT DO: Log aggregation for logs nobody reads."
backlog task edit task-554 -s Done --notes "WONT DO: Pattern analysis on CLI logs has no use case."
backlog task edit task-555 -s Done --notes "WONT DO: Central logging for local dev tool is over-engineering."

# Git Workflow
backlog task edit task-505 -s Done --notes "WONT DO: Git config exists. New YAML schema adds nothing."
backlog task edit task-506 -s Done --notes "WONT DO: Config loader for features we won't build."
backlog task edit task-514 -s Done --notes "WONT DO: Validating workflow transitions that need no validation."
backlog task edit task-515 -s Done --notes "WONT DO: git worktree add is already one command."
backlog task edit task-516 -s Done --notes "WONT DO: git worktree remove exists."
backlog task edit task-517 -s Done --notes "WONT DO: pre-commit.com has 50k stars and massive ecosystem."
backlog task edit task-518 -s Done --notes "WONT DO: pre-commit run ruff already works."
backlog task edit task-519 -s Done --notes "WONT DO: pre-commit run pytest already works."
backlog task edit task-520 -s Done --notes "WONT DO: pre-commit run bandit already works."
backlog task edit task-521 -s Done --notes "WONT DO: Local PR approval is theater. PRs need GitHub for CI."
backlog task edit task-522 -s Done --notes "WONT DO: gpg-agent exists. Don't reinvent key management."
backlog task edit task-523 -s Done --notes "WONT DO: Agents don't need GPG keys. User signs commits."
backlog task edit task-524 -s Done --notes "WONT DO: git config commit.gpgsign true already works."
backlog task edit task-525 -s Done --notes "WONT DO: Container orchestration is nanofuse's job."
backlog task edit task-526 -s Done --notes "WONT DO: Docker/podman already launch containers."
backlog task edit task-527 -s Done --notes "WONT DO: Docker secrets, K8s secrets exist."
backlog task edit task-528 -s Done --notes "WONT DO: docker stats, cAdvisor exist."
backlog task edit task-529 -s Done --notes "WONT DO: docker system prune exists."

# Role-Based
backlog task edit task-361 -s Done --notes "WONT DO: Role selection adds prompts for 'All'. Wasted time."
backlog task edit task-363 -s Done --notes "WONT DO: Role-based sync for filtering nobody wants."
backlog task edit task-364 -s Done --notes "WONT DO: VSCode doesn't need role configuration."
backlog task edit task-365 -s Done --notes "WONT DO: CI gatekeeping who runs dev commands is hostile."
backlog task edit task-367 -s Done --notes "WONT DO: Commands already organized by namespace."

# Rigor Integration
backlog task edit task-546 -s Done --notes "WONT DO: Rules in CLAUDE.md via @import. Redundant include."
backlog task edit task-547 -s Done --notes "WONT DO: Rules in CLAUDE.md via @import. Redundant include."
backlog task edit task-548 -s Done --notes "WONT DO: Rules in CLAUDE.md via @import. Redundant include."
backlog task edit task-549 -s Done --notes "WONT DO: Freeze is not a workflow concept. Use backlog status."
backlog task edit task-550 -s Done --notes "WONT DO: Backlog + git track status. Third system is noise."
backlog task edit task-552 -s Done --notes "WONT DO: No users, no trouble to document yet."

# Claude-Improves
backlog task edit task-293 -s Done --notes "WONT DO: LLM output testing is untestable. Outputs vary."
backlog task edit task-294 -s Done --notes "WONT DO: Config loading already tested."
backlog task edit task-469 -s Done --notes "WONT DO: Internal docs nobody reads."
backlog task edit task-471 -s Done --notes "WONT DO: Users write own CLAUDE.md. Generated ones ignored."
backlog task edit task-472 -s Done --notes "WONT DO: Placeholders work. No bugs reported."
backlog task edit task-474 -s Done --notes "WONT DO: Users install own extensions."
backlog task edit task-475 -s Done --notes "WONT DO: Copilot prompts work differently than Claude."
backlog task edit task-476 -s Done --notes "WONT DO: 20+ agents is enough. More = maintenance burden."
backlog task edit task-478 -s Done --notes "WONT DO: MCP config is project-specific. Templates don't help."
backlog task edit task-479 -s Done --notes "WONT DO: Template parity checked manually when needed."
backlog task edit task-481 -s Done --notes "WONT DO: Reporting on problems we don't have."
backlog task edit task-484 -s Done --notes "WONT DO: Users configure own IDE."

# Documentation
backlog task edit task-087 -s Done --notes "WONT DO: Need external users first. Can't write own testimonials."
backlog task edit task-134 -s Done --notes "WONT DO: CLI doesn't need architecture diagrams."

# Miscellaneous
backlog task edit task-079 -s Done --notes "WONT DO: 9 stacks, cleanup logic, CI per stack. Just delete files you don't need."
backlog task edit task-084 -s Done --notes "WONT DO: Spec metrics don't correlate with quality."
backlog task edit task-168 -s Done --notes "WONT DO: macOS tested locally. Linux CI sufficient."
backlog task edit task-196 -s Done --notes "WONT DO: Output works. Experiments without hypothesis."
backlog task edit task-197 -s Done --notes "WONT DO: Claude Code already supports statuslines."
backlog task edit task-285 -s Done --notes "WONT DO: Backlog hygiene is manual. CI check is overkill."
backlog task edit task-402 -s Done --notes "WONT DO: External project, uncertain timeline."
backlog task edit task-429 -s Done --notes "WONT DO: Logo already exists in flowspec --help."
backlog task edit task-430 -s Done --notes "WONT DO: flowspec init already works."
backlog task edit task-438 -s Done --notes "WONT DO: flowspec init is the guide."
backlog task edit task-444 -s Done --notes "WONT DO: Migration done. CI passes."
backlog task edit task-445 -s Done --notes "WONT DO: Migration done. System stable."
```

---

## Summary

| Category | Count | Decision |
|----------|-------|----------|
| Already Done | 2 | Mark Done |
| Won't Do - Event System | 24 | Close with reasons |
| Won't Do - Git Automation | 18 | Close with reasons |
| Won't Do - Role Commands | 5 | Close with reasons |
| Won't Do - Rigor Integration | 6 | Close with reasons |
| Won't Do - Claude-Improves | 11 | Close with reasons |
| Won't Do - Documentation | 2 | Close with reasons |
| Won't Do - Misc | 12 | Close with reasons |
| Keep Open | 5 | Continue |
| **Total** | **85** | **80 closed, 5 open** |
