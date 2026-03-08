# Flowspec Prompt Architecture Redesign

**Date:** 2026-03-08
**Companion files:** `03-08-decisions.jsonl`, `03-08-questions.md`

---

## The Problem

Flowspec has ~19,000 lines of prompt surface (23 commands, 22 skills, 10 agents, 8 rules, 4 partials). When `/flow:implement` runs, 3,500-4,000 lines of framework instructions load before any user code enters context. That's 15-25% of a 200K window consumed by the tool itself.

The security subsystem alone accounts for 37% of commands, 55% of skills, and 23% of CLI source. Most sessions never use it.

This is what happens when you keep adding. The answer is not to reorganize - it's to rethink what this actually needs to be.

---

## What Flowspec Actually Is

Flowspec is a **spec-driven development methodology** expressed as a small set of composable tools. It is not a developer tool suite, not a security platform, not a project management system.

One sentence: **Flowspec ensures you spec what you're building, build what you specced, and prove it works - with artifacts at every step.**

Everything that doesn't serve that sentence should be removed or extracted.

---

## Current State (Validated Inventory)

| Category | Count | Lines |
|----------|-------|-------|
| Slash commands | 23 | 6,756 |
| Skills | 22 | 8,737 |
| Agents | 10 | 852 |
| Rules | 8 | 744 |
| Partials | 4 | 1,861 |
| **Total prompt surface** | | **~18,950** |
| Hooks | 21 | 4,310 |
| Templates | 131 | 25,610 |
| CLI source | 137 | 50,033 |

---

## Clean-Slate Design

If we built this today, knowing what we know, what would it be?

### The Workflow (Slash Commands)

Four commands. Maybe five.

| Command | Input | Output Artifact | Purpose |
|---------|-------|-----------------|---------|
| `/spec` | Human intent | `spec.md` | Define what we're building and why |
| `/plan` | `spec.md` | `plan.md` | Decompose into atomic tasks with verify criteria |
| `/build` | `plan.md` or `spec.md` | Code + `result.md` | Execute tasks with closed-loop validation |
| `/validate` | Code changes | `validation.md` | Prove it works (built into `/build`, also standalone) |

No assess. No gate. No rigor. No intake. No reset. No map-codebase. No generate-prp. No custom. No vibe. If you want to just code without a spec, you don't need a command for that - just type.

`/plan` is optional for small work. `/validate` is never optional - it's built into every `/build` execution.

### The Capabilities (Skills)

Skills are things the workflow reaches for, not steps you invoke. Auto-invoked by the tools that need them.

| Skill | What | Used By |
|-------|------|---------|
| `test-loop` | Run tests -> analyze -> fix -> rerun (max N) | `/build` (always) |
| `code-quality` | Lint -> fix -> format -> verify | `/build` (always) |
| `git-ops` | Branching, worktrees, DCO | `/build` |
| `pr-lifecycle` | Create PR -> monitor CI -> fix -> resubmit | Standalone or post-`/build` |
| `security-scan` | Scan -> triage -> report | Plugin (not core) |
| `codebase-context` | Understand structure, entry points | `/spec`, `/plan` |

Six skills in core. Security is a plugin.

### The Closed Loop (Non-Negotiable)

Every `/build` execution:

1. Execute task (agent in fresh context)
2. Run tests - PASS? commit. FAIL? analyze, fix, rerun (max 3). Still fails? escalate.
3. Run lint/format - PASS? continue. FAIL? auto-fix, rerun.
4. Produce validation artifact (what passed, what failed, what was fixed)

No build completes without a validation artifact. The artifact is proof.

### The Artifacts (The Contract)

Every phase produces a named, structured, committed artifact:

```
.specs/{feature}/
  spec.md          # What and why
  plan.md          # How (atomic tasks with verify criteria)
  result.md        # What happened (commits, changes, deviations)
  validation.md    # Proof (test results, lint, coverage)
```

Artifacts are the interface between tools. `/plan` reads `spec.md`. `/build` reads `plan.md`. Each tool trusts the artifact, not conversation history.

### The Agents (Team Composition)

| Role | What | When |
|------|------|------|
| **Planner** | Decomposes spec into atomic tasks | `/plan` |
| **Builder** | Executes one task in fresh context | `/build` (one per task) |
| **Validator** | Closed-loop test+lint cycle | Built into every `/build` |
| **Reviewer** | Goal-backward verification (did we build what was specced?) | End of `/build` |

Four roles. Builder+Validator might even be one role since validation is always part of building.

### The Rules (Always-Loaded Conventions)

Minimal, <100 lines each:

- **coding-style**: Ruff, pathlib, naming, YAGNI
- **git-workflow**: No direct commits to main, branch naming, DCO
- **testing**: Never delete tests, AAA pattern, coverage targets
- **security**: No hardcoded secrets, input validation, injection prevention

Four rules. Everything else is either a skill (loaded on demand) or unnecessary.

---

## What Gets Cut

| Current | Lines | Action |
|---------|-------|--------|
| 5 security commands | 2,525 | Extract to plugin |
| 12+ security skills | ~6,200 | Extract to plugin |
| Security CLI module (50 files) | 11,493 | Extract to separate package |
| `/vibe` | 127 | Delete. Just type. |
| `/flow:assess` | 301 | Unnecessary. Read the spec, decide. |
| `/flow:gate` | 87 | Baked into `/build` |
| `/flow:rigor` | 150 | Baked into rules + `/build` closed loop |
| `/flow:map-codebase` | 347 | Becomes `codebase-context` skill |
| `/flow:generate-prp` | 365 | Template in `templates/`, not a command |
| `/flow:intake` | 256 | Not core workflow |
| `/flow:reset` | 280 | Not core workflow |
| `/flow:custom` | 222 | Not core workflow |
| `/flow:init` | 382 | Simplify to one-shot setup |
| `/flow:pre-pr` + `/flow:submit-n-watch-pr` | 329 | Becomes `pr-lifecycle` skill |
| `/flow:review` | 122 | Baked into `/build` (Reviewer role) |
| `_rigor-rules.md` partial | 1,278 | Move to CLI code |
| `_constitution-check.md` partial | 161 | Hook or delete |
| `sdd-methodology` skill | 200 | Merge into CLAUDE.md |
| `constitution-checker` skill | 343 | Hook or delete |
| `workflow-executor` skill | 265 | Delete |
| `context-extractor` skill | 317 | Merge into `pm-planner` or delete |
| Persona prose in commands | ~600 | Reference skills, don't inline |

---

## Target Footprint

| Category | Before | After |
|----------|--------|-------|
| Slash commands | 23 (6,756 lines) | 4-5 (~800 lines) |
| Skills | 22 (8,737 lines) | 6 (~600 lines) |
| Agents | 10 (852 lines) | 4 (~400 lines) |
| Rules | 8 (744 lines) | 4 (~350 lines) |
| Partials | 4 (1,861 lines) | 1-2 (~300 lines) |
| **Total prompt surface** | **~18,950 lines** | **~2,450 lines** |
| **Reduction** | | **87%** |

---

## What We Learned From Others

### From GSD (get-shit-done)

**Take:** Fresh context per task execution. Plans as executable contracts. Goal-backward verification. Wave-based parallelism for independent tasks.

**Leave:** 43KB agent prompts. 34 slash commands. 800KB+ of orchestration library. Complexity solving complexity problems.

### From Gastown

**Take:** External state + ephemeral agents (Git is truth, agents are disposable). Role separation (planners don't code, coders don't plan). Immutable work records.

**Leave:** $100/hour burn rate. Agents merging failing tests. "Vibecoded" architecture. Dolt dependency.

### The synthesis

Both systems prove that **context engineering matters more than prompt engineering**. Both over-build the orchestration layer. The lesson: keep the workflow thin, make the artifacts the contract, let Git be the state machine.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Prompt regression from rewrite | Golden test cases per command; migrate one at a time |
| Loss of institutional knowledge in prompts | Extract rationale into docs before deleting |
| Scope creep during redesign | Ship the 4 commands first, add nothing until they work |
| Over-engineering the simplification | If the design doc is longer than the code, start over |

---

## Open Questions

See `03-08-questions.md` for the 15 design questions that need answers before implementation.

Key ones:
1. Is flowspec a tool, a protocol, or a methodology?
2. How thin is the spec artifact?
3. Where do artifacts live?
4. What's the minimum viable version? (Probably `/spec` + `/build`)
5. What does flowspec do that Claude Code alone doesn't? (One sentence answer required.)

---

## Appendix: Inventory Validation

Validated 2026-03-08 against actual file counts and `wc -l`:

| Category | Claimed | Validated | Delta |
|----------|---------|-----------|-------|
| Commands | 23 / 6,756 | 23 / 6,756 | exact |
| Skills | 20 / 10,077 | 22 / 8,737 | +2 files, -1,340 lines |
| Agents | 10 / 559 | 10 / 852 | +293 lines |
| Rules | 8 / 744 | 8 / 744 | exact |
| Partials | 4 / 1,861 | 4 / 1,861 | exact |
| Hooks | 21 / 4,068 | 21 / 4,310 | +242 lines |
| Templates | 131 / 25,610 | 131 / 25,610 | exact |
| CLI source | 137 / 50,033 | 137 / 50,033 | exact |
