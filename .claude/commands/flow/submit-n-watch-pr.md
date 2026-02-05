---
description: Submit PR, monitor CI + Copilot, fix and resubmit until approval-ready
loop: outer
---

# /flow:submit-n-watch-pr

Submit PR and monitor until approval-ready. If CI fails or Copilot has comments: close PR, fix locally, create new PR. Never push fixes to existing PRs.

## Success Criteria

**PR is ready ONLY when BOTH are true:**

1. **All CI checks pass** (no failures, no pending)
2. **Copilot says exactly:** `"Copilot reviewed N files in this pull request and generated no comments."`

If either fails → close PR, fix, create new PR. No exceptions.

## Why New PRs Instead of Updates

Pushing fixes to existing PRs causes "Outdated" labels on Copilot comments. Copilot does NOT re-review after pushes. You'll never reach "generated no comments" state. Always close and create fresh.

## User Input

```
$ARGUMENTS
```

- No args: Create new PR from current branch
- `#123` or PR URL: Monitor existing PR
- `--closed #99`: Resume from closed PR

## Prerequisites

- Branch follows `{hostname}/task-{id}/{slug}` pattern
- Branch rebased on main
- Local lint/tests pass

## Outputs

- **Artifact:** `docs/pr/{date}-pr-{number}-summary.md`
- **Decision Log:** `.flowspec/logs/decisions/{date}-submit-pr.jsonl`
- **Backlog Update:** Task notes updated with PR link

---

## Workflow

### Phase 1: Setup

1. Parse arguments to determine mode (new/monitor/resume)
2. Extract task ID from branch name
3. Validate branch naming: `{hostname}/task-{id}/{slug}`
4. Ensure rebased on main (rebase if behind)

If monitoring existing PR, skip to Phase 3.

### Phase 2: Create PR

1. Check for existing open PR on branch
2. If exists and open: use it, skip creation
3. If none or closed: create new PR

**PR creation:**
```bash
gh pr create --title "feat: {task-title}" --body "$(cat <<'EOF'
## Summary
Completes: {task-id}

## Test Plan
- [ ] CI checks pass
- [ ] Copilot review clean

---
*Via /flow:submit-n-watch-pr*
EOF
)"
```

### Phase 3: Monitor CI

Poll every 30s for up to 15 minutes:

```bash
gh pr view $PR_NUMBER --json statusCheckRollup
```

**If all checks pass:** proceed to Phase 4

**If any check fails:**
1. Close PR: `gh pr close $PR_NUMBER`
2. Analyze failures
3. Fix locally (format, lint, code)
4. Commit fixes
5. Create new PR (go to Phase 2)

### Phase 4: Monitor Copilot Review

Poll every 60s for up to 10 minutes for Copilot review.

**Check for the exact success message:**
```
Copilot reviewed N files in this pull request and generated no comments.
```

Look in PR comments and review body:
```bash
gh pr view $PR_NUMBER --json comments,reviews
```

**If "generated no comments" found:** PR is ready → Phase 5

**If Copilot has comments:**
1. Close PR: `gh pr close $PR_NUMBER`
2. Read and understand each comment
3. Fix issues locally
4. Commit fixes
5. Create new PR (go to Phase 2)

### Phase 5: Complete

1. Log decision to `.flowspec/logs/decisions/`
2. Update backlog task with PR link
3. Write PR summary artifact

**Decision log entry:**
```json
{
  "timestamp": "{ISO8601}",
  "command": "/flow:submit-n-watch-pr",
  "task_id": "{task-id}",
  "decision": "PR ready for merge",
  "rationale": "CI passed, Copilot generated no comments",
  "pr_number": "{number}",
  "iterations": "{count}"
}
```

**Backlog update:**
```bash
backlog task edit {id} --append-notes "PR #{number} ready for merge"
```

**Artifact:** Write summary to `docs/pr/{date}-pr-{number}-summary.md`

---

## Fix Loop Rules

When fixing issues between iterations:

1. **Never push to existing PR** - always close first
2. **Fix root cause** - don't just silence warnings
3. **Run local validation before new PR:**
   ```bash
   uv run ruff format . && uv run ruff check . && uv run pytest tests/ -x -q
   ```
4. **Max 5 iterations** - if stuck, request human review

## Error Recovery

| Problem | Action |
|---------|--------|
| Branch name invalid | Rename: `git branch -m {correct-name}` |
| Rebase conflicts | Resolve manually, then re-run |
| CI timeout | Re-run command to resume monitoring |
| Copilot not reviewing | Check if enabled for repo, use `--skip-copilot` if needed |
| Stuck in loop | Max iterations reached → request human review |

## Command Reference

```bash
/flow:submit-n-watch-pr              # New PR
/flow:submit-n-watch-pr #123         # Monitor existing
/flow:submit-n-watch-pr --closed #99 # Resume from closed
```
