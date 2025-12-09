---
id: task-363
title: 'Enhance: sync-copilot-agents.sh for Role-Based Generation'
status: To Do
assignee: []
created_date: '2025-12-09 15:14'
labels:
  - infrastructure
  - automation
  - bash
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify sync script to generate role-filtered agents with metadata
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Role configuration reading from jpspec_workflow.yml implemented
- [ ] #2 get_role_metadata() function extracts agent role mappings
- [ ] #3 generate_frontmatter() enhanced with role and priority fields
- [ ] #4 Role-specific agent generation (--role flag) supported
- [ ] #5 VS Code settings generation (generate_vscode_settings) implemented
<!-- AC:END -->
