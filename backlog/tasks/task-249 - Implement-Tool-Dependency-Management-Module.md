---
id: task-249
title: Implement Tool Dependency Management Module
status: Done
assignee:
  - '@kinsale'
created_date: '2025-12-03 02:26'
updated_date: '2025-12-04 21:37'
labels:
  - infrastructure
  - tooling
  - security
  - 'workflow:Specified'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build tool installation, version management, and caching system for Semgrep and CodeQL. Support on-demand download, version pinning, and offline mode for air-gapped environments.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Implement Semgrep auto-installation (pip install with version pinning)
- [x] #2 Implement CodeQL license check and conditional download
- [x] #3 Add dependency size monitoring (alert if cache exceeds 500MB)
- [x] #4 Create tool version update mechanism with automated testing
- [x] #5 Support offline mode (use cached tools only, no network)
- [x] #6 Test installation flow on Linux, macOS, Windows
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Review existing security module structure
2. Design tool dependency management module
3. Implement Semgrep auto-installation
4. Implement CodeQL license check and download
5. Add dependency size monitoring
6. Create tool version update mechanism
7. Support offline mode
8. Add cross-platform tests
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementation completed with all 9 code review fixes:

Created src/specify_cli/security/tools/ module:
- __init__.py: Module exports
- models.py: ToolConfig, ToolInfo, ToolStatus, InstallResult, CacheInfo dataclasses
- manager.py: ToolManager class with robust implementation

Code Quality Fixes Applied:
1. Archive integrity verification after extraction
2. Efficient os.walk() instead of rglob for size calculation
3. Comprehensive test coverage with proper mocking
4. Download timeout with urllib.request.urlopen
5. Version format validation before URL construction
6. Depth-limited directory search (MAX_SEARCH_DEPTH=5)
7. File validation before chmod operations
8. Error handling for cache directory iteration
9. Robust regex-based version parsing

AC Coverage:
1. Semgrep auto-installation: pip install with version="1.45.0" pinning
2. CodeQL license check: license_check=True, license_url, binary_urls for linux/darwin/win32
3. Dependency size monitoring: get_cache_info() returns CacheInfo with size_warning at 500MB
4. Tool version update: check_for_updates() and update_tool() methods
5. Offline mode: offline_mode=True uses only cached tools, no network
6. Cross-platform: _get_platform_key() detects linux/darwin/win32, tests verify all platforms

57 unit tests in tests/security/tools/ (all passing)
<!-- SECTION:NOTES:END -->
