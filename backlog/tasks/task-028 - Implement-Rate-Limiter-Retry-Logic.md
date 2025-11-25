---
id: task-028
title: Implement Rate Limiter & Retry Logic
status: To Do
assignee: []
created_date: '2025-11-24'
labels:
  - implementation
  - core
  - P0
  - satellite-mode
dependencies:
  - task-026
---

## Description

Implement token bucket rate limiter and exponential backoff retry.

## Phase

Phase 3: Implementation - Core

## Acceptance Criteria

- [ ] `RateLimiter` class with token bucket algorithm
- [ ] Exponential backoff using `tenacity` library
- [ ] Configurable limits per provider
- [ ] Rate limit warnings logged
- [ ] Auto-resume after rate limit reset

## Deliverables

- `src/backlog_md/infrastructure/rate_limiter.py` - Implementation
- Unit tests with time mocking
- Integration tests with real APIs (controlled)

## Parallelizable

[P] with task-027
