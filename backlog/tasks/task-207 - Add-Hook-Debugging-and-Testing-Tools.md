---
id: task-207
title: Add Hook Debugging and Testing Tools
status: To Do
assignee:
  - '@pm-planner'
created_date: '2025-12-03 00:41'
updated_date: '2025-12-03 00:58'
labels:
  - implement
  - cli
  - dx
  - hooks
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
CLI commands for hook development: list hooks, test hooks, validate config, view audit log.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 specify hooks list - show all configured hooks and their matchers
- [ ] #2 specify hooks test --event-type <type> --dry-run - test without execution
- [ ] #3 specify hooks validate - validate hooks.yaml against schema
- [ ] #4 specify hooks audit - view execution history from audit log
- [ ] #5 specify hooks audit --tail - live tail of hook executions
- [ ] #6 Unit and integration tests for all CLI commands
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add specify hooks test --dry-run
   - Parse hooks.yaml and validate schema
   - Check event matching logic without execution
   - Report which hooks would trigger for event type
   - Validate all script paths exist and are executable

2. Add specify hooks audit --tail
   - Parse .specify/hooks/audit.log (JSONL)
   - Implement live tail with follow mode
   - Add filtering by hook name, status, date
   - Color-coded output (green=success, red=failed)

3. Add specify hooks list
   - Display all configured hooks from hooks.yaml
   - Show event matchers, timeout, fail_mode
   - Add --verbose mode with full config details
   - Add --json output for scripting

4. Add verbose logging mode
   - Environment variable: SPECIFY_HOOKS_DEBUG=1
   - Log detailed execution trace to debug.log
   - Include stdout/stderr, environment, timing
   - WARNING: May contain sensitive data

5. Create debugging documentation
   - Troubleshooting guide for common errors
   - How to interpret audit logs
   - Performance profiling tips
   - Security event investigation
<!-- SECTION:PLAN:END -->
