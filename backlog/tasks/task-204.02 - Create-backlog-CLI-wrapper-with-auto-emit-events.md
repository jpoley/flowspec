---
id: task-204.02
title: Create backlog CLI wrapper with auto-emit events
status: To Do
assignee:
  - '@galway'
created_date: '2025-12-03 02:19'
updated_date: '2025-12-04 04:01'
labels:
  - hooks
  - cli
  - backlog
  - wrapper
dependencies: []
parent_task_id: task-204
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a wrapper script/function around the `backlog` CLI that automatically emits jp-spec-kit events after each command.

**Context**: Since we can't modify backlog.md directly, we can wrap its CLI to add event emission. Users would use `bk` (or similar alias) instead of `backlog` directly.

**Architecture**:
```
User: bk task edit 123 -s Done
    ↓
Wrapper: backlog task edit 123 -s Done
    ↓
Backlog CLI executes normally
    ↓
Wrapper detects: status changed to Done
    ↓
Wrapper emits: specify hooks emit task.completed --task-id task-123
```

**Implementation Options**:

**Option A: Shell wrapper script**
```bash
#!/bin/bash
# bk - backlog wrapper with event emission
backlog "$@"
exit_code=$?

# Parse command and emit events
if [[ "$1" == "task" && "$2" == "edit" ]]; then
  task_id="$3"
  if [[ "$*" == *"-s Done"* || "$*" == *"-s \"Done\""* ]]; then
    specify hooks emit task.completed --task-id "$task_id"
  elif [[ "$*" == *"-s"* ]]; then
    specify hooks emit task.status_changed --task-id "$task_id"
  fi
fi

exit $exit_code
```

**Option B: Shell function (in .zshrc/.bashrc)**
```bash
bk() {
  backlog "$@"
  # ... emit logic
}
```

**Option C: Python wrapper CLI**
- More robust parsing
- Can read task file to get full context
- Installable via pip

**Recommended**: Option A (shell script) for simplicity, with Option C as enhancement.

**Files to create**:
- `scripts/bin/bk` (shell wrapper)
- `src/specify_cli/backlog_wrapper.py` (optional Python wrapper)
- `docs/guides/backlog-wrapper.md`
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Shell wrapper script created at scripts/bin/bk
- [ ] #2 Wrapper passes all arguments to backlog CLI transparently
- [ ] #3 Wrapper detects task create and emits task.created
- [ ] #4 Wrapper detects status changes and emits appropriate events
- [ ] #5 Wrapper detects AC check/uncheck and emits task.ac_checked
- [ ] #6 Wrapper preserves original exit code from backlog CLI
- [ ] #7 Installation instructions documented (PATH, alias)
- [ ] #8 Works with both bash and zsh
<!-- AC:END -->
