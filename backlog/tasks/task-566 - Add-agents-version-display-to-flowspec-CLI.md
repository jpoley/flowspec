---
id: task-566
title: Add agents version display to flowspec CLI
status: To Do
assignee: []
created_date: '2025-12-25 20:17'
labels:
  - implementation
  - cli
  - versioning
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend flowspec version command to show both core and agents versions. Read from pyproject.toml and agents-version.json. Display Claude Code compatibility.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 flowspec version shows core version
- [ ] #2 flowspec version shows agents version
- [ ] #3 Claude Code version displayed
- [ ] #4 JSON output format supported (--json flag)
- [ ] #5 Handles missing version files gracefully
<!-- AC:END -->
