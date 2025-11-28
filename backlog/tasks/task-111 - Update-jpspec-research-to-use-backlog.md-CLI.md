---
id: task-111
title: 'Update /jpspec:research to use backlog.md CLI'
status: Done
assignee:
  - '@research-agent'
created_date: '2025-11-28 16:56'
updated_date: '2025-11-28 20:18'
labels:
  - jpspec
  - backlog-integration
  - research
  - P1
dependencies:
  - task-107
  - task-108
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modify the research.md command to integrate backlog.md task management. Researcher and Business Validator agents must create research tasks and document findings in backlog.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Command discovers existing research-related backlog tasks
- [x] #2 Both agents receive shared backlog instructions from _backlog-instructions.md
- [x] #3 Researcher creates research spike tasks in backlog
- [x] #4 Business Validator creates validation tasks in backlog
- [x] #5 Agents add research findings as implementation notes to tasks
- [x] #6 Test: Run /jpspec:research and verify research tasks created with findings
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Read current research.md command
2. Integrate _backlog-instructions.md into both agent prompts
3. Add backlog search at command start
4. Update Researcher prompt with task creation
5. Update Business Validator prompt with task creation
6. Create comprehensive tests
7. Run tests and verify
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
# Implementation Summary

Successfully integrated backlog.md CLI into /jpspec:research command for both Researcher and Business Validator agents.

## Changes Made

### 1. Command-Level Discovery (research.md)
- Added backlog search at command start to discover existing research tasks
- Searches for "research" keyword and user-provided topic
- Lists all research-labeled tasks before agent execution
- Prevents duplicate research work

### 2. Researcher Agent Integration
- Added comprehensive backlog.md task management section
- Instructions for creating research spike tasks with 5 ACs:
  - Market analysis (TAM/SAM/SOM, growth, segments)
  - Competitive landscape (competitors, strengths/weaknesses)
  - Technical feasibility (technologies, complexity, risks)
  - Industry trends (patterns, best practices, outlook)
  - Sourced recommendations with confidence levels
- Task workflow: create → assign @researcher → plan → mark ACs → add findings → done
- Research findings added as structured implementation notes
- Labels: research, spike
- Priority: high

### 3. Business Validator Agent Integration
- Added comprehensive backlog.md task management section
- Instructions for creating business validation tasks with 6 ACs:
  - Market opportunity assessment (TAM/SAM/SOM)
  - Financial viability (revenue model, cost structure, unit economics)
  - Operational feasibility (resources, capabilities, gaps)
  - Strategic fit (organizational alignment)
  - Risk analysis (market, execution, financial risks)
  - Go/No-Go/Proceed-with-Caution recommendation
- Task workflow: create → assign @business-validator → plan → mark ACs → add assessment → done
- Validation findings added as structured implementation notes
- Labels: validation, business
- Priority: high

### 4. Comprehensive Testing
Created `tests/test_jpspec_research_backlog.py` with 32 tests covering:
- Command structure (discovery, existing task checks)
- Researcher backlog instructions (task creation, assignment, notes, ACs)
- Business Validator backlog instructions (task creation, assignment, notes, ACs)
- Task labels (research/spike, validation/business)
- Workflow integration (discovery before agents, task creation patterns)
- Acceptance criteria (coverage, progressive checking)
- Implementation notes (structured formats, multiline syntax)
- Task priority (high for both types)
- Command consistency (both agents follow same workflow)

All 32 tests passed successfully.

## Key Features

### Research Spike Tasks
- Title format: "Research: [TOPIC]"
- 5 acceptance criteria covering all research areas
- Structured findings template with sections:
  - Executive Summary
  - Market Analysis
  - Competitive Landscape
  - Technical Feasibility
  - Industry Trends
  - Recommendations
  - Sources

### Business Validation Tasks
- Title format: "Business Validation: [TOPIC]"
- 6 acceptance criteria covering all validation areas
- Structured assessment template with sections:
  - Executive Assessment (Go/No-Go/Caution)
  - Opportunity Score (1-10 across dimensions)
  - Market Opportunity
  - Financial Viability
  - Operational Feasibility
  - Strategic Fit
  - Risk Register (table format)
  - Critical Assumptions
  - Recommendations

### Agent Workflow
Both agents follow consistent pattern:
1. Search for existing tasks (command level)
2. Create task with appropriate ACs
3. Assign to self and set In Progress
4. Add implementation plan
5. Work and mark ACs progressively
6. Add findings/assessment as notes
7. Mark task Done

## Testing Results
```
32 passed in 0.05s
```

All tests verify:
- Discovery happens before agent execution
- Both agents include backlog instructions
- Task creation with proper structure
- AC coverage matches agent responsibilities
- Notes use proper multiline syntax
- Consistent workflow patterns
- Proper labeling and prioritization
<!-- SECTION:NOTES:END -->
