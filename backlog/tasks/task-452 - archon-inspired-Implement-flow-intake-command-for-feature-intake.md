---
id: task-452
title: 'archon-inspired: Implement /flow:intake command for feature intake'
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
Create a new /flow:intake command that processes INITIAL-style documents and bootstraps the feature workflow. This is DIFFERENT from /flow:init which handles constitution/project initialization.

**Location**: `.claude/commands/flow/intake.md`

**Why not /flow:init?**: /flow:init already exists and handles constitution initialization. This new command handles per-feature intake.

**Pattern Source**: Based on context-engineering-intro INITIAL doc processing
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Command file created at .claude/commands/flow/intake.md
- [ ] #2 Accepts path argument to INITIAL doc (default: docs/features/<slug>-initial.md)
- [ ] #3 Parses FEATURE section → backlog task title and description
- [ ] #4 Parses EXAMPLES, DOCUMENTATION, OTHER CONSIDERATIONS → task memory file
- [ ] #5 Creates new backlog task using backlog CLI
- [ ] #6 Creates task memory file at backlog/memory/<task-id>.md
- [ ] #7 Memory file includes: What/Why, Constraints, Examples, Docs, Initial gotchas
- [ ] #8 Command documented in CLAUDE.md slash commands section
<!-- AC:END -->
