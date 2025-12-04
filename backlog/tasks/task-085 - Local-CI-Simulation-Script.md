---
id: task-085
title: Local CI Simulation Script
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-11-27 21:54'
updated_date: '2025-12-04 16:31'
labels:
  - 'workflow:Specified'
  - cicd
  - inner-loop
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement scripts/bash/run-local-ci.sh to execute full CI pipeline locally using act (GitHub Actions local runner). Catches CI failures before push (inner loop principle). Reduces GitHub Actions costs. Faster feedback (<5 min). CLAUDE.md mentions act but implementation is missing. Note: Requires Docker, some GitHub Actions features don't work (OIDC, etc.).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create scripts/bash/run-local-ci.sh
- [ ] #2 Implement act installation check and auto-install
- [ ] #3 Run lint job via act
- [ ] #4 Run test job via act
- [ ] #5 Run build job via act
- [ ] #6 Run security job via act
- [ ] #7 Document act installation (scripts/bash/install-act.sh)
- [ ] #8 Document act limitations (Docker required, OIDC not supported)
- [x] #9 Test on Linux and macOS
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create scripts/bash/run-local-ci.sh script
2. Implement act installation check with version detection
3. Implement auto-install act (binary download from GitHub)
4. Add Docker daemon check and error handling
5. Implement selective job execution (-j lint -j test)
6. Add --list flag to show available jobs
7. Run lint job via act (ruff check, ruff format, mypy)
8. Run test job via act (pytest with coverage)
9. Run build job via act (uv build, twine check)
10. Run security job via act (Semgrep SAST)
11. Add fail-fast on first error
12. Document act limitations (OIDC, secrets, Docker requirement)
13. Create scripts/bash/install-act.sh helper script
14. Update CLAUDE.md and docs/reference/inner-loop.md
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Specification created: docs/prd/platform-devsecops-prd.md (FR-003, FR-004)
<!-- SECTION:NOTES:END -->
