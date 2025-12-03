---
id: task-274
title: Replace source repo commands with symlinks
status: To Do
assignee: []
created_date: '2025-12-03 14:01'
labels:
  - architecture
  - migration
  - implementation
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Delete direct files in .claude/commands/ and replace with symlinks created by dogfood
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Backup current .claude/commands/jpspec/ files (git commit before deletion)
- [ ] #2 Delete all .claude/commands/jpspec/*.md files
- [ ] #3 Run specify dogfood --force to create symlinks
- [ ] #4 Verify all .claude/commands/**/*.md are symlinks (none are regular files)
- [ ] #5 Test Claude Code reads commands via symlinks successfully
- [ ] #6 Commit symlink replacement to git
<!-- AC:END -->
