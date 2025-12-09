---
id: task-390
title: Implement Memory CLI - List Command
status: To Do
assignee: []
created_date: '2025-12-09 15:58'
labels:
  - backend
  - task-memory
  - cli
dependencies:
  - task-375
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create `backlog memory list` command to show active and archived task memories
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Implement list subcommand with --archived flag
- [ ] #2 Display task IDs with memory file sizes
- [ ] #3 Sort by last modified time (newest first)
- [ ] #4 Add color coding (green=active, yellow=archived)
- [ ] #5 Support --plain output for scripting
- [ ] #6 Test with various directory states (empty, 1000+ files)
- [ ] #7 Add CLI tests for list command
<!-- AC:END -->
