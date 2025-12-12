---
id: task-447
title: 'archon-inspired: Create PRP base template for flowspec'
status: To Do
assignee: []
created_date: '2025-12-12 01:00'
labels:
  - archon-inspired
  - architecture
  - templates
  - context-engineering
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a Product Requirements Prompt (PRP) template that acts as a self-contained context packet for each feature. If you give this PRP to an LLM as the only context, it should have everything needed to work on the feature.

**Location**: `templates/docs/prp/prp-base-flowspec.md`

**Pattern Source**: Based on context-engineering-intro PRP structure
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Template file created at templates/docs/prp/prp-base-flowspec.md
- [ ] #2 Contains ALL NEEDED CONTEXT section with subsections: Code Files, Docs/Specs, Examples, Known Gotchas, Related Backlog Tasks
- [ ] #3 Contains CODEBASE SNAPSHOT section (bounded directory tree placeholder)
- [ ] #4 Contains VALIDATION LOOP section: Commands, Expected Success, Known Failure Modes
- [ ] #5 All sections are machine-parseable with consistent heading structure
- [ ] #6 Template includes explanatory comments for each section
<!-- AC:END -->
