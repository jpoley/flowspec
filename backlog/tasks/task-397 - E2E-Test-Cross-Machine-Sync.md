---
id: task-397
title: 'E2E Test: Cross-Machine Sync'
status: To Do
assignee: []
created_date: '2025-12-09 15:58'
labels:
  - testing
  - task-memory
  - e2e
  - git
dependencies:
  - task-375
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create end-to-end test simulating task memory sync across multiple machines via git
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create E2E test in tests/e2e/test_task_memory_sync.py
- [ ] #2 Simulate two git clones (Machine A and Machine B)
- [ ] #3 Test memory creation on Machine A and sync to Machine B
- [ ] #4 Test concurrent edits and merge conflict resolution
- [ ] #5 Verify memory survives git push/pull cycles
- [ ] #6 Test append-only format reduces conflicts
- [ ] #7 Add test for conflict resolution helper command
- [ ] #8 Run test with temporary git repositories
<!-- AC:END -->
