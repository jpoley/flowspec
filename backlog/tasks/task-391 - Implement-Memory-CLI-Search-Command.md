---
id: task-391
title: Implement Memory CLI - Search Command
status: To Do
assignee: []
created_date: '2025-12-09 15:58'
labels:
  - backend
  - task-memory
  - cli
  - search
dependencies:
  - task-375
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create `backlog memory search` command to find memories containing specific text or patterns
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Implement search subcommand with query argument
- [ ] #2 Support regex pattern matching
- [ ] #3 Search across active and archived memories
- [ ] #4 Display results with context (surrounding lines)
- [ ] #5 Support --limit option to cap results
- [ ] #6 Add performance optimization for large memory corpus
- [ ] #7 Test with 1000+ memory files
- [ ] #8 Add CLI tests for search command
<!-- AC:END -->
