# Security Quickstart Guide

This guide helps you integrate security scanning into your development workflow using `/jpspec:security` commands.

## Prerequisites

- Python 3.11+
- JP Spec Kit installed (`pip install specify-cli`)
- At least one security scanner (Semgrep recommended)

### Installing Semgrep

```bash
# Via pip (recommended)
pip install semgrep

# Via Homebrew (macOS/Linux)
brew install semgrep

# Verify installation
semgrep --version
```

## Quick Start

### 1. Run Your First Scan

```bash
# Scan current directory
specify security scan

# Scan specific path
specify security scan ./src

# Output as JSON for CI/CD
specify security scan --format json --output results.json
```

### 2. Triage Findings with AI

```bash
# AI-powered triage to classify true/false positives
specify security triage results.json

# Interactive mode for manual confirmation
specify security triage results.json --interactive
```

### 3. Generate Fix Suggestions

```bash
# Generate fix patches for findings
specify security fix results.json

# Auto-apply patches (use with caution)
specify security fix results.json --apply
```

### 4. Generate Audit Report

```bash
# Generate compliance-ready report
specify security audit results.json --format markdown

# Generate SARIF for GitHub Code Scanning
specify security audit results.json --format sarif --output results.sarif
```

## CLI Command Summary

| Command | Description |
|---------|-------------|
| `specify security scan [PATH]` | Run security scanners on codebase |
| `specify security triage RESULTS` | AI-powered finding classification |
| `specify security fix RESULTS` | Generate remediation patches |
| `specify security audit RESULTS` | Generate compliance reports |
| `specify security status` | Show scan status and configuration |

## Slash Commands

Use these within Claude Code sessions:

| Command | Description |
|---------|-------------|
| `/jpspec:security scan` | Interactive security scan |
| `/jpspec:security triage` | AI triage with explanations |
| `/jpspec:security fix` | Generate and review fixes |
| `/jpspec:security audit` | Generate security report |

## Configuration

Create `.specify/security.yml` in your project root:

```yaml
# Security scanning configuration
version: "1.0"

# Scanner configuration
scanners:
  semgrep:
    enabled: true
    config: auto  # Use "auto" for OWASP rules
    severity_threshold: warning

  bandit:
    enabled: false
    severity_threshold: medium

# Fail threshold for CI/CD
fail_on:
  severity: high  # critical, high, medium, low
  confidence: high

# Exclusions
exclusions:
  paths:
    - "**/tests/**"
    - "**/node_modules/**"
    - "**/.venv/**"
  patterns:
    - "*.test.py"
    - "*.spec.ts"

# Triage configuration
triage:
  auto_dismiss_info: true
  require_review_for: critical

# Reporting
reporting:
  formats:
    - markdown
    - sarif
  owasp_mapping: true
  include_remediation: true
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install specify-cli semgrep

      - name: Run security scan
        run: specify security scan --format sarif --output results.sarif

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
```

### GitLab CI

```yaml
security-scan:
  stage: security
  image: python:3.11
  script:
    - pip install specify-cli semgrep
    - specify security scan --format json --output gl-sast-report.json
  artifacts:
    reports:
      sast: gl-sast-report.json
```

## Common Workflows

### Workflow 1: Quick Security Check

```bash
# Fast scan with default settings
specify security scan --quick

# View summary
specify security status
```

### Workflow 2: Pre-Commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: jpspec-security
        name: Security Scan
        entry: specify security scan --fail-on high
        language: python
        pass_filenames: false
```

### Workflow 3: Full Security Audit

```bash
# Comprehensive scan
specify security scan --all-scanners

# AI triage
specify security triage results.json --interactive

# Generate fixes
specify security fix results.json

# Generate audit report
specify security audit results.json --format markdown --compliance soc2
```

## Severity Levels

| Level | Description | Example |
|-------|-------------|---------|
| **Critical** | Immediate exploitation risk | SQL injection, RCE |
| **High** | Significant security impact | XSS, path traversal |
| **Medium** | Moderate risk with mitigations | Information disclosure |
| **Low** | Minor issues or hardening | Missing security headers |
| **Info** | Best practices, no risk | Code quality suggestions |

## OWASP Top 10 Mapping

Findings are automatically mapped to OWASP Top 10 2021:

| Category | CWEs | Example |
|----------|------|---------|
| A01 Broken Access Control | CWE-22, CWE-284 | Path traversal |
| A02 Cryptographic Failures | CWE-327, CWE-328 | Weak encryption |
| A03 Injection | CWE-79, CWE-89 | SQL injection, XSS |
| A04 Insecure Design | CWE-209, CWE-256 | Design flaws |
| A05 Security Misconfiguration | CWE-16, CWE-611 | XML external entities |
| A06 Vulnerable Components | CWE-829, CWE-1035 | Known vulnerabilities |
| A07 Auth Failures | CWE-287, CWE-384 | Broken authentication |
| A08 Data Integrity Failures | CWE-502, CWE-829 | Deserialization |
| A09 Logging Failures | CWE-117, CWE-223 | Log injection |
| A10 SSRF | CWE-918 | Server-side request forgery |

## Troubleshooting

### Scanner Not Found

```bash
# Check if scanner is installed
which semgrep

# Install if missing
pip install semgrep
```

### Permission Denied

```bash
# Ensure scanner is executable
chmod +x $(which semgrep)
```

### High False Positive Rate

1. Use conservative rulesets: `--config auto`
2. Enable AI triage: `specify security triage results.json`
3. Add exclusions for test files
4. Tune sensitivity in `.specify/security.yml`

### Memory Issues on Large Codebases

```bash
# Scan incrementally
specify security scan --incremental

# Limit parallel jobs
specify security scan --jobs 2
```

## Next Steps

- [Command Reference](../reference/jpspec-security-commands.md) - Full CLI documentation
- [CI/CD Integration](./security-cicd-integration.md) - Detailed pipeline setup
- [Custom Rules](./security-custom-rules.md) - Writing custom security rules
- [Threat Model](../reference/security-threat-model.md) - Security limitations
