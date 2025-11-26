---
id: task-015
title: Technical Feasibility - Notion API Spike
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
  - P2
  - satellite-mode
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Spike Notion SDK integration and database property mapping.

## Phase

Phase 1: Discovery

## User Stories

- US-1: Pull remote task by ID
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Authenticate using integration token
- [x] #2 Query database with filters
- [x] #3 Map properties to task fields
- [x] #4 Create/update database items
- [x] #5 Document limitations (rate limits, batch size)

## Deliverables

- `spikes/notion-api-spike.py` - Proof of concept
- `spikes/notion-api-spike.md` - Findings document

## Parallelizable

[P] with task-013, task-014

## Time Box

2 days
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Research Notion API documentation
2. Document integration token authentication
3. Document database query endpoint and filter syntax
4. Analyze property type mapping
5. Document rate limits (3 req/sec)
6. Document pagination patterns
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Notion API Spike Results

### AC#1: Authentication
Uses **Integration Token** authentication.

**Setup:**
1. Create integration at https://www.notion.so/my-integrations
2. Get internal integration token (starts with `secret_`)
3. Share database/page with integration

**Headers:**
```
Authorization: Bearer secret_xxx
Notion-Version: 2022-06-28
Content-Type: application/json
```

### AC#2: Query Database with Filters
**Endpoint:** `POST /v1/databases/{database_id}/query`

**Filter syntax:**
```json
{
  "filter": {
    "and": [
      { "property": "Status", "status": { "equals": "In Progress" } },
      { "property": "Assignee", "people": { "contains": "user_id" } }
    ]
  },
  "sorts": [
    { "property": "Created", "direction": "descending" }
  ]
}
```

**Supported filter types:**
- checkbox, date, files, formula
- multi_select, number, people, phone_number
- relation, rich_text, select, status, timestamp, title, url

### AC#3: Property Mapping

| Backlog Field | Notion Property Type | Notes |
|---------------|---------------------|-------|
| title | title | Required, one per DB |
| description | rich_text | Markdown support |
| status | status/select | Custom options |
| assignee | people | User references |
| labels | multi_select | Array of tags |
| priority | select | Custom options |
| due_date | date | ISO 8601 format |

**Property schema discovery:**
```
GET /v1/databases/{database_id}
```

### AC#4: Create/Update Items
**Create page:**
```
POST /v1/pages
{
  "parent": { "database_id": "xxx" },
  "properties": {
    "Title": { "title": [{ "text": { "content": "Task name" } }] },
    "Status": { "status": { "name": "To Do" } }
  }
}
```

**Update page:**
```
PATCH /v1/pages/{page_id}
{
  "properties": { ... }
}
```

### AC#5: Limitations

| Limit | Value | Notes |
|-------|-------|-------|
| Rate limit | 3 req/sec average | Bursts allowed |
| Page size | 100 items | Use pagination |
| Block children | 100 per request | Nested content |
| Text length | 2000 chars | Per rich_text block |
| Filter depth | 2 levels | Compound filters |

**Pagination:**
- Response includes `next_cursor` if more results
- Pass `start_cursor` in next request

**Retry handling:**
- HTTP 429 returns `Retry-After` header (seconds)
- Implement exponential backoff

### Key Findings
1. Property schema varies per database (must discover)
2. Rich text uses block-based format
3. 3 req/sec is limiting for large syncs - need batching strategy
4. Integration must be explicitly shared with each database
5. No bulk update API - must update pages individually
<!-- SECTION:NOTES:END -->
