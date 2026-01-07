---
id: task-579.06
title: 'P0.6: Fix upgrade-repo to remove deprecated files and directories'
status: Done
assignee: []
created_date: '2026-01-06 17:20'
updated_date: '2026-01-07 00:54'
labels:
  - phase-0
  - upgrade-repo
  - cleanup
  - release-blocker
dependencies: []
parent_task_id: task-579
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The upgrade_repo command does NOT clean up deprecated files/directories in target repos.

Items that should be removed during upgrade:
- .specify/ directory (legacy, replaced by .flowspec/)
- _DEPRECATED_*.md command files
- Other deprecated artifacts

Changes needed:
1. Add cleanup step to upgrade_repo
2. Detect and offer to remove .specify/ directory
3. Remove _DEPRECATED_*.md files from .claude/commands/
4. Report what was cleaned up
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 upgrade_repo removes .specify/ directory if present
- [x] #2 upgrade_repo removes _DEPRECATED_*.md files
- [x] #3 Cleanup is reported to user
- [x] #4 Backup created before removing files
- [x] #5 Test: running upgrade-repo cleans up deprecated artifacts
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Notes

### Files Created
- `src/flowspec_cli/deprecated.py` - New module for deprecated file/directory cleanup
- `tests/test_deprecated_cleanup.py` - 27 comprehensive tests

### Files Modified
- `src/flowspec_cli/__init__.py` - Added cleanup step to upgrade_repo command
  - Added 'cleanup' step to StepTracker
  - Added `.specify` to backup directories list
  - Integrated `cleanup_deprecated_files()` after MCP configuration step

### Key Design Decisions
1. **Modular design**: Created separate `deprecated.py` module for reusability
2. **Backup before removal**: All deprecated items are backed up to `backup_dir/_deprecated/` before removal
3. **Detailed result tracking**: `DeprecatedCleanupResult` dataclass tracks:
   - Directories and files removed
   - Backup paths for each item
   - Errors encountered
4. **Non-blocking errors**: Continues processing after individual item failures
5. **Dry-run support**: Cleanup respects dry_run flag (via future integration)

### Cleanup Items
- **Directories**: `.specify/` (legacy, replaced by `.flowspec/`)
- **Files**: `_DEPRECATED_*.md` in command directories

### Test Coverage
- 27 tests covering:
  - Detection of deprecated items
  - Backup creation and content preservation
  - Removal operations
  - Error handling and recovery
  - Dry-run mode
  - Summary generation

## Validation Summary (2026-01-06)

### Testing Results
- **Unit tests**: 27/27 passed (test_deprecated_cleanup.py)
- **Full suite**: 3587 passed, 23 skipped
- **Linting**: All checks passed
- **Formatting**: All files formatted

### Agent Validation
- **QA Guardian**: CONDITIONAL PASS - Comprehensive test coverage, all ACs verified. Recommended symlink handling improvement as optional enhancement.
- **Security Engineer**: PASS - No vulnerabilities found. Secure-by-design implementation with proper path validation, backup-before-removal pattern, and error handling.

### Key Implementation Details
1. **Modular design**: New `deprecated.py` module for reusability
2. **Backup safety**: All deprecated items backed up to `backup_dir/_deprecated/` before removal
3. **Error resilience**: Continues processing after individual item failures
4. **Clear reporting**: Summary method provides human-readable cleanup status
5. **Integration**: Cleanup step added to upgrade_repo after MCP configuration

### Security Assessment
- Path traversal: Protected via hardcoded patterns
- Symlink handling: Python default protects against target deletion
- Error handling: No sensitive data exposed
- Privilege model: User-level operations only

### Follow-up Recommendations (Optional)
- Consider adding `symlinks=True` to `shutil.copytree()` for better symlink preservation
- Split backup/removal error handling for clearer error messages
<!-- SECTION:NOTES:END -->
