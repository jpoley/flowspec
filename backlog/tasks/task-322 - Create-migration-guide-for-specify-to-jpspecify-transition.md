---
id: task-322
title: Create migration guide for specify to specflow transition
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
Create comprehensive migration documentation for users transitioning from specify to specflow.

**Contents:**
1. Why the rename happened (branding clarity)
2. Installation changes (uv tool install specflow-cli)
3. Command usage changes
4. Script migration (search/replace guidance)
5. CI/CD workflow updates
6. Troubleshooting common issues
7. Timeline for specify command removal

**Location:** docs/guides/migration-to-specflow.md
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Migration guide created at docs/guides/migration-to-specflow.md
- [x] #2 Includes installation instructions
- [x] #3 Includes automated migration script usage
- [x] #4 Includes manual update checklist
- [x] #5 Includes deprecation timeline
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Created migration guide at docs/guides/migration-to-specflow.md

Contents:
- Why the rename happened (branding clarity)
- Quick migration steps
- Installation instructions (AC #2)
- Deprecation timeline (AC #5)
- Automated script migration (bash, CI/CD, aliases) (AC #3)
- Manual update checklist (AC #4)
- What stays the same
- Troubleshooting section
<!-- SECTION:NOTES:END -->
