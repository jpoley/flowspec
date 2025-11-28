---
id: task-112
title: 'Update /jpspec:implement to use backlog.md CLI'
status: In Progress
assignee:
  - '@implement-agent'
created_date: '2025-11-28 16:56'
updated_date: '2025-11-28 20:17'
labels:
  - jpspec
  - backlog-integration
  - implement
  - P0
  - critical
dependencies:
  - task-107
  - task-108
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
CRITICAL: Modify the implement.md command to integrate backlog.md task management. Engineers must work exclusively from backlog tasks, checking ACs as they complete work. No feature work without backlog tasks.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Command REQUIRES existing backlog tasks to work on (fails gracefully if none found)
- [x] #2 All 5 engineer agents receive shared backlog instructions from _backlog-instructions.md
- [x] #3 Engineers pick up tasks from backlog (backlog task list -s To Do)
- [x] #4 Engineers assign themselves and set status to In Progress before coding
- [x] #5 Engineers check ACs (--check-ac) as each criterion is implemented
- [x] #6 Engineers add implementation notes describing what was built
- [x] #7 Code reviewers verify AC completion matches actual code changes
- [ ] #8 Test: Run /jpspec:implement with test task and verify AC progression
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read current implement.md
2. Add task requirement check at start
3. Integrate _backlog-instructions.md in all 5 agents
4. Update task assignment workflow
5. Update AC checking workflow
6. Update code reviewers to verify ACs
7. Create comprehensive tests
8. Run and verify tests
9. Run linting
<!-- SECTION:PLAN:END -->
