---
id: task-113
title: 'Update /jpspec:validate to use backlog.md CLI'
status: In Progress
assignee:
  - '@validate-agent'
created_date: '2025-11-28 16:56'
updated_date: '2025-11-28 20:17'
labels:
  - jpspec
  - backlog-integration
  - validate
  - P1
dependencies:
  - task-107
  - task-108
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify the validate.md command to integrate backlog.md task management. QA, Security, Tech Writer, and Release Manager agents must validate against backlog task ACs and update completion status.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Command discovers tasks in In Progress or Done status for validation
- [x] #2 All 4 validator agents receive shared backlog instructions from _backlog-instructions.md
- [x] #3 Quality Guardian validates ACs match test results
- [x] #4 Security Engineer validates security-related ACs
- [x] #5 Tech Writer creates/updates documentation tasks in backlog
- [x] #6 Release Manager verifies Definition of Done before marking tasks Done
- [ ] #7 Test: Run /jpspec:validate and verify task validation workflow
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read current validate.md
2. Add task discovery for In Progress/Done tasks
3. Integrate _backlog-instructions.md in all 4 agents
4. Update Quality Guardian AC validation workflow
5. Update Security Engineer AC validation workflow
6. Update Tech Writer task creation workflow
7. Update Release Manager DoD verification
8. Create tests in test_jpspec_validate_backlog.py
9. Run and verify tests
<!-- SECTION:PLAN:END -->
