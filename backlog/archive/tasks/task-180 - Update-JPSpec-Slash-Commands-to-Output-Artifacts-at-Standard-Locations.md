---
id: task-180
title: Update JPSpec Slash Commands to Output Artifacts at Standard Locations
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
Update all /jpspec:* slash commands to output their artifacts at the standardized locations defined in the workflow specification.

## Artifact Output Mapping

| Command | Output Artifact | Location |
|---------|-----------------|----------|
| /jpspec:assess | Assessment Report | ./docs/assess/{feature}-assessment.md |
| /jpspec:specify | PRD | ./docs/prd/{feature}.md |
| /jpspec:specify | Backlog Tasks | ./backlog/tasks/*.md |
| /jpspec:research | Research Report | ./docs/research/{feature}-research.md |
| /jpspec:research | Business Validation | ./docs/research/{feature}-validation.md |
| /jpspec:plan | Architecture Design | ./docs/adr/ADR-{NNN}-{slug}.md |
| /jpspec:plan | Platform Design | ./docs/platform/{feature}-platform.md |
| /jpspec:implement | Source Code | ./src/ or project-specific |
| /jpspec:implement | Tests | ./tests/ |
| /jpspec:implement | AC Coverage | ./tests/ac-coverage.json |
| /jpspec:validate | QA Report | ./docs/qa/{feature}-qa-report.md |
| /jpspec:validate | Security Report | ./docs/security/{feature}-security.md |
| /jpspec:operate | Deployment Manifest | ./deploy/ or ./k8s/ |

## Command Template Updates

Each slash command template (.claude/commands/jpspec/*.md) must:

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
- [ ] AC1: Update /jpspec:assess to output to ./docs/assess/{feature}-assessment.md
- [ ] AC2: Update /jpspec:specify to output PRD to ./docs/prd/{feature}.md
- [ ] AC3: Update /jpspec:research to output to ./docs/research/
- [ ] AC4: Update /jpspec:plan to output ADRs to ./docs/adr/ADR-{NNN}-{slug}.md
- [ ] AC5: Update /jpspec:implement to generate ./tests/ac-coverage.json
- [ ] AC6: Update /jpspec:validate to output reports to ./docs/qa/ and ./docs/security/
- [ ] AC7: Add artifact path resolution logic to handle feature name derivation
- [ ] AC8: Add artifact existence verification step to each command exit

## Dependencies
- task-172 (Workflow Artifacts Specification)
- task-179 (Directory Structure Scaffolding)
<!-- SECTION:NOTES:END -->
