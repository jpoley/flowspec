---
id: task-433
title: >-
  Fix incorrect deprecation mappings - /specflow is primary, role commands are
  aliases
status: To Do
assignee: []
created_date: '2025-12-10 22:20'
updated_date: '2025-12-10 22:48'
labels:
  - bug
  - commands
  - critical
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Target Architecture

**2 Workflows + Many Utilities**

- `/speckit:*` - Lightweight SDD workflow (10 commands)
- `/specflow:*` - Full agent-based SDD workflow (14 commands)
- `/dev:*`, `/sec:*`, `/arch:*`, `/ops:*`, `/qa:*` - Stateless utilities (run anytime)

## Problem

The "role-based" reorganization made things worse:
- 8 namespaces instead of 2 clear workflows
- Deprecation warnings pointing users AWAY from specflow (wrong direction)
- Duplicate commands scattered everywhere
- PM work duplicated as both workflow AND role namespace

## Solution

1. **DELETE** all `_DEPRECATED_*.md` files (13 files) - wrong direction
2. **DELETE** entire `/pm` namespace - PM work IS the workflow
3. **DELETE** workflow duplicates from role namespaces:
   - `/arch:design` → use `/specflow:plan`
   - `/dev:build` → use `/specflow:implement`
   - `/qa:verify` → use `/specflow:validate`
   - `/ops:deploy` → use `/specflow:operate`
   - `/sec:audit` → use `/specflow:security_workflow`
4. **KEEP** utility commands in role namespaces (debug, refactor, scan, etc.)

See: `docs/audit/command-cleanup-plan.md` for full implementation plan.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 All 13 _DEPRECATED_*.md files deleted from templates/commands/specflow/
- [ ] #2 Entire /pm namespace deleted (3 commands + symlink)
- [ ] #3 Workflow duplicate commands deleted: /arch:design, /dev:build, /qa:verify, /ops:deploy, /sec:audit
- [ ] #4 All symlinks in .claude/commands/ updated (no broken links)
- [ ] #5 /specflow:* commands work as primary workflow (no deprecation warnings)

- [ ] #6 Utility commands preserved: /dev:debug, /dev:refactor, /sec:scan, etc.
- [ ] #7 Documentation updated (CLAUDE.md, guides)
- [ ] #8 Command count reduced from 61 to 38
<!-- AC:END -->
