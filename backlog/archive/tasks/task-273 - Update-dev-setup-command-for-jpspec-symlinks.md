---
id: task-273
title: Update dev-setup command for flowspec symlinks
status: Done
assignee:
  - '@cli-engineer'
created_date: '2025-12-03 14:01'
updated_date: '2025-12-04 01:34'
labels:
  - cli
  - dogfood
  - implementation
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend specify dogfood to create symlinks for flowspec commands in addition to speckit
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add loop to process both speckit and flowspec namespaces
- [x] #2 Create flowspec symlinks pointing to templates/commands/flowspec/*.md
- [x] #3 Handle _backlog-instructions.md partial (create symlink)
- [x] #4 Add verification for all flowspec symlinks
- [x] #5 Update CLI help text to mention both speckit and flowspec
- [x] #6 Test dogfood creates 17 total symlinks (8 speckit + 9 flowspec)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AC#6 verified: Actually 18 symlinks created (8 speckit + 10 flowspec including _workflow-state.md)

Symlink breakdown:
- speckit: 8 commands (analyze, checklist, clarify, constitution, implement, plan, specify, tasks)
- flowspec: 10 commands (assess, implement, operate, plan, prune-branch, research, specify, validate, _backlog-instructions, _workflow-state)
<!-- SECTION:NOTES:END -->
