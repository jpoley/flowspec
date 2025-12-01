---
id: task-183
title: Fix 401 auth error when fetching latest release
status: To Do
assignee: []
created_date: '2025-12-01 02:17'
updated_date: '2025-12-01 02:17'
labels:
  - bug
  - github-api
  - authentication
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**GitHub Issue:** #161

**Problem:**
The specify CLI fails with a 401 authentication error when attempting to fetch the latest release from GitHub:

```
Could not resolve release for github/spec-kit (version='latest'). Last HTTP status: 401
```

The tool attempts multiple resolution paths:
- `/releases/latest`
- `/releases/tags/` with version prefixes
- `/releases list`

All fail with 401 Unauthorized.

**Key Insight:** This is a public repository - no authentication should be required to fetch release info from the GitHub API.

**Likely Root Causes:**
1. **Incorrect API URL** - May be hitting a wrong endpoint or malformed URL
2. **Wrong repo reference** - `github/spec-kit` looks wrong; should likely be `jpoley/jp-spec-kit`
3. **Sending invalid/stale auth header** - If a token is being sent but is invalid, GitHub returns 401
4. **Rate limiting edge case** - Though this typically returns 403, not 401

**Environment:**
- jp extension v0.0.147
- AI Assistant: copilot
- Script Type: sh
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Verify correct repository path is used (jpoley/jp-spec-kit, not github/spec-kit)
- [ ] #2 CLI can fetch latest release from public repos without any authentication
- [ ] #3 If an invalid token is present, either skip it or handle the 401 gracefully
- [ ] #4 Add unit tests for release fetching from public repos
- [ ] #5 Error messages clearly indicate the actual problem (not just 'add a token')
<!-- AC:END -->
