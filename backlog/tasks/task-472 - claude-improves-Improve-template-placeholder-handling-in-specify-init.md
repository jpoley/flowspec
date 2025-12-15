---
id: task-472
title: 'claude-improves: Improve template placeholder handling in specify init'
status: To Do
assignee:
  - '@kinsale'
created_date: '2025-12-12 01:15'
updated_date: '2025-12-15 01:49'
labels:
  - claude-improves
  - cli
  - specify-init
  - templates
  - phase-1
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Constitution and other templates contain unresolved [PLACEHOLDER] markers:
- [PROJECT_NAME]
- [LANGUAGES_AND_FRAMEWORKS]
- [LINTING_TOOLS]
- [DATE]

These should be either:
1. Auto-detected from project files
2. Prompted during init
3. Clearly marked as TODO for manual completion
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 PROJECT_NAME auto-detected from pyproject.toml, package.json, or directory name
- [ ] #2 LANGUAGES_AND_FRAMEWORKS detected from project file presence
- [ ] #3 LINTING_TOOLS detected from config files (ruff.toml, .eslintrc, etc.)
- [ ] #4 DATE automatically populated with current date
- [ ] #5 Any remaining placeholders clearly marked with TODO comments
- [ ] #6 Add --interactive flag to prompt for all values
<!-- AC:END -->
