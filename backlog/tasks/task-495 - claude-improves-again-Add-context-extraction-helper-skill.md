---
id: task-495
title: 'claude-improves-again: Add context extraction helper skill'
status: To Do
assignee: []
created_date: '2025-12-14 03:06'
labels:
  - context-engineering
  - skills
  - claude-improves-again
dependencies:
  - task-494
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a helper skill that parses the All Needed Context section from PRD files and returns structured data (JSON). This helper is used by /flow:implement, /flow:generate-prp, and /flow:validate.

Source: docs/research/archon-inspired.md Task 8
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Skill created at .claude/skills/context-extractor/SKILL.md
- [ ] #2 Accepts path to a PRD file as input
- [ ] #3 Parses All Needed Context section into structured JSON
- [ ] #4 Returns code files, docs, examples, gotchas as structured data
- [ ] #5 Can be invoked by other flow commands
<!-- AC:END -->
