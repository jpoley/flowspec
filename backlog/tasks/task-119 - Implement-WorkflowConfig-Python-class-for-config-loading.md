---
id: task-090
title: Implement WorkflowConfig Python class for config loading
status: To Do
assignee: []
created_date: '2025-11-28 15:57'
labels:
  - implementation
  - python
  - core
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement Python class to load, parse, and provide query API for workflow configuration
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 WorkflowConfig class created in src/specify_cli/workflow/config.py
- [ ] #2 Class loads jpspec_workflow.yml using YAML parser (PyYAML)
- [ ] #3 Class provides query methods: get_agents(workflow), get_next_state(current_state, workflow), get_transitions()
- [ ] #4 Class validates loaded config against JSON schema using jsonschema library
- [ ] #5 Class raises clear exceptions for validation errors with helpful messages
- [ ] #6 Class caches config in memory for performance
- [ ] #7 Class supports reloading config for development workflow
- [ ] #8 Comprehensive docstrings for all public methods
<!-- AC:END -->
