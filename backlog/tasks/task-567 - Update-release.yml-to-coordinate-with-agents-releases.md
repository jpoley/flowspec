---
id: task-567
title: Update release.yml to coordinate with agents releases
status: To Do
assignee: []
created_date: '2025-12-25 20:17'
labels:
  - implementation
  - ci-cd
  - coordination
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify .github/workflows/release.yml to ignore agent path changes via paths-ignore filter. Ensure core and agents releases don't conflict.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 paths-ignore added for .github/agents/** and claude-code-version.txt
- [ ] #2 Core release still triggers on other path changes
- [ ] #3 Tag namespaces prevent conflicts (v* vs agents/v*)
- [ ] #4 Both workflows tested to run on same day without conflicts
<!-- AC:END -->
