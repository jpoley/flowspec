---
id: task-244
title: 'Implement /speckit:constitution LLM customization command'
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-03 02:40'
updated_date: '2025-12-04 16:32'
labels:
  - 'workflow:Specified'
dependencies:
  - task-241
  - task-243
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create slash command that analyzes repo and customizes constitution template with repo-specific details
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create .claude/commands/speckit/constitution.md slash command
- [ ] #2 Command scans repo for: languages, frameworks, CI configs, test setup, linting tools
- [ ] #3 Command detects existing patterns: security scanning, code review requirements, etc.
- [ ] #4 Command customizes selected tier template with repo-specific findings
- [ ] #5 Output includes NEEDS_VALIDATION markers on auto-generated sections
- [ ] #6 Command outputs clear message: Constitution generated - please review and validate
- [ ] #7 Supports --tier {light|medium|heavy} flag to override detection
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create .claude/commands/speckit/constitution.md slash command
2. Implement repo scanning: detect languages (file extensions)
3. Implement repo scanning: detect frameworks (package.json, pyproject.toml, go.mod)
4. Implement repo scanning: detect CI configs (.github/workflows/, .gitlab-ci.yml)
5. Implement repo scanning: detect existing patterns (test frameworks, linting tools)
6. Implement principle detection heuristics (Library-First, CLI Interface, API-First, etc.)
7. Customize selected tier template with repo-specific findings
8. Add NEEDS_VALIDATION markers to auto-generated sections
9. Support --tier flag to override auto-detection
10. Output clear message: Constitution generated - please review and validate
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
PRD and Functional Spec created:
- docs/prd/architecture-enhancements-prd.md
- docs/specs/architecture-enhancements-functional.md

This task is part of the JP Spec Kit Architecture Enhancements feature group.
<!-- SECTION:NOTES:END -->
