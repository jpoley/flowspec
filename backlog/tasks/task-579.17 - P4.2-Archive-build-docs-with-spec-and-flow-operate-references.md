---
id: task-579.17
title: 'P4.2: Archive build-docs with /spec:* and /flow:operate references'
status: Done
assignee: []
created_date: '2026-01-06 17:21'
updated_date: '2026-01-08 02:46'
labels:
  - phase-4
  - documentation
  - cleanup
dependencies: []
parent_task_id: task-579
priority: low
ordinal: 90000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Archive or update build documentation that references deprecated commands.

Build-docs with /flow:operate references:
- build-docs/research/ (3 files)
- build-docs/adr/ (9 files)
- build-docs/architecture/ (3 files)
- build-docs/evaluations/ (2 files)
- build-docs/platform/ (3 files)
- build-docs/diagrams/ (1 file)
- build-docs/audit/ (1 file)

Options:
1. Move to build-docs/archive/ with deprecation notice
2. Update to reflect current workflow (if still relevant)
3. Add deprecation header to files
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Build-docs archived or updated
- [x] #2 Deprecation notices added where appropriate
- [x] #3 Active docs don't reference deprecated commands
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Archived build-docs with deprecated /flow:operate and /spec:* references:

- docs/building/archive/: 5 files moved with deprecation README

- docs/platform/archive/: 2 files moved with deprecation README

- ADR-002, ADR-003: Updated status to Implemented with historical context note

- docs/guides/custom-workflows.md: Already has removal note - no change needed
<!-- SECTION:NOTES:END -->
