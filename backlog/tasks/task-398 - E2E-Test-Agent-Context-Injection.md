---
id: task-398
title: 'E2E Test: Agent Context Injection'
status: To Do
assignee: []
created_date: '2025-12-09 15:58'
labels:
  - testing
  - task-memory
  - e2e
  - integration
dependencies:
  - task-382
  - task-383
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create end-to-end test verifying task memory gets injected into AI agent context via CLAUDE.md and MCP
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create E2E test in tests/e2e/test_task_memory_injection.py
- [ ] #2 Mock Claude Code reading backlog/CLAUDE.md with @import
- [ ] #3 Verify memory content present in mocked agent context
- [ ] #4 Mock MCP client querying backlog://memory/{task_id} resource
- [ ] #5 Verify MCP returns correct memory content
- [ ] #6 Test no active task scenario (no @import)
- [ ] #7 Add assertions for context content correctness
- [ ] #8 Run test with mocked agents (no live API calls)
<!-- AC:END -->
