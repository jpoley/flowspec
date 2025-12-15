---
id: task-493
title: 'claude-improves-again: Make /flow:implement PRP-first'
status: To Do
assignee:
  - '@muckross'
created_date: '2025-12-14 03:06'
updated_date: '2025-12-15 01:50'
labels:
  - context-engineering
  - commands
  - claude-improves-again
dependencies:
  - task-491
  - task-492
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update /flow:implement to check for and load PRP files as primary context. If PRP exists for the active task, load it first. If not, recommend running /flow:generate-prp before implementation.

Source: docs/research/archon-inspired.md Task 6
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 /flow:implement checks for docs/prp/<task-id>.md
- [ ] #2 If PRP exists, loads it as primary context for the agent
- [ ] #3 If PRP missing, recommends: Generate PRP via /flow:generate-prp first
- [ ] #4 Documentation updated to explain PRP-first workflow
<!-- AC:END -->
