---
id: task-481
title: 'claude-improves: Add deployment completeness report to specify init'
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-12 01:15'
updated_date: '2025-12-15 01:49'
labels:
  - claude-improves
  - cli
  - specify-init
  - ux
  - phase-2
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
After running `specify init`, users have no visibility into what was deployed vs what's available.

Init should output a completeness report showing:
- What was deployed
- What was skipped (and why)
- What optional features are available
- Suggestions for enabling more features
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Init outputs summary table of deployed components
- [ ] #2 Shows skills: deployed vs available
- [ ] #3 Shows hooks: enabled vs disabled
- [ ] #4 Shows templates: created vs skipped
- [ ] #5 Provides suggestions for --complete or individual flags
- [ ] #6 Summary includes next steps for user
- [ ] #7 Add --quiet flag to suppress report
<!-- AC:END -->
