---
id: task-017
title: Design Core Adapter Interface
status: In Progress
assignee:
  - '@claude'
created_date: '2025-11-24'
updated_date: '2025-11-26 02:33'
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
- [ ] #1 Interface supports all user stories (US-1 to US-4)
- [ ] #2 `RemoteTask` entity defined
- [ ] #3 `SyncResult` entity defined
- [ ] #4 Error handling patterns defined
- [ ] #5 Extension points documented

## Deliverables

- `src/backlog_md/domain/remote_provider.py` - Interface definition
- `src/backlog_md/domain/entities.py` - Domain entities
- `docs/architecture/adapter-interface.md` - Interface docs

## Parallelizable

No
<!-- AC:END -->
