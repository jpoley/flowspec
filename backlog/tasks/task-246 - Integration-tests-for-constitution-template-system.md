---
id: task-246
title: Integration tests for constitution template system
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-03 02:45'
updated_date: '2025-12-04 16:32'
labels:
  - 'workflow:Specified'
dependencies:
  - task-245
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Write comprehensive tests for the tiered constitution template feature
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Test specify init with --constitution light/medium/heavy flags
- [ ] #2 Test empty repo detection and tier prompting
- [ ] #3 Test existing project detection without constitution
- [ ] #4 Test /speckit:constitution command execution
- [ ] #5 Test NEEDS_VALIDATION marker handling
- [ ] #6 Test specify constitution validate command
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Write test for specify init with --constitution light/medium/heavy flags
2. Write test for empty repo detection and tier prompting
3. Write test for existing project detection without constitution
4. Write test for /speckit:constitution command execution (LLM mocking)
5. Write test for NEEDS_VALIDATION marker insertion and detection
6. Write test for specify constitution validate command (pass/fail scenarios)
7. Write integration test for full workflow: detect → customize → validate → approve
8. Add test fixtures for various project types (Python, Go, TypeScript, polyglot)
9. Test tier upgrade workflow (light → medium → heavy)
10. Verify test coverage >90% for constitution system
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
PRD and Functional Spec created:
- docs/prd/architecture-enhancements-prd.md
- docs/specs/architecture-enhancements-functional.md

This task is part of the JP Spec Kit Architecture Enhancements feature group.
<!-- SECTION:NOTES:END -->
