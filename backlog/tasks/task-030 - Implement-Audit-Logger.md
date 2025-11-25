---
id: task-030
title: Implement Audit Logger
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - implementation
  - core
  - compliance
  - P0
  - satellite-mode
dependencies:
  - task-023
---

## Description

Implement structured audit logging for compliance.

## Phase

Phase 3: Implementation - Core

## Acceptance Criteria

- [ ] Structured logging with `structlog`
- [ ] JSON format for parsing
- [ ] Human-readable markdown format
- [ ] Log rotation (max 100MB)
- [ ] Audit log query API
- [ ] SLSA attestation format

## Deliverables

- `src/backlog_md/infrastructure/audit_logger.py` - Implementation
- Unit tests
- `docs/compliance/audit-log-format.md` - Schema doc

## Parallelizable

[P] with task-029
