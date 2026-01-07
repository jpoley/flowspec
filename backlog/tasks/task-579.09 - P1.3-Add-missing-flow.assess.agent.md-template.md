---
id: task-579.09
title: 'P1.3: Add missing flow.assess.agent.md template'
status: Done
assignee: []
created_date: '2026-01-06 17:20'
updated_date: '2026-01-07 01:27'
labels:
  - phase-1
  - agents
  - templates
  - release-blocker
dependencies: []
parent_task_id: task-579
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the missing flow.assess.agent.md agent template. Currently only 5 agents exist, should be 6.

Current agents (5):
- flow.specify.agent.md
- flow.plan.agent.md
- flow.implement.agent.md
- flow.validate.agent.md
- flow.submit-n-watch-pr.agent.md

Missing:
- flow.assess.agent.md

The assess agent evaluates feature complexity and determines SDD workflow suitability (full SDD, spec-light, or skip).

Format:
```yaml
---
name: FlowAssess
description: Evaluate feature complexity and determine SDD workflow approach
target: "chat"
tools: [...]
handoffs:
  - label: "Create Specification"
    agent: "FlowSpecify"
---
```
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 flow.assess.agent.md template created
- [x] #2 Agent added to COPILOT_AGENT_TEMPLATES in __init__.py
- [x] #3 Template on disk at templates/.github/agents/
- [x] #4 Agent includes proper handoff to FlowSpecify
- [x] #5 VSCode shows exactly 6 flow agents
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Summary (2026-01-06)

Completed as part of task-579.10 implementation.

### Files Created
- `.github/agents/flow.assess.agent.md` - Deployed agent for flowspec repo
- `templates/.github/agents/flow.assess.agent.md` - Template for new projects
- Added to `COPILOT_AGENT_TEMPLATES` in `src/flowspec_cli/__init__.py`

### Agent Content
```yaml
name: FlowAssess
description: "Evaluate feature complexity and determine SDD workflow approach"
handoffs:
  - agent: "flow.specify"
```

### Verification
- VSCode shows 6 flow agents (FlowAssess, FlowSpecify, FlowPlan, FlowImplement, FlowValidate, FlowSubmitNWatchPR)
- All naming convention tests pass
- Full test suite: 3592 passed
<!-- SECTION:NOTES:END -->
