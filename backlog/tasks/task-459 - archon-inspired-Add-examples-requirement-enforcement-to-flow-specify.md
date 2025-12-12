---
id: task-459
title: 'archon-inspired: Add examples requirement enforcement to /flow:specify'
status: To Do
assignee: []
created_date: '2025-12-12 01:01'
labels:
  - archon-inspired
  - architecture
  - commands
  - context-engineering
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify /flow:specify to require at least one example reference in every PRD. Specs without example references should be flagged as incomplete.

**Target**: `.claude/commands/flow/specify.md` and related templates

**Purpose**: Tighten bindings between features and examples for better context.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 /flow:specify template includes Examples section with mandatory placeholder
- [ ] #2 Section requires: list of relevant files under examples/
- [ ] #3 Section requires: explanation of how each example relates to the feature
- [ ] #4 PRDs without examples trigger warning message
- [ ] #5 Warning suggests: 'Add at least one relevant example from examples/ directory'
- [ ] #6 Validation step checks for non-empty Examples section
<!-- AC:END -->
