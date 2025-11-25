---
id: task-019
title: Design Secret Management
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - design
  - security
  - P0
  - satellite-mode
dependencies:
  - task-017
---

## Description

Design secure credential storage using system keychain and env vars.

## Phase

Phase 2: Design

## Acceptance Criteria

- [ ] Multi-platform keychain support (macOS, Linux, Windows)
- [ ] Environment variable fallback
- [ ] CLI auth integration (gh, jira)
- [ ] Interactive prompt for missing tokens
- [ ] Never store secrets in config files

## Deliverables

- `src/backlog_md/infrastructure/secret_manager.py` - Secret manager class
- `docs/architecture/secret-management.md` - Design doc

## Parallelizable

[P] with task-018
