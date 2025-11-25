---
id: task-021
title: Design Conflict Resolution Strategies
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - design
  - architecture
  - US-2
  - P1
  - satellite-mode
dependencies:
  - task-020
---

## Description

Design strategy pattern for pluggable conflict resolution.

## Phase

Phase 2: Design

## User Stories

- US-2: Sync assigned tasks

## Acceptance Criteria

- [ ] LocalWinsStrategy
- [ ] RemoteWinsStrategy
- [ ] PromptStrategy
- [ ] SmartMergeStrategy
- [ ] Configuration options in config.yml

## Deliverables

- `src/backlog_md/domain/conflict_strategy.py` - Strategy interface
- `docs/architecture/conflict-resolution.md` - Design doc

## Parallelizable

[P] with task-020
