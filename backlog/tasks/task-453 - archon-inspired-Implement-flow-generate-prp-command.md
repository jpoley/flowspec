---
id: task-453
title: 'archon-inspired: Implement /flow:generate-prp command'
status: Done
assignee: []
created_date: '2025-12-12 01:00'
updated_date: '2025-12-12 19:37'
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
Create a new /flow:generate-prp command that generates a complete Product Requirements Prompt (PRP) file from existing artifacts.

**Location**: `.claude/commands/flow/generate-prp.md`

**Output**: `docs/prp/<task-id>.md`

**Purpose**: If you give the generated PRP to an LLM as the only context, it should have everything needed to work on the feature.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Command file created at .claude/commands/flow/generate-prp.md
- [ ] #2 Determines active task from backlog context or argument
- [ ] #3 Collects PRD from /flow:specify output
- [ ] #4 Collects docs and specs from docs/ directory
- [ ] #5 Collects relevant examples from examples/ directory
- [ ] #6 Collects learnings from memory/learnings/ or equivalent
- [ ] #7 Generates bounded directory tree of relevant code paths
- [ ] #8 Populates PRP template with collected material
- [ ] #9 Writes PRP to docs/prp/<task-id>.md
- [ ] #10 Command documented in CLAUDE.md slash commands section
<!-- AC:END -->
