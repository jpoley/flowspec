---
id: task-174
title: Implement ADR Requirement Gate with Transition Validation
status: To Do
assignee: []
created_date: '2025-11-30 21:31'
labels:
  - workflow-artifacts
  - critical
dependencies: []
priority: high
---

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Summary
Implement Architecture Decision Records (ADRs) as required output artifacts from /jpspec:plan with configurable transition validation.

## ADR Artifact Specification

### Location
- Directory: `./docs/adr/`
- Filename: `ADR-{NNN}-{title-slug}.md`
- Example: `./docs/adr/ADR-001-authentication-strategy.md`

### Transition Definition
```yaml
planned_to_implementing:
  from: "Researched"
  to: "Planned"
  via: "plan"
  input_artifacts:
    - type: prd
      path: ./docs/prd/{feature}.md
      required: true
    - type: research_report
      path: ./docs/research/{feature}-research.md
      required: false  # Research is optional
  output_artifacts:
    - type: adr
      path: ./docs/adr/ADR-{NNN}-{slug}.md
      required: true
      multiple: true  # Can have multiple ADRs per feature
    - type: platform_design
      path: ./docs/platform/{feature}-platform.md
      required: false
  validation: NONE  # Default, configurable to KEYWORD["ADR_APPROVED"] or PULL_REQUEST
```

### Validation Modes

| Mode | Behavior |
|------|----------|
| `NONE` | ADR(s) created, transition proceeds immediately |
| `KEYWORD["ADR_APPROVED"]` | User must type "ADR_APPROVED" to proceed |
| `PULL_REQUEST` | ADR(s) must be in a merged PR to proceed |

### ADR Structure (Michael Nygard Format)
```markdown
# ADR-{NNN}: {Title}

## Status
{Proposed | Accepted | Deprecated | Superseded by ADR-XXX}

## Context
{Problem statement and forces at play}

## Decision
{The decision made and rationale}

## Consequences
### Positive
- {Benefit 1}
- {Benefit 2}

### Negative
- {Tradeoff 1}
- {Tradeoff 2}

## Alternatives Considered
### Alternative 1: {Name}
- Pros: ...
- Cons: ...
- Why rejected: ...
```

## Acceptance Criteria
- [ ] AC1: Create ADR template at templates/adr-template.md following Nygard format
- [ ] AC2: Update /jpspec:plan to output ADRs to ./docs/adr/ADR-{NNN}-{slug}.md
- [ ] AC3: Add ADR existence check before transition to "Planned" state
- [ ] AC4: Implement ADR structural validation (required sections present)
- [ ] AC5: Support validation: NONE (default)
- [ ] AC6: Support validation: KEYWORD["<string>"] mode
- [ ] AC7: Support validation: PULL_REQUEST mode
- [ ] AC8: Support multiple ADRs per feature (ADR-001, ADR-002, etc.)
- [ ] AC9: Implement ADR numbering auto-increment

## Dependencies
- task-172 (Workflow Transition Validation Schema)
- task-173 (PRD Requirement Gate)
<!-- SECTION:NOTES:END -->
