---
id: task-036
title: Implement Jira Status Transition Mapping
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - implementation
  - provider
  - jira
  - US-2
  - US-4
  - P0
  - satellite-mode
dependencies:
  - task-034
---

## Description

Map local task status to Jira workflow transitions.

## Phase

Phase 4: Implementation - Providers

## User Stories

- US-2: Sync assigned tasks
- US-4: Compliance mode

## Acceptance Criteria

- [ ] Configurable status mapping (local → Jira)
- [ ] Workflow-aware transitions (validate allowed)
- [ ] Handle custom workflows
- [ ] Resolution field handling
- [ ] Comment on transition (optional)

## Deliverables

- Status mapping logic in provider
- Configuration schema
- Sample configs for common workflows
- Unit tests

## Parallelizable

[P] with task-035
