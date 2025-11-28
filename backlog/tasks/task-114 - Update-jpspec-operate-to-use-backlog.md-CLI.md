---
id: task-114
title: 'Update /jpspec:operate to use backlog.md CLI'
status: In Progress
assignee:
  - '@operate-agent'
created_date: '2025-11-28 16:56'
updated_date: '2025-11-28 20:15'
labels:
  - jpspec
  - backlog-integration
  - operate
  - P1
dependencies:
  - task-107
  - task-108
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify the operate.md command to integrate backlog.md task management. SRE agent must create and manage operational tasks for CI/CD, Kubernetes, DevSecOps, and observability work.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 SRE agent receives shared backlog instructions from _backlog-instructions.md
- [ ] #2 Agent creates operational tasks in backlog (deployment, monitoring, alerts)
- [ ] #3 Agent tracks infrastructure changes as tasks with clear ACs
- [ ] #4 Agent updates task status as operations complete
- [ ] #5 Runbook creation tasks added to backlog when alerts are defined
- [ ] #6 Test: Run /jpspec:operate and verify operational tasks created
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read and analyze current operate.md structure
2. Integrate _backlog-instructions.md into SRE agent prompt
3. Add operational task creation patterns (deployment, monitoring, alerts)
4. Add infrastructure change tracking guidance
5. Add runbook task creation when alerts are defined
6. Create comprehensive tests in test_jpspec_operate_backlog.py
7. Run tests and verify all pass
8. Run linting and formatting checks
<!-- SECTION:PLAN:END -->
