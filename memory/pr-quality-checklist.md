# PR Quality Checklist

Learnings from agent-hooks feature development (PRs #279, #300, #313, #333, #348).

## Pre-Commit Checklist

### Security
- [ ] No path traversal vulnerabilities (use `os.path.normpath()`, check for `..`)
- [ ] Auto-approve hooks ONLY allow read-only operations
- [ ] Never trust external input for file paths (use `$PWD` not event data)
- [ ] File operations use locking (`flock`) to prevent race conditions

### Code Quality
- [ ] Variable names consistent across all related files
- [ ] Regex patterns don't capture unintended characters (trailing punctuation)
- [ ] All dependencies documented in script headers
- [ ] Examples show all relevant flags/options

### Documentation
- [ ] All templates use consistent variable naming (`$FEATURE_ID` not `$FEATURE_NAME`)
- [ ] Shell scripts document dependencies (jq, flock, etc.)
- [ ] Examples are complete and demonstrate key features

### Testing
- [ ] All existing tests pass
- [ ] New functionality has test coverage
- [ ] Hook scripts have their own test files
- [ ] Security boundaries are tested (destructive ops NOT auto-approved)

### DCO
- [ ] Every commit has `Signed-off-by` line (use `git commit -s`)
- [ ] Verify with `git log -1 | grep "Signed-off-by"`

## Common Mistakes to Avoid

### 1. Overly Permissive Auto-Approval
**Wrong**: `r"^backlog\s+"` - approves ALL backlog commands including destructive ones
**Right**: `r"^backlog\s+(task\s+)?(list|show|view)\b"`  # Matches both "backlog list" and "backlog task list" (only read-only commands)

### 2. Path Traversal Vulnerabilities
**Wrong**: Direct use of user-provided paths
**Right**:
```python
import os
base_dir = os.path.abspath('/safe/base')
normalized = os.path.normpath(path)
full_path = os.path.abspath(os.path.join(base_dir, normalized))
if not full_path.startswith(base_dir):
    return False
```

### 3. Regex Capturing Too Much
**Wrong**: `r"Feature:\s*(\S+)"` - captures "feature." including period
**Right**: `r"Feature:\s*([\w.-]+)"` - only word characters, dots, hyphens

### 4. Inconsistent Variable Names
**Wrong**: Using `$FEATURE_NAME` in one file and `$FEATURE_ID` in others
**Right**: Grep all files for the variable before adding: `grep -r "FEATURE_" templates/`

### 5. Missing DCO Sign-off
**Wrong**: `git commit -m "message"`
**Right**: `git commit -s -m "message"`

### 6. Undocumented Dependencies
**Wrong**: Script uses `jq` without mentioning it
**Right**: Add header comment: `# Dependencies: jq, flock (util-linux)`

## Pre-PR Validation Script

Run before creating any PR:

```bash
#!/bin/bash
# pre-pr-validate.sh

set -e

echo "=== Linting ==="
ruff check .

echo "=== Formatting ==="
ruff format --check .

echo "=== Tests ==="
pytest tests/ -q

echo "=== DCO Check ==="
# Check all commits not yet pushed to origin/main
missing_dco=0
git log origin/main..HEAD --format="%H %s" | while read hash subject; do
    if ! git log -1 $hash | grep -q "Signed-off-by:"; then
        echo "✗ Missing DCO in commit: $hash $subject"
        missing_dco=1
    fi
done
if [ "$missing_dco" -eq 1 ]; then
    echo "✗ MISSING DCO - use: git commit --amend -s"
    exit 1
else
    echo "✓ All commits DCO signed"
fi

echo "=== Variable Consistency ==="
echo "ℹ Customize this check for your project's naming conventions"
# Example: Check for inconsistent feature variable names
# if grep -r "FEATURE_NAME" templates/ 2>/dev/null; then
#     echo "✗ Found FEATURE_NAME - should be FEATURE_ID"
#     exit 1
echo "✓ Variable names check (customize for your project)"

echo ""
echo "✓ All checks passed - ready for PR"
```

## Review Feedback Categories

When receiving PR feedback, categorize and address systematically:

1. **Security Issues** - Fix immediately, these block merge
2. **Code Quality** - Fix before merge, impacts maintainability
3. **Documentation** - Fix before merge, impacts usability
4. **Nitpicks** - Optional but recommended for polish

Never close a PR until ALL categories are addressed.
