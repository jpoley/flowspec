# Security Configuration Guide

This directory contains security configuration documentation and examples for JP Spec Kit.

## Quick Start

1. Copy the example config:
   ```bash
   cp docs/security/config-schema.yaml .jpspec/security-config.yml
   ```

2. Edit `.jpspec/security-config.yml` to enable/disable scanners and set thresholds

3. Run a security scan:
   ```bash
   specify security scan
   ```

## Configuration File

The security configuration file (`.jpspec/security-config.yml`) controls:

- Which scanners to run (Semgrep, CodeQL, Bandit)
- Severity thresholds for failing scans
- Path exclusions (dependencies, generated code)
- AI triage settings
- Report format and output

See [`config-schema.yaml`](config-schema.yaml) for a fully documented example with all available options.

## Configuration Locations

The system searches for configuration files in this order:

1. `.jpspec/security-config.yml`
2. `.jpspec/security-config.yaml`
3. `.security/config.yml`
4. `.security/config.yaml`
5. `security-config.yml`

If no config file is found, sensible defaults are used.

## Scanner Overview

### Semgrep (Recommended)
- **Speed**: Fast (seconds)
- **Languages**: 30+ languages
- **Setup**: None required
- **Best for**: Daily development, pre-commit hooks

Default rulesets:
- `p/default` - Comprehensive security rules
- `p/owasp-top-ten` - OWASP Top 10 vulnerabilities
- `p/cwe-top-25` - CWE Top 25 weaknesses

### CodeQL (Advanced)
- **Speed**: Slow (minutes to hours)
- **Languages**: 10+ languages (Python, JS, Go, Java, C/C++, C#, Ruby)
- **Setup**: Requires database creation
- **Best for**: CI/CD, scheduled scans, deep analysis

### Bandit (Python)
- **Speed**: Fast (seconds)
- **Languages**: Python only
- **Setup**: None required
- **Best for**: Python projects, quick checks

## Configuration Profiles

### Development (Fast Local Scans)
```yaml
scanners:
  semgrep:
    enabled: true
  bandit:
    enabled: true
  codeql:
    enabled: false
fail_on: high
```

**Use when**: Local development, pre-commit checks

### CI/CD (Comprehensive)
```yaml
scanners:
  semgrep:
    enabled: true
    timeout: 600
  codeql:
    enabled: true
  bandit:
    enabled: true
fail_on: high
triage:
  auto_dismiss_fp: true
reporting:
  format: sarif
```

**Use when**: GitHub Actions, GitLab CI, Jenkins

### Security Audit (Deep Analysis)
```yaml
scanners:
  semgrep:
    enabled: true
    registry_rulesets: [p/default, p/owasp-top-ten, p/security-audit]
  codeql:
    enabled: true
    query_suites: [security-extended]
  bandit:
    enabled: true
    confidence_level: low
fail_on: medium
triage:
  confidence_threshold: 0.5
  auto_dismiss_fp: false
```

**Use when**: Security reviews, compliance audits

## Severity Levels

From highest to lowest:
- **critical** - Exploitable vulnerabilities (SQL injection, RCE)
- **high** - Serious security issues (XSS, CSRF, auth bypass)
- **medium** - Security weaknesses (weak crypto, info disclosure)
- **low** - Best practice violations
- **info** - Informational findings

The `fail_on` setting determines which findings cause scans to fail:
- `fail_on: critical` - Only fail on critical
- `fail_on: high` - Fail on high and critical (recommended)
- `fail_on: medium` - Fail on medium, high, and critical
- `fail_on: low` - Fail on any finding except info
- `fail_on: none` - Never fail (report only)

## Path Exclusions

Exclude files/directories from scanning:

```yaml
exclusions:
  paths:
    - node_modules/    # Dependencies
    - .venv/          # Virtual environments
    - dist/           # Build output
  patterns:
    - "*.min.js"      # Minified files
    - "*_test.py"     # Test files
  file_extensions:
    - .map            # Source maps
    - .lock           # Lock files
```

**Common exclusions**:
- Dependencies (`node_modules/`, `vendor/`, `.venv/`)
- Generated code (`*.generated.*`, `*.pb.go`)
- Build artifacts (`dist/`, `build/`)
- Test files (`*_test.py`, `*_test.go`)

## AI Triage

AI-powered analysis to reduce false positives:

```yaml
triage:
  enabled: true
  confidence_threshold: 0.7    # 0.0-1.0
  auto_dismiss_fp: false       # Let humans review
  cluster_similar: true        # Group similar findings
```

**Confidence threshold**:
- `0.5` - More findings, some false positives
- `0.7` - Balanced (recommended)
- `0.9` - Fewer findings, very high confidence

**Auto-dismiss**:
- `false` - Human reviews all findings (recommended)
- `true` - Auto-dismiss low-confidence findings (CI/CD)

## Custom Semgrep Rules

Create custom rules in `.security/rules/`:

```yaml
# .security/rules/custom-api-key.yml
rules:
  - id: custom-hardcoded-api-key
    patterns:
      - pattern: api_key = "..."
    message: Hardcoded API key detected
    severity: ERROR
    languages: [python]
```

Then enable in config:

```yaml
semgrep:
  enabled: true
  custom_rules_dir: .security/rules/
```

## Report Formats

### Markdown (Default)
```yaml
reporting:
  format: markdown
```
Human-readable format for terminals and GitHub

### SARIF
```yaml
reporting:
  format: sarif
```
Standard format for GitHub Code Scanning, IDEs

### JSON
```yaml
reporting:
  format: json
```
Machine-readable for automation, dashboards

### HTML
```yaml
reporting:
  format: html
```
Rich format for manual review, reports

## Validation

Validate your configuration before committing:

```bash
specify security validate-config
```

Or validate a specific file:

```bash
specify security validate-config --file .jpspec/security-config.yml
```

## Environment Variables

Override config with environment variables:

- `SECURITY_FAIL_ON=critical` - Override fail_on threshold
- `SECURITY_PARALLEL=false` - Disable parallel scanning
- `SECURITY_CONFIG=/path/to/config.yml` - Use custom config path

## Troubleshooting

### "Scanner not found"
Install the scanner:
```bash
# Semgrep
pip install semgrep

# Bandit
pip install bandit

# CodeQL
# Download from GitHub
```

### "Configuration validation failed"
Run validation with verbose output:
```bash
specify security validate-config --verbose
```

### "Too many findings"
Adjust thresholds:
```yaml
fail_on: critical      # Only fail on critical
max_findings: 100      # Limit output
```

Or add exclusions:
```yaml
exclusions:
  paths:
    - legacy/          # Exclude legacy code
```

### "Scan timeout"
Increase timeout:
```yaml
semgrep:
  timeout: 600  # 10 minutes
```

## Related Documentation

- [Security Quick Start](../guides/security-quickstart.md) - Get started guide
- [Custom Rules Guide](../guides/security-custom-rules.md) - Writing custom rules
- [CI/CD Integration](../guides/security-cicd-integration.md) - GitHub Actions setup
- [Security Facts](../../memory/security/security-facts.md) - Key security facts
- [Scanner Defaults](../../memory/security/scanner-config.md) - Default configuration

## Examples

See [`config-schema.yaml`](config-schema.yaml) for:
- Full configuration with all options
- Development profile
- CI/CD profile
- Audit profile
- Minimal profile

## Support

- GitHub Issues: Report bugs or request features
- Documentation: See `docs/guides/security-*.md`
- Community: Discussions and questions
