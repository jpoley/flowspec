# Dogfood Recovery Runbook

## Overview

This runbook provides procedures for recovering from dogfood validation failures in the JP Spec Kit project. Use this when CI/CD checks fail or local development encounters inconsistencies.

## Quick Reference

| Scenario | Quick Fix | Details |
|----------|-----------|---------|
| Non-symlink files detected | `make dogfood-fix` | [Section 1](#scenario-1-non-symlink-files-detected) |
| Broken symlinks | `make dogfood-fix` | [Section 2](#scenario-2-broken-symlinks) |
| Pre-commit hook fails | `./scripts/bash/pre-commit-dogfood.sh` | [Section 3](#scenario-3-pre-commit-hook-failure) |
| CI validation fails on PR | Check diff, then `make dogfood-fix` | [Section 4](#scenario-4-ci-validation-fails) |
| Corrupted .claude directory | `rm -rf .claude/commands && make dogfood-fix` | [Section 5](#scenario-5-corrupted-claude-directory) |

---

## Scenario 1: Non-Symlink Files Detected

### Symptoms

```
❌ ERROR: Found non-symlink .md files in .claude/commands/
Files that should be symlinks:
  .claude/commands/jpspec/implement.md
  .claude/commands/jpspec/research.md
```

### Root Cause

Files were edited directly in `.claude/commands/` instead of through `templates/commands/`.

### Recovery Procedure

#### Option A: Quick Fix (Loses Local Changes)

```bash
# Recreate all symlinks from templates
make dogfood-fix

# Verify
make dogfood-validate
```

**Use when**: Changes in .claude/commands/ were accidental or can be discarded.

#### Option B: Preserve Changes

```bash
# 1. Identify changed files
git status .claude/commands/

# 2. Back up changes
cp .claude/commands/jpspec/implement.md /tmp/implement-backup.md

# 3. Merge changes into templates
# Compare and merge manually
diff .claude/commands/jpspec/implement.md templates/commands/jpspec/implement.md
vim templates/commands/jpspec/implement.md

# 4. Recreate symlinks
make dogfood-fix

# 5. Verify changes are present
cat .claude/commands/jpspec/implement.md

# 6. Commit template changes
git add templates/commands/jpspec/implement.md
git commit -s -m "fix: merge changes into template"
```

**Use when**: Changes in .claude/commands/ contain work that must be preserved.

### Prevention

- Always edit files in `templates/commands/`
- Use pre-commit hooks to catch mistakes early
- Review PRs for changes in `.claude/commands/`

---

## Scenario 2: Broken Symlinks

### Symptoms

```
❌ ERROR: Found broken symlinks in .claude/commands/
Broken symlinks:
  .claude/commands/speckit/analyze.md -> ../../../templates/commands/analyze.md
  .claude/commands/speckit/tasks.md -> ../../../templates/commands/tasks.md
```

### Root Cause

- Template files were deleted or moved
- Symlink paths are incorrect
- Git checkout switched branches with different structure

### Recovery Procedure

#### Step 1: Identify Missing Templates

```bash
# Check which templates are missing
ls -la .claude/commands/speckit/
ls -la templates/commands/

# Identify broken symlinks
find .claude/commands -type l ! -exec test -e {} \; -print
```

#### Step 2: Fix or Remove

**If templates should exist:**

```bash
# Restore from git
git checkout main -- templates/commands/analyze.md

# Recreate symlinks
make dogfood-fix
```

**If templates were intentionally removed:**

```bash
# Remove broken symlinks
rm .claude/commands/speckit/old-command.md

# Verify
make dogfood-validate
```

#### Step 3: Verify

```bash
# Check all symlinks resolve
make dogfood-status

# Run full validation
make dogfood-validate
```

### Prevention

- Don't delete templates without removing symlinks
- Run `make dogfood-fix` after major branch merges
- Use `git mv` when renaming templates

---

## Scenario 3: Pre-commit Hook Failure

### Symptoms

```
🔍 Validating dogfood consistency...
❌ ERROR: Found non-symlink .md files in .claude/commands/
```

Commit is blocked.

### Recovery Procedure

#### Step 1: Diagnose

```bash
# Run validation manually to see full output
./scripts/bash/pre-commit-dogfood.sh
```

#### Step 2: Fix Issues

Follow recovery procedures for specific errors detected.

#### Step 3: Retry Commit

```bash
# After fixing
git add <fixed-files>
git commit -s -m "fix: resolve dogfood issues"
```

### Bypass (Emergency Only)

```bash
# Skip pre-commit hooks (NOT RECOMMENDED)
git commit --no-verify -s -m "emergency fix"

# Immediately fix in next commit
make dogfood-fix
git add .claude/commands/
git commit -s -m "fix: restore dogfood consistency"
```

**Only use `--no-verify` in emergencies.** Always fix in next commit.

### Prevention

- Run `make dogfood-validate` before committing
- Install pre-commit hooks: `pre-commit install`
- Test changes locally first

---

## Scenario 4: CI Validation Fails on PR

### Symptoms

GitHub Actions workflow "Dogfood Validation" fails with validation errors.

### Recovery Procedure

#### Step 1: Review CI Logs

```bash
# View GitHub Actions logs
# Look for specific validation failure
```

Common errors:
- Non-symlink files detected
- Broken symlinks
- Test suite failures

#### Step 2: Reproduce Locally

```bash
# Clean workspace
git fetch origin
git checkout pr-branch-name

# Run same checks as CI
make dogfood-validate
make test-dogfood
```

#### Step 3: Fix Issues

```bash
# Fix identified issues
make dogfood-fix

# Verify locally
make ci-local  # Simulates full CI run

# Commit fix
git add .
git commit -s -m "fix: restore dogfood consistency"
git push origin pr-branch-name
```

#### Step 4: Verify CI Passes

- Check GitHub Actions re-runs successfully
- Review CI logs to confirm all checks pass

### Prevention

- Run `make ci-local` before pushing
- Enable pre-commit hooks
- Review diffs before creating PRs

---

## Scenario 5: Corrupted .claude Directory

### Symptoms

- Multiple validation errors
- Symlinks pointing to wrong locations
- Missing directories
- Git shows unexpected changes

### Recovery Procedure

#### Step 1: Backup Current State

```bash
# Backup current .claude directory
cp -r .claude /tmp/claude-backup-$(date +%s)
```

#### Step 2: Nuclear Reset

```bash
# Remove entire .claude/commands structure
rm -rf .claude/commands

# Recreate from scratch
make dogfood-fix
```

#### Step 3: Verify Integrity

```bash
# Check structure
make dogfood-status

# Run full validation
make dogfood-validate

# Run tests
make test-dogfood
```

#### Step 4: Review Changes

```bash
# See what changed
git diff .claude/commands/

# If correct, commit
git add .claude/commands/
git commit -s -m "fix: restore .claude/commands structure"
```

### Prevention

- Don't manually manipulate `.claude/commands/` structure
- Use `make dogfood-fix` for all symlink recreation
- Regular validation: `make dogfood-validate`

---

## Escalation Paths

### Level 1: Self-Service (5 minutes)

Try automated recovery:
```bash
make dogfood-fix
make dogfood-validate
```

### Level 2: Manual Recovery (15 minutes)

1. Review specific error messages
2. Follow scenario-specific procedures above
3. Test locally before committing

### Level 3: Team Review (30 minutes)

If automated recovery fails:
1. Create GitHub issue with:
   - Error messages
   - `make dogfood-status` output
   - Recent commits affecting templates/
2. Tag: `@platform-team`
3. Include reproduction steps

### Level 4: Rollback (Emergency)

If production is affected:
```bash
# Revert to last known good state
git revert HEAD
git push origin main

# Or roll back to specific commit
git reset --hard <last-good-commit>
git push --force origin main  # DANGEROUS - requires approval
```

**Production rollback requires**:
- Team lead approval
- Incident post-mortem
- Root cause analysis

---

## Monitoring and Alerts

### Key Metrics

| Metric | Target | Alert Threshold | Action |
|--------|--------|-----------------|--------|
| Non-symlink files | 0 | > 0 | Immediate fix |
| Broken symlinks | 0 | > 0 | Investigate |
| CI validation time | < 2 min | > 5 min | Performance review |
| Pre-commit failures | < 5% | > 20% | Developer training |

### Alert Channels

- **Slack**: `#jp-spec-kit-alerts`
- **Email**: `platform-team@example.com`
- **PagerDuty**: For production failures only

### Dashboard

Access real-time status:
- **CI/CD**: https://github.com/jpoley/jp-spec-kit/actions
- **Test Results**: See latest workflow run
- **Coverage**: Review test coverage reports

---

## Post-Incident Review

After resolving issues:

### 1. Document Root Cause

- What caused the validation failure?
- Why wasn't it caught earlier?
- What process failed?

### 2. Update Runbook

- Was this scenario covered?
- Are recovery steps accurate?
- Add new scenarios as needed

### 3. Improve Prevention

- Add new validation checks
- Enhance error messages
- Update documentation
- Additional training needed?

### 4. Share Learnings

- Post to team Slack channel
- Update onboarding docs
- Add to FAQ if common

---

## Common Commands Quick Reference

```bash
# Status and validation
make dogfood-status          # Show current state
make dogfood-validate        # Run all checks
./scripts/bash/pre-commit-dogfood.sh  # Manual pre-commit check

# Recovery
make dogfood-fix            # Recreate all symlinks
rm -rf .claude/commands && make dogfood-fix  # Nuclear reset

# Testing
make test-dogfood           # Run dogfood tests only
make ci-local               # Simulate full CI pipeline

# Development
specify dogfood --force     # Run dogfood command directly
```

---

## Additional Resources

- [Dogfood Consistency Guide](/docs/reference/dogfood-consistency.md)
- [CI/CD Workflow](/.github/workflows/dogfood-validation.yml)
- [Test Suite](/tests/test_dogfood_validation.py)
- [Backlog Quick Start](/docs/guides/backlog-quickstart.md)

---

## Runbook Maintenance

**Last Updated**: 2025-12-03
**Owner**: Platform Engineering Team
**Review Cycle**: Quarterly or after major incidents

**Changelog**:
- 2025-12-03: Initial version created
