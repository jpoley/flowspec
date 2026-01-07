---
id: task-579.08
title: 'P1.2: Fix agent names - kebab-case to PascalCase'
status: Done
assignee: []
created_date: '2026-01-06 17:20'
updated_date: '2026-01-07 01:19'
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
Fix the agent name field in COPILOT_AGENT_TEMPLATES frontmatter to use PascalCase instead of kebab-case.

Current (WRONG):
```yaml
name: "flow-specify"
name: "flow-implement"
```

Target (CORRECT):
```yaml
name: FlowSpecify
name: FlowImplement
```

The name field controls what appears in VSCode's agent dropdown menu.

Location: src/flowspec_cli/__init__.py (COPILOT_AGENT_TEMPLATES dictionary, lines 191-551)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Agent name fields use PascalCase (FlowSpecify, FlowPlan, etc.)
- [x] #2 VSCode agent menu shows professional names
- [x] #3 Test: verify agent names display correctly in VSCode dropdown
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Verification Results (2026-01-06)

All acceptance criteria verified as already implemented:

**AC1: Agent name fields use PascalCase** ✅
- All 5 agents in COPILOT_AGENT_TEMPLATES use PascalCase: FlowSpecify, FlowPlan, FlowImplement, FlowValidate, FlowSubmitNWatchPR
- Template files in templates/.github/agents/ also use PascalCase

**AC2: VSCode agent menu shows professional names** ✅
- The `name:` field directly controls VSCode dropdown display
- Tests verify no quotes, no hyphens, uppercase start

**AC3: Test verification** ✅
- Existing tests verify naming convention:
  - test_copilot_agent_templates_use_pascalcase_names
  - test_init_agents_have_correct_name_fields
  - All tests pass (12 naming-related tests)

**Implementation Details**:
- Work was completed in commit 4b0c074 (2026-01-05)
- ADR-001 documents the naming convention decision
- Tests in test_init_templates.py enforce the convention
<!-- SECTION:NOTES:END -->
