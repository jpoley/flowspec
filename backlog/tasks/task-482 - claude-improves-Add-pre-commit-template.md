---
id: task-482
title: "claude-improves: Add pre-commit configuration template"
status: To Do
assignee: []
created_date: '2025-12-12 01:15'
labels:
  - claude-improves
  - templates
  - pre-commit
  - quality
  - phase-2
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
No .pre-commit-config.yaml is created during init. Pre-commit hooks are essential for code quality enforcement.

Should provide template with common hooks based on project type.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .pre-commit-config.yaml template created
- [ ] #2 Python projects get: ruff, ruff-format, mypy, bandit
- [ ] #3 Node projects get: prettier, eslint, tsc
- [ ] #4 All projects get: trailing-whitespace, end-of-file-fixer, check-yaml
- [ ] #5 Template includes commented-out advanced hooks
- [ ] #6 Documentation explains how to enable/customize
<!-- AC:END -->
