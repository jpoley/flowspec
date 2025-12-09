---
id: task-387
title: Implement MCP Resource for Task Memory
status: To Do
assignee: []
created_date: '2025-12-09 15:57'
labels:
  - backend
  - task-memory
  - mcp
  - integration
dependencies:
  - task-375
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add MCP resource endpoint `backlog://memory/{task_id}` to expose task memory to MCP-compatible agents (Copilot, etc.)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add resource endpoint to existing backlog MCP server
- [ ] #2 Implement backlog://memory/{task_id} URI handler
- [ ] #3 Return markdown content from TaskMemoryStore
- [ ] #4 Handle missing memory files with 404 error
- [ ] #5 Add MCP resource tests with mock clients
- [ ] #6 Test with live MCP client (if available)
- [ ] #7 Document MCP resource URI in docs/reference/
<!-- AC:END -->
