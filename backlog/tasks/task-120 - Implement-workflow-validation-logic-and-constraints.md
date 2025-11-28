---
id: task-091
title: Implement workflow validation logic and constraints
status: To Do
assignee: []
created_date: '2025-11-28 15:57'
labels:
  - implementation
  - python
  - validation
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement semantic validation logic that checks workflow configuration for logical errors beyond schema syntax
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 WorkflowValidator class created in src/specify_cli/workflow/validator.py
- [ ] #2 Validator checks for circular state transitions (no cycles in DAG)
- [ ] #3 Validator checks all states are reachable from 'To Do'
- [ ] #4 Validator checks all referenced states exist in states list
- [ ] #5 Validator checks all workflow references exist in workflows list
- [ ] #6 Validator checks all agent names are valid/defined
- [ ] #7 Validator provides detailed error messages for each validation failure
- [ ] #8 Validator can be called at config load time and provides both warnings and errors
<!-- AC:END -->
