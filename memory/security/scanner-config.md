# Scanner Configuration Defaults

This document defines the default configuration for security scanners used in Flowspec.

## Default Scanner Configuration

### Semgrep (Default: Enabled)
```yaml
semgrep:
  enabled: true
  rulesets: []  # Empty - uses registry_rulesets instead
  registry_rulesets:
    - p/default  # Semgrep Registry default ruleset (comprehensive)
  custom_rules_dir: null  # No custom rules by default
  timeout: 300  # 5 minutes
  extra_args: []
```

**Rationale**:
- Semgrep is lightweight and fast
- `p/default` provides broad security coverage
- 5-minute timeout handles large codebases
- No custom rules by default - users opt-in

### CodeQL (Default: Disabled)
```yaml
codeql:
  enabled: false  # Requires database setup
  rulesets: []
  languages: []  # Auto-detect from codebase
  query_suites:
    - security-extended  # More comprehensive than security-and-quality
  database_path: null  # Must be created by user
  extra_args: []
```

**Rationale**:
- CodeQL requires database creation (slow)
- Not suitable for quick scans
- Best for CI/CD or scheduled scans
- Disabled by default to avoid setup issues

### Bandit (Default: Enabled)
```yaml
bandit:
  enabled: true
  rulesets: []
  skips: []  # No tests skipped by default
  confidence_level: medium  # Balance false positives vs coverage
  extra_args: []
```

**Rationale**:
- Python-specific scanner
- Fast and lightweight
- Medium confidence reduces false positives
- Complements Semgrep for Python projects

## Default Severity Threshold

```yaml
fail_on: high  # Fail on high and critical findings
```

**Rationale**:
- Critical: Always fail (security vulnerabilities)
- High: Fail (serious issues)
- Medium: Warn (should fix but not blocking)
- Low: Info (nice to fix)

This balances security with developer experience.

## Default Exclusions

```yaml
exclusions:
  paths:
    - node_modules/
    - .venv/
    - venv/
    - vendor/
    - dist/
    - build/
    - .git/
    - __pycache__/
  patterns:
    - "*.min.js"      # Minified JavaScript
    - "*.min.css"     # Minified CSS
    - "*.bundle.js"   # Bundled JavaScript
    - "*_test.go"     # Test files (often have test credentials)
    - "*_test.py"
    - "*.generated.*" # Generated code
    - "*.pb.go"       # Protobuf generated files
    - "*.pb.py"
  file_extensions:
    - .map           # Source maps
    - .lock          # Lock files (package-lock.json, poetry.lock)
    - .sum           # Checksum files (go.sum)
```

**Rationale**:
- Dependencies: Not our code, not our responsibility
- Generated code: Can't fix, would be overwritten
- Test files: May contain test credentials (false positives)
- Minified/bundled: Hard to read, source should be scanned instead

## Default AI Triage Settings

```yaml
triage:
  enabled: true  # AI triage helps reduce noise
  confidence_threshold: 0.7  # 70% confidence minimum
  auto_dismiss_fp: false  # Don't auto-dismiss - let humans decide
  cluster_similar: true  # Group similar findings together
```

**Rationale**:
- AI triage reduces false positive fatigue
- 0.7 threshold balances precision and recall
- Don't auto-dismiss - humans should review
- Clustering reduces duplicate noise

## Default Reporting Settings

```yaml
reporting:
  format: markdown  # Human-readable format
  output_dir: null  # Output to stdout by default
  include_false_positives: false  # Only show real issues
  max_remediations: 10  # Limit AI suggestions to top 10
```

**Rationale**:
- Markdown is readable in terminal and GitHub
- Stdout works with CI/CD pipes
- Hide false positives by default (reduce noise)
- Limit suggestions to avoid overwhelming developers

## Default Top-Level Settings

```yaml
parallel_scans: true  # Run scanners in parallel
max_findings: 1000    # Prevent overwhelming output
```

**Rationale**:
- Parallel scans are faster
- Limiting findings prevents UI/terminal overflow
- If >1000 findings, there are bigger problems

## Scanner Selection by Project Type

### Python Projects
```yaml
scanners:
  semgrep:
    enabled: true
  bandit:
    enabled: true
  codeql:
    enabled: false  # Optional for CI/CD
```

### JavaScript/TypeScript Projects
```yaml
scanners:
  semgrep:
    enabled: true
  codeql:
    enabled: false  # Good for CI/CD
  bandit:
    enabled: false  # Python-only
```

### Go Projects
```yaml
scanners:
  semgrep:
    enabled: true
  codeql:
    enabled: false  # Excellent Go support
  bandit:
    enabled: false  # Python-only
```

### Multi-Language Projects
```yaml
scanners:
  semgrep:
    enabled: true   # Works for all languages
  codeql:
    enabled: false  # Can scan multiple languages
  bandit:
    enabled: true   # Only scans Python files
```

## Environment-Specific Overrides

### Development (Local)
- All defaults work well
- Fast feedback loop
- Focus on high/critical findings

### CI/CD (GitHub Actions)
```yaml
scanners:
  semgrep:
    enabled: true
    timeout: 600  # 10 minutes for large codebases
  codeql:
    enabled: true  # Worth the time in CI
  bandit:
    enabled: true

fail_on: high  # Block PRs on high+ severity

triage:
  auto_dismiss_fp: true  # Reduce CI noise
```

### Production Audits
```yaml
scanners:
  semgrep:
    enabled: true
  codeql:
    enabled: true  # Deep analysis
  bandit:
    enabled: true

fail_on: medium  # Catch more issues

triage:
  confidence_threshold: 0.5  # Lower bar
  auto_dismiss_fp: false  # Review everything
```

## Custom Rule Directories

If you have custom Semgrep rules:

```yaml
semgrep:
  enabled: true
  custom_rules_dir: .security/rules/
  registry_rulesets:
    - p/default
    - p/owasp-top-ten
```

Rules in `.security/rules/` will be loaded in addition to registry rulesets.

## Scanner Performance Characteristics

| Scanner | Speed | Depth | Languages | Setup |
|---------|-------|-------|-----------|-------|
| Semgrep | Fast | Medium | 30+ | None |
| CodeQL | Slow | Deep | 10+ | Database |
| Bandit | Fast | Light | Python | None |

**Recommendations**:
- **Quick scans**: Semgrep + Bandit
- **Deep analysis**: CodeQL
- **CI/CD**: All three in parallel
- **Pre-commit**: Semgrep only

## Configuration Validation

All default values pass schema validation. If you override defaults:

1. Run `specify security validate-config` to check
2. Start with defaults and change one thing at a time
3. Test locally before committing
4. Use version control to track changes

## Related Files

- `src/specify_cli/security/config/models.py` - Default values in dataclasses
- `src/specify_cli/security/config/loader.py` - Config loading logic
- `src/specify_cli/security/config/schema.py` - Validation rules
- `memory/security/security-facts.md` - General security facts
