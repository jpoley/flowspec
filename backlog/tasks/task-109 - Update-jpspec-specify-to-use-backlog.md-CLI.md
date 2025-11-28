---
id: task-109
title: 'Update /jpspec:specify to use backlog.md CLI'
status: Done
assignee:
  - '@specify-agent'
created_date: '2025-11-28 16:56'
updated_date: '2025-11-28 20:18'
labels:
  - jpspec
  - backlog-integration
  - specify
  - P1
dependencies:
  - task-107
  - task-108
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify the specify.md command to integrate backlog.md task management. The PM planner agent must create tasks in backlog or work with existing tasks, not just output PRD sections.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Command checks for existing backlog tasks related to feature (backlog search)
- [x] #2 PM planner agent receives shared backlog instructions from _backlog-instructions.md
- [x] #3 Agent creates new tasks via backlog task create when defining work items
- [x] #4 Agent assigns itself to tasks it creates
- [x] #5 Generated PRD includes backlog task IDs (not just prose task lists)
- [x] #6 Test: Run /jpspec:specify and verify tasks appear in backlog with correct format
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read current specify.md and understand structure
2. Integrate _backlog-instructions.md template into agent prompt
3. Add backlog search step at command start
4. Update agent prompt to create tasks via backlog CLI
5. Update PRD output format to reference backlog task IDs
6. Create comprehensive tests in test_jpspec_specify_backlog.py
7. Run tests and verify correctness
8. Run linting and formatting
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated /jpspec:specify command to fully integrate with backlog.md CLI for task management.

Key Changes:
- Added Step 1 to discover existing tasks using `backlog search`
- Integrated _backlog-instructions.md into agent prompt using {{INCLUDE}} directive
- Added explicit task creation workflow in agent context
- Updated Task Breakdown section (#6) to create backlog tasks instead of prose lists
- Modified PRD output requirements to include backlog task ID references
- Added CRITICAL section emphasizing task creation during PRD development

Testing:
- Created comprehensive test suite in tests/test_jpspec_specify_backlog.py
- 21 tests covering command structure, execution, PRD format, and workflows
- All tests passing
- Code formatted with ruff

PR Description:
- PM Planner agent now creates tasks via `backlog task create` with acceptance criteria
- Agent assigns itself (@pm-planner) to tasks it creates
- PRD includes task ID references for full traceability (e.g., "See task-042")
- Task dependencies tracked using --dep flag
- Search step prevents duplicate task creation
<!-- SECTION:NOTES:END -->
