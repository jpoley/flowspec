---
id: task-264
title: Migrate flowspec commands to templates
status: To Do
assignee: []
created_date: '2025-12-03 13:55'
labels:
  - infrastructure
  - migration
  - dogfood
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Move enhanced flowspec commands from .claude/commands/flowspec/ to templates/commands/flowspec/ to eliminate content drift and establish single source of truth.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create templates/commands/flowspec/ directory
- [ ] #2 Copy all flowspec commands to templates (research, implement, validate, specify, plan, assess, operate)
- [ ] #3 Include _backlog-instructions.md in templates
- [ ] #4 Update specify dogfood to create flowspec symlinks
- [ ] #5 Verify symlinks work correctly
- [ ] #6 Remove old flowspec files from .claude/commands/
- [ ] #7 Update tests to verify flowspec template coverage
<!-- AC:END -->
