---
id: task-471
title: 'claude-improves: Add CLAUDE.md scaffolding to specify init'
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-12 01:15'
updated_date: '2025-12-15 01:49'
labels:
  - claude-improves
  - cli
  - specify-init
  - claude-md
  - phase-1
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
No root-level CLAUDE.md is created when running `specify init`. Projects need a CLAUDE.md with project-specific Claude Code instructions.

The init command should scaffold a CLAUDE.md file with:
- Project overview (detected or prompted)
- Tech stack (detected from pyproject.toml, package.json, etc.)
- Development commands
- Conventions and standards
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 specify init creates root CLAUDE.md file
- [ ] #2 CLAUDE.md includes project overview section
- [ ] #3 Tech stack auto-detected from project files where possible
- [ ] #4 Development commands section populated based on detected tooling
- [ ] #5 @import statements for memory/*.md files included
- [ ] #6 Template allows customization via prompts or flags
<!-- AC:END -->
