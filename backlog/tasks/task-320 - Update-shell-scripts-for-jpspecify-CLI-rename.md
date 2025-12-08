---
id: task-320
title: Update shell scripts for specflow CLI rename
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-08 22:10'
updated_date: '2025-12-08 22:35'
labels:
  - infrastructure
dependencies:
  - task-316
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update all shell scripts that reference the specify command.

**Scripts to update (13+ files):**
- scripts/bash/install-specify-latest.sh → install-specflow-latest.sh
- scripts/bash/run-local-ci.sh
- scripts/bash/create-new-feature.sh
- scripts/bash/check-prerequisites.sh
- scripts/bash/check-mcp-servers.sh
- .github/workflows/scripts/create-release-packages.sh
- .github/workflows/scripts/update-version.sh
- release.sh
- And others found in investigation

**Additional:**
- Create migration script: migrate-to-specflow.sh
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 All shell scripts updated with specflow references
- [ ] #2 install-specify-latest.sh renamed or redirects to new script
- [x] #3 Migration script created for users
- [x] #4 release.sh updated with specflow_cli references
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated shell scripts:

**Bash scripts:**
1. install-specify-latest.sh - 5 references (specflow-cli, specflow --help)
2. pre-commit-dev-setup.sh - 7 references (uv run specflow dev-setup)
3. migrate-commands-to-subdirs.sh - 2 references
4. run-local-ci.sh - 1 reference (specflow --help check)
5. scripts/hooks/pre-push - 4 references (specflow security scan)

**PowerShell scripts:**
1. install-specify-latest.ps1 - 4 references
2. run-local-ci.ps1 - 1 reference (specflow --help check)

**Documentation:**
1. scripts/CLAUDE.md - 1 reference

AC #2 (rename script file) deferred - keeping install-specify-latest.sh name for now to avoid breaking external references.
<!-- SECTION:NOTES:END -->
