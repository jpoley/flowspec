---
id: task-033
title: Implement GitHub Issue Field Mapping
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - implementation
  - provider
  - github
  - US-1
  - US-2
  - P1
  - satellite-mode
dependencies:
  - task-031
---

## Description

Map GitHub issue fields to task schema.

## Phase

Phase 4: Implementation - Providers

## User Stories

- US-1: Pull remote task by ID
- US-2: Sync assigned tasks

## Acceptance Criteria

- [ ] Title, body, state, assignee, labels
- [ ] Milestone mapping
- [ ] Project (beta) support
- [ ] Custom field handling (if available)
- [ ] Bidirectional mapping (task → issue)

## Deliverables

- Field mapping logic in provider
- Configuration schema in config.yml
- Unit tests for all field types

## Parallelizable

[P] with task-032
