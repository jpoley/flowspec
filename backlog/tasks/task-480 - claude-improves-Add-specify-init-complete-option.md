---
id: task-480
title: 'claude-improves: Add specify init --complete option'
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-12 01:15'
updated_date: '2025-12-15 01:49'
labels:
  - claude-improves
  - cli
  - specify-init
  - feature
  - phase-2
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Current `specify init` deploys ~60% of available features. Need a --complete flag that enables all features:
- All skills deployed
- All hooks enabled
- Full CI/CD template
- Complete VSCode configuration
- MCP configuration

This provides a "batteries included" experience for users who want full functionality.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 --complete flag enables all optional features
- [ ] #2 Skills deployed to .claude/skills/
- [ ] #3 All hooks enabled in hooks.yaml
- [ ] #4 Full CI/CD template with lint, test, security jobs
- [ ] #5 Complete VSCode settings and extensions
- [ ] #6 MCP configuration created
- [ ] #7 Documentation explains --complete vs default behavior
<!-- AC:END -->
