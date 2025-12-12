---
id: task-448
title: 'archon-inspired: Add ''All Needed Context'' section to PRD template'
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-12 01:00'
updated_date: '2025-12-12 01:34'
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
Extend the PRD template used by /flow:specify to include a structured 'All Needed Context' section that is easy to parse and reuse by other commands.

**Target**: Update existing PRD template (prd-template.md or equivalent)

**Purpose**: Enable machine-parsing of context for /flow:generate-prp, /flow:implement, and /flow:validate commands
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 PRD template includes 'All Needed Context' section
- [x] #2 Section contains: Code Files subsection with file paths and purposes
- [x] #3 Section contains: Docs/Specs subsection with links
- [x] #4 Section contains: Examples subsection with example files and relevance
- [x] #5 Section contains: Gotchas/Prior Failures subsection
- [x] #6 Section contains: External Systems/APIs subsection
- [x] #7 Section uses consistent markdown structure for parsing
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read existing prd-template.md
2. Identify insertion point for new section
3. Add 'All Needed Context' section with all subsections
4. Use consistent table format for machine parsing
5. Add explanatory comments
6. Verify all 7 acceptance criteria met
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added 'All Needed Context' section to PRD template for machine-parseable context.

**File Modified:**
- `templates/prd-template.md`

**New Section Added (after Dependencies, before Risks):**
- **All Needed Context** - Header with machine-parsing note

**Subsections (all with consistent table format):**
1. **Code Files** - Table: File Path | Purpose | Read Priority
2. **Docs / Specs** - Table: Document | Link | Key Sections  
3. **Examples** - Table: Example | Location | Relevance
4. **Gotchas / Prior Failures** - Table: Gotcha | Impact | Mitigation | Source
5. **External Systems / APIs** - Table: System | Type | Documentation | Notes

**Machine-Parsing Features:**
- Consistent H3 heading structure for each subsection
- All data in table format with fixed columns
- HTML comments document expected format for each table
- Placeholder variables use {variable} syntax
- Priority/type values are enumerated (High/Medium/Low, REST/GraphQL/gRPC)

**Consumers:**
- `/flow:generate-prp` - Extracts context for PRP creation
- `/flow:implement` - Loads context for implementation agents
- `/flow:validate` - Uses context for validation setup
<!-- SECTION:NOTES:END -->
