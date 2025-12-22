---
id: task-377
title: 'Task Memory: Claude Code integration via hooks and MCP (Phase 3)'
status: In Progress
assignee:
  - '@adare'
created_date: '2025-12-09 15:56'
updated_date: '2025-12-22 22:54'
labels:
  - infrastructure
  - claude-code
  - mcp
  - phase-3
  - 'workflow:Planned'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Inject Task Memory into Claude Code sessions automatically via session-start hook and MCP resources
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 session-start.sh extended to inject active task memories
- [ ] #2 Token-aware injection (max 2000 tokens per task)
- [x] #3 MCP resource backlog://memory/{task-id} available
- [x] #4 Session start displays active memory notification
- [x] #5 Hybrid approach: hooks for auto-inject, MCP for on-demand
- [ ] #6 E2E tests for Claude Code integration
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Wire token-aware truncation in LifecycleManager (1 line change)\n2. Update session-start.sh to use update_active_task_with_truncation()\n3. Create E2E test: test_memory_injection_e2e.py\n4. Test scenarios: active task, truncation, multiple tasks, no tasks, missing files\n5. Manual Claude Code integration test\n6. Update implementation notes with completion status
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented Claude Code integration for task memory:

- Extended session-start.sh to inject first active task memory into CLAUDE.md
- Uses ContextInjector Python integration (fail-silent for robustness)
- Displays "Task memory available" notification for each task with memory
- MCP resources implemented (backlog://memory/{task-id} and /active)
- Hybrid approach: @import for auto-load, MCP for on-demand access

Files modified:
- .claude/hooks/session-start.sh (added injection logic)
- src/specify_cli/memory/injector.py (ContextInjector)
- src/specify_cli/memory/mcp.py (MCP resources)

Note: AC#2 (token-aware injection) needs token counting implementation. AC#6 (E2E tests) requires live Claude Code session testing.
<!-- SECTION:NOTES:END -->
