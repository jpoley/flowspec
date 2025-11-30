# QA Report: [Feature Name]

**Date:** YYYY-MM-DD
**QA Engineer:** [Name]
**Test Cycle:** [Cycle identifier]
**Status:** [In Progress | Complete | Blocked]
**Environment:** [Testing environment]

## Executive Summary

[2-3 paragraph summary of testing results, coverage, and sign-off recommendation]

## Test Scope

### Features Tested

- [Feature 1]
- [Feature 2]
- [Feature 3]

### Features Not Tested (Out of Scope)

- [Feature 1]
- [Feature 2]

### Testing Types Performed

- [ ] Unit Testing
- [ ] Integration Testing
- [ ] Functional Testing
- [ ] Regression Testing
- [ ] Performance Testing
- [ ] Security Testing
- [ ] Accessibility Testing
- [ ] User Acceptance Testing

## Test Environment

**Environment:** [Staging/QA/Production-like]
**Configuration:**
- OS: [Operating system versions]
- Browsers: [Browser versions tested]
- Devices: [Device types tested]
- Test Data: [Description of test data used]

**Infrastructure:**
- Application Version: [Version/commit]
- Database Version: [Version]
- Dependencies: [Key dependency versions]

## Test Results Summary

### Overall Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Test Cases Executed | [X] | [X] | [Pass/Fail] |
| Test Cases Passed | [X] | [X%] | [Pass/Fail] |
| Test Cases Failed | [X] | [<X%] | [Pass/Fail] |
| Test Cases Blocked | [X] | [0] | [Pass/Fail] |
| Code Coverage | [X%] | [80%] | [Pass/Fail] |
| Defects Found | [X] | [Varies] | [Status] |

### Pass/Fail Breakdown

```
Total Test Cases: [X]
├── Passed: [X] ([X%])
├── Failed: [X] ([X%])
├── Blocked: [X] ([X%])
└── Not Run: [X] ([X%])
```

### Test Coverage

**Code Coverage:**
- Lines: [X%]
- Branches: [X%]
- Functions: [X%]
- Statements: [X%]

**Feature Coverage:**
- Critical Features: [X%]
- High Priority: [X%]
- Medium Priority: [X%]
- Low Priority: [X%]

## Test Execution

### Unit Tests

**Total:** [X tests]
**Passed:** [X] ([X%])
**Failed:** [X] ([X%])
**Coverage:** [X%]

**Notable Results:**
- [Result 1]
- [Result 2]

### Integration Tests

**Total:** [X tests]
**Passed:** [X] ([X%])
**Failed:** [X] ([X%])

**Test Scenarios:**
1. [Scenario 1] - [Pass/Fail]
2. [Scenario 2] - [Pass/Fail]
3. [Scenario 3] - [Pass/Fail]

### Functional Tests

**Total:** [X tests]
**Passed:** [X] ([X%])
**Failed:** [X] ([X%])

**Critical Paths Tested:**
- [Path 1] - [Pass/Fail]
- [Path 2] - [Pass/Fail]
- [Path 3] - [Pass/Fail]

### Regression Tests

**Total:** [X tests]
**Passed:** [X] ([X%])
**Failed:** [X] ([X%])

**Impact:**
[Description of regression test results]

### Performance Tests

**Load Testing Results:**
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Response Time (p50) | [X ms] | [X ms] | [Pass/Fail] |
| Response Time (p95) | [X ms] | [X ms] | [Pass/Fail] |
| Response Time (p99) | [X ms] | [X ms] | [Pass/Fail] |
| Throughput | [X req/s] | [X req/s] | [Pass/Fail] |
| Error Rate | [<X%] | [X%] | [Pass/Fail] |

**Stress Testing Results:**
- Maximum Load Supported: [X concurrent users/requests]
- Breaking Point: [Description]
- Recovery Time: [X seconds]

### Security Tests

**Security Scan Results:**
- Critical Vulnerabilities: [X]
- High Vulnerabilities: [X]
- Medium Vulnerabilities: [X]
- Low Vulnerabilities: [X]

**Security Tests Performed:**
- [ ] Authentication testing
- [ ] Authorization testing
- [ ] Input validation
- [ ] SQL injection
- [ ] XSS testing
- [ ] CSRF testing
- [ ] Security headers

## Defects

### Defect Summary

| Severity | Open | Resolved | Total |
|----------|------|----------|-------|
| Critical | [X] | [X] | [X] |
| High | [X] | [X] | [X] |
| Medium | [X] | [X] | [X] |
| Low | [X] | [X] | [X] |
| **Total** | **[X]** | **[X]** | **[X]** |

### Critical Defects

#### Defect 1: [Title]

**ID:** [Defect ID]
**Severity:** Critical
**Status:** [Open/Resolved/Verified]
**Description:** [Brief description]
**Impact:** [Impact on users/system]
**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:** [What should happen]
**Actual Result:** [What actually happens]
**Resolution:** [How it was fixed or current status]

### High Priority Defects

#### Defect 2: [Title]

**ID:** [Defect ID]
**Severity:** High
**Status:** [Open/Resolved/Verified]
**Description:** [Brief description]
**Impact:** [Impact on users/system]

### Medium and Low Priority Defects

[List or link to tracking system]

## Test Cases

### Critical Test Cases

| ID | Test Case | Priority | Result | Notes |
|----|-----------|----------|--------|-------|
| TC-001 | [Description] | Critical | [Pass/Fail] | [Notes] |
| TC-002 | [Description] | Critical | [Pass/Fail] | [Notes] |

### High Priority Test Cases

| ID | Test Case | Priority | Result | Notes |
|----|-----------|----------|--------|-------|
| TC-010 | [Description] | High | [Pass/Fail] | [Notes] |
| TC-011 | [Description] | High | [Pass/Fail] | [Notes] |

## Acceptance Criteria Verification

| Acceptance Criterion | Verified | Notes |
|---------------------|----------|-------|
| [AC 1] | [Yes/No] | [Notes] |
| [AC 2] | [Yes/No] | [Notes] |
| [AC 3] | [Yes/No] | [Notes] |

## Risks and Concerns

### Outstanding Risks

1. **Risk 1:** [Description]
   - **Impact:** [High/Medium/Low]
   - **Mitigation:** [Strategy]

2. **Risk 2:** [Description]
   - **Impact:** [High/Medium/Low]
   - **Mitigation:** [Strategy]

### Known Issues

- [Issue 1 - description and workaround]
- [Issue 2 - description and workaround]

## Recommendations

### Release Recommendation

**Recommendation:** [GO | NO-GO | GO WITH CONDITIONS]

**Rationale:**
[Detailed explanation]

### Conditions for Release (if applicable)

- [ ] [Condition 1 - e.g., Fix critical defect #123]
- [ ] [Condition 2 - e.g., Verify performance under load]
- [ ] [Condition 3]

### Post-Release Monitoring

- [Metric to monitor 1]
- [Metric to monitor 2]
- [Metric to monitor 3]

## Lessons Learned

### What Went Well

- [Success 1]
- [Success 2]

### What Could Be Improved

- [Improvement 1]
- [Improvement 2]

### Action Items

- [ ] [Action 1]
- [ ] [Action 2]

## Appendix

### Test Artifacts

- Test Plan: [Link]
- Test Cases: [Link to test management system]
- Automated Test Results: [Link]
- Performance Test Reports: [Link]
- Security Scan Reports: [Link]

### Test Data

[Description or link to test data sets used]

### Screenshots

[Links or embedded screenshots of defects]

### References

- PRD: [Link]
- Technical Design: [Link]
- API Documentation: [Link]

---

**QA Sign-off:**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| QA Lead | [Name] | YYYY-MM-DD | |
| QA Engineer | [Name] | YYYY-MM-DD | |

**Document Version:** 1.0
**Last Updated:** YYYY-MM-DD
