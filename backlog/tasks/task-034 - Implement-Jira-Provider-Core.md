---
id: task-034
title: Implement Jira Provider Core
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - implementation
  - provider
  - jira
  - US-1
  - US-4
  - P0
  - satellite-mode
dependencies:
  - task-024
  - task-025
---

## Description

Implement `JiraProvider` class with basic operations.

## Phase

Phase 4: Implementation - Providers

## User Stories

- US-1: Pull remote task by ID
- US-4: Compliance mode

## Acceptance Criteria

- [ ] Implement all `RemoteProvider` methods
- [ ] Use `jira-python` library
- [ ] API token auth
- [ ] OAuth support (future enhancement)
- [ ] JQL query support
- [ ] Pagination handling

## Deliverables

- `src/backlog_md/infrastructure/jira_provider.py` - Implementation
- Unit tests with mock API
- Integration tests with Jira test instance

## Parallelizable

No

## Estimated Time

2 weeks
