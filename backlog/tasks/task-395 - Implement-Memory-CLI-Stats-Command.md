---
id: task-395
title: Implement Memory CLI - Stats Command
status: To Do
assignee: []
created_date: '2025-12-09 15:58'
labels:
  - backend
  - task-memory
  - cli
  - analytics
dependencies:
  - task-375
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create `backlog memory stats` command to display analytics about task memory usage
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Implement stats subcommand (no arguments)
- [ ] #2 Display counts: active memories, archived memories
- [ ] #3 Display sizes: total size, average size, largest file
- [ ] #4 Show age statistics: oldest active, oldest archived
- [ ] #5 Add visual charts (ASCII bar charts for distributions)
- [ ] #6 Support --json output for scripting
- [ ] #7 Test stats calculation with large datasets
- [ ] #8 Add CLI tests for stats command
<!-- AC:END -->
