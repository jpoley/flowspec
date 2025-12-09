---
id: task-396
title: 'E2E Test: Task Memory Lifecycle'
status: To Do
assignee: []
created_date: '2025-12-09 15:58'
labels:
  - testing
  - task-memory
  - e2e
dependencies:
  - task-377
  - task-381
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create end-to-end test covering full task memory lifecycle from creation to archival
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create E2E test in tests/e2e/test_task_memory_lifecycle.py
- [ ] #2 Test full lifecycle: To Do → In Progress → Done → Archive
- [ ] #3 Verify memory file created, archived, and deleted correctly
- [ ] #4 Test rollback scenario: Done → In Progress restores memory
- [ ] #5 Verify CLAUDE.md @import updated correctly
- [ ] #6 Test with multiple concurrent tasks
- [ ] #7 Add assertions for file existence and content
- [ ] #8 Run test in CI/CD pipeline
<!-- AC:END -->
