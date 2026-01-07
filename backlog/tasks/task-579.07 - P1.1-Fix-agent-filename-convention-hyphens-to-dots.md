---
id: task-579.07
title: 'P1.1: Fix agent filename convention - hyphens to dots'
status: Done
assignee: []
created_date: '2026-01-06 17:20'
updated_date: '2026-01-07 01:12'
labels:
  - phase-1
  - agents
  - naming
  - release-blocker
dependencies: []
parent_task_id: task-579
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fix the agent filename convention in COPILOT_AGENT_TEMPLATES to use DOT notation instead of HYPHEN notation.

Current (WRONG):
- flow-specify.agent.md
- flow-plan.agent.md
- flow-implement.agent.md

Target (CORRECT):
- flow.specify.agent.md
- flow.plan.agent.md
- flow.implement.agent.md

Location: src/flowspec_cli/__init__.py (COPILOT_AGENT_TEMPLATES dictionary, lines 191-551)

This aligns with VSCode Copilot agent discovery conventions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 COPILOT_AGENT_TEMPLATES keys use dot notation (flow.specify.agent.md)
- [x] #2 Templates on disk renamed to dot notation
- [x] #3 flowspec init creates agents with dot-notation filenames
- [x] #4 Test: verify agent files created with correct naming
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Summary (2026-01-06)

### Files Changed

**Template Files Renamed:**
- `flow-specify.agent.md` -> `flow.specify.agent.md`
- `flow-plan.agent.md` -> `flow.plan.agent.md`
- `flow-implement.agent.md` -> `flow.implement.agent.md`
- `flow-validate.agent.md` -> `flow.validate.agent.md`
- `flow-submit-n-watch-pr.agent.md` -> `flow.submit-n-watch-pr.agent.md`

**Template Content Updated:**
- `name:` field changed from `"flow-xxx"` to `FlowXxx` (PascalCase)
- Handoff `agent:` references updated from hyphen to dot notation

**COPILOT_AGENT_TEMPLATES (src/flowspec_cli/__init__.py):**
- Dictionary keys updated to use dot notation
- Embedded template names updated to PascalCase
- Handoff agent references updated to dot notation

### Verification
- All tests pass (3587 passed, 23 skipped)
- Linting passes
- No remaining hyphen-notation references

## Validation Complete (2026-01-06)

- All tests pass: 3592 passed, 23 skipped
- Lint: All checks passed
- 5 new tests added for ADR-001 compliance:
  1. test_copilot_agent_templates_use_dot_notation_filenames
  2. test_copilot_agent_templates_use_pascalcase_names
  3. test_copilot_agent_handoffs_use_dot_notation
  4. test_init_creates_agents_with_dot_notation_filenames
  5. test_init_agents_have_correct_name_fields
<!-- SECTION:NOTES:END -->
