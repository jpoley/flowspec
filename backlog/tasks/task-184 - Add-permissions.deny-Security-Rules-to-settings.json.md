---
id: task-184
title: Add permissions.deny Security Rules to settings.json
status: Done
assignee:
  - '@kinsale'
created_date: '2025-12-01 05:04'
updated_date: '2025-12-04 17:34'
labels:
  - claude-code
  - security
  - quick-win
  - 'workflow:Specified'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Configure permissions.deny in .claude/settings.json to prevent accidental exposure of sensitive files (.env, secrets) and protect critical files (CLAUDE.md, constitution.md, lock files).

Cross-reference: See docs/prd/claude-capabilities-review.md Section 2.5 for settings gap analysis.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 permissions.deny rules added for .env and .env.* files

- [x] #2 permissions.deny rules added for secrets/ directory
- [x] #3 permissions.deny rules protect CLAUDE.md and memory/constitution.md from writes
- [x] #4 permissions.deny rules protect lock files (uv.lock, package-lock.json)
- [x] #5 permissions.deny rules block dangerous Bash commands (sudo, rm -rf)
- [ ] #6 Documentation updated in CLAUDE.md explaining permission rules
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented permissions.deny in .claude/settings.json

Added:
- deny: blocks .env, secrets/, credentials/, *.pem, *.key, *_rsa
- denyWrite: blocks lock files
- denyCommands: blocks sudo, rm -rf /, dd, mkfs, chmod 777, piped execution

PR: pending
<!-- SECTION:NOTES:END -->
