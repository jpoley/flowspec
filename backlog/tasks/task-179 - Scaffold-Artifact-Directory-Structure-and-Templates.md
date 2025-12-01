---
id: task-179
title: Scaffold Artifact Directory Structure and Templates
status: Done
assignee: []
created_date: '2025-11-30 21:33'
updated_date: '2025-12-01 01:53'
labels:
  - workflow-artifacts
  - critical
dependencies: []
priority: high
---

<!-- AC:BEGIN -->
- [x] AC1: Create docs/assess/ with README
- [x] AC2: Create docs/prd/ with README
- [x] AC3: Create docs/research/ with README
- [x] AC4: Create docs/adr/ with README and template.md
- [x] AC5: Create docs/platform/ with README
- [x] AC6: Create docs/qa/ with README
- [x] AC7: Create docs/security/ with README
- [x] AC8: Create all templates in templates/ directory
- [x] AC9: Update `specify init` to scaffold these directories
- [x] AC10: Add directory structure to CLAUDE.md documentation
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Summary
Create the standard directory structure and templates for all workflow artifacts.

## Directory Structure

```
project/
├── docs/
│   ├── assess/                 # Assessment reports
│   │   ├── .gitkeep
│   │   └── README.md
│   ├── prd/                    # Product Requirements Documents
│   │   ├── .gitkeep
│   │   └── README.md
│   ├── research/               # Research and validation reports
│   │   ├── .gitkeep
│   │   └── README.md
│   ├── adr/                    # Architecture Decision Records
│   │   ├── .gitkeep
│   │   ├── README.md
│   │   └── template.md
│   ├── platform/               # Platform design docs
│   │   ├── .gitkeep
│   │   └── README.md
│   ├── qa/                     # QA reports
│   │   ├── .gitkeep
│   │   └── README.md
│   └── security/               # Security reports
│       ├── .gitkeep
│       └── README.md
├── templates/
│   ├── assessment-template.md
│   ├── prd-template.md
│   ├── research-template.md
│   ├── business-validation-template.md
│   ├── adr-template.md
│   ├── qa-report-template.md
│   └── security-report-template.md
└── tests/
    └── ac-coverage.json        # Generated
```

## Template Contents

### Assessment Template
- Feature name, description
- Recommendation (Full/Light/Skip)
- Complexity, Risk, Impact scores
- Next steps

### PRD Template
- Executive Summary
- Problem Statement
- User Stories with ACs
- Requirements (Functional/Non-Functional)
- Success Metrics
- Dependencies, Risks, Out of Scope

### ADR Template (Nygard Format)
- Status
- Context
- Decision
- Consequences (Positive/Negative)
- Alternatives Considered

### QA Report Template
- Test Summary
- Test Results by Category
- Coverage Metrics
- Known Issues
- Recommendations

### Security Report Template
- Security Assessment Summary
- Vulnerabilities Found
- Compliance Checklist
- Recommendations
- Sign-off

Completed via PR #137
<!-- SECTION:NOTES:END -->
