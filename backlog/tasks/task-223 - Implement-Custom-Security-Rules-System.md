---
id: task-223
title: Implement Custom Security Rules System
status: To Do
assignee:
  - '@muckross'
created_date: '2025-12-03 02:16'
updated_date: '2025-12-04 16:51'
labels:
  - 'workflow:Planned'
  - security
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Allow users to define custom security rules in .jpspec/security-rules/ directory. Support Semgrep custom rules and pattern definitions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create .jpspec/security-rules/ directory structure
- [ ] #2 Support custom Semgrep rule definitions
- [ ] #3 Load and validate custom rules at scan time
- [ ] #4 Document custom rule creation process
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## CORRECTED Implementation Plan

**CRITICAL: Custom rules = scanner config, not AI logic.**

### Phase 1: Rule Directory Structure
- Create `docs/security/rules/` directory
- Subdirectories:
  - `semgrep/` - Semgrep YAML rules
  - `bandit/` - Bandit config files
  - `custom/` - Project-specific rules

### Phase 2: Rule Loader (Python)
- Create `src/specify_cli/scanners/custom_rules.py`
  - Load rules from `docs/security/rules/`
  - Validate rule syntax
  - Pass to scanners
  - **NO AI logic, just file I/O**

### Phase 3: Rule Templates
- Create example rules:
  - `docs/security/rules/semgrep/django-custom.yaml`
  - `docs/security/rules/semgrep/flask-custom.yaml`
- Document rule creation process

### Phase 4: Integration
- Update scanners to load custom rules
- Custom rules included in findings metadata
- Skills consider custom rules when triaging

### Success Criteria
- [ ] Rule directory structure created
- [ ] Rule loader implemented
- [ ] Example rules provided
- [ ] Scanners use custom rules
- [ ] **ZERO AI LOGIC in rule system**

### Files Created
- `src/specify_cli/scanners/custom_rules.py`
- `docs/security/rules/semgrep/django-custom.yaml`
- `docs/security/rules/semgrep/flask-custom.yaml`
- `docs/guides/custom-rules.md`
<!-- SECTION:PLAN:END -->
