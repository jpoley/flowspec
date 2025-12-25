---
id: task-563
title: Implement release-agents.yml workflow
status: To Do
assignee: []
created_date: '2025-12-25 20:17'
labels:
  - implementation
  - ci-cd
  - workflow
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create .github/workflows/release-agents.yml with path and version triggers. Implement version extraction, tag creation, packaging, and GitHub release creation steps.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 release-agents.yml workflow created
- [ ] #2 Path-based triggers working (.github/agents/**, claude-code-version.txt)
- [ ] #3 Version extraction from agents-version.json implemented
- [ ] #4 Tag creation with agents/v* format working
- [ ] #5 GitHub release creation functional
<!-- AC:END -->
