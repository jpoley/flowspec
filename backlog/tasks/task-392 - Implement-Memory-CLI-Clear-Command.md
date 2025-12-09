---
id: task-392
title: Implement Memory CLI - Clear Command
status: To Do
assignee: []
created_date: '2025-12-09 15:58'
labels:
  - backend
  - task-memory
  - cli
dependencies:
  - task-375
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create `backlog memory clear` command to delete task memory with confirmation
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Implement clear subcommand with task_id argument
- [ ] #2 Require --confirm flag for safety
- [ ] #3 Prompt user for confirmation if flag missing
- [ ] #4 Create backup before deletion (optional --no-backup flag)
- [ ] #5 Support --force flag to skip all prompts
- [ ] #6 Add CLI tests for clear command with mocks
- [ ] #7 Document clear usage and safety in docs/guides/
<!-- AC:END -->
