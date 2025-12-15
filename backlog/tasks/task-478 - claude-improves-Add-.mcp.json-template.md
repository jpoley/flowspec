---
id: task-478
title: 'claude-improves: Add .mcp.json template'
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-12 01:15'
updated_date: '2025-12-15 01:49'
labels:
  - claude-improves
  - templates
  - mcp
  - configuration
  - phase-2
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
No .mcp.json configuration is created during `specify init`. Projects using MCP servers need this configuration file.

Should provide a template with common MCP server configurations.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .mcp.json template created with common server stubs
- [ ] #2 Template includes backlog MCP server configuration
- [ ] #3 Documentation comments explain each server option
- [ ] #4 specify init prompts for MCP configuration (optional)
- [ ] #5 Template is JSON5 compatible for comments
<!-- AC:END -->
