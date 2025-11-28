---
id: task-094
title: 'Integration - Enhanced /jpspec:validate Command'
status: To Do
assignee: []
created_date: '2025-11-28 15:56'
labels:
  - validate-enhancement
  - integration
  - slash-command
dependencies:
  - task-088
  - task-089
  - task-090
  - task-091
  - task-092
  - task-093
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Wire all phases together into the enhanced /jpspec:validate slash command. This task creates the main command file that orchestrates the complete workflow from task loading through PR generation, with proper error handling and user feedback at each stage.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Command accepts optional task-id argument; defaults to current in-progress task if not provided
- [ ] #2 Executes phases in order: 0 (load) → 1 (test) → 2 (agents, parallel) → 3 (verify) → 4 (complete) → 5 (PR)
- [ ] #3 Each phase reports progress to user before execution (e.g., 'Phase 1: Running automated tests...')
- [ ] #4 Phase failures halt workflow with clear error message indicating which phase failed and why
- [ ] #5 Command can be re-run after fixing issues - handles partial completion state gracefully
- [ ] #6 Updates .claude/commands/jpspec/validate.md with the enhanced implementation
- [ ] #7 Updates templates/commands/jpspec/validate.md to match the enhanced version
- [ ] #8 Includes comprehensive help text explaining the workflow and expected inputs
<!-- AC:END -->
