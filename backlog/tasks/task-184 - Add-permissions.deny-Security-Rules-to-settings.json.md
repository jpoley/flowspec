---
id: task-184
title: Add permissions.deny Security Rules to settings.json
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-01 05:04'
updated_date: '2025-12-04 16:31'
labels:
  - 'workflow:Specified'
  - security
  - platform
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
- [ ] #1 permissions.deny rules added for .env and .env.* files

- [ ] #2 permissions.deny rules added for secrets/ directory
- [ ] #3 permissions.deny rules protect CLAUDE.md and memory/constitution.md from writes
- [ ] #4 permissions.deny rules protect lock files (uv.lock, package-lock.json)
- [ ] #5 permissions.deny rules block dangerous Bash commands (sudo, rm -rf)
- [ ] #6 Documentation updated in CLAUDE.md explaining permission rules
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Define permissions.deny schema in ADR-014
2. Create .claude/settings.json with deny rules (Layer 1-4)
3. Implement file read/write permission checking
4. Implement command pattern matching and blocking
5. Add audit logging (.claude/audit.log)
6. Update CLAUDE.md with permission rules documentation
7. Test with .env, CLAUDE.md, sudo attempts
8. Create examples of common blocked operations
9. Add override mechanism with user confirmation
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Specification created: docs/prd/platform-devsecops-prd.md (FR-001, FR-002)
<!-- SECTION:NOTES:END -->
