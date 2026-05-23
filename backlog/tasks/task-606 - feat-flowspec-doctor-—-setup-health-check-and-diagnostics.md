---
id: TASK-606
title: 'feat: flowspec doctor — setup health check and diagnostics'
status: In Progress
assignee:
  - '@jpoley'
created_date: '2026-05-23 09:09'
updated_date: '2026-05-23 09:09'
labels:
  - feature
  - ux
  - cli
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add 'flowspec doctor' CLI command that checks the environment and surfaces problems before they cause confusing failures. Implements all checks from GitHub issue #1221.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Running 'flowspec doctor' runs all health checks and prints pass/warn/fail status for each
- [ ] #2 Checks: Python version, flowspec version vs latest, backlog.md installed, beads installed, flowspec_workflow.yml present+valid, .github/agents naming convention, memory/constitution.md present
- [ ] #3 Output uses rich formatting with ✅/⚠️/❌ symbols per check with actionable fix message
- [ ] #4 'flowspec doctor --fix' attempts auto-fix where possible (agent naming, constitution)
- [ ] #5 Unit tests cover each check function with pass and fail cases
<!-- AC:END -->
