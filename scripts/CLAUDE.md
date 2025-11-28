# Scripts Directory

## Available Scripts

### bash/
| Script | Purpose |
|--------|---------|
| `run-local-ci.sh` | Run full CI simulation locally |
| `flush-backlog.sh` | Archive Done tasks with summary report |
| `install-act.sh` | Install act for local GitHub Actions testing |

### powershell/
PowerShell equivalents of bash scripts for Windows.

### hooks/
Git hooks and Claude Code hooks.

## Usage

Always run scripts from the project root:
```bash
./scripts/bash/flush-backlog.sh --dry-run  # Preview
./scripts/bash/flush-backlog.sh            # Execute
./scripts/bash/run-local-ci.sh             # Local CI
```

## flush-backlog.sh

Archives completed tasks and generates summary reports.

```bash
# Preview what would be archived
./scripts/bash/flush-backlog.sh --dry-run

# Archive all Done tasks
./scripts/bash/flush-backlog.sh

# Archive without summary
./scripts/bash/flush-backlog.sh --no-summary

# Archive and auto-commit
./scripts/bash/flush-backlog.sh --auto-commit
```

**Exit codes:**
- 0: Success
- 1: Validation error
- 2: No Done tasks to archive
- 3: Partial failure

## act (Local GitHub Actions)

Test GitHub Actions workflows locally:

```bash
# Install
./scripts/bash/install-act.sh

# Usage
act -l                    # List workflows
act -j test               # Run test job
act -j lint               # Run lint job
act -n                    # Dry run
```

**Requirements:** Docker must be running.

## Making Scripts Executable

```bash
chmod +x scripts/bash/*.sh
chmod +x scripts/hooks/*
```

## Documentation

- Flush details: `docs/guides/backlog-flush.md`
- act setup: See act documentation at https://github.com/nektos/act
