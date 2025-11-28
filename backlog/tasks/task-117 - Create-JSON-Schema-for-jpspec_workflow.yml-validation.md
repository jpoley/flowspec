---
id: task-088
title: Create JSON Schema for jpspec_workflow.yml validation
status: To Do
assignee: []
created_date: '2025-11-28 15:57'
labels:
  - architecture
  - schema
  - validation
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create JSON Schema for validating jpspec_workflow.yml configuration files to ensure structure, types, and references are correct
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 JSON schema file created at memory/jpspec_workflow.schema.json
- [ ] #2 Schema validates all required fields (version, states, workflows, transitions, agent_loops)
- [ ] #3 Schema enforces correct types for all fields (strings, arrays, objects)
- [ ] #4 Schema validates state names are unique and referenced in transitions
- [ ] #5 Schema validates workflow commands match /jpspec pattern
- [ ] #6 Schema validates state references in transitions exist in states list
- [ ] #7 Schema validation examples provided in documentation
- [ ] #8 Schema passes jsonschema validation tool
<!-- AC:END -->
