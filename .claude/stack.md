# Stack — flowspec-cli

## Language
- **Python 3.11+** — pinned via `requires-python = ">=3.11"` in `pyproject.toml`
- No other languages in active use

## Package Manager
- **uv** — `uv sync` (install deps), `uv tool install . --force` (install CLI globally)
- Lock file: `uv.lock` — never edit manually, never commit without `uv sync`

## CLI Framework
- **Typer** — all commands defined with `@app.command()` or `app.add_typer()`
- **Rich** — all terminal output (Console, Panel, Table, Tree, Live)
- Entry point: `flowspec_cli:main` (also aliased as `specify`)

## HTTP Client
- **httpx** with **truststore** for system SSL — module-level `client` singleton in `__init__.py`
- Timeouts: 5s default for version checks, longer for downloads

## Persistence
- Flat files only: YAML (`flowspec_workflow.yml`), JSONL (`.logs/decisions/`), Markdown (backlog tasks)
- No database, no cache, no object storage

## Dependencies (key)
| Package | Use |
|---------|-----|
| `typer` | CLI framework |
| `rich` | Terminal output |
| `httpx[socks]` | HTTP client |
| `truststore` | System SSL certs |
| `pyyaml` | YAML parsing |
| `keyring` | Secure token storage |
| `jsonschema` | Schema validation |
| `mcp` | MCP server protocol |
| `readchar` | Interactive prompts |

## CI
- **GitHub Actions** — `.github/workflows/ci.yml`
- Jobs: lint (ruff format + ruff check), test (pytest), docs
- Triggers: push to `main`, PRs targeting `main`
- Python version in CI: 3.11

## Task Management
- **backlog.md CLI** — `backlog task list --plain`, `backlog task edit <id> ...`
- Task files in `backlog/tasks/` — **never edit directly**, CLI only
