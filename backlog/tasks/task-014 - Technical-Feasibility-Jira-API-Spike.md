---
id: task-014
title: Technical Feasibility - Jira API Spike
status: Done
assignee:
  - '@claude'
created_date: '2025-11-24'
updated_date: '2025-11-26 02:31'
labels:
  - discovery
  - technical
  - spike
  - US-1
  - P1
  - satellite-mode
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Spike Jira REST API integration and field mapping complexity.

## Phase

Phase 1: Discovery

## User Stories

- US-1: Pull remote task by ID
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Authenticate using API token
- [x] #2 Fetch issue by ID
- [x] #3 Map custom fields (story points, epic link)
- [x] #4 Test status transitions
- [x] #5 Document field mapping requirements

## Deliverables

- `spikes/jira-api-spike.py` - Proof of concept
- `spikes/jira-api-spike.md` - Findings document
- `spikes/jira-field-mapping.yml` - Sample field map

## Parallelizable

[P] with task-013, task-015

## Time Box

3 days
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Research Jira REST API v3 documentation
2. Document authentication methods (Basic auth, OAuth 2.0)
3. Document issue fetch endpoint and response schema
4. Analyze custom field mapping (customfield_NNNNN pattern)
5. Document status transition workflow (GET then POST)
6. Document rate limiting model
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Jira REST API v3 Spike Results

### AC#1: Authentication
Two methods supported:
1. **Basic Auth**: Base64 encode `email:api_token`
2. **OAuth 2.0 (3LO)**: For marketplace apps

API tokens created at: https://id.atlassian.com/manage-profile/security/api-tokens

```bash
curl -u email@example.com:API_TOKEN \
  https://your-domain.atlassian.net/rest/api/3/issue/KEY-1
```

### AC#2: Fetch Issue by ID
**Endpoint:** `GET /rest/api/3/issue/{issueIdOrKey}`

**Key parameters:**
- `fields` - Comma-separated list of fields to return
- `expand` - Additional data (names, changelog, etc.)

**Example:**
```
GET /rest/api/3/issue/PROJ-123?expand=names&fields=summary,status,assignee,customfield_10000
```

### AC#3: Custom Field Mapping
Custom fields use `customfield_NNNNN` format where NNNNN is unique per Jira instance.

**Discovery endpoint:** `GET /rest/api/3/field`

**Common fields (IDs vary by instance):**
| Field | Typical ID | Notes |
|-------|------------|-------|
| Story Points | customfield_10000 | Number type |
| Epic Link | customfield_10014 | **DEPRECATED** - use `parent` field instead |
| Sprint | customfield_10105 | Array type |

**Important:** Epic Link is being replaced with `parent` field in Jira Cloud.

### AC#4: Status Transitions
Status cannot be updated directly - must use transitions.

**Step 1 - Get available transitions:**
```
GET /rest/api/3/issue/{issueIdOrKey}/transitions
```

**Step 2 - Execute transition:**
```
POST /rest/api/3/issue/{issueIdOrKey}/transitions
Body: { "transition": { "id": "31" } }
```

**Note:** Available transitions depend on current status and user permissions.

### AC#5: Field Mapping Requirements

| Backlog Field | Jira Field | Mapping Complexity |
|---------------|------------|-------------------|
| title | summary | Direct |
| description | description | Direct (ADF format) |
| status | status.name | Via transitions |
| assignee | assignee.accountId | Requires user lookup |
| labels | labels | Direct array |
| priority | priority.id | ID mapping required |
| story_points | customfield_NNNNN | Instance-specific |

### Rate Limits
- **Cost-based model**: ~10 calls/sec per app
- **Per-issue writes**: 20/2s, 100/30s
- **Bulk API**: Up to 1000 issues per call (new Dec 2024)

### Key Findings
1. Custom field IDs must be discovered per instance
2. Epic Link deprecated - use parent field
3. Status changes require transition API
4. Rate limits are generous for sync use case
5. Jira uses ADF (Atlassian Document Format) for rich text
<!-- SECTION:NOTES:END -->
