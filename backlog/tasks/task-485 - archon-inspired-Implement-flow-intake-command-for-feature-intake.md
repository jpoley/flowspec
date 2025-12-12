---
id: task-485
title: 'archon-inspired: Implement /flow:intake command for feature intake'
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-12 01:45'
updated_date: '2025-12-12 01:46'
labels:
  - archon-inspired
  - commands
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a new /flow:intake command that processes INITIAL-style documents and bootstraps the feature workflow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Command file created
- [x] #2 Accepts path argument
- [x] #3 Parses FEATURE section
- [x] #4 Parses EXAMPLES, DOCUMENTATION sections
- [x] #5 Creates backlog task
- [x] #6 Creates task memory file
- [x] #7 Memory file complete
- [x] #8 Documented in CLAUDE.md
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented /flow:intake command for processing INITIAL feature intake documents.

**Files Created:**
- `templates/commands/flow/intake.md` - Command implementation
- `.claude/commands/flow/intake.md` - Symlink to template

**Files Modified:**
- `CLAUDE.md` - Added /flow:intake to slash commands section

**Command Features:**
1. Accepts path argument to INITIAL document
2. Parses FEATURE section for task title/description
3. Parses EXAMPLES, DOCUMENTATION, OTHER CONSIDERATIONS sections
4. Creates backlog task using backlog CLI
5. Creates comprehensive memory file at backlog/memory/<task-id>.md
6. Memory file includes: What/Why, Constraints, Examples, Docs, Initial gotchas
7. Outputs summary with next steps (assess, specify, plan)

**Usage:**
```bash
/flow:intake docs/features/user-auth-initial.md
```

**Workflow Integration:**
This command bridges INITIAL documents to the SDD workflow, enabling:
- INITIAL doc → /flow:intake → backlog task + memory → /flow:assess → /flow:specify → ...
<!-- SECTION:NOTES:END -->
