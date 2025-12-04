---
id: task-197
title: Create Custom Statusline with Workflow Context
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-01 05:05'
updated_date: '2025-12-04 16:32'
labels:
  - 'workflow:Specified'
  - ux
  - future
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create custom statusline showing workflow context (phase, active task, progress). Low priority nice-to-have.

Cross-reference: See docs/prd/claude-capabilities-review.md Section 2.12 for statusline assessment.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Statusline script created

- [ ] #2 Displays current workflow phase indicator
- [ ] #3 Displays active backlog task and AC progress
- [ ] #4 Displays git branch
- [ ] #5 Configuration added to .claude/settings.json
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Research statusline API and configuration options
2. Design statusline format (workflow phase, task, AC progress, branch)
3. Create scripts/statusline.sh script
4. Implement current workflow phase indicator (detect from .claude/context)
5. Implement active backlog task detection (read from backlog.md)
6. Implement AC progress calculation (count checked/total ACs)
7. Implement git branch display (git branch --show-current)
8. Add color coding for status (green=on track, yellow=blocked, red=failed)
9. Test statusline with real workflows (/jpspec:implement, /jpspec:validate)
10. Add configuration to .claude/settings.json (statusline.enabled)
11. Document statusline customization options
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Specification created: docs/prd/platform-devsecops-prd.md (FR-016, nice-to-have)
<!-- SECTION:NOTES:END -->
