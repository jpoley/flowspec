---
id: task-370
title: 'Task Memory: Lifecycle integration with backlog.md (Phase 2)'
status: To Do
assignee: []
created_date: '2025-12-09 15:56'
labels:
  - infrastructure
  - integration
  - phase-2
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Integrate Task Memory with backlog task lifecycle events: auto-create on In Progress, auto-archive on Done
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Hook support added to backlog CLI (post-task-update event)
- [ ] #2 .backlog/hooks/post-task-update.sh created and functional
- [ ] #3 Memory created automatically when task → In Progress
- [ ] #4 Memory archived automatically when task → Done
- [ ] #5 Hook configuration in .backlog/config.yml
- [ ] #6 Integration tests for lifecycle events
<!-- AC:END -->
