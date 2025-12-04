---
id: task-218
title: Write Comprehensive Security Commands Documentation
status: To Do
assignee:
  - '@muckross'
created_date: '2025-12-03 01:58'
updated_date: '2025-12-04 16:51'
labels:
  - 'workflow:Planned'
  - security
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create user documentation, command reference, CI/CD integration guides, and security best practices.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Security Quickstart Guide (docs/guides/security-quickstart.md)
- [ ] #2 Command Reference (docs/reference/jpspec-security-commands.md)
- [ ] #3 CI/CD Integration Examples (GitHub Actions, GitLab, Jenkins)
- [ ] #4 Threat Model and Limitations documentation
- [ ] #5 Privacy Policy for AI data usage
- [ ] #6 Custom Rule Writing Guide
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## CORRECTED Implementation Plan

**CRITICAL: Documentation only, no code.**

### Phase 1: Quick Start Guide
- Create `docs/guides/security-quickstart.md`
  - Installation and setup
  - First scan: `/jpspec:security scan`
  - First triage: `/jpspec:security triage`
  - First fix: `/jpspec:security fix`
  - Configuration basics

### Phase 2: Detailed Guides
- Create `docs/guides/security-triage.md`
  - How triage works (skill-based)
  - Persona selection
  - Interpreting results
- Create `docs/guides/security-fix-generation.md`
  - How fix generation works
  - Reviewing patches
  - Applying fixes safely
- Create `docs/guides/security-configuration.md`
  - config.yaml reference
  - Custom rules
  - Policy as code

### Phase 3: Command Reference
- Create `docs/reference/security-commands.md`
  - `/jpspec:security scan` - Full reference
  - `/jpspec:security triage` - Full reference
  - `/jpspec:security fix` - Full reference
  - `/jpspec:security report` - Full reference
  - `/jpspec:security` - Orchestrator reference

### Phase 4: Architecture Documentation
- Create `docs/architecture/security-skills-architecture.md`
  - Explain skill-based design
  - Why no API keys
  - How AI coding tools execute skills
  - Data flow diagrams

### Success Criteria
- [ ] Quick start guide complete
- [ ] Detailed guides for each command
- [ ] Command reference complete
- [ ] Architecture explained clearly
- [ ] **ZERO CODE, documentation only**

### Files Created
- `docs/guides/security-quickstart.md`
- `docs/guides/security-triage.md`
- `docs/guides/security-fix-generation.md`
- `docs/guides/security-configuration.md`
- `docs/reference/security-commands.md`
- `docs/architecture/security-skills-architecture.md`
<!-- SECTION:PLAN:END -->
