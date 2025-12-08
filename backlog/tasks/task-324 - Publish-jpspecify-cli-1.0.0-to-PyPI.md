---
id: task-324
title: Publish specflow-cli 1.0.0 to PyPI
status: To Do
assignee: []
created_date: '2025-12-08 22:10'
labels:
  - infrastructure
  - release
dependencies:
  - task-316
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Execute the production release of specflow-cli 1.0.0.

**Pre-conditions:**
- All code changes merged
- Test PyPI upload successful
- CI passing on main

**Steps:**
1. Verify all tests pass
2. Run release script
3. Validate GitHub release created
4. Validate PyPI upload succeeded
5. Test installation: uv tool install specflow-cli
6. Verify specflow --version works
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 specflow-cli 1.0.0 published to PyPI
- [ ] #2 GitHub release created with correct artifacts
- [ ] #3 Installation from PyPI works
- [ ] #4 specflow --version returns 1.0.0
<!-- AC:END -->
