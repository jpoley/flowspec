---
id: task-275
title: Update init command for subdirectory structure
status: To Do
assignee: []
created_date: '2025-12-03 14:01'
labels:
  - cli
  - init
  - implementation
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify specify init to create subdirectory structure for commands instead of flat files
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Update command copying logic to use subdirectories (jpspec/, speckit/)
- [ ] #2 Ensure subdirectories are created before copying files
- [ ] #3 Copy _backlog-instructions.md partial along with commands
- [ ] #4 Test init creates correct subdirectory structure
- [ ] #5 Verify init output matches dogfood structure (files vs symlinks)
<!-- AC:END -->
