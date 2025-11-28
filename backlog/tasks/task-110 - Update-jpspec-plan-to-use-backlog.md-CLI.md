---
id: task-110
title: 'Update /jpspec:plan to use backlog.md CLI'
status: Done
assignee:
  - '@plan-agent'
created_date: '2025-11-28 16:56'
updated_date: '2025-11-28 20:28'
labels:
  - jpspec
  - backlog-integration
  - plan
  - P1
dependencies:
  - task-107
  - task-108
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify the plan.md command to integrate backlog.md task management. Software Architect and Platform Engineer agents must work with backlog tasks, creating architecture/infrastructure tasks as they plan.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Command discovers existing backlog tasks for the feature being planned
- [x] #2 Both agents receive shared backlog instructions from _backlog-instructions.md
- [x] #3 Software Architect creates architecture tasks in backlog (ADRs, design docs)
- [x] #4 Platform Engineer creates infrastructure tasks in backlog (CI/CD, observability)
- [x] #5 Agents update task status and add implementation plans to existing tasks
- [x] #6 Test: Run /jpspec:plan and verify architecture/infra tasks created in backlog
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read current plan.md and understand structure
2. Integrate _backlog-instructions.md into both agent prompts
3. Add task discovery section at the start
4. Update Software Architect prompt to create architecture tasks
5. Update Platform Engineer prompt to create infrastructure tasks
6. Create comprehensive tests in test_jpspec_plan_backlog.py
7. Run tests and verify all pass
8. Run linting and formatting
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated /jpspec:plan command to integrate with backlog.md CLI for comprehensive task management.

Key Changes:
- Added Step 0: Backlog Task Discovery section to discover existing tasks before planning
- Created _backlog-instructions.md with comprehensive backlog CLI usage guidance
- Integrated backlog instructions into both Software Architect and Platform Engineer agent prompts using {{INCLUDE:...}} pattern
- Added "Backlog Task Management Requirements" sections to both agents with:
  - Software Architect: Creates ADRs, design docs, and pattern implementation tasks with architecture labels
  - Platform Engineer: Creates CI/CD, observability, security, and IaC tasks with infrastructure labels
- Both agents can update existing tasks discovered in Step 0
- Created comprehensive test suite (38 tests) in test_jpspec_plan_backlog.py covering:
  - Command structure validation
  - Task discovery workflow
  - Architecture task creation patterns
  - Infrastructure task creation patterns
  - Backlog instructions content
  - Integration scenarios
  - CLI usage patterns

All tests pass. PR created: https://github.com/jpoley/jp-spec-kit/pull/39
<!-- SECTION:NOTES:END -->
