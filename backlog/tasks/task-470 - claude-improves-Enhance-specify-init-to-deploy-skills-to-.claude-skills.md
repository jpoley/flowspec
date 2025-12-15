---
id: task-470
title: 'claude-improves: Enhance specify init to deploy skills to .claude/skills/'
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-12 01:15'
updated_date: '2025-12-15 01:49'
labels:
  - claude-improves
  - cli
  - specify-init
  - skills
  - phase-1
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Skills exist only in .specify/templates/skills/ as templates but are never deployed to .claude/skills/ where Claude Code can auto-invoke them.

The `specify init` command should copy skills from templates/skills/ to .claude/skills/ so they are immediately available for Claude Code to use.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 specify init copies all skills from templates/skills/ to .claude/skills/
- [ ] #2 Skills maintain proper SKILL.md directory structure
- [ ] #3 Existing skills in .claude/skills/ are not overwritten without --force flag
- [ ] #4 Add --skip-skills flag to opt out of skill deployment
- [ ] #5 Document skill deployment in init output
<!-- AC:END -->
