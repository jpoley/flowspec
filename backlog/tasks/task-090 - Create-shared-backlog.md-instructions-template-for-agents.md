---
id: task-090
title: Create shared backlog.md instructions template for agents
status: To Do
assignee: []
created_date: '2025-11-28 15:48'
labels:
  - jpspec
  - backlog-integration
  - P0
  - infrastructure
dependencies:
  - task-089
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a reusable template file containing backlog.md CLI instructions that can be injected into all sub-agent prompts. This ensures consistent task management behavior across all jpspec commands.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Template covers task discovery: how to find existing tasks via backlog search/list
- [ ] #2 Template covers task assignment: assign self and set status to In Progress
- [ ] #3 Template covers AC management: check ACs as work completes using --check-ac
- [ ] #4 Template covers implementation notes: add notes using --notes or --append-notes
- [ ] #5 Template covers task completion: verify all ACs checked before marking Done
- [ ] #6 Template is stored in .claude/commands/jpspec/_backlog-instructions.md (underscore prefix for include)
<!-- AC:END -->
