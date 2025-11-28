---
id: task-091
title: Create test framework for backlog.md integration
status: To Do
assignee: []
created_date: '2025-11-28 15:51'
labels:
  - jpspec
  - backlog-integration
  - P0
  - testing
dependencies:
  - task-090
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Set up pytest-based test framework to verify jpspec commands correctly use backlog.md CLI. Tests should verify task creation, status updates, AC checking, and proper workflow completion.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create tests/test_jpspec_backlog_integration.py test module
- [ ] #2 Implement fixture to create temporary backlog directory with test config
- [ ] #3 Implement fixture to create sample tasks for testing (known IDs, known ACs)
- [ ] #4 Create helper function to verify backlog CLI was called with expected arguments
- [ ] #5 Create helper to parse backlog task output and verify state changes
- [ ] #6 Add test for task discovery (backlog search, backlog task list)
- [ ] #7 Add test for task assignment (backlog task edit -a -s)
- [ ] #8 Add test for AC checking (backlog task edit --check-ac)
- [ ] #9 All tests pass: pytest tests/test_jpspec_backlog_integration.py
<!-- AC:END -->
