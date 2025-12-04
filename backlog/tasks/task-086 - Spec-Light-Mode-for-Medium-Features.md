---
id: task-086
title: Spec-Light Mode for Medium Features
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-11-27 21:54'
updated_date: '2025-12-04 16:32'
labels:
  - 'workflow:Specified'
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create simplified SDD workflow for medium-complexity features (after /jpspec:assess recommends it). Addresses Böckeler concern about 'a LOT of markdown files'. Creates spec-light.md (combined stories + AC), plan-light.md (high-level only), tasks.md (standard). Skips: /jpspec:research, /jpspec:analyze, detailed data models, API contracts. Still enforces: constitutional compliance, test-first. 40-50% faster workflow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create spec-light.md template (combined user stories + AC)
- [ ] #2 Create plan-light.md template (high-level approach only)
- [ ] #3 Implement 'specify init --light' flag
- [ ] #4 Skip research and analyze phases for light mode
- [ ] #5 Maintain constitutional compliance requirement
- [ ] #6 Simplified quality gates for light mode
- [ ] #7 Document when to use light vs full mode
- [ ] #8 Test workflow with medium-complexity features
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create spec-light.md template (combined user stories + AC, no detailed sections)
2. Create plan-light.md template (high-level approach only, skip detailed design)
3. Implement specify init --light flag to use light templates
4. Skip /jpspec:research phase for light mode (direct assess → specify → plan → implement)
5. Skip /jpspec:analyze phase for light mode
6. Maintain constitutional compliance requirement (Test-First, Task Quality)
7. Implement simplified quality gates for light mode (threshold 50/100)
8. Document when to use light vs full mode (decision criteria)
9. Test light mode workflow with medium-complexity features
10. Compare light vs full mode time-to-implementation
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
PRD and Functional Spec created:
- docs/prd/architecture-enhancements-prd.md
- docs/specs/architecture-enhancements-functional.md

This task is part of the JP Spec Kit Architecture Enhancements feature group.
<!-- SECTION:NOTES:END -->
