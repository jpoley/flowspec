# Security Reports

This directory contains security assessment and validation reports.

## Purpose

Security reports document security analysis and compliance:
- **Vulnerabilities**: Security issues identified and their severity
- **Compliance**: Adherence to security standards and policies
- **Threat Model**: Security threats and mitigations
- **Dependencies**: Third-party dependency security status
- **Recommendations**: Security improvements and remediation steps

## Structure

Each security report is named `security-{feature-name}.md` and follows the template in `../../templates/security-report-template.md`.

## Usage

Security reports are created by the `/jpspec:validate` workflow (Security Agent):

```bash
/jpspec:validate
```

Security validation is a required gate before features can be released.

## Related Workflows

- **Created By**: `/jpspec:validate` workflow
- **Prerequisites**: Implementation must be complete
- **Templates**: See `templates/security-report-template.md`
