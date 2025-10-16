---
description: Execute validation and quality assurance using QA, security, documentation, and release management agents.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Instructions

This command executes comprehensive validation using multiple specialized agents, ensuring production readiness with human approval gates.

### Phase 1: Testing and Security Validation (Parallel Execution)

**IMPORTANT**: Launch QA and Security agents in parallel for efficiency.

#### Quality Assurance Testing

Use the Task tool to launch the **quality-guardian** agent:

```
Conduct comprehensive quality validation for: [USER INPUT FEATURE]

Code and Artifacts:
[Include implementation code, API specs, test coverage reports]

Validation Requirements:

1. **Functional Testing**
   - Verify all acceptance criteria met
   - Test user workflows end-to-end
   - Validate edge cases and boundary conditions
   - Test error handling and recovery

2. **API and Contract Testing**
   - API endpoint testing (REST/GraphQL/gRPC)
   - Contract testing for API compatibility
   - Response validation
   - Error response testing

3. **Integration Testing**
   - Frontend-backend integration
   - Third-party service integration
   - Database integration
   - Message queue/event processing

4. **Performance Testing**
   - Load testing (expected traffic)
   - Stress testing (peak traffic)
   - Latency measurement (p50, p95, p99)
   - Resource utilization
   - Scalability validation

5. **Non-Functional Requirements**
   - Accessibility (WCAG 2.1 AA compliance)
   - Cross-browser/platform compatibility
   - Mobile responsiveness
   - Internationalization (if applicable)

6. **Risk Analysis**
   - Identify failure modes
   - Assess impact and likelihood
   - Validate monitoring and alerting
   - Verify rollback procedures

Deliver comprehensive test report with:
- Test results (passed/failed)
- Quality metrics
- Risk assessment
- Issues categorized by severity
- Recommendations for production readiness
```

#### Security Validation

Use the Task tool to launch the **secure-by-design-engineer** agent:

```
Conduct comprehensive security assessment for: [USER INPUT FEATURE]

Code and Infrastructure:
[Include implementation code, infrastructure configs, dependencies]

Security Validation Requirements:

1. **Code Security Review**
   - Authentication and authorization implementation
   - Input validation and sanitization
   - SQL/NoSQL injection prevention
   - XSS/CSRF prevention
   - Secure error handling (no sensitive data exposure)

2. **Dependency Security**
   - Scan for known vulnerabilities (CVEs)
   - Check dependency licenses
   - Validate supply chain security
   - Review SBOM (Software Bill of Materials)

3. **Infrastructure Security**
   - Secrets management validation
   - Network security configuration
   - Access controls and IAM
   - Encryption at rest and in transit
   - Container security (if applicable)

4. **Compliance**
   - GDPR compliance (if handling EU data)
   - SOC2 requirements
   - Industry-specific regulations
   - Data privacy requirements

5. **Threat Modeling**
   - Identify attack vectors
   - Assess exploitability
   - Validate security controls
   - Test defense in depth

6. **Penetration Testing** (for critical features)
   - Manual security testing
   - Automated vulnerability scanning
   - Authentication bypass attempts
   - Authorization escalation tests

Deliver comprehensive security report with:
- Security findings by severity (Critical/High/Medium/Low)
- Vulnerability details with remediation steps
- Compliance status
- Risk assessment
- Security gate approval status (Pass/Fail)
```

### Phase 2: Documentation (After validation results available)

Use the Task tool to launch the **tech-writer** agent:

```
Create comprehensive documentation for: [USER INPUT FEATURE]

Context:
[Include feature description, implementation details, API specs, test results, security findings]

Documentation Deliverables:

1. **API Documentation** (if API changes)
   - Endpoint documentation
   - Request/response examples
   - Authentication requirements
   - Error codes and messages
   - Rate limiting and quotas

2. **User Documentation**
   - Feature overview and benefits
   - Getting started guide
   - Step-by-step tutorials
   - Screenshots/diagrams
   - Troubleshooting guide

3. **Technical Documentation**
   - Architecture overview
   - Component documentation
   - Configuration options
   - Deployment instructions
   - Monitoring and alerting setup

4. **Release Notes**
   - Feature summary
   - Breaking changes (if any)
   - Migration guide (if needed)
   - Known limitations
   - Bug fixes

5. **Internal Documentation**
   - Code comments for complex logic
   - Runbooks for operations
   - Incident response procedures
   - Rollback procedures

Ensure all documentation is:
- Accurate and up-to-date
- Clear and audience-appropriate
- Well-formatted with proper structure
- Accessible (alt text, headings, etc.)
- Ready for publication
```

### Phase 3: Release Management (Final gate with Human Approval)

Use the Task tool to launch the **release-manager** agent:

```
Conduct release readiness assessment for: [USER INPUT FEATURE]

Validation Artifacts:
[Include QA test report, security assessment, documentation, code review results]

Release Management Requirements:

1. **Pre-Release Validation**
   - Review all quality gates status
   - Verify all critical/high issues resolved
   - Confirm test coverage meets threshold
   - Validate security scan passed
   - Check documentation completeness

2. **Release Planning**
   - Determine release type (major/minor/patch/hotfix)
   - Plan deployment strategy (canary/blue-green/rolling)
   - Schedule deployment window
   - Identify stakeholders for approval
   - Prepare rollback plan

3. **Risk Assessment**
   - Identify deployment risks
   - Assess user impact
   - Evaluate rollback complexity
   - Review monitoring readiness

4. **Release Checklist**
   - [ ] All CI/CD pipelines passing
   - [ ] Code reviews completed and approved
   - [ ] Test coverage meets minimum threshold
   - [ ] No critical or high severity bugs/security issues
   - [ ] Performance benchmarks met
   - [ ] Documentation updated
   - [ ] Monitoring and alerts configured
   - [ ] Rollback plan tested
   - [ ] Stakeholders notified

5. **Human Approval Request**
   Prepare approval request with:
   - Release summary
   - Quality metrics
   - Security status
   - Risk assessment
   - Deployment plan
   - **REQUEST EXPLICIT HUMAN APPROVAL** before proceeding

6. **Post-Approval Actions**
   - Coordinate deployment execution
   - Monitor deployment progress
   - Validate post-deployment health
   - Document release outcome

Deliver release readiness report with clear go/no-go recommendation and human approval checkpoint.
```

### Deliverables

- Comprehensive QA test report
- Security assessment report
- Complete documentation package
- Release readiness assessment
- **Human approval for production release**
- Deployment plan and runbooks
