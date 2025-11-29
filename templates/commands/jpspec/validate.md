---
mode: agent
description: Execute validation and quality assurance using QA, security, documentation, and release management agents.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

This command executes comprehensive validation using multiple specialized agents:

1. **Q/A Tester Agent**: Quality guardian for API and contract testing
   - Performs comprehensive API testing
   - Executes contract testing to ensure API compatibility
   - Can use SRE and debugging tools (Brendan Gregg methodology)
   - Validates functional and non-functional requirements
   - Ensures quality gates are met

2. **Cyber Agent**: Secure by design and security tooling
   - Conducts security assessments
   - Implements secure by design principles
   - Uses security scanning and testing tools
   - Identifies vulnerabilities and security risks
   - Validates security controls and compliance

3. **Tech Writer Agent**: Documentation for blogs, documents, and well-formatted content
   - Creates comprehensive documentation
   - Formats content suitable for target audience
   - Writes technical blogs and user guides
   - Ensures documentation quality and accuracy
   - Maintains documentation standards

4. **Release Manager Agent**: Validates and merges code, manages promotions
   - Reviews all validation results
   - Validates code is ready for release
   - Manages code merges and version control
   - Coordinates release promotion process
   - **Requires Human Approval** for critical decisions

## Execution Flow

1. Parse user input and load implementation artifacts

2. **Quality Assurance Testing**:
   - Dispatch Q/A Tester agent
   - Execute API and contract tests
   - Perform integration testing
   - Run performance and load tests
   - Use SRE debugging tools for deep analysis
   - Generate test reports

3. **Security Validation**:
   - Dispatch Cyber agent
   - Run security scans and penetration tests
   - Validate secure coding practices
   - Check for vulnerabilities and compliance issues
   - Generate security assessment report

4. **Documentation**:
   - Dispatch Tech Writer agent
   - Create/update technical documentation
   - Write user guides and API documentation
   - Format content for appropriate audiences
   - Ensure documentation completeness

5. **Release Validation**:
   - Dispatch Release Manager agent
   - Review all test and security results
   - Validate code quality and readiness
   - **Request Human Approval** for release decision
   - Coordinate merge and promotion activities

6. **Output**:
   - Complete test suite results
   - Security assessment report
   - Comprehensive documentation
   - Release readiness assessment
   - Human approval checkpoints

## Notes

- This command is a placeholder for future agent implementation
- Full Q/A, Cyber, Tech Writer, and Release Manager agent integration will be completed in a future task
- Release Manager requires explicit human approval for critical decisions
