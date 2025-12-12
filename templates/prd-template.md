# PRD: {Feature Name}

## Executive Summary

{Brief 2-3 sentence overview of the feature and its business value.}

## Problem Statement

{Describe the problem being solved.}

### Current State

- {Current limitation or pain point 1}
- {Current limitation or pain point 2}

### Desired State

- {What success looks like 1}
- {What success looks like 2}

## User Stories

### US1: {Story Title}

As a {user role}, I want {goal} so that {benefit}.

**Acceptance Criteria:**
- [ ] AC1: {Testable criterion}
- [ ] AC2: {Testable criterion}
- [ ] AC3: {Testable criterion}

### US2: {Story Title}

As a {user role}, I want {goal} so that {benefit}.

**Acceptance Criteria:**
- [ ] AC1: {Testable criterion}
- [ ] AC2: {Testable criterion}

## Functional Requirements

### FR1: {Requirement Title}

{Description of the functional requirement}

- {Sub-requirement 1}
- {Sub-requirement 2}

### FR2: {Requirement Title}

{Description of the functional requirement}

## Non-Functional Requirements

### Performance

- {Performance requirement 1}
- {Performance requirement 2}

### Security

- {Security requirement 1}
- {Security requirement 2}

### Reliability

- {Reliability requirement 1}

### Scalability

- {Scalability requirement 1}

## Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| {Metric 1} | {Target value} | {How to measure} |
| {Metric 2} | {Target value} | {How to measure} |

## Dependencies

### Internal Dependencies

- {Internal system or service 1}
- {Internal system or service 2}

### External Dependencies

- {External API or service 1}
- {External vendor or tool 1}

## All Needed Context

> This section provides all context needed for implementation. Machine-parseable for use by `/flow:generate-prp`, `/flow:implement`, and `/flow:validate`.

### Code Files

<!-- List source code files relevant to this feature -->
<!-- Format: | Path | Purpose | Read Priority | -->

| File Path | Purpose | Read Priority |
|-----------|---------|---------------|
| `{path/to/file1}` | {What this file does and why it's relevant} | High/Medium/Low |
| `{path/to/file2}` | {What this file does and why it's relevant} | High/Medium/Low |

<!-- Read Priority Guide:
- High: Must read before starting implementation
- Medium: Read when working on related functionality
- Low: Reference if needed
-->

### Docs / Specs

<!-- Link to related documentation, specs, and design documents -->
<!-- Format: | Document | Link | Key Sections | -->

| Document | Link | Key Sections |
|----------|------|--------------|
| Architecture Doc | `{docs/path}` | {Relevant sections} |
| ADR | `{docs/adr/path}` | {Decision summary} |
| API Spec | `{docs/path}` | {Relevant endpoints} |
| External RFC | `{URL}` | {Relevant sections} |

### Examples

<!-- List example files that demonstrate patterns or expected behavior -->
<!-- Format: | Example | Location | Relevance | -->

| Example | Location | Relevance to This Feature |
|---------|----------|---------------------------|
| {Example name} | `examples/{path}` | {How this example relates to the feature} |
| {Example name} | `examples/{path}` | {How this example relates to the feature} |

### Gotchas / Prior Failures

<!-- Document known pitfalls, historical issues, and lessons learned -->
<!-- Format: | Gotcha | Impact | Mitigation | Source | -->

| Gotcha | Impact | Mitigation | Source |
|--------|--------|------------|--------|
| {Known issue or pitfall} | {What goes wrong} | {How to avoid it} | {task-XXX or doc link} |
| {Previous failure mode} | {What went wrong} | {Lesson learned} | {task-XXX or doc link} |

<!-- Sources for gotchas:
- memory/learnings/*.md files
- Previous task implementation notes
- ADR consequences sections
- Post-mortem documents
-->

### External Systems / APIs

<!-- Document external systems and APIs this feature interacts with -->
<!-- Format: | System | Type | Documentation | Notes | -->

| System / API | Type | Documentation | Notes |
|--------------|------|---------------|-------|
| {External service name} | REST/GraphQL/gRPC | {Link to docs} | {Auth method, rate limits, etc.} |
| {Database/Cache} | {Type} | {Link to docs} | {Connection details, constraints} |
| {Third-party SDK} | Library | {Link to docs} | {Version requirements, limitations} |

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| {Risk 1} | High/Medium/Low | High/Medium/Low | {Mitigation strategy} |
| {Risk 2} | High/Medium/Low | High/Medium/Low | {Mitigation strategy} |

## Out of Scope

- {Explicitly excluded item 1}
- {Explicitly excluded item 2}
- {Items to consider for future iterations}

## Timeline

| Phase | Description | Target Date |
|-------|-------------|-------------|
| Design | Architecture and detailed design | {Date} |
| Implementation | Core development | {Date} |
| Testing | QA and validation | {Date} |
| Launch | Production deployment | {Date} |

---

*Document Version: 1.0*
*Last Updated: {Date}*
*Author: {Author Name}*
