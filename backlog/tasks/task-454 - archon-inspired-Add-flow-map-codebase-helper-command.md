---
id: task-454
title: 'archon-inspired: Add /flow:map-codebase helper command'
status: To Do
assignee: []
created_date: '2025-12-12 01:00'
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
Create a helper command that generates bounded directory tree listings and feature maps for relevant parts of the codebase.

**Location**: `.claude/commands/flow/map-codebase.md`

**Purpose**: Ensure every feature has a short, readable map of the code area it touches. Supports PRP generation and feature context.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Command file created at .claude/commands/flow/map-codebase.md
- [ ] #2 Accepts one or more paths of interest (directories under src/)
- [ ] #3 Runs bounded directory tree listing (limited depth)
- [ ] #4 Filters to relevant files only (excludes node_modules, __pycache__, etc.)
- [ ] #5 Can write output to: PRP file under CODEBASE SNAPSHOT section OR separate file at docs/feature-maps/<task-id>.md
- [ ] #6 Supports --depth flag for tree depth control
- [ ] #7 Supports --output flag for destination control
- [ ] #8 Command documented in CLAUDE.md slash commands section
<!-- AC:END -->
