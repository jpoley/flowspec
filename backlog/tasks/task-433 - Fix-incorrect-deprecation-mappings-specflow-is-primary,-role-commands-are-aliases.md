---
id: task-433
title: >-
  Fix incorrect deprecation mappings - /specflow is primary, role commands are
  aliases
status: To Do
assignee: []
created_date: '2025-12-10 22:20'
labels:
  - bug
  - commands
  - critical
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The DEPRECATED commands have WRONG mappings. They tell users to use role-based commands (`/pm:define`, `/arch:design`, etc.) instead of `/specflow:*` commands.

**This is backwards.**

The rule is:
- `/specflow` is the PRIMARY namespace - all SDD workflow functionality MUST be available here
- Role-based commands (`/pm`, `/arch`, `/dev`, `/qa`, `/sec`, `/ops`) are OPTIONAL convenience aliases
- `/specflow:specify` should NOT be deprecated - it's the canonical command
- `/pm:define` is an ALIAS to `/specflow:specify`, not a replacement

Current WRONG deprecation messages:
- `/specflow:_DEPRECATED_specify` → "Use /pm:define" ❌
- `/specflow:_DEPRECATED_assess` → "Use /pm:assess" ❌  
- `/specflow:_DEPRECATED_research` → "Use /pm:discover" ❌
- `/specflow:_DEPRECATED_plan` → "Use /arch:design" ❌
- `/specflow:_DEPRECATED_validate` → "Use /qa:verify" ❌
- etc.

**Fix**: Remove all `_DEPRECATED_*` files from `/specflow` namespace. The `/specflow:*` commands are NOT deprecated.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 All _DEPRECATED_*.md files removed from templates/commands/specflow/
- [ ] #2 All _DEPRECATED_*.md symlinks removed from .claude/commands/specflow/
- [ ] #3 /specflow:specify, /specflow:assess, /specflow:plan, /specflow:validate etc. work as primary commands
- [ ] #4 Role-based commands (/pm:*, /arch:*, etc.) remain as optional aliases
- [ ] #5 Documentation updated to clarify /specflow is primary namespace
<!-- AC:END -->
