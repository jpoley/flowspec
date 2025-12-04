---
id: task-216
title: 'Integrate /jpspec:security with Workflow and Backlog'
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
Wire /jpspec:security commands into jpspec_workflow.yml and add backlog.md task creation for findings.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add optional pre-commit hook integration
- [ ] #2 Implement --create-tasks flag to auto-create backlog tasks for findings
- [ ] #3 Task format includes severity, CWE, location, AI explanation
- [ ] #4 Document workflow integration options (validate extension, dedicated state)
- [ ] #5 CI/CD integration examples (GitHub Actions, GitLab CI)
- [ ] #6 SARIF output for GitHub Code Scanning
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## CORRECTED Implementation Plan

**CRITICAL: Python handles backlog integration, no AI.**

### Phase 1: Workflow Config
- Update `jpspec_workflow.yml`:
  ```yaml
  workflows:
    security:
      command: "/jpspec:security"
      agents: ["security-triage", "security-fixer"]
      input_states: ["In Implementation", "Validated"]
      output_state: "Security Reviewed"
      artifacts:
        - "docs/security/findings.json"
        - "docs/security/triage-results.json"
        - "docs/security/patches/"
  ```

### Phase 2: Backlog Integration (Python)
- Create `src/specify_cli/commands/security_backlog.py`
  - Read triage-results.json
  - For each HIGH/CRITICAL finding:
    - Create task: `backlog task create "Fix: {rule_id} in {file}"`
    - Add acceptance criteria from remediation
    - Tag with `security`, `vulnerability`
  - **NO AI logic, just task creation**

### Phase 3: Slash Command Integration
- Update `.claude/commands/jpspec-security.md`
  - After triage: create backlog tasks
  - After fix: update task status to Done
  - Link tasks to findings by ID

### Phase 4: Status Tracking
- `/jpspec:security` checks current workflow state
- Validates state is valid input (In Implementation or Validated)
- Transitions to Security Reviewed on completion

### Success Criteria
- [ ] Workflow config updated
- [ ] Backlog integration implemented
- [ ] Tasks created for findings
- [ ] State transitions working
- [ ] **ZERO AI LOGIC in integration**

### Files Created
- Updated `jpspec_workflow.yml`
- `src/specify_cli/commands/security_backlog.py`
- Updated `.claude/commands/jpspec-security.md`
<!-- SECTION:PLAN:END -->
