---
name: FlowSubmitNWatchPR
description: "Submit PR and autonomously monitor CI checks and Copilot reviews until approval-ready. Iteratively fix issues and resubmit."
target: "chat"
tools:
  - "Read"
  - "Write"
  - "Edit"
  - "Grep"
  - "Glob"
  - "Bash"
  - "mcp__github__*"
  - "mcp__backlog__*"
  - "mcp__serena__*"
  - "Skill"
---

# /flow:submit-n-watch-pr - Autonomous PR Management

Submit a PR and autonomously monitor CI checks and code review feedback until approval-ready.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Critical Success Criteria

Your PR is ONLY ready for merge when you see BOTH:
1. **All CI checks pass** (green checkmarks)
2. **Zero Copilot review comments** or all addressed

## Instructions

**Prerequisites:**
1. Run `/flow:validate` first to ensure quality
2. All local tests pass
3. Branch is rebased from main

**Workflow:**

### Step 1: Pre-Submit Validation
```bash
# Verify branch is up to date
git fetch origin main
git rebase origin/main

# Run final validation
uv run ruff check .
uv run pytest tests/ -x -q
```

### Step 2: Create PR
```bash
# Push branch
git push origin $(git branch --show-current)

# Create PR with proper description
gh pr create \
  --title "feat(scope): description" \
  --body "## Summary
1. Wait for CI checks to complete
2. Check for Copilot review comments: `gh pr view --comments`
3. If issues found:
   - Fix the issues locally
   - Push updates: `git push`
   - Wait for re-check
4. Repeat until all checks pass and no comments remain

### Step 4: Request Review
```bash
# When ready, request human review
gh pr ready
gh pr edit --add-reviewer <reviewer>
```

**Key Commands:**
```bash
# Check PR status
gh pr status
