# JP Spec Kit - Claude Code Configuration

## Project Overview

**JP Spec Kit** is a toolkit for Spec-Driven Development (SDD):
- **Specify CLI**: Command-line tool to bootstrap projects (`specify-cli` package)
- **Templates**: SDD templates for multiple AI agents
- **Documentation**: Comprehensive guides in `docs/`

## Essential Commands

```bash
# Development
pytest tests/                    # Run tests
ruff check . --fix               # Lint and auto-fix
ruff format .                    # Format code
uv sync                          # Install dependencies
uv tool install . --force        # Install CLI locally

# Backlog (NEVER edit task files directly!)
backlog task list --plain        # List tasks (AI-friendly output)
backlog task 42 --plain          # View task details
backlog task edit 42 -s "In Progress" -a @myself  # Start work
backlog task edit 42 --check-ac 1  # Mark acceptance criterion done
backlog task edit 42 -s Done     # Complete task
```

## Slash Commands

```bash
/jpspec:specify   # Create/update feature specs
/jpspec:plan      # Execute planning workflow
/jpspec:research  # Research and validation
/jpspec:implement # Implementation with code review
/jpspec:validate  # QA, security, docs validation
/jpspec:operate   # SRE operations (CI/CD, K8s)
```

## Critical Rules

### DCO Sign-off (Required)
All commits MUST include sign-off:
```bash
git commit -s -m "feat: description"
```

### Version Management
When modifying `src/specify_cli/__init__.py`:
1. Update version in `pyproject.toml`
2. Add entry to `CHANGELOG.md`
3. Follow semantic versioning

### Backlog.md Task Management
**NEVER edit task files directly** - Use `backlog task edit` CLI commands only.
Direct file editing breaks metadata sync, Git tracking, and relationships.

See: `backlog/CLAUDE.md` for detailed guidance.

### Git Worktrees for Parallel Work
Worktree name MUST match branch name:
```bash
git worktree add ../feature-auth feature-auth  # Correct
git worktree add ../work1 feature-auth         # Wrong
```

## Project Structure

```
jp-spec-kit/
├── src/specify_cli/        # CLI source code
├── tests/                  # Test suite (pytest)
├── templates/              # Project templates
├── docs/                   # Documentation
│   ├── guides/             # User guides
│   └── reference/          # Reference docs
├── memory/                 # Constitution & specs
├── scripts/bash/           # Automation scripts
├── backlog/                # Task management
└── .claude/commands/       # Slash command implementations
```

## Code Standards

### Python
- **Linter/Formatter**: Ruff (replaces Black, Flake8, isort)
- **Line length**: 88 characters
- **Type hints**: Required for public APIs
- **File paths**: Use `pathlib`

### Testing
- **Framework**: pytest
- **Coverage**: >80% on core functionality
- **Pattern**: Arrange-Act-Assert (AAA)

### Commits
Follow conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

## Documentation References

| Topic | Location |
|-------|----------|
| Backlog Quick Start | `docs/guides/backlog-quickstart.md` |
| Backlog User Guide | `docs/guides/backlog-user-guide.md` |
| Backlog Commands | `docs/reference/backlog-commands.md` |
| Inner Loop | `docs/reference/inner-loop.md` |
| Outer Loop | `docs/reference/outer-loop.md` |
| Agent Classification | `docs/reference/agent-loop-classification.md` |
| Flush Backlog | `docs/guides/backlog-flush.md` |

## Subfolder Context

Additional context loaded when working in specific directories:
- `backlog/CLAUDE.md` - Task management workflow
- `scripts/CLAUDE.md` - Script execution guidance
- `src/CLAUDE.md` - Python code standards

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GITHUB_JPSPEC` | GitHub token for API requests |
| `SPECIFY_FEATURE` | Override feature detection for non-Git repos |

## Quick Troubleshooting

```bash
# Dependencies issues
uv sync --force

# CLI not found
uv tool install . --force

# Make scripts executable
chmod +x scripts/bash/*.sh

# Check Python version (requires 3.11+)
python --version
```

---

*Subfolder CLAUDE.md files provide additional context when working in those directories.*
