---
id: task-105
title: 'Update /jpspec:implement to use backlog.md CLI'
status: To Do
assignee: []
created_date: '2025-11-28 16:01'
labels:
  - jpspec
  - backlog-integration
  - implement
  - P0
  - critical
dependencies:
  - task-090
  - task-091
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify the implement.md command to integrate backlog.md task management. This is the MOST CRITICAL integration - engineers must work exclusively from backlog tasks, checking ACs as they complete work.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Command REQUIRES existing backlog tasks to work on (fails gracefully if none found)
- [ ] #2 All 5 engineer agents receive shared backlog instructions from _backlog-instructions.md
- [ ] #3 Engineers pick up tasks from backlog (backlog task list -s 'To Do')
- [ ] #4 Engineers assign themselves and set status to In Progress before coding
- [ ] #5 Engineers check ACs (--check-ac) as each criterion is implemented
- [ ] #6 Engineers add implementation notes describing what was built
- [ ] #7 Code reviewers verify AC completion matches actual code changes
- [ ] #8 Test: Run /jpspec:implement with test task and verify AC progression
<!-- AC:END -->
