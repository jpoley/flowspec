---
description: Create or update feature specifications using PM planner agent (manages /speckit.tasks).
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Instructions

This command creates comprehensive feature specifications using the PM Planner agent, integrating with /speckit.tasks for task management.

### Specification Creation

Use the Task tool to launch the **product-requirements-manager-enhanced** agent with the following prompt:

```
Create a comprehensive Product Requirement Document (PRD) for: [USER INPUT FEATURE]

Context:
[Include any research findings, business validation, or context from previous phases]

Your deliverables should include:

1. **Executive Summary**
   - Problem statement
   - Proposed solution
   - Success metrics
   - Business value

2. **User Stories and Use Cases**
   - Primary user personas
   - User journey maps
   - Detailed user stories with acceptance criteria
   - Edge cases and error scenarios

3. **Functional Requirements**
   - Core features and capabilities
   - User interface requirements
   - API requirements (if applicable)
   - Integration requirements
   - Data requirements

4. **Non-Functional Requirements**
   - Performance requirements (latency, throughput)
   - Scalability requirements
   - Security requirements
   - Accessibility requirements (WCAG 2.1 AA)
   - Compliance requirements

5. **Task Breakdown for /speckit.tasks**
   - Epics and user stories
   - Task dependencies
   - Priority ordering (P0, P1, P2)
   - Estimated complexity (S, M, L, XL)
   - Success criteria for each task

6. **Acceptance Criteria and Testing**
   - Acceptance test scenarios
   - Definition of Done
   - Quality gates
   - Test coverage requirements

7. **Dependencies and Constraints**
   - Technical dependencies
   - External dependencies
   - Timeline constraints
   - Resource constraints
   - Risk factors

8. **Success Metrics**
   - Key Performance Indicators (KPIs)
   - Success criteria
   - Measurement approach
   - Target values

Please ensure the PRD is:
- Clear and unambiguous
- Complete and actionable
- Traceable (requirements → tasks → tests)
- Aligned with business objectives
- Ready for engineering implementation
```

### Output

The agent will produce a comprehensive PRD that integrates with /speckit.tasks and provides clear direction for the planning and implementation phases.
