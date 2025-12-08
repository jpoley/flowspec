---
id: task-304
title: 'Integrate Janitor into /jpspec:validate Workflow'
status: Done
assignee:
  - '@claude'
created_date: '2025-12-07 20:38'
updated_date: '2025-12-08 00:08'
labels:
  - implement
  - workflow
  - integration
dependencies:
  - task-303
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a Phase 7 to /jpspec:validate that invokes the github-janitor agent after successful PR creation:
1. New phase after Phase 6 (PR Generation)
2. Runs github-janitor agent with current branch context
3. Reports cleanup actions taken
4. Sets flag indicating janitor has run

Also update jpspec_workflow.yml to include janitor in workflow configuration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Phase 7 added to validate.md command template
- [x] #2 github-janitor agent invoked after PR creation
- [x] #3 Cleanup results reported to user
- [x] #4 Janitor completion flag set for warning system
- [x] #5 jpspec_workflow.yml updated with janitor step
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

### Overview
Integrate github-janitor agent into /jpspec:validate workflow as Phase 7.

### Tasks

1. **Define github-janitor Agent**
   - Location: .claude/agents/github-janitor.md
   - Define agent capabilities (prune branches, clean worktrees)
   - Extend /jpspec:prune-branch patterns
   - Add PR status sync capability
   - Add branch naming validation
   - Generate cleanup report

2. **Update /jpspec:validate Command**
   - Location: .claude/commands/jpspec/validate.md
   - Add Phase 7: Janitor Cleanup
   - Invoke github-janitor after validation phases
   - Pass push-rules.md config to janitor
   - Capture cleanup report

3. **Create Janitor State Writer**
   - Location: src/specify_cli/janitor/state.py
   - Write pending-cleanup.json after janitor scan
   - Update janitor-last-run timestamp
   - Clear pending items after successful cleanup
   - Log cleanup actions to audit.log

4. **Integration Tests**
   - Location: tests/integration/test_validate_workflow.py
   - Test janitor runs after validation
   - Test state files updated correctly
   - Test cleanup report generated

### Files to Create/Modify
- .claude/agents/github-janitor.md (NEW)
- .claude/commands/jpspec/validate.md (MODIFY - add Phase 7)
- src/specify_cli/janitor/state.py (NEW)
- tests/integration/test_validate_workflow.py (NEW or MODIFY)

### Dependencies
- task-301 (requires push-rules.md config)

### Reference
- Platform design: docs/platform/push-rules-platform-design.md Section 2
- PRD Section 4.3 (github-janitor)
- Existing command: .claude/commands/jpspec/prune-branch.md
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Summary

### Deliverables

| File | Description |
|------|-------------|
| `.claude/agents/github-janitor.md` | GitHub Janitor agent definition |
| `src/specify_cli/janitor/__init__.py` | Module exports |
| `src/specify_cli/janitor/reader.py` | State reading functions |
| `src/specify_cli/janitor/state.py` | State writing functions |
| `templates/commands/jpspec/validate.md` | Added Phase 7 |
| `jpspec_workflow.yml` | Added github-janitor agent |
| `tests/test_janitor.py` | 36 unit tests |

### Phase 7 in /jpspec:validate

1. Load janitor configuration from push-rules.md
2. Invoke github-janitor agent
3. Update state files (janitor-last-run, pending-cleanup.json)
4. Write audit log
5. Report cleanup results

### Test Results

- 36 tests covering reader, writer, audit logging
- 100% pass rate
<!-- SECTION:NOTES:END -->
