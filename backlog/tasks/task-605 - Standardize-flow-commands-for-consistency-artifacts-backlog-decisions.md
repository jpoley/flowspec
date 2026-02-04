---
id: task-605
title: 'Standardize flow commands for consistency (artifacts, backlog, decisions)'
status: To Do
assignee: []
created_date: '2026-02-04 03:44'
labels:
  - refactor
  - commands
  - consistency
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
All /flow:* commands must consistently implement three core behaviors: produce artifacts in docs/, integrate with backlog tasks, and log decisions to .flowspec/logs/decisions/. Currently only 9/23 commands are fully compliant. See docs/reference/command-consistency-requirements.md for full audit and implementation plan.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 All core commands (assess, specify, plan, implement, validate, review) log decisions
- [ ] #2 All commands that produce work output artifacts to docs/ subdirectories
- [ ] #3 All commands accept optional task ID and update backlog on completion
- [ ] #4 No command exceeds 300 lines (excluding security commands being moved)
- [ ] #5 Security commands moved to ps/dev-guard
<!-- AC:END -->
