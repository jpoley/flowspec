# CRITICAL: ALWAYS REBASE BEFORE PR

**Date**: 2025-12-26
**Severity**: CRITICAL - Workflow Violation
**PR**: #1060 (created with merge conflicts - FAILURE)

## What Happened

Created PR #1060 without rebasing against main. The branch was stale, resulting in merge conflicts. This is a 100% failure regardless of how good the code changes were.

## Root Cause

1. Saw closed PR #1053, mentally entered "fix mode" instead of "full workflow mode"
2. Skipped Phase 1.3 (Ensure Branch is Rebased) of /flow:submit-n-watch-pr
3. Tunnel vision on Copilot comment fixes - forgot the foundation
4. Misread workflow: "closed PR" should mean "start from Phase 1", not "skip to Phase 3"

## The Rule (NON-NEGOTIABLE)

**BEFORE ANY `gh pr create` OR `git push` FOR A PR:**

```bash
git fetch origin main
BEHIND=$(git rev-list --count HEAD..origin/main)
if [ "$BEHIND" -gt 0 ]; then
    # STOP. REBASE FIRST. NO EXCEPTIONS.
    git rebase origin/main
    # Resolve any conflicts
    # Then and ONLY then proceed
fi
```

## Mental Checkpoint

Before creating or updating ANY PR, ask:

1. **"Have I fetched main?"** - If no, STOP.
2. **"Am I behind main?"** - If yes, STOP and rebase.
3. **"Are there conflicts?"** - If yes, STOP and resolve.
4. **"Is my branch clean and rebased?"** - Only proceed if YES.

## Why This Matters

- Merge conflicts = PR cannot be merged = wasted work
- Shows lack of discipline and attention to process
- Disrespects the reviewer's time
- Breaks CI/CD pipelines
- Creates noise in the repository

## Never Again

This learning exists because I failed. I will read this before every PR operation. There are no excuses for skipping rebase. None.
