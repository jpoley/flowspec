# Flowspec v2 — Requirements & Specification

Starting-over spec. Assumes Claude Code capabilities available today: plugins,
skills, slash commands, sub-agents, hooks, settings, MCP servers.

---

## 1. Purpose

Flowspec enforces Spec-Driven Development (SDD): a small, linear workflow that
forces feature work through defined phases with artifact gates, so features
ship with specs, tests, and review.

It is delivered as **one Claude Code plugin** plus a **thin Python CLI**.

**Out of scope** — explicitly separate products, not part of v2:
- Security scanning, triage, fixing, reporting (all security tooling)
- Exploit research, fuzzing, patch engineering
- AI/ML pipelines, platform engineering, tech writing automation
- Release management, PR monitoring automation

## 2. Users & Goals

- **Primary user**: a developer or small team using Claude Code for feature
  work.
- **Goal**: every non-trivial feature moves through the same short checklist
  with artifacts landing in predictable places, backed by a backlog.md task.
- **Non-goal**: replacing human judgment. Flowspec does not write the spec —
  it ensures one exists before code lands.

## 3. Core Model

### 3.1 The workflow (6 phases)

| Phase     | User invocation        | Gate artifact                     | Exits when          |
| --------- | ---------------------- | --------------------------------- | ------------------- |
| Assess    | `/flow:assess <id>`    | Assessment note + tier on task    | Tier decided        |
| Specify   | `/flow:specify <id>`   | PRD under `docs/prd/` + ACs       | ACs defined         |
| Plan      | `/flow:plan <id>`      | ADR under `docs/adr/` (tier H)    | Design decided      |
| Implement | `/flow:implement <id>` | Code + tests on feature branch    | Tests pass locally  |
| Validate  | `/flow:validate <id>`  | All ACs checked, tests green      | Quality gate passes |
| Ship      | `/flow:ship <id>`      | PR merged                         | Task status = Done  |

Phases are linear. The **backlog task status is the single source of state.**
There is no separate workflow state machine and no `flowspec_workflow.yml`.

### 3.2 Tiers (complexity-scaled ceremony)

Assess picks one tier. The tier controls how much ceremony is required.

| Tier       | Criteria                                             | Required artifacts     |
| ---------- | ---------------------------------------------------- | ---------------------- |
| **Light**  | Single file, <100 LOC, no design choices             | Backlog task + ACs     |
| **Medium** | Multiple files, new module, clear design             | + PRD                  |
| **Heavy**  | Cross-cutting, new architecture, breaking change     | + PRD + ADR            |

Artifact presence is a boolean gate. If the required artifact for the next
phase is missing, the phase is blocked.

## 4. Artifacts — where they live

```
docs/
  prd/<slug>.md          # Product requirements (written in Specify)
  adr/NNN-<slug>.md      # Architecture decisions (written in Plan)
backlog/
  tasks/                 # Backlog.md — source of truth for task state + ACs
memory/
  constitution.md        # Project principles (once, via init)
```

No `.flowspec/` directory. No per-project YAML config. No templates copied
into the consumer repo.

## 5. Distribution — Claude Code plugin

Flowspec is one installable plugin:

```
.claude-plugin/
  plugin.json
  commands/flow/   # 6 slash command files
  skills/          # 4 role skills
  agents/          # 4 sub-agent definitions
  hooks/           # ≤5 hooks
  rules/           # 5 rule files (auto-loaded to context)
```

- Install: `claude plugin install flowspec`
- Upgrade: `claude plugin upgrade flowspec`
- Per-project footprint: zero files copied. One `flowspec init` creates
  `docs/prd/`, `docs/adr/`, `memory/constitution.md` only.

## 6. Primitives — what goes where

### 6.1 Slash commands (6 total) — user-invoked phase transitions

Each command is a short markdown file (<200 lines) that:
1. Calls `flowspec gate <id>` to verify the previous phase's artifact.
2. Invokes the role skill for this phase.
3. Updates the gate artifact.
4. Advances the backlog task status.

Every command takes a task id. That is the only argument.

**Removed** (folded into the six above or into the CLI): `build`, `gate`,
`review`, `rigor`, `pre-pr`, `generate-prp`, `map-codebase`, `reset`,
`submit-n-watch-pr`, `init`, `intake`, `vibe`, all `/flow:security_*`.

### 6.2 Skills (4 total) — role expertise

A skill is a persona and checklist. It is invoked from a command (or by model
context), not directly by the user.

| Skill          | Invoked by         | Purpose                                      |
| -------------- | ------------------ | -------------------------------------------- |
| `pm-planner`   | `/flow:specify`    | Turn feature idea into PRD + atomic ACs      |
| `architect`    | `/flow:plan`       | Make design choices, write ADR               |
| `engineer`     | `/flow:implement`  | Write code + tests to spec on a worktree     |
| `qa-validator` | `/flow:validate`   | Verify ACs, coverage, run the quality gate   |

**Removed**: `sdd-methodology`, `constitution-checker`, `context-extractor`,
`workflow-executor`, `gather-learnings`, and every security-adjacent skill.
Their responsibilities collapse into the four above or into the CLI.

### 6.3 Sub-agents (optional, parallel work)

The `engineer` skill may spawn `backend-engineer` and `frontend-engineer`
sub-agents when a task is labelled `parallel-work:frontend,backend`.
Otherwise it runs in the main loop. Two agent definitions, not fourteen.

### 6.4 Hooks (≤5, always-on)

| Hook                    | Event                     | Purpose                                   |
| ----------------------- | ------------------------- | ----------------------------------------- |
| `session-start`         | SessionStart              | Load active task memory, confirm branch   |
| `block-sensitive-writes`| PreToolUse (Edit/Write)   | Block writes to `.env`, private keys      |
| `git-safety`            | PreToolUse (Bash)         | Warn on force push, hard reset, main push |
| `autoformat`            | PostToolUse (Edit/Write)  | Run `ruff format` on changed Python       |
| `gate-check`            | Stop                      | Warn if task status and artifacts diverge |

No auto-lint hook (lint runs in `/flow:validate`). No PR-watcher hook (CLI
subcommand). No metrics emitter. No quality-gate duplication across events.

### 6.5 Rules (5 files, auto-loaded into context)

`.claude/rules/` contents:

1. `critical.md` — NEVER delete tests; no direct commits to main; DCO
   sign-off; mandatory pre-PR `ruff format --check && ruff check && pytest`.
2. `git-workflow.md` — Branch naming, worktrees, conventional commits.
3. `coding-style.md` — Ruff, 88 char lines, type hints, module-level imports.
4. `testing.md` — pytest, AAA, coverage floor.
5. `agents.md` — When to delegate, parallel execution conventions.

**Removed**: `performance.md` (advisory only, not enforced), `rigor.md` (folds
into critical/git), `security.md` (separate product).

### 6.6 MCP servers

**Required**:
- `backlog` — task CRUD, status, AC check-off. The single source of task
  state.

**Optional** (auto-detected if configured):
- `github` — PR creation and CI status for `/flow:ship`.
- `serena` — semantic code navigation for `engineer`/`architect` skills.

No custom flowspec MCP server.

### 6.7 CLI (`flowspec`)

A small Python CLI for the things hooks and skills cannot cleanly do.

```
flowspec init                 # Create docs/prd/, docs/adr/, memory/constitution.md
flowspec gate <task-id>       # Check artifact presence for task's next phase
flowspec status               # Show current task + phase + missing gates
flowspec prd new <slug>       # Scaffold a PRD from template
flowspec adr new <slug>       # Scaffold an ADR from template
```

Target size: **≤2K LOC**, down from 51K. No workflow validator, no satellite
audit, no memory/learnings system, no test executor, no security subcommands,
no hook event framework, no template injection pipeline.

## 7. Task state — derived, not stored

State is derived from (task status, artifact presence) — never written to two
places.

```
Task status            Gate for the NEXT phase
----------------       -------------------------------------------
To Do                  — (assess has no precondition)
Assessed               assessment note on task
Specified              PRD exists (tier ≥ Medium) + ACs defined
Planned                ADR exists (tier Heavy)
In Implementation      feature branch exists
Validated              all ACs checked + tests pass
Done                   PR merged
```

`flowspec gate <id>` is the only validator. Commands call it. The
`gate-check` Stop-hook calls it. No duplicated logic.

## 8. Non-requirements (explicitly out)

- All security tooling — separate product.
- Custom user-defined workflows (`quick_build`, `full_design`, `ship_it`) —
  tiers cover the variation.
- Role-namespace commands (`/arch:*`, `/dev:*`, `/qa:*`, `/ops:*`) — one
  `/flow:*` namespace.
- Template directory with scaffolding files — plugin replaces it.
- Workflow YAML configuration — tiers + backlog status replace it.
- Beads integration — backlog.md only.
- Activity logs, decision logs, learnings database, memory CLI —
  out of the CLI. A user may keep their own `docs/decisions/` by convention.

## 9. Success criteria

A user can go from zero to first shipped feature with:

```bash
claude plugin install flowspec
cd my-project
flowspec init
backlog task create "Add foo"
# then, in Claude Code:
/flow:assess 1
/flow:specify 1
/flow:plan 1          # skipped if tier < Heavy
/flow:implement 1
/flow:validate 1
/flow:ship 1
```

**Measurable targets**:

| Target                                      | v2        | v1 (for contrast) |
| ------------------------------------------- | --------- | ----------------- |
| Plugin files shipped                        | ≤20       | 131+              |
| Slash commands                              | 6         | 22                |
| Skills                                      | 4         | 20                |
| Sub-agent definitions                       | 4         | 14 (in YAML)      |
| Hooks                                       | ≤5        | 17                |
| Rules files                                 | 5         | 8                 |
| Per-project config files                    | 0         | many              |
| CLI size                                    | ≤2K LOC   | ~51K LOC          |
| Time from install to first `/flow:assess`   | <2 min    | —                 |

## 10. Migration from v1

Separate document. Not in scope here.
