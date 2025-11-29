---
id: task-137
title: Add Pipecat voice dependencies to pyproject.toml
status: To Do
assignee:
  - '@pm-planner'
created_date: '2025-11-28'
labels:
  - implement
  - voice
  - setup
  - phase1
dependencies: []
priority: high
---

## Description

Add pipecat-ai with optional extras [daily,deepgram,openai,cartesia] as an optional dependency group named 'voice'. Reference: docs/research/pipecat-voice-integration-summary.md Section 1.2 Dependencies

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 pyproject.toml contains [project.optional-dependencies] voice = ["pipecat-ai[daily,deepgram,openai,cartesia]>=0.0.50"]
- [ ] #2 Command `uv sync --extra voice` completes without dependency resolution errors
- [ ] #3 Command `python -c "import pipecat"` executes without ImportError
- [ ] #4 pipecat version in uv.lock matches constraint (>=0.0.50)
<!-- AC:END -->
