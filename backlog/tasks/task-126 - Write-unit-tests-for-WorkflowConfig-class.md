---
id: task-100
title: Write unit tests for WorkflowConfig class
status: To Do
assignee: []
created_date: '2025-11-28 15:58'
labels:
  - testing
  - unit-tests
  - python
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Write comprehensive unit tests for WorkflowConfig class to ensure correct loading and querying of configuration
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Test file created at tests/test_workflow_config.py
- [ ] #2 Tests for loading valid jpspec_workflow.yml
- [ ] #3 Tests for loading invalid YAML (syntax errors)
- [ ] #4 Tests for missing required fields
- [ ] #5 Tests for wrong field types
- [ ] #6 Tests for query methods (get_agents, get_next_state, etc)
- [ ] #7 Tests for config caching mechanism
- [ ] #8 Tests for config reload functionality
- [ ] #9 Tests for validation against schema
- [ ] #10 Test coverage >90% for WorkflowConfig class
<!-- AC:END -->
