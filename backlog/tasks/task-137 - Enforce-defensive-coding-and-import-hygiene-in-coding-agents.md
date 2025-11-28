---
id: task-137
title: Enforce defensive coding and import hygiene in coding agents
status: Done
assignee:
  - '@claude'
created_date: '2025-11-28 22:17'
updated_date: '2025-11-28 22:19'
labels:
  - quality
  - agents
  - python
  - defensive-coding
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update /jpspec:implement coding agents to enforce defensive coding practices including input validation, unused import detection, and language-specific quality checks. Python has been causing issues with unused imports and missing validation - prioritize Python-specific rules.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 #1 Add 'Code Hygiene' section to Backend Engineer agent requiring: remove unused imports before completion, run language linter (ruff for Python, golangci-lint for Go, eslint for TS)
- [x] #2 #2 Add 'Defensive Coding' section requiring: validate all function inputs at boundaries, use type hints/annotations, handle None/null explicitly, validate external data (API responses, file contents, env vars)
- [x] #3 #3 Add Python-specific rules: run 'ruff check --select F401' for unused imports, use Pydantic or dataclasses for data validation, require type hints on all public functions
- [x] #4 #4 Add Go-specific rules: run 'go vet' and 'staticcheck', use explicit error checking (no ignored errors), validate struct fields
- [x] #5 #5 Add TypeScript-specific rules: run 'tsc --noEmit' for type checking, use Zod or similar for runtime validation, enable strict mode
- [x] #6 #6 Update Backend Code Reviewer agent to explicitly check for: unused imports, missing input validation, unhandled edge cases, type safety violations
- [x] #7 #7 Add pre-completion checklist to agents: 'Before marking complete, verify: no unused imports, all inputs validated, edge cases handled, types annotated'
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add Code Hygiene section to Backend Engineer agent prompt
2. Add Defensive Coding section with input validation requirements
3. Add language-specific validation rules (Python, Go, TypeScript)
4. Update Backend Code Reviewer to check for these issues
5. Add pre-completion checklist to all coding agents
6. Test changes and create PR
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated /jpspec:implement command with comprehensive defensive coding requirements:

**Backend Engineer Agent:**
- Added Code Hygiene Requirements section (mandatory unused import removal)
- Added Defensive Coding Requirements section (input validation, type safety, error handling)
- Added Language-Specific Rules for Python, Go, and TypeScript with examples
- Added Pre-Completion Checklist (blocking) to verify all requirements

**Backend Code Reviewer Agent:**
- Added Code Hygiene Checks section (BLOCK MERGE for violations)
- Added Defensive Coding Violations section (BLOCK MERGE for violations)
- Updated review conduct to prioritize hygiene and defensive coding
- Added explicit Critical flags for common violations

**Python-specific (critical priority):**
- ruff check --select F401,F841 for unused imports/variables
- Required type hints on all public functions
- Pydantic/dataclasses for validation
- Explicit None handling with Optional[T]
<!-- SECTION:NOTES:END -->
