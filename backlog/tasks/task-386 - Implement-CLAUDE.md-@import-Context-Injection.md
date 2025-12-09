---
id: task-386
title: Implement CLAUDE.md @import Context Injection
status: To Do
assignee: []
created_date: '2025-12-09 15:57'
labels:
  - backend
  - task-memory
  - claude-code
  - integration
dependencies:
  - task-377
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update backlog/CLAUDE.md to dynamically include active task memory via @import directive for Claude Code
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add Active Task Context section to backlog/CLAUDE.md
- [ ] #2 Implement dynamic @import update in LifecycleManager
- [ ] #3 Test @import with Claude Code (verify memory loads automatically)
- [ ] #4 Handle no active task scenario gracefully
- [ ] #5 Add section replacement logic with regex
- [ ] #6 Test with multiple rapid state transitions
- [ ] #7 Document @import mechanism in docs/reference/
<!-- AC:END -->
