---
id: task-458
title: 'archon-inspired: Enhance /flow:validate with Feature Validation Plan'
status: To Do
assignee: []
created_date: '2025-12-12 01:01'
labels:
  - archon-inspired
  - architecture
  - commands
  - context-engineering
dependencies:
  - task-449
  - task-455
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Enhance the existing /flow:validate command to extract and execute the Feature Validation Plan from PRD/PRP files. Moves from generic 'run tests' to feature-specific validation recipes.

**Target**: `.claude/commands/flow/validate.md`

**Purpose**: Enable reproducible, documented validation traces for each feature.

**Dependency**: Requires task-449 (Feature Validation Plan section) and task-455 (context extraction skill)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 /flow:validate locates PRD or PRP file for active task
- [ ] #2 Extracts 'Feature Validation Plan' section using context extraction skill
- [ ] #3 Option A (automated): Runs validation commands via bash, parses and summarizes results
- [ ] #4 Option B (semi-automated): Prints commands with instructions for user to run
- [ ] #5 Updates backlog task notes with validation results
- [ ] #6 Updates task memory with: Current State, Latest validation run, Known Issues if failures
- [ ] #7 Documents validation trace in task history
<!-- AC:END -->
