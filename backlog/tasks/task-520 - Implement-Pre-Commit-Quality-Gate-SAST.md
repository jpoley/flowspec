---
id: task-520
title: Implement Pre-Commit Quality Gate - SAST
status: To Do
assignee: []
created_date: '2025-12-14 03:35'
updated_date: '2025-12-14 03:35'
labels:
  - agent-event-system
  - phase-4
  - infrastructure
  - security
  - devsecops
  - cicd
  - git-workflow
dependencies:
  - task-517
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create security scanning gate with bandit and semgrep.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Pre-commit hook calls quality-gates/sast.sh
- [ ] #2 Runs bandit and semgrep
- [ ] #3 Emits security.vulnerability_found events
- [ ] #4 Fail on high/critical findings
- [ ] #5 SARIF output stored in .flowspec/security/sarif
<!-- AC:END -->
