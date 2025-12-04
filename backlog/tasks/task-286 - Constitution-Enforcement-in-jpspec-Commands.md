---
id: task-286
title: Constitution Enforcement in /jpspec Commands
status: To Do
assignee: []
created_date: '2025-12-04 16:08'
updated_date: '2025-12-04 16:31'
labels:
  - constitution-cleanup
dependencies:
  - task-245
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add constitution checks to all /jpspec slash commands before execution
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Before command execution, check memory/constitution.md existence
- [ ] #2 Check for NEEDS_VALIDATION markers in constitution
- [ ] #3 Warn if missing or unvalidated
- [ ] #4 Respect tier-specific enforcement (light = warn, medium = confirm, heavy = block)
- [ ] #5 Add --skip-validation flag for emergencies
<!-- AC:END -->
