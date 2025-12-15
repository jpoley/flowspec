---
id: task-487
title: Implement Event Router with Namespace Dispatch
status: To Do
assignee:
  - '@chamonix'
created_date: '2025-12-14 03:06'
updated_date: '2025-12-15 01:33'
labels:
  - agent-event-system
  - phase-1
  - architecture
  - infrastructure
  - foundation
dependencies:
  - task-485
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create event routing system dispatching events to handlers based on namespace with pluggable consumers.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 EventRouter class with register_handler method
- [ ] #2 Pattern matching supports wildcards like git.* matches all git events
- [ ] #3 Built-in handlers for JSONL file and MCP server
- [ ] #4 Event filtering by task_id agent_id time_range
- [ ] #5 Unit tests for routing to multiple handlers
<!-- AC:END -->
