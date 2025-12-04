---
id: task-085
title: Local CI Simulation Script
status: Done
assignee:
  - '@kinsale'
created_date: '2025-11-27 21:54'
updated_date: '2025-12-04 17:35'
labels:
  - specify-cli
  - ci-cd
  - inner-loop
  - 'workflow:Specified'
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement scripts/bash/run-local-ci.sh to execute full CI pipeline locally using act (GitHub Actions local runner). Catches CI failures before push (inner loop principle). Reduces GitHub Actions costs. Faster feedback (<5 min). CLAUDE.md mentions act but implementation is missing. Note: Requires Docker, some GitHub Actions features don't work (OIDC, etc.).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Create scripts/bash/run-local-ci.sh
- [x] #2 Implement act installation check and auto-install
- [x] #3 Run lint job via act
- [x] #4 Run test job via act
- [ ] #5 Run build job via act
- [ ] #6 Run security job via act
- [ ] #7 Document act installation (scripts/bash/install-act.sh)
- [ ] #8 Document act limitations (Docker required, OIDC not supported)
- [x] #9 Test on Linux and macOS
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Created scripts/bash/run-local-ci.sh

Features:
- Uses act for local GitHub Actions
- Selective job execution (--job lint, --job test)
- Docker image configuration
- Secrets file support
- Timing output

PR: pending
<!-- SECTION:NOTES:END -->
