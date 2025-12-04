---
id: task-168
title: Add macOS CI Matrix Testing
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-11-30 16:49'
updated_date: '2025-12-04 16:31'
labels:
  - 'workflow:Specified'
  - cicd
  - platform
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add macos-latest to GitHub Actions CI matrix to verify cross-platform compatibility of run-local-ci.sh and other bash scripts. This follows up on task-085 AC #9 which verified Linux compatibility and documented portable design.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add macos-latest to strategy.matrix.os in .github/workflows/ci.yml
- [ ] #2 Verify run-local-ci.sh passes on macOS runner
- [ ] #3 Fix any platform-specific issues discovered (if any)
- [ ] #4 Document macOS-specific requirements or limitations in scripts/CLAUDE.md
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Review current ci.yml matrix configuration
2. Add macos-latest to strategy.matrix.os
3. Test run-local-ci.sh on macOS runner
4. Fix any macOS-specific issues (path differences, bash version)
5. Verify act compatibility with macOS (Docker Desktop required)
6. Test cross-platform compatibility (portable bash features)
7. Document macOS-specific requirements in scripts/CLAUDE.md
8. Document Docker Desktop requirement for macOS
9. Update CI/CD documentation with macOS support
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Specification created: docs/prd/platform-devsecops-prd.md (FR-005)
<!-- SECTION:NOTES:END -->
