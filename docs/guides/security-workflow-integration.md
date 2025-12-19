# Security Workflow Integration Guide

This guide explains how to integrate `/flow:security` commands into your Spec-Driven Development workflow with automatic backlog task creation.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Workflow Patterns](#workflow-patterns)
- [Automatic Task Creation](#automatic-task-creation)
- [CI/CD Integration](#cicd-integration)
- [Pre-Commit Hooks](#pre-commit-hooks)
- [SARIF Export](#sarif-export)
- [Best Practices](#best-practices)

## Overview

The `/flow:security` command family integrates security assessment into your development workflow:

1. **Scanning** - SAST, SCA, secrets detection on codebase
2. **Triaging** - AI-powered vulnerability assessment and false positive detection
3. **Reporting** - Comprehensive audit reports with OWASP Top 10 compliance
4. **Task Creation** - Automatic backlog task creation for findings
5. **Workflow Integration** - Seamless integration with flowspec_workflow.yml states

## Quick Start

### Basic Scan

```bash
# Scan current directory
flowspec security scan

# Scan with JSON output
flowspec security scan --format json --output security-results.json

# Generate SARIF for GitHub Security
flowspec security scan --format sarif --output security-results.sarif
```

### Scan with Task Creation

```bash
# Create tasks for all findings
flowspec security scan --create-tasks

# Create tasks only for critical and high severity
flowspec security scan --create-tasks --task-severity critical,high

# Group findings by CWE (fewer tasks)
flowspec security scan --create-tasks --group-by-cwe

# Dry run to see what would be created
flowspec security scan --create-tasks --dry-run
```

## Workflow Patterns

### Pattern 1: Dedicated Security State

Add a dedicated security verification state for security-focused teams:

```yaml
# flowspec_workflow.yml additions

states:
  - "To Do"
  - "Assessed"
  - "Specified"
  - "Researched"
  - "Planned"
  - "In Implementation"
  - "Security Review"      # NEW: Dedicated security state
  - "Validated"
  - "Deployed"
  - "Done"

workflows:
  security:
    command: "/flow:security"
    description: "Execute security scans and create remediation tasks"
    agents:
      - name: "secure-by-design-engineer"
        identity: "@secure-by-design-engineer"
        description: "Security specialist for vulnerability assessment"
        responsibilities:
          - "Security scanning (SAST, SCA, secrets)"
          - "Vulnerability triage and prioritization"
          - "Security task creation in backlog"
          - "SARIF generation for GitHub Security"
    input_states: ["In Implementation"]
    output_state: "Security Review"
    optional: false
    creates_backlog_tasks: true

transitions:
  - name: "security_review"
    from: "In Implementation"
    to: "Security Review"
    via: "security"
    description: "Security scan completed, findings triaged"
    output_artifacts:
      - type: "security_scan_results"
        path: "./docs/security/scan-results.json"
        required: true
      - type: "security_triage"
        path: "./docs/security/triage-results.json"
        required: true
      - type: "security_report"
        path: "./docs/security/audit-report.md"
        required: true
      - type: "backlog_tasks"
        path: "./backlog/tasks/*.md"
        multiple: true
    validation: "NONE"
```

**When to use:**
- Security is a critical gate in your workflow
- Dedicated security team reviews all changes
- Want explicit security approval before QA
- Need clear audit trail for compliance

**Workflow sequence:**
```
Implementation → Security Review → Validated → Deployed
```

### Pattern 2: Extend Validate Workflow

Integrate security into existing validate workflow:

```yaml
# flowspec_workflow.yml - extend validate workflow

workflows:
  validate:
    command: "/flow:validate"
    description: "Execute validation using QA, security, and documentation agents"
    agents:
      - name: "quality-guardian"
        identity: "@quality-guardian"
        description: "Quality Guardian"
        responsibilities:
          - "Functional and integration testing"
          - "Performance testing"
      - name: "secure-by-design-engineer"
        identity: "@secure-by-design-engineer"
        description: "Secure-by-Design Engineer"
        responsibilities:
          - "Security scanning (SAST, SCA, secrets)"
          - "Vulnerability triage and assessment"
          - "Security task creation with --create-tasks"
          - "SARIF output generation"
      - name: "tech-writer"
        identity: "@tech-writer"
        description: "Senior Technical Writer"
        responsibilities:
          - "API documentation and user guides"
    input_states: ["In Implementation"]
    output_state: "Validated"
    optional: false
    creates_backlog_tasks: true
```

**When to use:**
- Integrated security approach
- Fast-moving teams
- Security is part of definition of done
- Fewer formal gates preferred

**Workflow sequence:**
```
Implementation → Validated (includes security) → Deployed
```

## Automatic Task Creation

### Command Options

```bash
flowspec security scan [OPTIONS]

Options:
  --create-tasks              Create backlog tasks for findings
  --task-severity TEXT        Severity threshold (e.g., 'critical,high')
  --group-by-cwe             Group findings by CWE
  --dry-run                  Show what would be created
```

### Task Format

Each created task includes:

**Title:**
```
Fix CRITICAL: SQL Injection in user authentication
```

**Description:**
```markdown
## Security Finding: SQL Injection

**Severity:** CRITICAL
**CWE:** CWE-89
**Scanner:** semgrep
**Confidence:** high

### Location

`src/auth/login.py:42-45`

### Code

```python
query = "SELECT * FROM users WHERE id = " + user_id
cursor.execute(query)
```

### Description

User input is concatenated into SQL query without sanitization.

### Remediation Guidance

Use parameterized queries instead of string concatenation:

```python
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### References

- https://owasp.org/SQL_Injection
```

**Acceptance Criteria:**
- Vulnerability at src/auth/login.py:42 is fixed
- No regression in existing functionality
- Security test added to prevent regression
- Code review by security-aware developer
- Re-scan shows finding is resolved

**Labels:**
- `security`
- `critical`
- `cwe89`
- `semgrep`

**Priority:** `high` (mapped from CRITICAL severity)

### Examples

```bash
# Create tasks for all findings
flowspec security scan --create-tasks

# Only critical and high severity
flowspec security scan --create-tasks --task-severity critical,high

# Group by CWE (fewer tasks, one per vulnerability type)
flowspec security scan --create-tasks --group-by-cwe

# See what would be created without creating
flowspec security scan --create-tasks --dry-run

# Full workflow: scan, output SARIF, create tasks
flowspec security scan \
  --format sarif \
  --output docs/security/scan-results.sarif \
  --create-tasks \
  --task-severity critical,high
```

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/security.yml`:

```yaml
name: Security Scan

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Weekly scan

permissions:
  contents: read
  security-events: write  # For SARIF upload
  pull-requests: write    # For comments

jobs:
  security-scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv sync
          uv tool install .

      - name: Run security scan
        run: |
          flowspec security scan \
            --format sarif \
            --output security-results.sarif \
            --fail-on high

      - name: Upload SARIF to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: security-results.sarif
          category: flowspec-security

      - name: Create backlog tasks for PR
        if: github.event_name == 'pull_request'
        run: |
          flowspec security scan \
            --create-tasks \
            --task-severity critical,high

      - name: Block on critical findings
        run: |
          CRITICAL_COUNT=$(jq '[.findings[] | select(.severity == "critical")] | length' docs/security/scan-results.json || echo 0)
          if [ "$CRITICAL_COUNT" -gt 0 ]; then
            echo "❌ Found $CRITICAL_COUNT critical vulnerabilities"
            exit 1
          fi
```

### GitLab CI

Add to `.gitlab-ci.yml`:

```yaml
security-scan:
  stage: test
  image: python:3.11

  before_script:
    - pip install uv
    - uv sync
    - uv tool install .

  script:
    - |
      flowspec security scan \
        --format sarif \
        --output gl-sast-report.json \
        --create-tasks \
        --task-severity critical,high \
        --fail-on high

  artifacts:
    reports:
      sast: gl-sast-report.json
    paths:
      - docs/security/
    when: always

  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

## Pre-Commit Hooks

### Optional Pre-Commit Integration

Pre-commit hooks are **optional** - teams can enable them if desired:

```bash
# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

echo "Running security scan on staged files..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
  echo "No staged files to scan"
  exit 0
fi

# Run security scan on staged files
flowspec security scan --output /tmp/security-scan.json --fail-on critical

# Check for critical findings
CRITICAL_COUNT=$(jq '[.findings[] | select(.severity == "critical")] | length' /tmp/security-scan.json 2>/dev/null || echo 0)

if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo "❌ Found $CRITICAL_COUNT critical security issues"
  echo "   Run 'flowspec security scan' to review findings"
  exit 1
fi

echo "✅ No critical security issues found"
exit 0
EOF

chmod +x .git/hooks/pre-commit
```

### Configuration Options

Pre-commit behavior can be configured:

```bash
# Warn only (don't block)
if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo "⚠️  Warning: Found $CRITICAL_COUNT critical security issues"
  # Don't exit with error - allow commit
fi

# Block on high and critical
if [ "$HIGH_COUNT" -gt 0 ]; then
  echo "❌ Found $HIGH_COUNT high or critical security issues"
  exit 1
fi

# Auto-create tasks but allow commit
if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo "Creating backlog tasks for findings..."
  flowspec security scan --create-tasks --task-severity critical,high
  echo "⚠️  Backlog tasks created, but allowing commit"
fi
```

## SARIF Export

### What is SARIF?

SARIF (Static Analysis Results Interchange Format) is a standard format for static analysis tool output. GitHub Code Scanning uses SARIF to display security findings in the Security tab.

### Generate SARIF

```bash
# Generate SARIF output
flowspec security scan --format sarif --output security-results.sarif
```

### Upload to GitHub Security

```yaml
# In GitHub Actions workflow
- name: Upload SARIF to GitHub Security
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: security-results.sarif
    category: flowspec-security
```

### Benefits

1. **GitHub Security Tab** - Findings appear in repository Security tab
2. **Code Annotations** - Vulnerabilities annotated inline in PRs
3. **Trend Analysis** - Track security posture over time
4. **Alerts** - GitHub notifies on new vulnerabilities
5. **Standard Format** - Works with all SARIF-compatible tools

## Best Practices

### Workflow Integration

1. **Choose the Right Pattern**
   - Use dedicated state for security-focused teams
   - Extend validate for fast-moving integrated teams

2. **Gate Appropriately**
   - Block on Critical/High in production branches
   - Warn on Medium/Low to maintain velocity

3. **Automate Task Creation**
   - Use `--create-tasks` for consistent tracking
   - Filter by severity to avoid noise (`--task-severity critical,high`)

4. **Track Remediation**
   - Use backlog tasks to track fixes
   - Re-scan after fixes to verify
   - Close tasks when findings are resolved

### CI/CD Integration

1. **Run on Every PR** - Catch issues before merge
2. **Upload SARIF** - Integrate with GitHub/GitLab Security
3. **Block Critical** - Prevent merging vulnerable code
4. **Track Metrics** - Monitor security posture trends
5. **Schedule Scans** - Weekly scans on main branch

### Pre-Commit Hooks

1. **Optional by Design** - Let teams choose their workflow
2. **Fast Scans Only** - Only scan staged files
3. **Warn, Don't Block** - Use warnings for most teams
4. **Critical Only** - Block only on critical findings
5. **Clear Feedback** - Show exactly what's wrong and how to fix

### Task Management

1. **Group by CWE** - Use `--group-by-cwe` for fewer, focused tasks
2. **Filter by Severity** - `--task-severity critical,high` to avoid noise
3. **Dry Run First** - Use `--dry-run` to preview tasks
4. **Track Progress** - Use backlog task status to track remediation
5. **Re-scan** - Verify fixes with new scans

## Troubleshooting

### Tasks Not Being Created

```bash
# Check if --create-tasks flag is set
flowspec security scan --create-tasks --task-severity critical,high

# Verify backlog CLI is available
which backlog

# Check for findings
flowspec security scan --format json --output findings.json
cat findings.json | jq '.findings | length'
```

### SARIF Upload Fails

```bash
# Verify SARIF format is valid
jq . security-results.sarif

# Check GitHub Actions permissions
# Add to workflow:
permissions:
  security-events: write
```

### Pre-Commit Hook Not Running

```bash
# Verify hook is installed
ls -l .git/hooks/pre-commit

# Check hook script is executable
chmod +x .git/hooks/pre-commit

# Test manually
bash .git/hooks/pre-commit
```

## See Also

- [Security Command Reference](../reference/security-commands.md)
- [CI/CD Integration Examples](../platform/security-cicd-examples.md)
- [Workflow Customization Guide](workflow-customization.md)
- [Backlog Integration Guide](flowspec-backlog-workflow.md)
