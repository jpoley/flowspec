# GitHub Copilot Instructions — flowspec-cli

## Project
flowspec-cli: CLI toolkit for Spec-Driven Development (`flowspec init`, `upgrade-repo`, `doctor`). Python 3.11+, Typer + Rich, uv, pytest, ruff.

## Hard Rules (no exceptions)
- Never commit directly to `main`. All changes through PRs.
- Never delete test files or test methods without explicit human instruction.
- Never edit `backlog/tasks/*.md` files directly — use `backlog task edit` CLI.
- All commits require DCO sign-off: `git commit -s -m "..."`.
- Run `uv run ruff format --check .` + `uv run ruff check .` + `uv run pytest tests/ -x -q` before any PR.
- Never force-push. Never `reset --hard` without operator approval.

## Code Style
- Ruff: formatter + linter, line length 88.
- Type hints required on public API functions.
- `pathlib.Path` for all file paths, never `os.path`.
- Prefer module-level imports; inline imports inside functions are acceptable to avoid circular imports or defer heavy loads in Typer command handlers.
- `encoding="utf-8"` on all file reads/writes.
- No Python builtin shadowing (`type`, `list`, `dict`, `input`, `filter`, `map`, `hash`).

## Test Style
- pytest, `tests/test_<module>.py`, Arrange→Act→Assert.
- `tmp_path` fixture for file isolation. `monkeypatch` for subprocess/env.
- Return type `-> None` on all test methods.
- Meaningful assert messages: `assert x, f"Expected y, got {x}"`.

## Adding a Command
New commands go in `src/flowspec_cli/<name>/` — never add more to the 10K-line `__init__.py`.
Register with `@app.command("name")` wrapper at the bottom of `__init__.py`.
Reuse: `check_backlog_installed_version()`, `check_beads_installed_version()`, `get_github_latest_release()`, `console`, `show_banner()`.

## Current Focus
Check the active backlog task: `backlog task list -s "In Progress" --plain`
Plans live in `.claude/plans/`. Follow the DoD in `.claude/workflow.md`.
