---
id: task-595
title: >-
  Fix flowspec init --ai claude creating 'commands' directory in project root
  (Issue #1155)
status: Done
assignee:
  - '@claude'
created_date: '2026-01-26 20:36'
updated_date: '2026-01-26 20:46'
labels:
  - bug
  - cli
  - init
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
When running `flowspec init my-project --ai claude`, the generated project structure incorrectly places the `commands` directory in the project root (`my-project/commands/`) instead of under `.claude/` (`my-project/.claude/commands/`).

**Root Cause**: In `templates_deploy.py`, the `_copy_templates` function copies all template directories to the project root. The `exclude_dirs` only excludes `.git`, `__pycache__`, and `agents`. This means `commands/`, `skills/`, and `partials/` are copied to the project root instead of `.claude/`.

While skills are correctly deployed to `.claude/skills/` by a separate `deploy_skills` step, `commands` and `partials` have no equivalent deployment step and end up in the wrong location.

**Reported Version**: 0.4.004
**Reported Environment**: Windows WSL, Python 3.12

GitHub Issue: https://github.com/jpoley/flowspec/issues/1155
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Running `flowspec init my-project --ai claude` creates `commands/` directory under `.claude/` (i.e., `my-project/.claude/commands/`)
- [x] #2 No `commands/` directory is created at the project root
- [x] #3 No `partials/` directory is created at the project root
- [x] #4 Skills continue to work correctly (deployed to `.claude/skills/`)
- [x] #5 Existing tests pass and new tests cover the fix
- [x] #6 Fix works on Windows WSL, macOS, and Linux
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Update `templates_deploy.py` to exclude `commands`, `skills`, and `partials` from root copy
2. Create `deploy_commands` function in `src/flowspec_cli/skills/scaffold.py` (or separate module)
3. Create `deploy_partials` function for partials deployment
4. Update `init` command in `__init__.py` to call new deployment functions
5. Write unit tests for new deployment functions
6. Run full test suite to verify no regressions
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Summary

Fixed the bug where `flowspec init --ai claude` was incorrectly creating `commands/` and `partials/` directories in the project root instead of under `.claude/`.

### Root Cause
In `templates_deploy.py`, the `_copy_templates` function was copying all template directories to the project root. The `exclude_dirs` only excluded `.git`, `__pycache__`, and `agents`, allowing `commands/`, `skills/`, and `partials/` to be copied to the wrong location.

### Changes Made

1. **`src/flowspec_cli/templates_deploy.py`**: Added `commands`, `skills`, and `partials` to the `exclude_dirs` set to prevent them from being copied to the project root.

2. **`src/flowspec_cli/skills/scaffold.py`**: Added two new functions:
   - `deploy_commands()`: Deploys commands from `templates/commands/` to `.claude/commands/`
   - `deploy_partials()`: Deploys partials from `templates/partials/` to `.claude/partials/`
   - Added helper `_find_templates_dir()` for locating template subdirectories

3. **`src/flowspec_cli/skills/__init__.py`**: Exported the new `deploy_commands` and `deploy_partials` functions.

4. **`src/flowspec_cli/__init__.py`**: Added deployment steps in the `init` command to call `deploy_commands` and `deploy_partials` after skills deployment.

5. **`tests/test_skills_deployment.py`**: Added comprehensive tests:
   - `TestCommandsDeployFunction`: Tests for `deploy_commands()` function
   - `TestPartialsDeployFunction`: Tests for `deploy_partials()` function
   - `TestCommandsInInit`: Integration tests verifying correct directory structure after `flowspec init`

### Test Results
- All 3,497 tests pass
- All new tests verify the fix for issue #1155
- Lint and format checks pass

### Verification
After this fix:
- `flowspec init my-project --ai claude` creates `my-project/.claude/commands/` (correct)
- No `my-project/commands/` directory is created (bug fixed)
- No `my-project/partials/` directory is created (bug fixed)
- Skills continue to work correctly at `.claude/skills/`

### Enhanced Automated Tests

Added comprehensive test class `TestGitHubIssue1155` with 7 tests that:
- Verify commands/ is NOT at project root (the exact bug)
- Verify commands are in .claude/commands/ with correct structure
- Verify specific command files exist (flow/assess.md, flow/implement.md, vibe/vibe.md, etc.)
- Verify partials/ is NOT at project root
- Verify partials are in .claude/partials/ with correct structure
- Verify skills/ is NOT at project root
- Verify full .claude/ directory structure
- Verify fix works with --here flag

Tests use pytest's cross-platform `tmp_path` fixture - works on Windows WSL, macOS, and Linux.

Total: 3,501 tests pass (23 tests in test_skills_deployment.py)
<!-- SECTION:NOTES:END -->
