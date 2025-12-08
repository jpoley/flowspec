---
id: task-325
title: Deprecate specify-cli package on PyPI
status: To Do
assignee: []
created_date: '2025-12-08 22:10'
labels:
  - infrastructure
  - release
dependencies:
  - task-316
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
After specflow-cli is successfully published, mark specify-cli as deprecated.

**Steps:**
1. Publish final specify-cli release (0.2.344) with deprecation notice
2. Update specify-cli description on PyPI to point to specflow-cli
3. Optionally: make specify-cli a thin wrapper that depends on specflow-cli
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Final specify-cli release published with deprecation notice
- [ ] #2 PyPI page for specify-cli points to specflow-cli
- [ ] #3 Users installing specify-cli see migration instructions
<!-- AC:END -->
