---
id: task-501
title: 'claude-improves-again: Implement gather-learnings helper skill'
status: To Do
assignee:
  - '@muckross'
created_date: '2025-12-14 03:07'
updated_date: '2025-12-15 01:50'
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
- [ ] #1 Skill created at .claude/skills/gather-learnings/SKILL.md
- [ ] #2 Reads learning files from memory/learnings directory
- [ ] #3 Matches entries by relevant file paths
- [ ] #4 Matches entries by keywords or tags
- [ ] #5 Returns curated list suitable for PRD/PRP insertion
- [ ] #6 Can be invoked by /flow:specify and /flow:generate-prp
<!-- AC:END -->
