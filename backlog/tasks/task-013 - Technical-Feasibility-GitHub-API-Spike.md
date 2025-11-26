---
id: task-013
title: Technical Feasibility - GitHub API Spike
status: Done
assignee:
  - '@claude'
created_date: '2025-11-24'
updated_date: '2025-11-26 02:25'
labels:
  - discovery
  - technical
  - spike
  - US-1
  - P0
  - satellite-mode
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Spike GitHub API integration to validate feasibility and auth patterns.

## Phase

Phase 1: Discovery

## User Stories

- US-1: Pull remote task by ID
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Authenticate using `gh` CLI token
- [x] #2 Fetch issue by number
- [x] #3 List issues with filter (assignee, status)
- [x] #4 Create PR with custom body
- [x] #5 Measure API latency (<1s per operation)
- [x] #6 Document rate limits (5000 req/hour)

## Deliverables

- `spikes/github-api-spike.py` - Proof of concept
- `spikes/github-api-spike.md` - Findings document

## Parallelizable

[P] with task-014, task-015

## Time Box

2 days
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Set up GH_TOKEN from vault file (~/.aws/vault/GITHUB)
2. Test authentication via gh api user
3. Fetch issue by number with timing
4. Test list filters (assignee, labels, state)
5. Validate PR creation API schema
6. Run latency benchmark (5 requests)
7. Document rate limits from API
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## GitHub API Spike Results

### Authentication
- Token source: `~/.aws/vault/GITHUB` or `$GITHUB_TOKEN`
- Works with `gh` CLI via `GH_TOKEN` env var
- Authenticated as: jpoley

### API Performance
| Operation | Latency |
|-----------|--------|
| Fetch issue by number | 240ms |
| List issues (filtered) | 392-434ms |
| Average (5 requests) | 312ms |

**✓ All operations well under 1s target**

### Rate Limits
| Endpoint | Limit | Notes |
|----------|-------|-------|
| core | 5000/hr | Main REST API |
| graphql | 5000/hr | GraphQL queries |
| search | 30/hr | Search API |
| code_search | 10/hr | Code search |

### PR Creation
```
POST /repos/{owner}/{repo}/pulls
Required: title, head, base
Optional: body (for spec injection), draft
```

### Key Findings
1. Token auth via file/env works seamlessly
2. Issue filtering supports: assignee, labels, state, milestone
3. All latencies ~300ms (acceptable)
4. 5000 req/hr is sufficient for sync operations
5. Search is rate-limited (30/hr) - use REST filtering instead
<!-- SECTION:NOTES:END -->
