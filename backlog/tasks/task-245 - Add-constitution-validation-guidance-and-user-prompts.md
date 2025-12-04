---
id: task-245
title: Add constitution validation guidance and user prompts
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-03 02:43'
updated_date: '2025-12-04 16:32'
labels:
  - 'workflow:Specified'
dependencies:
  - task-244
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ensure users are clearly informed when constitution needs validation and provide guidance
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add NEEDS_VALIDATION marker format documentation
- [ ] #2 Create validation checklist output after constitution generation
- [ ] #3 Add specify constitution validate command to check for unvalidated sections
- [ ] #4 Warn user if they try to use /jpspec commands with unvalidated constitution
- [ ] #5 Document constitution validation process in docs/guides/
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Document NEEDS_VALIDATION marker format and usage in docs/
2. Create validation checklist template output after constitution generation
3. Implement specify constitution validate command to check for unvalidated sections
4. Add warning to /jpspec commands if unvalidated constitution detected
5. Create docs/guides/constitution-validation-process.md guide
6. Add validation status to specify constitution show output
7. Test validation workflow (generate → validate → remove markers → re-validate)
8. Document best practices for reviewing auto-generated content
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
PRD and Functional Spec created:
- docs/prd/architecture-enhancements-prd.md
- docs/specs/architecture-enhancements-functional.md

This task is part of the JP Spec Kit Architecture Enhancements feature group.
<!-- SECTION:NOTES:END -->
