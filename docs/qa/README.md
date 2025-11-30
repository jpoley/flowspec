# QA Reports

This directory contains Quality Assurance reports generated during feature validation.

## Purpose

QA reports document test results and quality verification:
- **Test Summary**: Overview of test execution and results
- **Coverage**: Code coverage metrics
- **Test Cases**: Detailed test scenarios and results
- **Defects**: Issues found during testing
- **Sign-off**: QA approval status

## Structure

Each QA report is named `qa-{feature-name}.md` and follows the template in `../../templates/qa-report-template.md`.

## Usage

QA reports are created by the `/jpspec:validate` workflow (QA Agent):

```bash
/jpspec:validate
```

QA validation is a required gate before features can be released.

## Related Workflows

- **Created By**: `/jpspec:validate` workflow
- **Prerequisites**: Implementation must be complete
- **Templates**: See `templates/qa-report-template.md`
