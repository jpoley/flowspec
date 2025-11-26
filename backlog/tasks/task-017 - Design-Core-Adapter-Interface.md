---
id: task-017
title: Design Core Adapter Interface
status: Done
assignee:
  - '@claude'
created_date: '2025-11-24'
updated_date: '2025-11-26 02:35'
labels:
  - design
  - architecture
  - P0
  - satellite-mode
dependencies:
  - task-016
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Design `RemoteProvider` interface and domain entities.

## Phase

Phase 2: Design
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Interface supports all user stories (US-1 to US-4)
- [x] #2 `RemoteTask` entity defined
- [x] #3 `SyncResult` entity defined
- [x] #4 Error handling patterns defined
- [x] #5 Extension points documented

## Deliverables

- `src/backlog_md/domain/remote_provider.py` - Interface definition
- `src/backlog_md/domain/entities.py` - Domain entities
- `docs/architecture/adapter-interface.md` - Interface docs

## Parallelizable

No
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Review user stories US-1 through US-4 requirements
2. Design RemoteProvider abstract interface
3. Define RemoteTask dataclass with all required fields
4. Define SyncResult dataclass for operation outcomes
5. Design error hierarchy and handling patterns
6. Document extension points for custom providers
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Core Adapter Interface Design Complete

Full documentation: `backlog/docs/satellite-mode-core-adapter-design.md`

### AC#1: Interface Supports All User Stories
- US-1 (Pull): `get_task()` method
- US-2 (Sync): `list_tasks()`, `update_task()`, `create_task()`
- US-3 (PR): `create_pull_request()`, `link_pr_to_task()`
- US-4 (Compliance): `get_task_history()`, `to_audit_log()`

### AC#2: RemoteTask Entity
Comprehensive dataclass with:
- Identity: id, provider, url
- Core: title, description, status
- Assignment: assignee, reporter
- Classification: labels, priority, task_type
- Hierarchy: parent_id, subtask_ids
- Timestamps: created_at, updated_at, due_date
- Sync: etag, version, extra_fields

### AC#3: SyncResult Entity
Captures:
- Operation metadata (id, timestamp, direction)
- Per-task operations with SyncOperation enum
- Summary counts (created, updated, conflicts, failed)
- Audit log generation

### AC#4: Error Handling Patterns
Hierarchy:
- SatelliteError (base)
- Auth: AuthenticationError, TokenExpiredError
- Resource: TaskNotFoundError, PermissionDeniedError
- Sync: ConflictError, SyncError
- Provider: RateLimitError, ProviderUnavailableError
- Validation: ValidationError

### AC#5: Extension Points
- ProviderRegistry: Register custom providers
- FieldMapper: Custom field transformations
- ConflictResolver: Pluggable conflict strategies
- AuditLogger: Custom audit backends
<!-- SECTION:NOTES:END -->
