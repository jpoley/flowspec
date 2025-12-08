---
id: task-317
title: Update pyproject.toml for specflow CLI rename
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-08 22:10'
updated_date: '2025-12-08 22:14'
labels:
  - architecture
  - backend
dependencies:
  - task-316
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update package metadata and entry points for CLI rename.

**Changes Required:**
1. Package name: specify-cli → specflow-cli
2. Add specflow entry point as primary CLI command
3. Add deprecated specify entry point with warning
4. Version bump to 1.0.0 (major version for breaking change)
5. Update pytest plugin marker if needed
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pyproject.toml [project] name = 'specflow-cli'
- [x] #2 specflow entry point defined pointing to specify_cli:main
- [x] #3 specify entry point defined pointing to specify_cli:main_deprecated
- [x] #4 version bumped to 1.0.0
- [x] #5 uv build produces specflow-cli-*.tar.gz and *.whl artifacts
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementation completed:

1. Updated pyproject.toml:
   - name = "specflow-cli" (AC #1 ✓)
   - specflow entry point → specify_cli:main (AC #2 ✓)
   - specify entry point → specify_cli:main_deprecated (AC #3 ✓)
   - version = "1.0.0" (AC #4 ✓)

2. uv build produces:
   - dist/specflow_cli-1.0.0.tar.gz (AC #5 ✓)
   - dist/specflow_cli-1.0.0-py3-none-any.whl (AC #5 ✓)

3. Both commands installed and working:
   - specflow --version → "jp-spec-kit 1.0.0"
   - specify --version → shows deprecation warning then version

4. All 2770 tests pass
<!-- SECTION:NOTES:END -->
