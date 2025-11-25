---
id: task-029
title: Implement Task Schema Migration
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - implementation
  - core
  - data-model
  - P0
  - satellite-mode
dependencies:
  - task-022
---

## Description

Implement task file migration from schema v1 to v2.

## Phase

Phase 3: Implementation - Core

## Acceptance Criteria

- [ ] `TaskMigration` class with migrate() method
- [ ] Backward compatibility check
- [ ] Atomic file updates (backup + write + verify)
- [ ] Bulk migration CLI command
- [ ] Dry-run mode

## Deliverables

- `src/backlog_md/infrastructure/task_migration.py` - Implementation
- Unit tests with sample task files
- `backlog migrate` CLI command

## Parallelizable

[P] with task-030
