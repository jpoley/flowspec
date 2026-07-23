# Architecture — flowspec-cli

## Overview
flowspec-cli is a Python CLI package. The entry point is `src/flowspec_cli/__init__.py` — a Typer app that wires together all subcommands. New features go in dedicated submodules and register at the bottom of `__init__.py`.

## Module Structure
```
src/flowspec_cli/
├── __init__.py        # Main Typer app, COPILOT_AGENT_TEMPLATES, all top-level commands
│                      # 10,541 lines — do not add more; extract instead (see issue #1226)
├── doctor/            # Health-check command (TASK-606, in progress)
├── workflow/          # State machine: assessor, validator, transition, config, state_guard
├── security/          # SAST tools, MCP security server
├── memory/            # Task memory CLI (backlog/memory/)
├── hooks/             # Claude Code hook system: events, schema, cli
├── telemetry/         # Telemetry events, config, CLI
├── backlog/           # Backlog shim and integration
├── satellite/         # Migration and audit utilities
├── skills/            # Skill scaffold system
├── quality/           # Quality assessors, scorer, config
├── vscode/            # VS Code settings generator
├── logging/           # Structured logging utilities
├── deprecated.py      # Deprecated-file cleanup for upgrade-repo
├── placeholders.py    # Template placeholder substitution
├── task_context.py    # Task context extraction
├── validation_agents.py # Validation agent orchestration
└── templates/         # Files deployed to user repos (agents, commands, hooks)
```

## Adding a New Command
1. Create `src/flowspec_cli/<name>/` with `__init__.py`, `checks.py`/core logic, `cli.py`
2. Register in `__init__.py` near the bottom:
   - Simple command: `@app.command(name="<name>")` wrapping `from flowspec_cli.<name>.cli import run_<name>`
   - Sub-app: `from flowspec_cli.<name>.cli import <name>_app; app.add_typer(<name>_app, name="<name>")`
3. Write tests in `tests/test_<name>.py`

## Existing Utilities (reuse, don't reinvent)
All in `src/flowspec_cli/__init__.py`:
- `check_backlog_installed_version()` — `backlog --version` via subprocess
- `check_beads_installed_version()` — `bd --version` via subprocess
- `get_github_latest_release(owner, repo)` — GitHub API, returns version string or None
- `get_npm_latest_version(package)` — npm registry, returns version string or None
- `compare_semver(a, b)` — returns -1/0/1
- `show_banner()` — prints the flowspec banner
- `console` — shared `rich.Console` singleton
- `COPILOT_AGENT_TEMPLATES` — embedded agent file content dict
- `CONSTITUTION_TEMPLATES` — embedded constitution template dict
- `SOURCE_REPO_MARKER` — sentinel file name for source repo detection

## Key Boundaries
- **No circular imports**: submodules import from `__init__.py` only for constants/utilities; `__init__.py` imports submodules only at the bottom (lazy, inside command wrappers, or via `app.add_typer`)
- **No global state mutation**: the module-level `client` (httpx) and `console` (Rich) are the only singletons
- **Template files are king**: `templates/` and `src/flowspec_cli/templates/` must stay in sync; `COPILOT_AGENT_TEMPLATES` is the embedded fallback

## Anti-Patterns
- Do not add more top-level code to `__init__.py` — extract to a submodule
- Do not mock subprocess in tests when a real temp file works — use `tmp_path`
- Do not use `os.path` — always `pathlib.Path`
- Do not hardcode version strings outside `__version__` and `get_backlog_validated_version()`
