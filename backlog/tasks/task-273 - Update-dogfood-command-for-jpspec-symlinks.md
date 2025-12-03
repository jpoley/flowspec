---
id: task-273
title: Update dogfood command for jpspec symlinks
status: To Do
assignee: []
created_date: '2025-12-03 14:01'
labels:
  - cli
  - dogfood
  - implementation
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend specify dogfood to create symlinks for jpspec commands in addition to speckit
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add loop to process both speckit and jpspec namespaces
- [ ] #2 Create jpspec symlinks pointing to templates/commands/jpspec/*.md
- [ ] #3 Handle _backlog-instructions.md partial (create symlink)
- [ ] #4 Add verification for all jpspec symlinks
- [ ] #5 Update CLI help text to mention both speckit and jpspec
- [ ] #6 Test dogfood creates 17 total symlinks (8 speckit + 9 jpspec)
<!-- AC:END -->
