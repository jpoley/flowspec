---
id: task-228
title: Create Claude Code hook to auto-emit events on /flowspec completion
status: Done
assignee: []
created_date: '2025-12-03 02:10'
updated_date: '2025-12-03 22:27'
labels:
  - hooks
  - claude-code
  - integration
  - automation
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a Claude Code PostToolUse hook that automatically emits flowspec events when /flowspec slash commands complete. This provides automatic event emission without requiring explicit agent instructions.

**Context**: Claude Code has a native hook system in `.claude/hooks/` that can intercept tool calls. We can use PostToolUse to detect when slash commands complete and emit corresponding events.

**Architecture**:
```
Agent runs /flowspec:implement
    ↓
Claude Code executes slash command
    ↓
PostToolUse hook fires
    ↓
Hook detects /flowspec command completion
    ↓
Hook calls: specify hooks emit implement.completed
    ↓
User's hooks in .specify/hooks/ execute
```

**Implementation**:
1. Create `.claude/hooks/flowspec-event-emitter.py`
2. Hook into PostToolUse or command completion
3. Parse command output to extract feature/task IDs
4. Call `specify hooks emit` with appropriate event type
5. Handle errors gracefully (don't break workflow)

**Event Mapping**:
| Command | Event |
|---------|-------|
| /flowspec:assess | workflow.assessed |
| /flowspec:specify | spec.created |
| /flowspec:research | research.completed |
| /flowspec:plan | plan.created |
| /flowspec:implement | implement.completed |
| /flowspec:validate | validate.completed |
| /flowspec:operate | deploy.completed |

**Considerations**:
- Must be idempotent (don't double-emit if agent also emits manually)
- Should extract context from command output (spec-id, task-id, files)
- Fail-open: errors in hook shouldn't break the workflow
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 PostToolUse hook created at .claude/hooks/flowspec-event-emitter.py
- [ ] #2 Hook detects /flowspec:* command completion
- [ ] #3 Hook extracts spec-id and task-id from command context
- [ ] #4 Hook calls specify hooks emit with correct event type
- [ ] #5 Hook is fail-open (errors logged but don't break workflow)
- [ ] #6 Hook is idempotent (detects if event already emitted)
- [ ] #7 Hook registered in .claude/settings.json
- [ ] #8 Integration tests verify hook fires on command completion
<!-- AC:END -->
