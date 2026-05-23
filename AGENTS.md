<!-- CLAUDE.md and AGENTS.md share Operator Preferences and Hard Guardrails. Keep in sync. -->

# AGENTS.md — flowspec-cli

Entry point for OpenAI Codex and compatible agents.

## Project
**Name:** flowspec-cli  
**Repo:** github.com/jpoley/flowspec  
**Purpose:** CLI toolkit that initialises, upgrades, and orchestrates AI agent workflows using Spec-Driven Development (SDD). Ships as `flowspec` (and legacy alias `specify`).  
**Current focus:** TASK-606 — `flowspec doctor` health-check command, branch `galway/task-606/flowspec-doctor`

---

## Operator Preferences
- State facts only. No sugarcoating.
- Surface problems, blockers, and risks immediately.
- Consult before one-way-door decisions and before any architectural change.
- Never guess. If validation is not possible, say so explicitly.
- Objective language. No first-person pronouns. No apologies or hedges.

---

## Hard Guardrails (always apply)
- Plan before any non-trivial change. Write the plan to `.claude/plans/`. Wait for approval.
- Never commit or merge directly to `main`.
- Never commit secrets, tokens, keys, or `.env` files.
- No destructive git without explicit operator approval.
- **NEVER delete test files or test methods** without explicit human instruction.
- **NEVER edit `backlog/tasks/*.md` files directly** — use `backlog task edit` CLI only.
- All commits require DCO sign-off: `git commit -s -m "..."`.
- Run `ruff format --check`, `ruff check`, and `pytest tests/ -x -q` before declaring done.

---

## Required Reading

Read these files **before** acting:

| Before | Read |
|--------|------|
| Any code change | `.claude/workflow.md` (planning + DoD) |
| Writing/editing Python | `.claude/language.md` |
| Architecture decision | `.claude/architecture.md` |
| Git / branch / PR | `.claude/sourcecontrol.md` |
| Runtime / deps | `.claude/stack.md` |
| Decision logging | `.claude/history.md` |
| Absolute rules | `.claude/rules/critical.md` |

---

## Current Task

**TASK-606** — `flowspec doctor` setup health-check command  
Plan: `.claude/plans/task-606-flowspec-doctor.md`  
Branch: `galway/task-606/flowspec-doctor`  

### What to build
```
src/flowspec_cli/doctor/
├── __init__.py      — exports run_doctor()
├── checks.py        — CheckResult dataclass + 8 check functions
└── cli.py           — Typer command + run_doctor()
tests/test_doctor.py — ~15 unit tests
```
Register in `src/flowspec_cli/__init__.py` near line 9179 as `@app.command("doctor")`.

### Test command
```bash
uv run pytest tests/ -x -q
```
