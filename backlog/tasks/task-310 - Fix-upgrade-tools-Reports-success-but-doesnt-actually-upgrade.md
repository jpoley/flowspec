---
id: task-310
title: 'Fix upgrade-tools: Reports success but doesn''t actually upgrade'
status: To Do
assignee: []
created_date: '2025-12-08 01:40'
labels:
  - bug
  - cli
  - upgrade-tools
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Bug Description

`specify upgrade-tools` reports successful upgrade but the version doesn't change.

**Observed Behavior:**
```
Component      Current    Available    Status
flowspec    0.2.328    0.2.332      ✓ Installed version 0.2.328 (was: 0.2.328)
```

Notice: Status shows ✓ success, but version stayed at 0.2.328 (should be 0.2.332).

## Root Cause Analysis

The issue is in `_upgrade_jp_spec_kit()` at line 3973-3986 in `src/specify_cli/__init__.py`:

```python
# For latest, try uv upgrade first
if not target_version:
    try:
        result = subprocess.run(
            ["uv", "tool", "upgrade", "specify-cli"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            new_version = _get_installed_jp_spec_kit_version()
            if new_version and compare_semver(new_version, current_version) > 0:
                return True, f"Upgraded from {current_version} to {new_version}"
    except FileNotFoundError:
        pass

# Install from git at the specific release tag
git_url = f"git+https://github.com/{EXTENSION_REPO_OWNER}/{EXTENSION_REPO_NAME}.git"
git_url = f"{git_url}@v{install_version}"
```

**The Bug:** When `uv tool upgrade specify-cli` returns `returncode == 0` but the version didn't actually change (because `uv` thinks it's already up-to-date), the code checks if `new_version > current_version`. Since the versions are equal, it does NOT return early - this part is correct.

**However**, the code then falls through to the git install section (lines 3988-4010), which DOES install from git. The issue is that `_get_installed_jp_spec_kit_version()` runs `specify version` which invokes the **same Python process that's already running** - it can't detect the newly installed version because the `specify` binary being executed might be cached or the shell hasn't refreshed its PATH cache.

**Additionally**, there's a more subtle issue: `uv tool upgrade` may return success (0) even when no upgrade was needed, because `specify-cli` was installed via git, not PyPI. The `uv tool upgrade` command doesn't know about the GitHub release versions.

## Technical Details

1. `uv tool upgrade specify-cli` returns 0 but doesn't upgrade (package not on PyPI, installed from git)
2. Version check `new_version > current_version` is false (0.2.328 == 0.2.328)
3. Falls through to git install section
4. Git install succeeds with `check=True`
5. `_get_installed_jp_spec_kit_version()` runs `specify version` but may get stale version
6. Reports "Installed version 0.2.328 (was: 0.2.328)" - technically the git install ran, but version detection is broken

## Suspected Fix Locations

- `src/specify_cli/__init__.py:3903-3917` - `_get_installed_jp_spec_kit_version()` may need to use a different method
- `src/specify_cli/__init__.py:4007-4009` - Post-install version detection logic

## Possible Solutions

1. **Skip `uv tool upgrade` entirely** for git-installed packages - go straight to git install
2. **Hash-based detection**: Compare file hashes before/after to verify install changed
3. **Use `uv tool list --show-paths`** to get the installation path and read version from there
4. **Force shell PATH refresh** before running `specify version` (exec new shell)
5. **Read version from installed package metadata** instead of running binary
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 When Available > Current version, `specify upgrade-tools` actually installs the new version
- [ ] #2 Status message shows correct 'Upgraded from X to Y' (not same version twice)
- [ ] #3 Version detection after install correctly reads new version
- [ ] #4 Works for both targeted (--version X.X.X) and latest upgrades
- [ ] #5 Unit tests cover the upgrade flow scenarios
<!-- AC:END -->
