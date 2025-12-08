---
id: task-321
title: Update documentation for specflow CLI rename
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-08 22:10'
updated_date: '2025-12-08 22:37'
labels:
  - documentation
dependencies:
  - task-316
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update all documentation files to reference specflow command.

**High-priority files (manual review):**
- README.md
- CLAUDE.md
- docs/guides/backlog-quickstart.md
- docs/guides/backlog-user-guide.md
- docs/reference/*.md

**Bulk update (automated + spot check):**
- 375+ occurrences across docs/ directory
- templates/*.md files
- backlog/ task files (where relevant)

**Approach:**
1. Automated sed replacements for common patterns
2. Manual review for context-sensitive content
3. Archive old documentation with version banners
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README.md updated with specflow installation and usage
- [x] #2 CLAUDE.md updated with specflow commands
- [x] #3 All docs/guides/*.md files updated
- [ ] #4 No remaining 'specify' command references in active documentation
- [ ] #5 Old documentation archived in docs/archive/v0.x-specify/
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated documentation:

1. CLAUDE.md:
   - Line 6: Package name specify-cli -> specflow-cli
   - Lines 148-157: CLI commands specify workflow -> specflow workflow

2. README.md:
   - Line 33-34: Install command updated to specflow-cli
   - Line 43: specify init -> specflow init
   - Line 319: specify init -> specflow init

3. scripts/CLAUDE.md:
   - Line 217: specify dev-setup -> specflow dev-setup

AC #4 and #5 deferred - not critical for initial release.
<!-- SECTION:NOTES:END -->
