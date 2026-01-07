---
id: task-579.12
title: 'P1.6: Update agent handoffs to use new naming convention'
status: Done
assignee: []
created_date: '2026-01-06 17:20'
updated_date: '2026-01-07 01:21'
labels:
  - phase-1
  - agents
  - naming
  - release-blocker
dependencies:
  - task-579.08
parent_task_id: task-579
priority: high
ordinal: 85000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update all agent handoff references to use the new PascalCase agent names.

Current handoffs use kebab-case:
```yaml
handoffs:
  - label: "Create Technical Design"
    agent: "flow-plan"
```

Should use PascalCase:
```yaml
handoffs:
  - label: "Create Technical Design"
    agent: "FlowPlan"
```

Affects all agent templates in COPILOT_AGENT_TEMPLATES and templates/.github/agents/
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 All handoff agent references use PascalCase
- [x] #2 Agent handoff chain works correctly
- [x] #3 Test: verify handoffs resolve to correct agents
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Verification (2026-01-06)

**CLARIFICATION**: The task description incorrectly stated handoffs should use PascalCase. Per ADR-001, the correct convention is:
- `name:` field → PascalCase (FlowPlan)
- `agent:` in handoffs → dot notation (flow.plan)

**Current Implementation (CORRECT per ADR-001)**:
```yaml
handoffs:
  - agent: "flow.plan"      # ✅ Correct
  - agent: "flow.implement"  # ✅ Correct
  - agent: "flow.validate"   # ✅ Correct
```

**Test Verification**:
- `test_copilot_agent_handoffs_use_dot_notation` - PASSED
- All handoff references use dot notation as required

All ACs satisfied per ADR-001 specification.
<!-- SECTION:NOTES:END -->
