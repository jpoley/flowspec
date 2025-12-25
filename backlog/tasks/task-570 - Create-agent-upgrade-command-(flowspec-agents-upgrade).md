---
id: task-570
title: Create agent upgrade command (flowspec agents upgrade)
status: To Do
assignee: []
created_date: '2025-12-25 20:17'
labels:
  - implementation
  - cli
  - agents
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement CLI command to upgrade agents independently. Download latest agents release, extract to .github/agents/, update local version tracking.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 flowspec agents upgrade command implemented
- [ ] #2 Command downloads latest release from GitHub
- [ ] #3 Agents extracted to correct location
- [ ] #4 Local version tracking updated
- [ ] #5 Dry-run mode supported (--dry-run)
- [ ] #6 Tests pass for upgrade command
<!-- AC:END -->
