---
id: task-564
title: Implement agent packaging script
status: To Do
assignee: []
created_date: '2025-12-25 20:17'
labels:
  - implementation
  - packaging
  - agents
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create .github/workflows/scripts/package-agents.sh to build agent-only archives. Package all .github/agents/ files with metadata into flowspec-agents-vX.Y.Z.zip.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 package-agents.sh script created
- [ ] #2 Script packages all 49 agent files
- [ ] #3 Metadata files included (agents-version.json, claude-code-version.txt, README)
- [ ] #4 Archive size < 1MB
- [ ] #5 Package structure validated
<!-- AC:END -->
