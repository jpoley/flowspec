---
id: task-180
title: Update Flowspec Slash Commands to Output Artifacts at Standard Locations
status: To Do
assignee: []
created_date: '2025-11-30 20:07'
updated_date: '2025-11-30 20:08'
labels:
  - workflow-artifacts
  - critical
dependencies: []
priority: high
---

<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Summary
Update all /flowspec:* slash commands to output their artifacts at the standardized locations defined in the workflow specification.

## Artifact Output Mapping

| Command | Output Artifact | Location |
|---------|-----------------|----------|
| /flowspec:assess | Assessment Report | ./docs/assess/{feature}-assessment.md |
| /flowspec:specify | PRD | ./docs/prd/{feature}.md |
| /flowspec:specify | Backlog Tasks | ./backlog/tasks/*.md |
| /flowspec:research | Research Report | ./docs/research/{feature}-research.md |
| /flowspec:research | Business Validation | ./docs/research/{feature}-validation.md |
| /flowspec:plan | Architecture Design | ./docs/adr/ADR-{NNN}-{slug}.md |
| /flowspec:plan | Platform Design | ./docs/platform/{feature}-platform.md |
| /flowspec:implement | Source Code | ./src/ or project-specific |
| /flowspec:implement | Tests | ./tests/ |
| /flowspec:implement | AC Coverage | ./tests/ac-coverage.json |
| /flowspec:validate | QA Report | ./docs/qa/{feature}-qa-report.md |
| /flowspec:validate | Security Report | ./docs/security/{feature}-security.md |
| /flowspec:operate | Deployment Manifest | ./deploy/ or ./k8s/ |

## Command Template Updates

Each slash command template (.claude/commands/flowspec/*.md) must:

1. **Define output path explicitly**:
```markdown
## Output Artifacts
- Primary: ./docs/prd/{FEATURE_NAME}.md
- Secondary: ./backlog/tasks/*.md
```

2. **Use consistent feature naming**:
```markdown
Set FEATURE_NAME from input or derive from context
Slug format: lowercase, hyphens (e.g., user-authentication)
```

3. **Verify artifact creation**:
```markdown
After completing work, verify:
- [ ] Primary artifact exists at expected path
- [ ] Artifact contains all required sections
- [ ] Artifact follows template structure
```

## Acceptance Criteria
- [ ] AC1: Update /flowspec:assess to output to ./docs/assess/{feature}-assessment.md
- [ ] AC2: Update /flowspec:specify to output PRD to ./docs/prd/{feature}.md
- [ ] AC3: Update /flowspec:research to output to ./docs/research/
- [ ] AC4: Update /flowspec:plan to output ADRs to ./docs/adr/ADR-{NNN}-{slug}.md
- [ ] AC5: Update /flowspec:implement to generate ./tests/ac-coverage.json
- [ ] AC6: Update /flowspec:validate to output reports to ./docs/qa/ and ./docs/security/
- [ ] AC7: Add artifact path resolution logic to handle feature name derivation
- [ ] AC8: Add artifact existence verification step to each command exit

## Dependencies
- task-172 (Workflow Artifacts Specification)
- task-179 (Directory Structure Scaffolding)
<!-- SECTION:NOTES:END -->
