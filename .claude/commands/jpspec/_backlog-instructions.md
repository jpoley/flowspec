# Backlog.md Task Management Instructions

## Critical Rules

**NEVER edit task files directly.** All task operations MUST use the backlog CLI.

- ✅ DO: `backlog task edit <id> --check-ac 1`
- ✅ DO: `backlog task list --plain`
- ❌ DON'T: Edit markdown files directly
- ❌ DON'T: Manually change checkboxes in files

## Task Discovery

Before starting work, discover relevant tasks:

```bash
# List all tasks
backlog task list --plain

# Find tasks by status
backlog task list -s "To Do" --plain
backlog task list -s "In Progress" --plain

# Search for specific tasks
backlog search "keyword" --plain

# View task details
backlog task <id> --plain
```

## Starting Work on a Task

When you begin work on a task:

```bash
# Assign yourself and set status
backlog task edit <id> -s "In Progress" -a @<your-agent-identity>

# Add your implementation plan
backlog task edit <id> --plan $'1. Step one\n2. Step two\n3. Step three'
```

## Tracking Progress with Acceptance Criteria

Mark acceptance criteria as complete as you finish them:

```bash
# Check a single AC
backlog task edit <id> --check-ac 1

# Check multiple ACs at once
backlog task edit <id> --check-ac 1 --check-ac 2 --check-ac 3

# Add new acceptance criteria if needed
backlog task edit <id> --ac "New criterion"
```

## Completing Tasks

When finishing a task:

```bash
# Add implementation notes (PR description style)
backlog task edit <id> --notes "Summary of what was implemented"

# Or append notes progressively
backlog task edit <id> --append-notes "Additional detail"

# Mark task as Done (only after ALL ACs are checked)
backlog task edit <id> -s Done
```

## Definition of Done Checklist

Before marking any task as Done, verify:

1. ✅ All acceptance criteria are checked
2. ✅ Implementation notes have been added
3. ✅ Tests pass (if applicable)
4. ✅ Code has been reviewed
5. ✅ Documentation updated (if applicable)

## Creating New Tasks

When you need to create follow-up tasks:

```bash
backlog task create "Task title" \
  -d "Description of the task" \
  --ac "Acceptance criterion 1" \
  --ac "Acceptance criterion 2" \
  -l label1,label2 \
  --priority medium \
  -a @your-agent-identity
```

## Key Flags Reference

| Flag | Purpose |
|------|---------|
| `--plain` | AI-readable output (use with list/view commands) |
| `-s` | Status: "To Do", "In Progress", "Done" |
| `-a` | Assignee: @agent-identity |
| `--ac` | Add acceptance criterion |
| `--check-ac N` | Mark AC #N as complete |
| `--uncheck-ac N` | Mark AC #N as incomplete |
| `--notes` | Replace implementation notes |
| `--append-notes` | Add to existing notes |
| `--plan` | Set implementation plan |
| `-l` | Labels (comma-separated) |
| `--priority` | Priority: low, medium, high |
