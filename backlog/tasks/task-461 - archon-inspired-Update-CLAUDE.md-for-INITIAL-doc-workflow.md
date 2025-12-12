---
id: task-461
title: 'archon-inspired: Update CLAUDE.md for INITIAL doc workflow'
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
Update the main CLAUDE.md instructions to prefer INITIAL docs as the starting point for feature work. Ensure agents load INITIAL docs before running /flow:assess or /flow:specify.

**Target**: `CLAUDE.md`

**Purpose**: Make INITIAL docs the canonical intake point for all feature work.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 CLAUDE.md includes guidance about INITIAL docs
- [ ] #2 Guidance states: 'If there is an INITIAL doc for the current feature, read that document before running /flow:assess or /flow:specify'
- [ ] #3 Guidance states: 'The INITIAL doc is the primary source of high-level context for the feature'
- [ ] #4 Documents location of INITIAL docs (docs/features/<slug>-initial.md)
- [ ] #5 Documents relationship between INITIAL -> PRD -> PRP pipeline
- [ ] #6 Slash commands section updated to include /flow:intake and /flow:generate-prp
<!-- AC:END -->
