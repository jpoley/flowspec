---
id: task-394
title: Implement Memory CLI - Cleanup Command
status: To Do
assignee: []
created_date: '2025-12-09 15:58'
labels:
  - backend
  - task-memory
  - cli
  - cleanup
dependencies:
  - task-387
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create `backlog memory cleanup` command to manually trigger archival and deletion of old memories
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Implement cleanup subcommand with --archive-older-than and --delete-archived-older-than options
- [ ] #2 Support time units (d=days, w=weeks, m=months)
- [ ] #3 Add --dry-run flag to preview cleanup operations
- [ ] #4 Display summary of files affected before/after
- [ ] #5 Add interactive confirmation for destructive operations
- [ ] #6 Test cleanup with various time ranges
- [ ] #7 Add CLI tests for cleanup command
<!-- AC:END -->
