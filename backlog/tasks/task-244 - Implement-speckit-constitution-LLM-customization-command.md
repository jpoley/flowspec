---
id: task-244
title: 'Implement /speckit:constitution LLM customization command'
status: In Progress
assignee:
  - '@galway'
created_date: '2025-12-03 02:40'
updated_date: '2025-12-04 17:20'
labels:
  - constitution-cleanup
dependencies:
  - task-241
  - task-243
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create slash command that analyzes repo and customizes constitution template with repo-specific details
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Create .claude/commands/speckit/constitution.md slash command
- [x] #2 Command scans repo for: languages, frameworks, CI configs, test setup, linting tools
- [x] #3 Command detects existing patterns: security scanning, code review requirements, etc.
- [x] #4 Command customizes selected tier template with repo-specific findings
- [x] #5 Output includes NEEDS_VALIDATION markers on auto-generated sections
- [x] #6 Command outputs clear message: Constitution generated - please review and validate
- [x] #7 Supports --tier {light|medium|heavy} flag to override detection

- [x] #8 Command outputs validation checklist after generation
- [x] #9 Command supports --tier override flag
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented /speckit:constitution command that analyzes repository and customizes constitution templates.

Key Features:
- Repository analysis for languages, frameworks, testing, linting, CI/CD, security tools
- Auto-detection of appropriate tier (light/medium/heavy) based on project complexity
- Support for --tier {light|medium|heavy} flag to override auto-detection
- Template customization with detected values (project name, tech stack, tools, date)
- NEEDS_VALIDATION markers on auto-generated sections
- Comprehensive validation checklist output
- Detailed next steps guidance

Detection Capabilities:
- Languages: Python, TypeScript/JavaScript, Go, Rust, Java
- Frameworks: FastAPI, Flask, React, Next.js, Gin, Actix, Spring, etc.
- Testing: pytest, jest, vitest, Go testing, Rust testing, JUnit
- Linting: ruff, eslint, prettier, golangci-lint, clippy
- CI/CD: GitHub Actions, GitLab CI, Jenkins, CircleCI
- Security: Semgrep, Trivy, Dependabot, Renovate
- Code Review: PR templates, CODEOWNERS

Tier Auto-Detection:
- Light: 3 or fewer indicators (minimal controls)
- Medium: 4-7 indicators (balanced governance)
- Heavy: 8+ indicators (full production-grade)

Files Created:
- templates/commands/speckit/constitution.md (main command)
- .claude/commands/speckit/constitution.md (symlink)

Validation:
- Command follows existing /jpspec command patterns
- Supports --tier override flag as required
- Outputs validation checklist as required
- Includes NEEDS_VALIDATION markers as required
<!-- SECTION:NOTES:END -->
