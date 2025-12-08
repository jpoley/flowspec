---
id: task-316
title: Rename CLI command from 'specify' to 'specflow'
status: In Progress
assignee: []
created_date: '2025-12-08 22:10'
updated_date: '2025-12-08 22:52'
labels:
  - architecture
  - breaking-change
  - epic
  - 'workflow:In Implementation'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Strategic CLI rename to establish clear branding identity for JP Spec Kit. This is a coordinated multi-phase change affecting package naming, entry points, documentation, and CI/CD infrastructure.

**Scope Summary:**
- 600+ references across the codebase
- 236+ Python import references to specify_cli
- 375+ documentation references
- 6 GitHub Actions workflows
- 13+ shell scripts
- PyPI package distribution

**Recommended Approach:** Phased dual-support strategy with 6-month deprecation timeline.

**Key Architectural Decisions:**
1. External rename only (CLI: specflow, PyPI: specflow-cli)
2. Preserve internal specify_cli package name to avoid breaking 236+ imports
3. Dual command support during transition
4. Major version bump to 1.0.0
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 PyPI package specflow-cli is published and installable
- [x] #2 specflow command works with all existing subcommands
- [x] #3 specify command shows deprecation warning (during transition period)
- [ ] #4 All CI/CD workflows pass with new command name
- [x] #5 All documentation updated to reference specflow
- [x] #6 Migration guide created for existing users
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Phases

### Phase 0: Preparation (Prerequisite)
- [ ] task-323: Reserve specflow-cli package name on PyPI
- [ ] Validate PyPI name availability
- [ ] Configure trusted publishing

### Phase 1: Core Rename (Week 1-2)
- [ ] task-317: Update pyproject.toml for specflow CLI rename
- [ ] task-318: Implement deprecation warning for specify command
- [ ] Run all tests locally

### Phase 2: CI/CD & Scripts (Week 2)
- [ ] task-319: Update GitHub Actions workflows for specflow command
- [ ] task-320: Update shell scripts for specflow CLI rename
- [ ] Test PyPI upload (test.pypi.org)

### Phase 3: Documentation (Week 3)
- [ ] task-321: Update documentation for specflow CLI rename
- [ ] task-322: Create migration guide for specify to specflow transition
- [ ] Archive old documentation

### Phase 4: Release (Week 4)
- [ ] task-324: Publish specflow-cli 1.0.0 to PyPI
- [ ] Validate installation from PyPI
- [ ] Monitor for issues (24-48 hours)

### Phase 5: Post-Release
- [ ] task-325: Deprecate specify-cli package on PyPI
- [ ] Announce migration complete
- [ ] Schedule specify alias removal (version 2.0.0)

## Key Architectural Decisions

### ADR-001: Package Naming Strategy
**Decision:** External rename only
- CLI: specify → specflow (primary), specify (deprecated alias)
- PyPI: specify-cli → specflow-cli
- Internal: specify_cli (UNCHANGED)

**Rationale:** Preserves 236+ internal imports while achieving branding goals.

### ADR-002: Import Path Strategy
**Decision:** Preserve internal package name (specify_cli)
- No breaking changes to Python imports
- Zero risk to existing tests
- Mismatch acceptable (implementation detail)

### ADR-003: User Migration Path
**Decision:** 6-month dual support period
- Phase 1 (0-2mo): Both commands work, no warnings
- Phase 2 (2-4mo): specify shows deprecation warning
- Phase 3 (4-6mo): specify fails with migration guide
- Phase 4 (6mo+): specify removed

## Risk Register
| Risk | Impact | Mitigation |
|------|--------|------------|
| PyPI name unavailable | HIGH | Reserve name FIRST (task-323) |
| Breaking user scripts | HIGH | Dual support + migration tooling |
| CI/CD failures | MEDIUM | Test on feature branch first |
| Documentation outdated | MEDIUM | Automated + manual updates |

## Estimated Effort
- Total: ~56 hours
- Timeline: 4 weeks (development) + 6 months (deprecation)
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Phase 1 Implementation Complete (2025-12-08)

### Completed Tasks:
- task-317: pyproject.toml updated ✓
- task-318: Deprecation warning implemented ✓

### Verification:
- specflow --version → works (AC #2 ✓)
- specify --version → shows deprecation warning (AC #3 ✓)
- All 2770 tests pass
- Build produces correctly named artifacts

### Remaining Tasks:
- task-319: Update GitHub Actions workflows
- task-320: Update shell scripts
- task-321: Update documentation
- task-322: Create migration guide
- task-323: Reserve PyPI name (manual step)
- task-324: Publish to PyPI
- task-325: Deprecate old package

## Phase 1-3 Implementation Complete (2025-12-08)

### All Completed Tasks:
- task-317: pyproject.toml updated ✓
- task-318: Deprecation warning implemented ✓
- task-319: GitHub Actions workflows updated ✓
- task-320: Shell scripts updated ✓
- task-321: Documentation updated ✓
- task-322: Migration guide created ✓

### Final Verification:
- All 2770 tests pass
- Lint checks pass
- specflow --version works
- specify --version shows deprecation warning
- Build produces correctly named artifacts

### Pending Tasks (Post-Merge):
- task-323: Reserve PyPI name (manual step)
- task-324: Publish to PyPI
- task-325: Deprecate old package

## Validation Complete (2025-12-08)

### Validation Results:
- **Phase 1 (Automated Tests)**: All 2770 tests pass, lint clean, formatting correct
- **Phase 2 (QA Guardian)**: Migration validated, all functionality working
- **Phase 2 (Security Engineer)**: No critical vulnerabilities, APPROVED for release
- **Phase 3 (Documentation)**: Migration guide and docs updated
- **Phase 4 (AC Verification)**: 4/6 ACs verified (2 pending post-merge)

### AC Status:
- [x] #2 specflow command works with all existing subcommands
- [x] #3 specify command shows deprecation warning
- [x] #5 All documentation updated to reference specflow
- [x] #6 Migration guide created for existing users
- [ ] #1 PyPI package (post-merge: task-324)
- [ ] #4 CI/CD workflows pass (requires CI run after merge)

### Files Changed (16 files):
1. pyproject.toml - Package name, version 1.0.0, dual entry points
2. src/specify_cli/__init__.py - Version, deprecation function
3. .github/workflows/dev-setup-validation.yml
4. .github/workflows/security-scan.yml
5. .github/workflows/security-parallel.yml
6. scripts/bash/install-specify-latest.sh
7. scripts/bash/pre-commit-dev-setup.sh
8. scripts/bash/migrate-commands-to-subdirs.sh
9. scripts/bash/run-local-ci.sh
10. scripts/hooks/pre-push
11. scripts/powershell/install-specify-latest.ps1
12. scripts/powershell/run-local-ci.ps1
13. scripts/CLAUDE.md
14. CLAUDE.md
15. README.md
16. docs/guides/migration-to-specflow.md (NEW)

### Ready for PR to branch: specflow-galway
<!-- SECTION:NOTES:END -->
