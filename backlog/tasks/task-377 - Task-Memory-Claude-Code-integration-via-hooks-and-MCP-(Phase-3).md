---
id: task-377
title: 'Task Memory: Claude Code integration via hooks and MCP (Phase 3)'
status: To Do
assignee: []
created_date: '2025-12-09 15:56'
labels:
  - infrastructure
  - claude-code
  - mcp
  - phase-3
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Inject Task Memory into Claude Code sessions automatically via session-start hook and MCP resources
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 session-start.sh extended to inject active task memories
- [ ] #2 Token-aware injection (max 2000 tokens per task)
- [ ] #3 MCP resource backlog://memory/{task-id} available
- [ ] #4 Session start displays active memory notification
- [ ] #5 Hybrid approach: hooks for auto-inject, MCP for on-demand
- [ ] #6 E2E tests for Claude Code integration
<!-- AC:END -->
