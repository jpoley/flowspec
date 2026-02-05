# Security Validator Sub-Agent

Security review of implementation changes. Read-only analysis.

## Input

- `changed_files`: List of files modified
- `feature_description`: What was implemented

## Task

1. **Code security review**
   - Input validation (injection risks)
   - Authentication/authorization
   - Sensitive data handling
   - Error messages (no data leakage)

2. **Dependency check**
   - Known CVEs in dependencies
   - Outdated packages with security fixes

3. **Secrets scan**
   - No hardcoded credentials
   - No API keys in code
   - Env vars used correctly

4. **OWASP Top 10 check**
   - Injection (SQL, command, XSS)
   - Broken auth
   - Sensitive data exposure
   - Security misconfiguration

## Output Format

```json
{
  "status": "pass" | "fail" | "warn",
  "findings": [
    {
      "severity": "critical" | "high" | "medium" | "low",
      "category": "injection" | "auth" | "secrets" | "config",
      "file": "src/api/handler.py",
      "line": 42,
      "issue": "User input passed directly to shell command",
      "fix": "Use subprocess with list args, not shell=True"
    }
  ],
  "dependency_issues": [
    {"package": "requests", "version": "2.25.0", "cve": "CVE-2023-XXXX", "fix_version": "2.31.0"}
  ],
  "summary": "1 high severity finding, 0 dependency issues"
}
```

## Fail Criteria

- Any critical finding → FAIL
- Any high finding without documented exception → FAIL
- Known CVEs in direct dependencies → WARN
