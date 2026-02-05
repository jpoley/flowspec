---
description: Validate implementation with tests, QA, security, and AC verification
loop: both
---

# /flow:validate

Orchestrate validation workflow: tests → QA → security → docs → AC verification → PR.

## User Input

```
$ARGUMENTS
```

- Optional `task-id`: Specific task to validate
- If omitted: Auto-discover single "In Progress" task

## Prerequisites

- Task in "In Progress" status (or use `--skip-state-check`)
- Implementation complete

## Outputs

- **Artifact:** `docs/qa/{task-id}-validation-report.md`
- **Decision Log:** `.flowspec/logs/decisions/{date}-validate.jsonl`
- **Backlog Update:** ACs checked, task marked Done

---

## Workflow

**Philosophy: Collect ALL issues, report once, fix in one pass.** No early halts except for blocking prerequisites (no task found).

### Phase 0: Task Discovery

1. If `$ARGUMENTS` provided, use as task ID
2. Otherwise: `backlog task list -s "In Progress" --plain`
3. If multiple in-progress: ask user to pick
4. If none: **STOP** (can't proceed without a task)

Load task details:
```bash
backlog task {task-id} --plain
```

Extract: task ID, title, acceptance criteria, status.

**Initialize results collector:**
```
issues = []
warnings = []
```

---

### Phase 1: Run Tests

**Delegate to:** `test-runner` sub-agent

Run ALL checks, collect ALL failures:
- Tests (capture all failures, not just first)
- Lint (all errors)
- Type checks (all errors)

**Collect results** - don't stop:
```
if tests failed: issues.append(test_failures)
if lint failed: issues.append(lint_errors)
if types failed: issues.append(type_errors)
```

---

### Phase 2: Agent Validation (Parallel)

Launch BOTH agents in parallel, wait for both:

**Agent A: QA Validator**
**Agent B: Security Validator**

**Collect all findings:**
```
issues.extend(qa_findings.critical + qa_findings.high)
issues.extend(security_findings.critical + security_findings.high)
warnings.extend(qa_findings.medium + qa_findings.low)
warnings.extend(security_findings.medium + security_findings.low)
```

---

### Phase 3: Documentation Check

Run regardless of previous failures.

**Collect findings:**
```
if docs_missing: warnings.append(docs_needed)
```

---

### Phase 4: AC Verification

Check all ACs, collect all gaps:
```
for each AC:
  if not verifiable: issues.append("AC #{n} not verified: {text}")
```

---

### Phase 5: Report ALL Issues

**If issues is not empty:**

```
================================================================================
VALIDATION FAILED - {len(issues)} issues to fix
================================================================================

## Critical (must fix)

1. [TEST] 3 tests failed:
   - test_foo: AssertionError at line 42
   - test_bar: Timeout
   - test_baz: Missing fixture

2. [SECURITY] SQL injection in src/api/handler.py:55
   - User input passed to query without sanitization
   - Fix: Use parameterized query

3. [AC] Acceptance criteria #3 not verified:
   "Error messages are user-friendly"

## Warnings (should fix)

1. [LINT] 2 unused imports in src/utils.py
2. [DOCS] README not updated for new --verbose flag

================================================================================
Fix all issues above, then re-run: /flow:validate {task-id}
================================================================================
```

**If issues is empty:** Proceed to completion.

---

### Phase 6: Completion (only if no issues)

1. Mark all verified ACs: `backlog task edit {task-id} --check-ac 1 --check-ac 2 ...`

2. Update task:
   ```bash
   backlog task edit {task-id} --notes "{summary}" -s Done
   ```

3. Log decision (JSONL)

4. Write artifact: `docs/qa/{task-id}-validation-report.md`

---

### Phase 7: PR Submission (only if no issues)

**Delegate to:** `/flow:submit-n-watch-pr`

---

## Flow Summary

```
Phase 0: Load task (STOP if not found)
    ↓
Phases 1-4: Run ALL checks, collect ALL issues
    ↓
Phase 5: Report everything at once
    ↓
    ├── Issues found → User fixes ALL, re-runs ONCE
    │
    └── No issues → Phase 6-7: Complete + PR
```

**One run, all feedback. One fix cycle. Done.**

---

## Sub-Agents

| Agent | Purpose |
|-------|---------|
| `test-runner` | Tests, lint, types - returns ALL failures |
| `qa-validator` | QA + AC coverage - returns ALL gaps |
| `security-validator` | Security review - returns ALL findings |
| `docs-validator` | Docs completeness - returns ALL missing |

Located in: `.claude/agents/validate/`

---

## Command Reference

```bash
/flow:validate              # Auto-discover task
/flow:validate task-123     # Specific task
```
