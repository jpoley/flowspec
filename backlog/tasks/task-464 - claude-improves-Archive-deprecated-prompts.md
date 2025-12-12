---
id: task-464
title: 'claude-improves: Archive deprecated prompts'
status: Done
assignee: []
created_date: '2025-12-12 01:15'
updated_date: '2025-12-12 22:07'
labels:
  - claude-improves
  - source-repo
  - prompts
  - cleanup
  - phase-1
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
13 deprecated prompts exist in .github/prompts/ that should be archived or removed:
- specflow._DEPRECATED_*.prompt.md (13 files)

These clutter the prompts directory and may cause confusion.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Create .github/prompts/archive/ directory
- [x] #2 Move all *DEPRECATED* files to archive directory
- [x] #3 Verify no deprecated files remain in main prompts directory
- [x] #4 Update any documentation referencing these prompts
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
PR #801 merged to main on 2025-12-12. All acceptance criteria verified complete.
<!-- SECTION:NOTES:END -->
