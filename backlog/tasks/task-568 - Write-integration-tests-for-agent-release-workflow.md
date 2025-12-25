---
id: task-568
title: Write integration tests for agent release workflow
status: To Do
assignee: []
created_date: '2025-12-25 20:17'
labels:
  - testing
  - ci-cd
  - agents
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create test suite for release-agents.yml workflow. Test path triggers, version triggers, manual triggers. Validate tag creation, packaging, and release notes generation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Test path-based trigger (agent file change)
- [ ] #2 Test version-based trigger (claude-code-version.txt change)
- [ ] #3 Test manual trigger (workflow_dispatch)
- [ ] #4 Test tag creation validation
- [ ] #5 Test package contents validation
- [ ] #6 All tests pass in CI
<!-- AC:END -->
