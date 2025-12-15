---
id: task-310.02
title: Remove unnecessary uv tool upgrade attempt
status: To Do
assignee:
  - '@adare'
created_date: '2025-12-08 01:41'
updated_date: '2025-12-15 01:48'
labels:
  - bug
  - cli
  - upgrade-tools
  - cleanup
dependencies: []
parent_task_id: task-310
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Remove or skip the `uv tool upgrade specify-cli` attempt at lines 3973-3986.

**Rationale**: `specify-cli` is installed from git, not PyPI. The `uv tool upgrade` command cannot upgrade git-installed packages - it always returns success without doing anything useful.

**Current behavior**: Wastes time trying `uv tool upgrade`, then falls through to git install anyway.

**Proposed**: Go directly to git install for all upgrades.

**Location**: `src/specify_cli/__init__.py:3973-3986`
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 uv tool upgrade is not called for git-installed packages
- [ ] #2 Git install is used directly for upgrades
<!-- AC:END -->
