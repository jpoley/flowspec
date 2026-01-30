<div align="center">
    <img src="./images/flowspec.png"/>
    <h1>flowspec</h1>
    <h3><em>Spec-Driven Development for AI-Assisted Coding</em></h3>
</div>

<p align="center">
    <strong>Structured specifications. Tracked tasks. Confident shipping.</strong>
</p>

<p align="center">
    <a href="https://github.com/jpoley/flowspec/actions/workflows/release.yml"><img src="https://github.com/jpoley/flowspec/actions/workflows/release.yml/badge.svg" alt="Release"/></a>
    <a href="https://github.com/jpoley/flowspec/stargazers"><img src="https://img.shields.io/github/stars/jpoley/flowspec?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/jpoley/flowspec/blob/main/LICENSE"><img src="https://img.shields.io/github/license/jpoley/flowspec" alt="License"/></a>
    <a href="https://scorecard.dev/viewer/?uri=github.com/jpoley/flowspec"><img src="https://api.scorecard.dev/projects/github.com/jpoley/flowspec/badge" alt="OpenSSF Scorecard"/></a>
</p>

---

## What is flowspec?

flowspec provides structured workflows for AI-assisted development. Instead of ad-hoc prompting, you use slash commands that:

1. **Assess** feature complexity and choose the right workflow
2. **Create** specifications and technical designs
3. **Track** progress in your backlog
4. **Validate** quality before shipping

## Quick Start

```bash
# Install flowspec CLI
uv tool install flowspec-cli --from git+https://github.com/jpoley/flowspec.git

# Initialize your project
flowspec init my-project --ai claude
cd my-project
```

During init, you'll be prompted to install:
- **backlog.md** - task management
- **beads** - detailed work tracking for AI agents

## Core Workflow

```
/flow:assess  →  /flow:specify  →  /flow:plan  →  /flow:implement  →  /flow:validate
     ↓               ↓                ↓                 ↓                   ↓
  Assessed       Specified         Planned        In Progress          Validated
```

### The Five Core Commands

| Command | What It Does | Output |
|---------|--------------|--------|
| `/flow:assess` | Evaluate complexity, decide if SDD is needed | Assessment report, workflow recommendation |
| `/flow:specify` | Create PRD and feature specifications | PRD in `docs/prd/` |
| `/flow:plan` | Design architecture, create ADRs | Technical spec in `docs/specs/`, ADRs in `docs/adr/` |
| `/flow:implement` | Write code, run tests, review | Source code, tests, documentation |
| `/flow:validate` | QA validation, quality checks | QA reports in `docs/qa/` |

## Workflow Modes

Run `/flow:assess` first. It scores complexity and recommends:

| Score | Mode | Approach |
|-------|------|----------|
| 8-12 | Simple | Skip SDD, just code it |
| 13-20 | Light/Medium | Quick specs, faster iteration |
| 21+ | Full SDD | All phases, thorough review |

### Simple Tasks
```bash
# Just create a task and implement directly
backlog task create "Fix login button alignment"
# Then code it
```

### Medium Features
```bash
/flow:assess Add user settings page
/flow:specify
/flow:implement
```

### Complex Features
```bash
/flow:assess Build REST API with JWT authentication
/flow:specify
/flow:plan
/flow:implement
/flow:validate
```

## All Commands Reference

### Core Workflow (5 commands)

| Command | Description |
|---------|-------------|
| `/flow:assess` | Evaluate feature complexity and recommend workflow mode |
| `/flow:specify` | Create PRD and specifications using PM planner agent |
| `/flow:plan` | Create technical design and ADRs using architect agent |
| `/flow:implement` | Orchestrate implementation (calls build, review, rigor, gate, pre-pr) |
| `/flow:validate` | Run QA validation and quality checks |

### Setup (2 commands)

| Command | Description |
|---------|-------------|
| `/flow:init` | Initialize project with constitution and configuration |
| `/flow:reset` | Re-run workflow configuration questions |

### Implementation Sub-Commands (5 commands)

These are called by `/flow:implement` but can also be run independently:

| Command | Description |
|---------|-------------|
| `/flow:build` | Launch frontend/backend engineer agents in parallel |
| `/flow:review` | Conduct code review with acceptance criteria verification |
| `/flow:rigor` | Validate branch naming, worktree, backlog linkage |
| `/flow:gate` | Validate spec quality before implementation proceeds |
| `/flow:pre-pr` | Run validation checklist before creating PR |

### Utilities (2 commands)

| Command | Description |
|---------|-------------|
| `/flow:generate-prp` | Generate context bundles from existing artifacts |
| `/flow:map-codebase` | Generate directory tree listings for context |

### Automation (1 command)

| Command | Description |
|---------|-------------|
| `/flow:submit-n-watch-pr` | Submit PR, monitor CI, iterate on feedback until approval-ready |

## Artifacts Produced

| Phase | Artifact | Location |
|-------|----------|----------|
| Assess | Assessment report | `docs/assess/` |
| Specify | PRD | `docs/prd/` |
| Plan | Technical spec | `docs/specs/` |
| Plan | ADRs | `docs/adr/` |
| Implement | Source code | `src/` |
| Implement | Tests | `tests/` |
| Validate | QA reports | `docs/qa/` |

## Working with Tasks

```bash
# List tasks
backlog task list --plain

# Start work on a task
backlog task edit 42 -s "In Progress" -a @myself

# Check off acceptance criteria
backlog task edit 42 --check-ac 1

# Complete task
backlog task edit 42 -s Done
```

## Project Structure

```
project/
├── .claude/commands/flow/   # Slash commands
├── docs/
│   ├── assess/              # Assessment reports
│   ├── prd/                 # PRDs
│   ├── specs/               # Technical specs
│   ├── adr/                 # Architecture Decision Records
│   └── qa/                  # QA reports
├── src/                     # Implementation
├── tests/                   # Test suites
├── backlog/                 # Task management
└── memory/
    └── constitution.md      # Project principles
```

## Supported AI Agents

| Agent | Status |
|-------|--------|
| [Claude Code](https://www.anthropic.com/claude-code) | Primary, fully supported |
| [GitHub Copilot](https://github.com/features/copilot) | Supported |
| [Cursor](https://cursor.sh/) | Supported |

```bash
# Initialize with specific agent
flowspec init my-project --ai claude
flowspec init my-project --ai copilot
```

## Documentation

- **[Spec-Driven Development](docs/spec-driven.md)** - Core methodology
- **[Task Management](docs/guides/task-management-tiers.md)** - Backlog.md + Beads workflow
- **[What's New](docs/whats-new.md)** - Recent updates

## Contributing

Contributions welcome. All commits require DCO sign-off:

```bash
git commit -s -m "feat: your feature"
```

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines.

**Found a bug?** Open an issue at [github.com/jpoley/flowspec/issues](https://github.com/jpoley/flowspec/issues)

## License

MIT License - see [LICENSE](LICENSE) for details.
