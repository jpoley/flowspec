# Satellite Mode Security Architecture Review

**Related Task:** task-016 - Security Architecture Review
**Status:** Phase 1: Discovery
**Dependencies:** task-013 (GitHub), task-014 (Jira), task-015 (Notion)

---

## 1. Threat Model (STRIDE)

### 1.1 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Workstation                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ Backlog.md  │◄──►│ Satellite   │◄──►│ Token Storage       │  │
│  │ Local Tasks │    │ Sync Engine │    │ (Keychain/Vault)    │  │
│  └─────────────┘    └──────┬──────┘    └─────────────────────┘  │
└────────────────────────────┼────────────────────────────────────┘
                             │ HTTPS
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   ┌───────────┐       ┌───────────┐       ┌───────────┐
   │  GitHub   │       │   Jira    │       │  Notion   │
   │   API     │       │   API     │       │   API     │
   └───────────┘       └───────────┘       └───────────┘
```

### 1.2 STRIDE Analysis

| Threat | Category | Asset | Risk | Mitigation |
|--------|----------|-------|------|------------|
| **S** - Token theft | Spoofing | API tokens | HIGH | Keychain storage, no plaintext |
| **T** - Modified tasks | Tampering | Local task files | MEDIUM | Checksum verification, audit log |
| **R** - Unauthorized changes | Repudiation | Sync operations | MEDIUM | Audit trail with timestamps |
| **I** - Token exposure in logs | Info Disclosure | Credentials | HIGH | Log sanitization, redaction |
| **D** - API unavailability | Denial of Service | Sync service | LOW | Retry with backoff, offline mode |
| **E** - Privilege escalation | Elevation | Remote access | MEDIUM | Minimal scope tokens, RBAC |

### 1.3 Attack Vectors

#### A1: Token Extraction
- **Vector:** Malicious process reads token from config file
- **Impact:** Full access to remote tracker
- **Mitigation:** System keychain (OS-level protection)

#### A2: Man-in-the-Middle
- **Vector:** Intercept API traffic
- **Impact:** Token capture, data modification
- **Mitigation:** TLS 1.3 only, certificate pinning (optional)

#### A3: Injection via Task Content
- **Vector:** Malicious content in remote task synced locally
- **Impact:** Command injection, XSS in viewers
- **Mitigation:** Input sanitization, content-type validation

#### A4: Log Leakage
- **Vector:** Debug logs contain tokens/sensitive data
- **Impact:** Credential exposure
- **Mitigation:** Structured logging with redaction

#### A5: Supply Chain Attack
- **Vector:** Compromised dependency
- **Impact:** Token theft, data exfiltration
- **Mitigation:** SBOM, dependency scanning, lockfiles

---

## 2. Token Storage Strategy

### 2.1 Recommended Approach: System Keychain

| Platform | Backend | Library |
|----------|---------|---------|
| macOS | Keychain | `keyring` (Python) |
| Linux | Secret Service (GNOME) / KWallet | `keyring` |
| Windows | Credential Manager | `keyring` |

### 2.2 Token Hierarchy

```yaml
# ~/.config/backlog/satellite.yml (public config)
providers:
  github:
    enabled: true
    token_ref: "keychain://backlog/github-token"  # Reference, not value
  jira:
    enabled: true
    base_url: "https://company.atlassian.net"
    token_ref: "keychain://backlog/jira-token"
  notion:
    enabled: false
```

### 2.3 Fallback Options (In Priority Order)

1. **System Keychain** (preferred)
2. **Environment Variable** (CI/CD contexts)
3. **Encrypted File** (with user-provided passphrase)
4. **Plain Config** (NOT RECOMMENDED, warn user)

### 2.4 Token Validation

```python
def validate_token(provider: str, token: str) -> bool:
    """Validate token works before storing."""
    # GitHub: GET /user
    # Jira: GET /rest/api/3/myself
    # Notion: POST /v1/users/me
    ...
```

### 2.5 Token Rotation

- Warn user if token is >90 days old (if metadata available)
- Support `backlog remote auth refresh` command
- Log token usage for audit

---

## 3. Sanitization Requirements

### 3.1 Input Sanitization (Remote → Local)

| Field | Sanitization | Reason |
|-------|--------------|--------|
| title | Strip control chars, limit 200 chars | Prevent terminal injection |
| description | HTML → Markdown, strip scripts | Prevent XSS in viewers |
| labels | Alphanumeric + hyphen only | Filename safety |
| assignee | Validate against allowlist | Prevent spoofing |
| status | Map to known values | Workflow integrity |
| custom_fields | Type validation per schema | Data integrity |

### 3.2 Output Sanitization (Local → Remote)

| Field | Sanitization | Reason |
|-------|--------------|--------|
| All text | Escape provider-specific chars | Prevent injection |
| Markdown | Convert to ADF (Jira) / Blocks (Notion) | Format compatibility |
| File paths | Never include in sync | Path traversal prevention |

### 3.3 Content Security Rules

```python
SANITIZATION_RULES = {
    "strip_patterns": [
        r"<script.*?>.*?</script>",  # XSS
        r"javascript:",               # JS URLs
        r"\x00-\x1f",                 # Control chars
    ],
    "max_lengths": {
        "title": 200,
        "description": 50000,
        "label": 50,
    },
    "allowed_html_tags": ["p", "br", "ul", "ol", "li", "strong", "em", "code", "pre"],
}
```

---

## 4. Compliance Requirements

### 4.1 SLSA (Supply-chain Levels for Software Artifacts)

| Level | Requirement | Implementation |
|-------|-------------|----------------|
| SLSA 1 | Build process documented | GitHub Actions workflow |
| SLSA 2 | Version control, hosted build | GitHub + signed commits |
| SLSA 3 | Isolated build, provenance | Reproducible builds |

**Actions:**
- [ ] Generate SBOM on each release
- [ ] Sign release artifacts (Sigstore/cosign)
- [ ] Publish provenance attestations
- [ ] Use locked dependencies (uv.lock)

### 4.2 NIST Cybersecurity Framework Mapping

| Function | Category | Satellite Mode Control |
|----------|----------|----------------------|
| **Identify** | Asset Management | Document all data flows |
| **Protect** | Access Control | Token-based auth, minimal scope |
| **Protect** | Data Security | Encryption at rest (keychain) and in transit (TLS) |
| **Detect** | Anomalies | Audit logging, sync conflict alerts |
| **Respond** | Response Planning | Token revocation procedure |
| **Recover** | Recovery Planning | Local-first architecture (offline capable) |

### 4.3 SOC 2 Considerations

For enterprise users requiring SOC 2 compliance:

| Control | Implementation |
|---------|----------------|
| CC6.1 - Logical Access | Token-based auth, no shared credentials |
| CC6.6 - System Boundaries | Clear data flow documentation |
| CC7.2 - System Monitoring | Audit log for all sync operations |

---

## 5. Security Checklist

### 5.1 Pre-Implementation Checklist

- [ ] Token storage uses system keychain by default
- [ ] No tokens in plaintext config files
- [ ] All API calls use HTTPS (TLS 1.2+)
- [ ] Input sanitization implemented for all remote data
- [ ] Output sanitization implemented for all local data
- [ ] Audit logging captures all sync operations
- [ ] Error messages don't leak sensitive information
- [ ] Dependencies scanned for vulnerabilities
- [ ] SBOM generated for release artifacts

### 5.2 Code Review Checklist

- [ ] No hardcoded credentials
- [ ] No token logging (even in debug mode)
- [ ] SQL/NoSQL injection prevented (if applicable)
- [ ] Command injection prevented in shell operations
- [ ] Path traversal prevented in file operations
- [ ] Rate limiting respected (provider-specific)
- [ ] Timeout handling for all network calls
- [ ] Graceful degradation on API errors

### 5.3 Deployment Checklist

- [ ] Documentation includes security setup guide
- [ ] Token rotation procedure documented
- [ ] Incident response procedure documented
- [ ] Security contact published (SECURITY.md)
- [ ] Vulnerability disclosure policy defined

### 5.4 Ongoing Security Tasks

- [ ] Weekly dependency vulnerability scan (Dependabot/Snyk)
- [ ] Quarterly security review
- [ ] Annual penetration testing (if applicable)
- [ ] Monitor provider API security advisories

---

## 6. Implementation Recommendations

### 6.1 High Priority (Must Have)

1. **Keychain-based token storage** - Non-negotiable for sensitive data
2. **Input sanitization** - Prevent injection attacks
3. **Audit logging** - Required for compliance
4. **HTTPS-only** - No exceptions

### 6.2 Medium Priority (Should Have)

1. **Token validation on storage** - Catch misconfigurations early
2. **SBOM generation** - Supply chain transparency
3. **Signed releases** - Tamper evidence

### 6.3 Lower Priority (Nice to Have)

1. **Certificate pinning** - Defense in depth
2. **Encrypted local cache** - Additional protection
3. **Hardware token support** - For high-security environments

---

## 7. Risk Summary

| Risk | Likelihood | Impact | Priority | Mitigation Status |
|------|------------|--------|----------|-------------------|
| Token theft from config | Medium | High | P0 | Keychain storage |
| Injection via sync | Low | High | P0 | Input sanitization |
| Log leakage | Medium | Medium | P1 | Structured logging |
| Supply chain attack | Low | High | P1 | SBOM + signing |
| API rate limiting | High | Low | P2 | Backoff + caching |

---

*Created for task-016 - Security Architecture Review*
*Based on findings from task-013 (GitHub), task-014 (Jira), task-015 (Notion)*
