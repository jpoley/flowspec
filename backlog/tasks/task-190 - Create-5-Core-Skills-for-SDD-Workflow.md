---
id: task-190
title: Create 5 Core Skills for SDD Workflow
status: Done
assignee:
  - '@galway'
created_date: '2025-12-01 05:04'
updated_date: '2025-12-04 22:57'
labels:
  - claude-code
  - skills
  - sdd-workflow
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement 5 core Skills for SDD workflow automation: pm-planner, architect, qa-validator, security-reviewer, and sdd-methodology. Skills enable Claude to automatically invoke domain expertise based on task context.

Cross-reference: See docs/prd/claude-capabilities-review.md Section 2.3 for Skills gap analysis and docs/prd/workflow-engine-review.md for workflow context.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pm-planner skill created with SKILL.md, task templates, and atomic task examples

- [x] #2 architect skill created with ADR templates and architecture decision patterns
- [x] #3 qa-validator skill created with test plan templates and QA checklists
- [x] #4 security-reviewer skill created with SLSA requirements and security review checklists
- [x] #5 sdd-methodology skill created with SDD workflow guidance and best practices
- [x] #6 All skills have proper frontmatter (name, description) for automatic discovery
- [x] #7 Skills documented in CLAUDE.md hooks section
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
All 5 core SDD skills implemented and documented:\n\n**Skills created** (`.claude/skills/`):\n1. pm-planner - task management, AC writing\n2. architect - ADRs, system design\n3. qa-validator - test plans, quality gates\n4. security-reviewer - SLSA, vulnerability assessment\n5. sdd-methodology - workflow guidance\n\n**Features**:\n- Each skill has SKILL.md with proper frontmatter (name, description)\n- Descriptions enable automatic model invocation\n- Templates and examples included\n- Skills documented in memory/claude-skills.md\n- CLAUDE.md imports skill documentation via @import
<!-- SECTION:NOTES:END -->
