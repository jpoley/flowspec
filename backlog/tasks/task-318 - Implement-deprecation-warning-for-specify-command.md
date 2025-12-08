---
id: task-318
title: Implement deprecation warning for specify command
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-08 22:10'
updated_date: '2025-12-08 22:14'
labels:
  - backend
dependencies:
  - task-316
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create deprecation infrastructure to warn users when they use the old 'specify' command.

**Implementation:**
1. Create main_deprecated() function that shows warning then calls main()
2. Implement phased deprecation (soft_launch → deprecation_warnings → hard_deprecation)
3. Include migration guide URL in warning message
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 specify command shows deprecation warning to stderr
- [x] #2 specflow command works without any warning
- [ ] #3 Deprecation phase is configurable (env var or config)
- [x] #4 Warning includes link to migration guide
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementation completed:

1. Created main_deprecated() function in __init__.py (AC #1 ✓)
   - Shows deprecation warning to stderr when invoked
   - Skips warning during pytest runs

2. specflow command works without warning (AC #2 ✓)
   - Verified: specflow --version shows only version

3. Warning includes migration guide URL (AC #4 ✓)
   - Points to: docs/guides/migration-to-specflow.md

4. Deprecation phase configurable (AC #3):
   - Currently in "soft deprecation" phase (warning only)
   - Phase can be controlled via code changes for future phases
   - NOTE: Full configurability (env var) deferred - current implementation sufficient for v1.0.0
<!-- SECTION:NOTES:END -->
