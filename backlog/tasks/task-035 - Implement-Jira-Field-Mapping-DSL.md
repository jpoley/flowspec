---
id: task-035
title: Implement Jira Field Mapping DSL
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - implementation
  - provider
  - jira
  - US-1
  - P0
  - satellite-mode
dependencies:
  - task-034
---

## Description

Implement configurable field mapping for Jira custom fields.

## Phase

Phase 4: Implementation - Providers

## User Stories

- US-1: Pull remote task by ID

## Acceptance Criteria

- [ ] Map standard fields (summary, description, status, assignee)
- [ ] Map custom fields by customfield_* IDs
- [ ] Support story points, epic link, sprint
- [ ] Field type validation
- [ ] Error handling for missing fields

## Deliverables

- Field mapping engine in provider
- Configuration schema in config.yml
- Sample configs for common Jira setups
- Unit tests for mapping logic

## Parallelizable

[P] with task-036
