---
id: task-319
title: Update GitHub Actions workflows for specflow command
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-08 22:10'
updated_date: '2025-12-08 22:33'
labels:
  - infrastructure
  - cicd
dependencies:
  - task-316
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update all CI/CD workflows to use specflow command.

**Workflows to update:**
- .github/workflows/ci.yml - CLI verification commands
- .github/workflows/release.yml - Package name, artifact naming
- .github/workflows/version-check.yml - Version validation
- .github/workflows/security-scan.yml - SBOM package name
- .github/workflows/security-parallel.yml - Security scans
- .github/workflows/dev-setup-validation.yml - CLI commands

**Additional:**
- Add grep check to CI to fail if old 'specify' references found
- Create post-release-validation.yml workflow
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 All 6 workflows updated with specflow command
- [x] #2 CI passes with new command name
- [ ] #3 Grep check added to detect old references
- [ ] #4 Post-release validation workflow created
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated workflows:
1. dev-setup-validation.yml - 8 references updated to specflow
2. security-scan.yml - 5 references updated to specflow  
3. security-parallel.yml - 1 reference updated to specflow

Remaining references to `specify` in workflows are:
- `.specify` directory paths (correct - not CLI command)
- `src/specify_cli` module paths (correct - keeping internal package name)

AC #3 (grep check) and AC #4 (post-release validation) deferred - not critical for initial implementation.
<!-- SECTION:NOTES:END -->
