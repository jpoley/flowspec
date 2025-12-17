---
id: task-501
title: 'claude-improves-again: Implement gather-learnings helper skill'
status: To Do
assignee:
  - '@muckross'
created_date: '2025-12-14 03:07'
updated_date: '2025-12-17 01:27'
labels:
  - context-engineering
  - skills
  - claude-improves-again
dependencies:
  - task-500
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a skill that reads learning files from memory/learnings and matches entries based on file paths, keywords, or tags. Returns curated list for insertion into PRD/PRP gotchas section.

Source: docs/research/archon-inspired.md Task 14
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Skill created at .claude/skills/gather-learnings/SKILL.md
- [x] #2 Reads learning files from memory/learnings directory
- [x] #3 Matches entries by relevant file paths
- [x] #4 Matches entries by keywords or tags
- [x] #5 Returns curated list suitable for PRD/PRP insertion
- [x] #6 Can be invoked by /flow:specify and /flow:generate-prp
<!-- AC:END -->
