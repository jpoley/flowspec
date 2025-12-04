---
id: task-243
title: Detect existing projects without constitution
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-03 02:38'
updated_date: '2025-12-04 16:32'
labels:
  - 'workflow:Specified'
dependencies:
  - task-242
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add logic to detect when specify init/upgrade runs on existing project missing a constitution
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Detect existing project (has .git, package.json, pyproject.toml, etc.)
- [ ] #2 Check for missing memory/constitution.md
- [ ] #3 Prompt user: 'No constitution found. Select tier: light/medium/heavy'
- [ ] #4 Trigger LLM constitution customization flow after tier selection
- [ ] #5 Works with both specify init --here and specify upgrade
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Implement project detection heuristic (check for .git, package.json, pyproject.toml, go.mod)
2. Check for missing memory/constitution.md in detected project
3. Build interactive tier selection prompt (light/medium/heavy with descriptions)
4. Implement tier recommendation algorithm (team size, file count, CI presence)
5. Trigger LLM constitution customization flow after tier selection
6. Test with existing projects (various languages/frameworks)
7. Integrate with specify init --here command
8. Integrate with specify upgrade command
9. Document project detection markers and tier recommendation logic
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
PRD and Functional Spec created:
- docs/prd/architecture-enhancements-prd.md
- docs/specs/architecture-enhancements-functional.md

This task is part of the JP Spec Kit Architecture Enhancements feature group.
<!-- SECTION:NOTES:END -->
