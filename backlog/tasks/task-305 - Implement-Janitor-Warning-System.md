---
id: task-305
title: Implement Janitor Warning System
status: Done
assignee:
  - '@claude'
created_date: '2025-12-07 20:38'
updated_date: '2025-12-08 00:10'
labels:
  - implement
  - hooks
  - ux
dependencies:
  - task-304
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a warning system that alerts when github-janitor hasn't been run after validation:
1. Track janitor execution in session state or temp file
2. Warn in session-start hook if pending janitor tasks exist
3. Display warning in backlog task list when janitor is overdue
4. Integrate with existing session-start.sh hook

Warning should be non-blocking but persistent until janitor runs.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Janitor state tracking implemented
- [x] #2 session-start.sh updated with janitor warning
- [x] #3 Warning displays pending cleanup count
- [x] #4 Warning clears after janitor runs
- [x] #5 Non-blocking behavior confirmed
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

### Overview
Implement janitor warning system in session-start hook to alert when cleanup is pending.

### Tasks

1. **Modify session-start.sh Hook**
   - Location: .claude/hooks/session-start.sh
   - Add check for pending-cleanup.json (after line 92)
   - Parse pending branches count
   - Parse pending worktrees count
   - Add warning if total > 0
   - Suggest /jpspec:validate or github-janitor

2. **Create Pending Cleanup Reader**
   - Location: src/specify_cli/janitor/reader.py
   - Read pending-cleanup.json
   - Parse counts safely (handle missing/corrupted files)
   - Return structured cleanup status

3. **Add Warning Display Logic**
   - Integrate with existing warning system in session-start.sh
   - Use consistent format (⚠ symbol, yellow color)
   - Show counts of pending items
   - Non-blocking (warning only, not error)

4. **Integration Tests**
   - Location: .claude/hooks/test-session-start.sh
   - Test warning displays when cleanup pending
   - Test no warning when cleanup empty
   - Test handles missing state file gracefully
   - Test handles corrupted JSON gracefully

### Files to Create/Modify
- .claude/hooks/session-start.sh (MODIFY - add janitor warning)
- src/specify_cli/janitor/reader.py (NEW)
- .claude/hooks/test-session-start.sh (MODIFY - add janitor tests)

### Dependencies
- task-304 (requires janitor state files)

### Reference
- Platform design: docs/platform/push-rules-platform-design.md Section 1.3
- PRD Section 4.4 (Warning System)
- Existing hook: .claude/hooks/session-start.sh
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Summary

### Deliverables

| File | Description |
|------|-------------|
| `.claude/hooks/session-start.sh` | Added janitor warning check |
| `.claude/hooks/test-session-start.sh` | Added 4 new tests for janitor |

### How It Works

1. On session start, checks `.specify/state/pending-cleanup.json`
2. Parses JSON to count pending branches, worktrees, non-compliant branches
3. If any items pending, displays warning in session context
4. Warning suggests running `/jpspec:prune-branch` or github-janitor
5. Non-blocking (fail-open principle maintained)

### Warning Format

```
Environment Warnings:
  ⚠ Repository cleanup pending: 1 branch(es) to prune
  ⚠   Run '/jpspec:prune-branch' or github-janitor to clean up
```

### Test Results

- Warning displays when pending items exist
- No warning when cleanup is empty
- Handles missing file gracefully
- Handles corrupted JSON gracefully
<!-- SECTION:NOTES:END -->
