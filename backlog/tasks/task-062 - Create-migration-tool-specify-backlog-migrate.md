---
id: task-062
title: Create migration tool (specify backlog migrate) for existing tasks.md files
status: Done
assignee:
  - backend-engineer
created_date: '2025-11-25 00:24'
completed_date: '2025-11-25 00:52'
labels:
  - US2
  - migration
  - P1
  - migrated
dependencies: []
---

## Migration Tool Complete

Implemented `specify backlog migrate` command for converting legacy tasks.md to Backlog.md format.

### Features
- Full data preservation (IDs, labels, status, dependencies)
- Automatic backup creation
- Dry-run mode for preview
- Force overwrite option
- Comprehensive migration summary

### Files Modified
- `src/specify_cli/__init__.py` - Added migrate command
- `CHANGELOG.md` - Documented changes
- `README.md` - Updated command reference

### Production Ready
All self-critique criteria met with robust error handling and safety features.


