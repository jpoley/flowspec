---
id: task-451
title: 'archon-inspired: Add ''Loop Classification'' section to templates'
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-12 01:00'
updated_date: '2025-12-12 01:41'
labels:
  - archon-inspired
  - architecture
  - templates
  - context-engineering
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add explicit loop classification to PRD and PRP templates to make inner vs outer loop behavior clear for each feature.

**Targets**: 
- PRD template
- PRP template

**Purpose**: Make it obvious which parts of the workflow should be handled by inner-loop (implementation-focused) vs outer-loop (planning-focused) agents
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Loop Classification section added to PRD template
- [x] #2 Loop Classification section added to PRP template
- [x] #3 Section contains: Inner Loop Responsibilities (fast, implementation tasks)
- [x] #4 Section contains: Outer Loop Responsibilities (planning, risk analysis)
- [x] #5 Section includes examples of task classification
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added Loop Classification section to PRD template to match PRP template.

**PRD Template Changes** (`templates/prd-template.md`, lines 214-244):
- Added Loop Classification section after Feature Validation Plan
- Inner Loop Responsibilities subsection with 5 example tasks
- Outer Loop Responsibilities subsection with 5 example tasks
- HTML comments explaining each section
- Reference links to inner/outer loop documentation

**PRP Template** (`templates/docs/prp/prp-base-flowspec.md`, lines 187-206):
- Already had LOOP CLASSIFICATION section from task-447
- Contains Inner Loop and Outer Loop subsections with examples

**Consistency:**
- Both use checkbox list format for tasks
- Both include concrete examples
- Both explain inner loop = fast implementation, outer loop = planning/review
- PRD has additional reference links to documentation
<!-- SECTION:NOTES:END -->
