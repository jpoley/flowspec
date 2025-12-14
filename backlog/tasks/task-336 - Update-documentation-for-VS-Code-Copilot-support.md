---
id: task-336
title: Update documentation for VS Code Copilot support
status: Done
assignee:
  - '@muckross'
created_date: '2025-12-08 22:28'
updated_date: '2025-12-14 20:17'
labels:
  - docs
  - 'workflow:Planned'
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document how flowspec supports both Claude Code CLI and VS Code Copilot with setup instructions and screenshots
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README.md mentions both .claude/commands/ and .github/agents/ directories
- [x] #2 CLAUDE.md documents sync script usage and workflow
- [x] #3 New guide created: docs/guides/vscode-copilot-setup.md with setup steps
- [ ] #4 Setup guide includes screenshots of Copilot Chat command picker
- [x] #5 Troubleshooting section added for common sync issues
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Complete (2025-12-14)

1. **README.md** (AC#1): Added VS Code Copilot Chat to supported agents table, added integration section, updated file structure

2. **CLAUDE.md** (AC#2): Added VS Code Copilot Agent Sync section with script usage

3. **Setup Guide** (AC#3): Created `docs/guides/vscode-copilot-setup.md` with:
   - Prerequisites and directory structure
   - Using agents via @ mention, command picker, handoffs
   - Sync workflow (automatic and manual)
   - Troubleshooting section (AC#5)

4. **Screenshots** (AC#4): Not included - requires manual VS Code interaction. Guide describes how to access command picker.
<!-- SECTION:NOTES:END -->
