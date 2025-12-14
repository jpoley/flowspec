---
id: task-489
title: 'claude-improves-again: Add /flow:intake command'
status: To Do
assignee: []
created_date: '2025-12-14 03:06'
labels:
  - context-engineering
  - commands
  - claude-improves-again
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a new Claude command that turns INITIAL docs into backlog tasks and task memory files. This command parses INITIAL documents and creates structured backlog entries with populated context.

Source: docs/research/archon-inspired.md Task 2
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Command file created at .claude/commands/flow/intake.md
- [ ] #2 Command accepts path to INITIAL doc (defaults to docs/features/<slug>-initial.md)
- [ ] #3 Parses FEATURE section to create backlog task title/description
- [ ] #4 Creates task memory file at backlog/memory/<task-id>.md
- [ ] #5 Populates memory with What/Why, Constraints, Examples, Docs, Gotchas
<!-- AC:END -->
