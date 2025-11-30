# Security Report: [Feature Name]

**Date:** YYYY-MM-DD
**Security Analyst:** [Name]
**Review Type:** [Code Review | Penetration Test | Vulnerability Assessment | Compliance Audit]
**Status:** [In Progress | Complete]
**Severity Level:** [Critical | High | Medium | Low | Informational]

## Executive Summary

[2-3 paragraph summary of security assessment, critical findings, and recommendations]

**Overall Security Posture:** [Strong | Acceptable | Needs Improvement | Critical Issues]

## Scope

### Components Reviewed

- [Component 1]
- [Component 2]
- [Component 3]

### Security Domains Assessed

- [ ] Authentication & Authorization
- [ ] Data Protection
- [ ] Input Validation
- [ ] Cryptography
- [ ] Session Management
- [ ] Error Handling
- [ ] Logging & Monitoring
- [ ] API Security
- [ ] Infrastructure Security
- [ ] Dependency Security

### Out of Scope

- [Item 1]
- [Item 2]

## Findings Summary

### Vulnerability Summary

| Severity | Count | Remediated | Remaining |
|----------|-------|------------|-----------|
| Critical | [X] | [X] | [X] |
| High | [X] | [X] | [X] |
| Medium | [X] | [X] | [X] |
| Low | [X] | [X] | [X] |
| Informational | [X] | [X] | [X] |
| **Total** | **[X]** | **[X]** | **[X]** |

### Risk Score

**CVSS Base Score:** [X.X] ([Critical/High/Medium/Low])
**Overall Risk Rating:** [Critical/High/Medium/Low]

## Critical Vulnerabilities

### CVE-001: [Vulnerability Title]

**Severity:** Critical
**CVSS Score:** [X.X]
**Status:** [Open | In Progress | Resolved | Mitigated]
**CWE:** [CWE-XXX - Weakness Name]

**Description:**
[Detailed description of the vulnerability]

**Impact:**
[What could an attacker do? What data/systems are at risk?]

**Affected Components:**
- [Component 1]
- [Component 2]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Proof of Concept:**
```
[Code or steps demonstrating the vulnerability]
```

**Remediation:**
[Specific steps to fix the vulnerability]

**Remediation Priority:** [Immediate | High | Medium | Low]
**Estimated Effort:** [Hours/Days]

**Mitigation (if remediation not possible):**
[Temporary mitigation measures]

**Verification:**
[How to verify the fix]

### CVE-002: [Vulnerability Title]

[Repeat structure for each critical vulnerability]

## High Severity Vulnerabilities

### CVE-003: [Vulnerability Title]

**Severity:** High
**CVSS Score:** [X.X]
**Status:** [Open | In Progress | Resolved | Mitigated]
**CWE:** [CWE-XXX]

**Description:** [Brief description]
**Impact:** [Impact summary]
**Remediation:** [Fix summary]

[Repeat for each high severity issue]

## Medium Severity Vulnerabilities

| ID | Vulnerability | CVSS | Status | Priority |
|----|--------------|------|--------|----------|
| CVE-004 | [Title] | [X.X] | [Status] | [Priority] |
| CVE-005 | [Title] | [X.X] | [Status] | [Priority] |

[Link to detailed descriptions in appendix]

## Low Severity Vulnerabilities

| ID | Vulnerability | CVSS | Status |
|----|--------------|------|--------|
| CVE-006 | [Title] | [X.X] | [Status] |
| CVE-007 | [Title] | [X.X] | [Status] |

## Security Testing Results

### SAST (Static Application Security Testing)

**Tool:** [Tool name]
**Scan Date:** YYYY-MM-DD

**Results:**
- Total Issues: [X]
- Critical: [X]
- High: [X]
- Medium: [X]
- Low: [X]

**Key Findings:**
- [Finding 1]
- [Finding 2]

### DAST (Dynamic Application Security Testing)

**Tool:** [Tool name]
**Scan Date:** YYYY-MM-DD

**Results:**
- Total Issues: [X]
- Critical: [X]
- High: [X]
- Medium: [X]
- Low: [X]

**Attack Vectors Tested:**
- [ ] SQL Injection
- [ ] Cross-Site Scripting (XSS)
- [ ] CSRF
- [ ] Authentication bypass
- [ ] Authorization bypass
- [ ] Command injection
- [ ] Path traversal

### Dependency Scan

**Tool:** [Tool name and version]
**Scan Date:** YYYY-MM-DD

**Vulnerable Dependencies:**
| Package | Version | Vulnerability | Severity | Fix Version |
|---------|---------|--------------|----------|-------------|
| [Package 1] | [X.X.X] | [CVE-XXXX] | [Critical] | [X.X.X] |
| [Package 2] | [X.X.X] | [CVE-XXXX] | [High] | [X.X.X] |

**Recommendations:**
- [Recommendation 1]
- [Recommendation 2]

### Container Security Scan

**Tool:** [Tool name]
**Scan Date:** YYYY-MM-DD
**Image:** [Image name:tag]

**Results:**
- Total Vulnerabilities: [X]
- Critical: [X]
- High: [X]
- Medium: [X]
- Low: [X]

**Base Image:** [Image name]
**Base Image Issues:** [X vulnerabilities]

### Penetration Testing

**Tester:** [Name/Firm]
**Date:** YYYY-MM-DD
**Methodology:** [OWASP/PTES/Custom]

**Attack Scenarios:**
1. [Scenario 1] - [Result]
2. [Scenario 2] - [Result]
3. [Scenario 3] - [Result]

**Successful Exploits:**
- [Exploit 1 - description]
- [Exploit 2 - description]

## Security Controls Assessment

### Authentication

**Status:** [Implemented | Partial | Missing]

**Controls:**
- [ ] Multi-factor authentication
- [ ] Password complexity requirements
- [ ] Account lockout policy
- [ ] Secure password storage (hashing)
- [ ] Session timeout

**Findings:**
- [Finding 1]
- [Finding 2]

### Authorization

**Status:** [Implemented | Partial | Missing]

**Controls:**
- [ ] Role-based access control (RBAC)
- [ ] Principle of least privilege
- [ ] Permission verification on all endpoints
- [ ] Attribute-based access control (ABAC)

**Findings:**
- [Finding 1]
- [Finding 2]

### Data Protection

**Status:** [Implemented | Partial | Missing]

**Controls:**
- [ ] Encryption at rest
- [ ] Encryption in transit (TLS)
- [ ] Sensitive data identification
- [ ] Data masking/redaction
- [ ] Secure key management

**Findings:**
- [Finding 1]
- [Finding 2]

### Input Validation

**Status:** [Implemented | Partial | Missing]

**Controls:**
- [ ] Input sanitization
- [ ] Whitelist validation
- [ ] Parameter type checking
- [ ] File upload restrictions
- [ ] Size limits

**Findings:**
- [Finding 1]
- [Finding 2]

### Logging & Monitoring

**Status:** [Implemented | Partial | Missing]

**Controls:**
- [ ] Security event logging
- [ ] Audit trail
- [ ] Log integrity protection
- [ ] Anomaly detection
- [ ] Alerting on security events

**Findings:**
- [Finding 1]
- [Finding 2]

## Compliance Assessment

### Standards Evaluated

- [ ] OWASP Top 10
- [ ] CWE Top 25
- [ ] PCI DSS
- [ ] GDPR
- [ ] SOC 2
- [ ] HIPAA
- [ ] ISO 27001

### Compliance Status

| Requirement | Status | Gaps | Remediation |
|------------|--------|------|-------------|
| [Req 1] | [Compliant/Non-Compliant] | [Gap description] | [Action] |
| [Req 2] | [Compliant/Non-Compliant] | [Gap description] | [Action] |

## Threat Model

### Identified Threats

#### Threat 1: [Name]

**Description:** [Threat description]
**Attack Vector:** [How could this be exploited?]
**Likelihood:** [High/Medium/Low]
**Impact:** [High/Medium/Low]
**Risk Level:** [Critical/High/Medium/Low]
**Mitigation:** [Current or proposed controls]

#### Threat 2: [Name]

[Repeat structure]

### Attack Surface

- [Entry point 1]
- [Entry point 2]
- [Entry point 3]

### Trust Boundaries

[Diagram or description of trust boundaries]

## Recommendations

### Immediate Actions (Critical)

1. **[Action 1]**
   - **Issue:** [Related vulnerability]
   - **Fix:** [Specific remediation]
   - **Deadline:** [Date]

2. **[Action 2]**
   - **Issue:** [Related vulnerability]
   - **Fix:** [Specific remediation]
   - **Deadline:** [Date]

### Short-term Actions (High Priority)

1. [Action 1]
2. [Action 2]
3. [Action 3]

### Medium-term Actions

1. [Action 1]
2. [Action 2]
3. [Action 3]

### Long-term Improvements

1. [Action 1]
2. [Action 2]
3. [Action 3]

## Security Best Practices

### Implemented

- [Practice 1]
- [Practice 2]
- [Practice 3]

### Missing/Recommended

- [Practice 1]
- [Practice 2]
- [Practice 3]

## Remediation Plan

| Priority | Vulnerability | Owner | Due Date | Status |
|----------|--------------|-------|----------|--------|
| Critical | [CVE-001] | [Name] | YYYY-MM-DD | [Status] |
| High | [CVE-002] | [Name] | YYYY-MM-DD | [Status] |
| Medium | [CVE-003] | [Name] | YYYY-MM-DD | [Status] |

## Release Recommendation

**Recommendation:** [APPROVE | CONDITIONAL APPROVAL | DO NOT RELEASE]

**Rationale:**
[Detailed explanation of recommendation]

**Conditions for Release (if applicable):**
- [ ] All critical vulnerabilities must be fixed
- [ ] [Specific condition 1]
- [ ] [Specific condition 2]

**Acceptable Risks (if any):**
- [Risk 1 - with justification]
- [Risk 2 - with justification]

## Post-Release Security

### Monitoring Requirements

- [Monitoring requirement 1]
- [Monitoring requirement 2]

### Incident Response

[Brief incident response plan for this feature]

### Security Updates

[Plan for ongoing security updates and patches]

## Appendix

### Detailed Vulnerability Descriptions

[Full details of medium/low vulnerabilities]

### Tool Configurations

[Security tool configurations used]

### Test Evidence

[Screenshots, logs, proof of concepts]

### References

- [OWASP Guide]
- [CWE Database]
- [Security standards]

### Glossary

| Term | Definition |
|------|------------|
| CVSS | Common Vulnerability Scoring System |
| CWE | Common Weakness Enumeration |
| SAST | Static Application Security Testing |
| DAST | Dynamic Application Security Testing |

---

**Security Sign-off:**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Lead | [Name] | YYYY-MM-DD | |
| Security Analyst | [Name] | YYYY-MM-DD | |

**Document Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Next Review Date:** YYYY-MM-DD
