---
id: task-365
title: 'CI/CD: Role-Based Validation Workflows'
status: To Do
assignee: []
created_date: '2025-12-09 15:14'
labels:
  - infrastructure
  - ci-cd
  - github-actions
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add GitHub Actions workflows for role-based artifact validation and team role enforcement
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Role-based CI workflow detects changed role artifacts
- [ ] #2 PM validation job checks PRD structure
- [ ] #3 Dev validation job runs tests and ADR checks
- [ ] #4 Sec validation job runs security scanning
- [ ] #5 QA validation job checks test coverage and docs
- [ ] #6 Team role validation prevents .vscode/settings.json commits in team mode
<!-- AC:END -->
