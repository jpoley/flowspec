---
id: task-079
title: Stack Selection During Init
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-11-27 21:53'
updated_date: '2025-12-04 16:32'
labels:
  - 'workflow:Specified'
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Allow users to select a technology stack (React+Go, React+Python, Full-Stack TypeScript, Mobile+Go, Data/ML Pipeline, etc.) when running 'specify init'. After selection, remove unselected stack files to reduce clutter. Copy selected stack's CI/CD workflow to .github/workflows/. Feasibility: MEDIUM-HIGH complexity, 3-5 days effort.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add STACK_CONFIG to specify-cli with all 9 stack definitions
- [ ] #2 Create interactive stack selection UI (arrow keys)
- [ ] #3 Add --stack CLI flag for non-interactive use
- [ ] #4 Implement cleanup function to remove unselected stacks
- [ ] #5 Copy selected stack workflow to .github/workflows/
- [ ] #6 Add skip option to keep all stacks
- [ ] #7 Update release packages to include stacks
- [ ] #8 Create integration tests for stack selection
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Define STACK_CONFIG with all 9 stack definitions (Python dataclass)
2. Implement interactive stack selection UI with inquirer (arrow keys navigation)
3. Add --stack CLI flag for non-interactive mode (single or comma-separated IDs)
4. Implement conditional scaffolding logic (only copy selected stack files)
5. Implement CI/CD workflow selection and copy per stack
6. Add "ALL STACKS" option for polyglot projects
7. Add --no-stack flag to skip selection (SDD only)
8. Update release packages to include stack templates
9. Test single stack, multiple stacks, and all stacks scenarios
10. Create integration tests for stack selection and scaffolding
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
PRD and Functional Spec created:
- docs/prd/architecture-enhancements-prd.md
- docs/specs/architecture-enhancements-functional.md

This task is part of the JP Spec Kit Architecture Enhancements feature group.
<!-- SECTION:NOTES:END -->
