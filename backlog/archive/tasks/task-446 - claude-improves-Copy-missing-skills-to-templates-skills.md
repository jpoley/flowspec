---
id: task-446
title: 'claude-improves: Copy missing skills to templates/skills/'
status: To Do
assignee: []
created_date: '2025-12-12 01:09'
labels:
  - claude-improves
  - source-repo
  - skills
  - phase-1
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Two skills exist in .claude/skills/ but are NOT in templates/skills/, meaning users running `specify init` won't get them:
- security-fixer
- security-workflow

These skills should be copied to templates/skills/ so they are distributed to all new projects.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 security-fixer skill directory copied to templates/skills/
- [ ] #2 security-workflow skill directory copied to templates/skills/
- [ ] #3 Both skills have proper SKILL.md structure
- [ ] #4 Verify with: diff <(ls templates/skills/) <(ls .claude/skills/ | grep -v '\.md$')
<!-- AC:END -->
