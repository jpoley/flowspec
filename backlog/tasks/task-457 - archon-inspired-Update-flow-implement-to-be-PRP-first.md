---
id: task-457
title: 'archon-inspired: Update /flow:implement to be PRP-first'
status: To Do
assignee: []
created_date: '2025-12-12 01:01'
labels:
  - archon-inspired
  - architecture
  - commands
  - context-engineering
dependencies:
  - task-447
  - task-453
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify the existing /flow:implement command to check for and prioritize PRP files. When a PRP exists, it should be loaded as the primary context for implementation.

**Target**: `.claude/commands/flow/implement.md`

**Purpose**: Make PRP files part of the normal workflow rather than optional extras.

**Dependency**: Requires task-447 (PRP template) and task-453 (/flow:generate-prp)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Updated /flow:implement checks for PRP file at docs/prp/<task-id>.md
- [ ] #2 If PRP exists, it is loaded first as primary context
- [ ] #3 If PRP does not exist, command recommends: 'Generate a PRP via /flow:generate-prp before doing non-trivial implementation work'
- [ ] #4 PRP context is passed to implementation agents
- [ ] #5 Backward compatible - works without PRP (with recommendation)
- [ ] #6 Change documented in command description
<!-- AC:END -->
