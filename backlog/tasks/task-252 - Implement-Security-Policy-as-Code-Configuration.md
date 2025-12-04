---
id: task-252
title: Implement Security Policy as Code Configuration
status: To Do
assignee:
  - '@muckross'
created_date: '2025-12-03 02:26'
updated_date: '2025-12-04 16:51'
labels:
  - 'workflow:Planned'
  - security
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build .jpspec/security-policy.yml parser and enforcement engine. Support severity-based gates, tool configuration, compliance mappings, and finding exemptions with expiration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Define YAML schema for security policy configuration (gates, tools, triage, reporting, exemptions)
- [ ] #2 Implement policy parser and validator with clear error messages
- [ ] #3 Add policy enforcement in scan/triage/fix commands
- [ ] #4 Support exemptions (paths, specific findings with justification and expiration)
- [ ] #5 Create default policy template with OWASP Top 10 compliance
- [ ] #6 Test policy enforcement with multiple test cases
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## CORRECTED Implementation Plan

**CRITICAL: Policy = configuration, not AI logic.**

### Phase 1: Policy Schema
- Create `docs/security/policies/` directory
- Define policy YAML format:
  ```yaml
  policies:
    severity_thresholds:
      block: "critical"
      warn: "high"
    ignore_patterns:
      - "test/**"
      - "docs/**"
    require_fix_for:
      - "sql-injection"
      - "xss"
  ```

### Phase 2: Policy Engine (Python)
- Create `src/specify_cli/config/policy_engine.py`
  - Load policies from `docs/security/policies/`
  - Evaluate findings against policies
  - Mark findings as blocked/warned/allowed
  - **NO AI logic, just rule evaluation**

### Phase 3: Policy Templates
- Create default policies:
  - `docs/security/policies/strict.yaml`
  - `docs/security/policies/permissive.yaml`
  - `docs/security/policies/compliance.yaml`

### Phase 4: Integration
- Policy engine filters findings before triage
- Skills receive policy context
- Reports include policy compliance status

### Success Criteria
- [ ] Policy schema defined
- [ ] Policy engine implemented
- [ ] Default policies provided
- [ ] Integration with scanners and skills
- [ ] **ZERO AI LOGIC in policy system**

### Files Created
- `src/specify_cli/config/policy_engine.py`
- `docs/security/policies/strict.yaml`
- `docs/security/policies/permissive.yaml`
- `docs/security/policies/compliance.yaml`
<!-- SECTION:PLAN:END -->
