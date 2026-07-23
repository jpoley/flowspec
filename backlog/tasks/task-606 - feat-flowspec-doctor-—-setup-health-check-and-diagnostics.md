---
id: TASK-606
title: 'feat: flowspec doctor — setup health check and diagnostics'
status: Done
assignee:
  - '@jpoley'
created_date: '2026-05-23 09:09'
updated_date: '2026-05-23 09:25'
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
- [x] #1 Running 'flowspec doctor' runs all health checks and prints pass/warn/fail status for each
- [x] #2 Checks: Python version, flowspec version vs latest, backlog.md installed, beads installed, flowspec_workflow.yml present+valid, .github/agents naming convention, memory/constitution.md present
- [x] #3 Output uses rich formatting with ✅/⚠️/❌ symbols per check with actionable fix message
- [x] #4 'flowspec doctor --fix' attempts auto-fix where possible (agent naming, constitution)
- [x] #5 Unit tests cover each check function with pass and fail cases
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented flowspec doctor command.

- New module: src/flowspec_cli/doctor/ (checks.py, cli.py, __init__.py)
- 8 health checks: Python version, flowspec version vs latest, backlog.md, beads, flowspec_workflow.yml, agent naming convention, constitution.md, .flowspec/ dir
- Rich table output with ✅/⚠️/❌ per check and actionable fix hints
- --fix flag auto-creates constitution.md and runs upgrade-repo for agent naming
- 23 unit tests, all passing; full suite 3496 passed
- Registered as top-level app.command("doctor") in __init__.py
<!-- SECTION:NOTES:END -->
