---
id: task-088
title: Phase 0 - Task Context Loader for AC Validation
status: To Do
assignee: []
created_date: '2025-11-28 15:56'
labels:
  - validate-enhancement
  - phase-0
  - backend
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the foundational task context loading capability for the enhanced /jpspec:validate command. This phase is responsible for loading a backlog task by ID, parsing its acceptance criteria into a structured format, and determining the validation approach (automated vs manual) for each AC based on naming conventions and task metadata.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Given a task ID, the loader retrieves task details via `backlog task <id> --plain` and parses all fields (title, description, status, ACs)
- [ ] #2 Acceptance criteria are extracted into a structured list with index, text, and checked status for each AC
- [ ] #3 The loader identifies related code files by searching for references in task description/notes (e.g., file paths, module names)
- [ ] #4 The loader identifies related test files by matching patterns like `test_<feature>.py` or `<feature>.test.ts` based on task context
- [ ] #5 For each AC, the loader determines validation approach: 'automated' (has matching test), 'manual' (requires human judgment), or 'hybrid'
- [ ] #6 If no task ID is provided, the loader finds the current in-progress task via `backlog task list -s "In Progress" --plain`
- [ ] #7 Returns a TaskContext object with: task_id, title, description, acceptance_criteria[], related_files[], validation_plan[]
- [ ] #8 Handles error cases: task not found, no in-progress task, invalid task ID format
<!-- AC:END -->
