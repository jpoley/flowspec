---
id: task-68
title: Enable flowspec to dogfood itself without circular dependency
status: Done
assignee:
  - '@claude'
created_date: '2025-11-25 21:57'
updated_date: '2025-11-25 23:00'
labels:
  - P0
  - dogfooding
  - developer-experience
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Allow flowspec to use its own /speckit.* and /flowspec:* commands during development without running specify init on itself (which would clobber source files). This enables true dogfooding of the spec-driven workflow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Create .flowspec-source marker file at repo root to identify this as the source repository
- [x] #2 Update specify init to detect .flowspec-source and skip/warn instead of clobbering
- [x] #3 Create .claude/commands/speckit/ directory with symlinks to templates/commands/*.md files
- [x] #4 Verify all /speckit.* commands work in flowspec repo (analyze, checklist, clarify, constitution, implement, plan, specify, tasks)
- [x] #5 Verify all /flowspec:* commands still work (implement, operate, plan, research, specify, validate)
- [ ] #6 Add specify dogfood command as alternative to manually creating symlinks (optional convenience)
- [x] #7 Document dogfooding setup in CONTRIBUTING.md with platform-specific notes (Windows symlink requirements)
- [x] #8 Test that specify upgrade also respects the .flowspec-source marker
- [x] #9 Ensure symlinks are tracked in git (verify .gitattributes if needed)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented via PR #6 (merged):
- Added .flowspec-source marker file for source repo detection
- Updated specify init/upgrade to respect marker
- Created symlinks in .claude/commands/speckit/ pointing to templates/commands/
- Documented in CONTRIBUTING.md

AC #6 (specify dogfood command) deferred as optional convenience feature.
<!-- SECTION:NOTES:END -->
