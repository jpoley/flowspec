# Archived Build Documentation

This directory contains build and development documentation that has been archived due to containing deprecated command references.

## Archived Files

These files reference `/flow:operate` or `/spec:*` commands which have been removed:

- `upgrade-repo-visual-summary.md` - Visual summary of upgrade-repo work
- `upgrade-repo-architecture-summary.md` - Architecture summary
- `fix-flowspec-plan.md` - Planning document for flowspec fixes
- `dec31-task-review.md` - Task review from Dec 31
- `command-mapping-review.md` - Command mapping analysis

## Current Commands

The current workflow uses only `/flow:*` commands:
- `/flow:assess` - Evaluate task complexity
- `/flow:specify` - Create specifications
- `/flow:research` - Market/technical research
- `/flow:plan` - Architecture design
- `/flow:implement` - Implementation
- `/flow:validate` - QA and security validation

Deployment is now an "outer loop" concern handled by CI/CD pipelines.
Use `/ops:*` commands for operational tasks.

## Archived Date

2025-01-07
