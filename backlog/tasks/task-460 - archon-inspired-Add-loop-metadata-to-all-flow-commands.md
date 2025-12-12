---
id: task-460
title: 'archon-inspired: Add loop metadata to all flow commands'
status: To Do
assignee: []
created_date: '2025-12-12 01:01'
labels:
  - archon-inspired
  - architecture
  - documentation
  - context-engineering
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add explicit inner vs outer loop metadata annotations to all /flow: command files. This enables reasoning about which agents or UI contexts should handle which commands.

**Targets**: All files in `.claude/commands/flow/`

**Classifications**:
- Outer loop: /flow:assess, /flow:specify, /flow:research, /flow:plan
- Inner loop: /flow:implement
- Spanning: /flow:validate, /flow:operate

**Purpose**: Enable different models, safety rules, or agent contexts for different loop types.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 All /flow: commands have loop metadata marker near top of file
- [ ] #2 Marker format: 'loop: Inner' or 'loop: Outer' or 'loop: Spanning'
- [ ] #3 /flow:assess, /flow:specify, /flow:research, /flow:plan marked as Outer
- [ ] #4 /flow:implement marked as Inner
- [ ] #5 /flow:validate, /flow:operate marked as Spanning (with explanation)
- [ ] #6 New commands (/flow:intake, /flow:generate-prp, /flow:map-codebase) also annotated
- [ ] #7 Loop classification documented in reference guide
<!-- AC:END -->
