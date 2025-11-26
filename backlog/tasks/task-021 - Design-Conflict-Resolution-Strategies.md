---
id: task-021
title: Design Conflict Resolution Strategies
status: Done
assignee:
  - '@claude'
created_date: '2025-11-24'
updated_date: '2025-11-26 02:42'
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

<!-- SECTION:DESCRIPTION:BEGIN -->
Design strategy pattern for pluggable conflict resolution.

## Phase

Phase 2: Design

## User Stories

- US-2: Sync assigned tasks
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 LocalWinsStrategy
- [x] #2 RemoteWinsStrategy
- [x] #3 PromptStrategy
- [x] #4 SmartMergeStrategy
- [x] #5 Configuration options in config.yml

## Deliverables

- `src/backlog_md/domain/conflict_strategy.py` - Strategy interface
- `docs/architecture/conflict-resolution.md` - Design doc

## Parallelizable

[P] with task-020
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Conflict Resolution Design Complete

Full docs: `backlog/docs/satellite-mode-conflict-resolution.md`

### Strategies Implemented
1. **LocalWinsStrategy**: Always prefer local, simple and fast
2. **RemoteWinsStrategy**: Always prefer remote, for SoT workflows
3. **PromptStrategy**: Interactive resolution with batch mode
4. **SmartMergeStrategy**: Auto-merge with type-aware logic

### Smart Merge Logic
- Text: Three-way merge or conflict markers
- Lists: Union (labels, ACs)
- Scalar: Newest timestamp wins

### Configuration
- Default strategy in config.yml
- Per-provider overrides
- Per-field overrides
- Smart merge tuning options
<!-- SECTION:NOTES:END -->
