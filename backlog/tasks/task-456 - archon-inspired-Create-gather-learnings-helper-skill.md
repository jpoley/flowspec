---
id: task-456
title: 'archon-inspired: Create gather-learnings helper skill'
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
Create a skill that reads learning files and returns relevant learnings based on file paths, keywords, or tags. Automatically pulls historical lessons into feature context bundles.

**Location**: `.claude/skills/gather-learnings.md`

**Consumers**: /flow:specify, /flow:generate-prp

**Pattern Source**: Based on context-engineering-intro gotchas integration
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Skill file created at .claude/skills/gather-learnings.md
- [ ] #2 Reads learning files from memory/learnings/ directory or equivalent
- [ ] #3 Matches entries based on: relevant file paths, keywords, tags
- [ ] #4 Supports YAML front matter with tags field for matching
- [ ] #5 Returns curated list of relevant learnings
- [ ] #6 Output can be inserted into Known Gotchas sections
- [ ] #7 Handles case where no learnings directory exists
- [ ] #8 Includes usage examples in skill documentation
<!-- AC:END -->
