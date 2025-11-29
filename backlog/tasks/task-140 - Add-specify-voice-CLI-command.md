---
id: task-140
title: Add specify voice CLI command
status: To Do
assignee:
  - '@pm-planner'
created_date: '2025-11-28'
labels:
  - implement
  - voice
  - foundational
  - cli
  - phase2
dependencies:
  - task-139
priority: high
---

## Description

Add 'specify voice' subcommand to src/specify_cli/cli.py that loads configuration, validates API keys, and launches voice bot. Initial implementation should validate config and print readiness status. Reference: docs/research/pipecat-voice-integration-summary.md Section 1.3 Initial Tasks

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Command `specify voice --help` displays usage information with --config option
- [ ] #2 Command `specify voice --config path/to/config.json` loads and validates specified config file
- [ ] #3 Missing API keys displays error listing which specific keys are missing
- [ ] #4 Valid configuration displays "Voice assistant ready" status with provider names
- [ ] #5 Exit code 0 on success, exit code 1 on configuration errors
<!-- AC:END -->
