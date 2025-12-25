---
id: task-556
title: Implement separate flowspec-agents release process
status: To Do
assignee: []
created_date: '2025-12-25 20:11'
updated_date: '2025-12-25 20:26'
labels:
  - design
  - ci-cd
  - agents
  - 'workflow:Specified'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create independent release workflow for flowspec-agents that triggers on:
1. Agent file changes in .github/agents/
2. Claude Code version updates (tracked)
3. Manual workflow_dispatch

Design decision (assessed): Conditional CI in same repo with independent versioning.

Context:
- Agents need to release more frequently than flowspec core
- Current: agents synced via sync-copilot-agents.sh from templates
- Current: 49 agent files in .github/agents/
- Current: validate-agent-sync.yml handles drift detection/auto-fix
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Design separate release workflow trigger logic
- [ ] #2 Implement Claude Code version tracking mechanism
- [ ] #3 Create flowspec-agents packaging and versioning
- [ ] #4 Update existing CI to coordinate with agents release
- [ ] #5 Document release process and version tracking
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Design workflow trigger strategy (path-based + version-based)
2. Implement version tracking for Claude Code
3. Create release-agents.yml workflow
4. Add agent packaging/versioning logic
5. Coordinate with existing release.yml
6. Document tracking and release process
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
PRD created: docs/prd/flowspec-agents-release-spec.md (2000 lines, sections 1-10 complete)

Implementation tasks created:
- Design: task-557, task-558, task-559, task-560
- Implementation: task-561, task-562, task-563, task-564, task-565, task-566, task-567
- Testing/Docs: task-568, task-569
- Future: task-570, task-571

Total: 15 tasks, 40-52 hours estimated, 4-week delivery timeline
<!-- SECTION:NOTES:END -->
