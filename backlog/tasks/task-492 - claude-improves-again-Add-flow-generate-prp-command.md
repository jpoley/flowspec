---
id: task-492
title: 'claude-improves-again: Add /flow:generate-prp command'
status: To Do
assignee:
  - '@muckross'
created_date: '2025-12-14 03:06'
updated_date: '2025-12-15 01:50'
labels:
  - context-engineering
  - commands
  - claude-improves-again
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a command that generates PRP (Product Requirements Prompt) files by collecting PRD, docs, examples, learnings, and codebase snapshots into a single context bundle.

Source: docs/research/archon-inspired.md Task 5
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Command file created at .claude/commands/flow/generate-prp.md
- [ ] #2 Collects PRD from /flow:specify for the active task
- [ ] #3 Gathers docs/specs, examples, and learnings relevant to the task
- [ ] #4 Generates bounded directory tree of relevant code paths
- [ ] #5 Writes filled PRP to docs/prp/<task-id>.md
<!-- AC:END -->
