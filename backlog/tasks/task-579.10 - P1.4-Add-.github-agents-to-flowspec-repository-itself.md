---
id: task-579.10
title: 'P1.4: Add .github/agents/ to flowspec repository itself'
status: Done
assignee: []
created_date: '2026-01-06 17:20'
updated_date: '2026-01-07 01:27'
labels:
  - phase-1
  - agents
  - infrastructure
  - release-blocker
dependencies: []
parent_task_id: task-579
priority: high
ordinal: 83000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add deployed .github/agents/ directory to the flowspec repository itself so VSCode Copilot integration works when developing flowspec.

Currently flowspec only has:
- templates/.github/agents/ (template sources)

Should also have:
- .github/agents/ (deployed for flowspec repo)

This enables flowspec developers to use the VSCode agent integration while working on flowspec itself.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .github/agents/ directory created in flowspec repo
- [x] #2 All 6 agents deployed with correct naming
- [x] #3 VSCode agent integration works in flowspec repo
- [x] #4 Agents match templates/.github/agents/ content
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Summary (2026-01-06)

### Files Created

**Deployed agents in `.github/agents/`:**
1. `flow.assess.agent.md` - NEW (was missing)
2. `flow.specify.agent.md`
3. `flow.plan.agent.md`
4. `flow.implement.agent.md`
5. `flow.validate.agent.md`
6. `flow.submit-n-watch-pr.agent.md`

**Template agents in `templates/.github/agents/`:**
- Added `flow.assess.agent.md` (was missing)

**Code changes:**
- `src/flowspec_cli/__init__.py`: Added `flow.assess.agent.md` to `COPILOT_AGENT_TEMPLATES`
- Updated comment from "5 key workflow commands" to "6 key workflow commands"

### Agent Names (PascalCase per ADR-001)
- FlowAssess
- FlowSpecify
- FlowPlan
- FlowImplement
- FlowValidate
- FlowSubmitNWatchPR

### Verification
- All 5 naming convention tests pass
- Full test suite: 3592 passed, 23 skipped
- Lint check passes

### What FlowAssess Does
- Entry point for SDD workflow
- Evaluates feature complexity
- Recommends workflow mode (Full SDD, Spec-Light, or Skip)
- Creates initial backlog task
- Hands off to FlowSpecify
<!-- SECTION:NOTES:END -->
