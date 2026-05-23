<!-- CLAUDE.md and AGENTS.md share Operator Preferences and Hard Guardrails. Keep in sync. -->

# CLAUDE.md — flowspec-cli

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
- Never answer from a guess. Validate claims against primary sources; if impossible, say so explicitly.
- Objective language. No first-person pronouns. No apologies or hedges.

---

## Hard Guardrails (always apply)
- Plan before any non-trivial change. Write the plan to `.claude/plans/`. Wait for approval.
- Never commit or merge directly to `main`.
- Never commit secrets, tokens, keys, or `.env` files.
- No destructive git (`reset --hard`, force-push, branch delete) without explicit operator approval.
- **NEVER delete test files or test methods** without explicit human instruction — see `.claude/rules/critical.md`.
- **NEVER edit `backlog/tasks/*.md` files directly** — use `backlog task edit` CLI only.
- All commits require DCO sign-off: `git commit -s -m "..."`.
- Run formatter + linter + tests after every change set before declaring done.

---

## Stack
| Layer | Detail |
|-------|--------|
| Language | Python 3.11+ (`requires-python = ">=3.11"` in `pyproject.toml`) |
| Package manager | `uv` — `uv sync` to install, `uv tool install . --force` to install CLI |
| Formatter | `ruff format` |
| Linter | `ruff check` |
| Test framework | `pytest` — run with `uv run pytest tests/ -x -q` |
| CLI framework | Typer + Rich (`src/flowspec_cli/__init__.py` — 10K-line monolith, decompose carefully) |
| HTTP client | `httpx` with `truststore` for SSL |
| Config | `pyproject.toml`, `flowspec_workflow.yml` |

## Key Commands
```bash
uv sync                            # install deps
uv tool install . --force          # install CLI locally
uv run pytest tests/ -x -q        # run tests
uv run ruff check . --fix && uv run ruff format .   # lint + format
backlog task list --plain          # list tasks
backlog task 606 --plain           # view current task
backlog task edit 606 --check-ac 1 # mark AC done
```

## Project Structure
```
src/flowspec_cli/
├── __init__.py        # main CLI — Typer app, COPILOT_AGENT_TEMPLATES, all top-level commands
├── doctor/            # NEW — health-check module (TASK-606)
├── workflow/          # workflow state machine, validator, config
├── security/          # SAST, MCP security server
├── memory/            # task memory CLI
├── hooks/             # Claude Code hook system
├── telemetry/         # telemetry CLI
├── deprecated.py      # cleanup logic for upgrade-repo
└── templates/         # files deployed to user repos
tests/                 # pytest suite (3473 tests, ~37s)
backlog/tasks/         # project task files — CLI-only, never edit directly
.claude/
├── plans/             # implementation plans (write here before coding)
├── rules/             # critical, git-workflow, testing, coding-style, security, rigor
└── workflow.md        # planning/DoD reference
```

## Existing Utilities to Reuse
When adding new commands, use these already-present helpers in `__init__.py`:
- `check_backlog_installed_version()` — runs `backlog --version`
- `check_beads_installed_version()` — runs `bd --version`
- `get_github_latest_release(owner, repo)` — GitHub API fetch
- `get_npm_latest_version(package)` — npm registry fetch
- `COPILOT_AGENT_TEMPLATES` — embedded agent file content
- `show_banner()` — standard CLI banner
- `console` — shared `rich.Console` instance

New modules go in `src/flowspec_cli/<name>/` and register via `@app.command()` or `app.add_typer()` at the bottom of `__init__.py`.

---

## Required Reading
`.claude/workflow.md` is loaded on every task — planning and DoD apply always.

Before you act:
- write or edit code → `.claude/rules/coding-style.md`, `.claude/rules/testing.md`
- architectural decision → `.claude/rules/critical.md`
- git / branch / PR → `.claude/rules/git-workflow.md`
- security-touching code → `.claude/rules/security.md`

@.claude/workflow.md
