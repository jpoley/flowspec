---
id: task-310.03
title: Add unit tests for upgrade-tools scenarios
status: Done
assignee:
  - '@galway'
created_date: '2025-12-08 01:41'
updated_date: '2026-01-06 21:26'
labels:
  - test
  - cli
  - upgrade-tools
dependencies: []
parent_task_id: task-310
priority: medium
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add comprehensive unit tests for `_upgrade_jp_spec_kit()` covering:

1. Upgrade when newer version available
2. No-op when already at latest
3. Downgrade with explicit `--version`
4. Version not found error handling
5. uv not installed error handling
6. Git install failure handling

**Location**: `tests/test_upgrade_commands.py` (existing file)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Tests cover upgrade success path
- [x] #2 Tests cover already-at-latest path
- [x] #3 Tests cover error scenarios
- [x] #4 Tests use mocking for subprocess calls
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Tests already exist in tests/test_upgrade_commands.py covering all scenarios
<!-- SECTION:NOTES:END -->
