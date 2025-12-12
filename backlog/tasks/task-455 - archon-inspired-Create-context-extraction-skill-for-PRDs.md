---
id: task-455
title: 'archon-inspired: Create context extraction skill for PRDs'
status: To Do
assignee: []
created_date: '2025-12-12 01:00'
labels:
  - archon-inspired
  - architecture
  - skills
  - context-engineering
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a skill that parses the 'All Needed Context' section from PRD files and returns structured data (JSON). This helper enables other commands to automatically know which files, docs, and examples are relevant.

**Location**: `.claude/skills/context-extractor.md`

**Consumers**: /flow:implement, /flow:generate-prp, /flow:validate

**Pattern Source**: Based on context-engineering-intro PRD parsing needs
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Skill file created at .claude/skills/context-extractor.md
- [ ] #2 Accepts path to PRD file as input
- [ ] #3 Parses 'All Needed Context' section
- [ ] #4 Returns structured data with: code_files[], docs_specs[], examples[], gotchas[], external_systems[]
- [ ] #5 Handles missing sections gracefully (returns empty arrays)
- [ ] #6 Output format is JSON-parseable
- [ ] #7 Includes usage examples in skill documentation
<!-- AC:END -->
