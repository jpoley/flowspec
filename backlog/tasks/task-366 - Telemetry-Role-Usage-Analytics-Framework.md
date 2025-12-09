---
id: task-366
title: 'Telemetry: Role Usage Analytics Framework'
status: To Do
assignee: []
created_date: '2025-12-09 15:14'
labels:
  - infrastructure
  - telemetry
  - analytics
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement privacy-preserving telemetry for role usage patterns and feedback
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 RoleEvent enum with event types (role.selected, agent.invoked, handoff.clicked)
- [ ] #2 track_role_event() function with PII hashing
- [ ] #3 JSONL telemetry file format (.jpspec/telemetry.jsonl)
- [ ] #4 Opt-in telemetry via config (telemetry.enabled)
- [ ] #5 Feedback prompt UI designed
<!-- AC:END -->
