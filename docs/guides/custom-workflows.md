# Custom Workflows Guide

## Overview

Custom workflows allow you to define your own sequences of flowspec commands in `flowspec_workflow.yml`. This enables flexible orchestration while maintaining full rigor enforcement.

## Quick Start

### 1. Define a Custom Workflow

Add to `flowspec_workflow.yml`:

```yaml
custom_workflows:
  quick_build:
    name: "Quick Build"
    description: "Lightweight workflow for simple features"
    mode: "vibing"  # autonomous, no checkpoints
    steps:
      - workflow: "specify"
      - workflow: "implement"
      - workflow: "validate"
    rigor:  # REQUIRED - cannot be disabled
      log_decisions: true
      log_events: true
      backlog_integration: true
      memory_tracking: true
      follow_constitution: true
```

### 2. Run the Custom Workflow

```bash
# List available custom workflows
/flow:custom

# Execute a specific workflow
/flow:custom quick_build
```

## Execution Modes

### Vibing Mode (Autonomous)
```yaml
mode: "vibing"
```
- Executes all steps automatically
- No user interaction
- Full logging to `.logs/decisions/` and `.logs/events/`

### Spec-ing Mode (Checkpoints)
```yaml
mode: "spec-ing"
steps:
  - workflow: "specify"
    checkpoint: "Review PRD before continuing?"
  - workflow: "plan"
```
- Stops at checkpoints for user approval
- Allows review between stages
- Still maintains full logging

## Conditional Execution

Skip steps based on context variables:

```yaml
custom_workflows:
  adaptive_design:
    name: "Adaptive Design"
    mode: "vibing"
    steps:
      - workflow: "assess"
      - workflow: "specify"
      - workflow: "research"
        condition: "complexity >= 7"  # only run if complex
      - workflow: "plan"
        condition: "complexity >= 5"  # skip for very simple features
      - workflow: "implement"
```

### Supported Operators

- `>=` - Greater than or equal
- `<=` - Less than or equal
- `==` - Equal to
- `!=` - Not equal to
- `>` - Greater than
- `<` - Less than

### Context Variables

Context variables can come from:
- Previous workflow outputs (e.g., `complexity` from `/flow:assess`)
- Task metadata
- User-provided values

## Rigor Enforcement (Required)

All custom workflows MUST have these rigor rules set to `true`:

```yaml
rigor:
  log_decisions: true       # Log to .logs/decisions/*.jsonl
  log_events: true          # Log to .logs/events/*.jsonl
  backlog_integration: true # Integrate with backlog.md via MCP
  memory_tracking: true     # Track task state across sessions
  follow_constitution: true # Follow memory/constitution.md
  create_adrs: true         # Create ADRs (optional, defaults to true)
```

**These cannot be disabled.** The schema enforces this with `const: true`.

## Built-in Examples

### quick_build
```yaml
quick_build:
  name: "Quick Build"
  mode: "vibing"
  steps:
    - workflow: "specify"
    - workflow: "implement"
    - workflow: "validate"
```
**Use case:** Simple features that don't need research or extensive planning

### full_design
```yaml
full_design:
  name: "Full Design Workflow"
  mode: "spec-ing"
  steps:
    - workflow: "assess"
    - workflow: "specify"
      checkpoint: "Review PRD before continuing?"
    - workflow: "research"
      condition: "complexity >= 7"
    - workflow: "plan"
      checkpoint: "Review architecture before implementing?"
```
**Use case:** Complex features needing full design review

### ship_it
```yaml
ship_it:
  name: "Build and Ship"
  mode: "vibing"
  steps:
    - workflow: "implement"
    - workflow: "validate"
    - workflow: "submit-n-watch-pr"
```
**Use case:** When design is complete, just build and ship

## Workflow Architecture

Custom workflows orchestrate the 4 core + 2 supporting workflows:

### Core Workflows (Inner Loop)
1. `/flow:specify` - Requirements (PM Planner)
2. `/flow:plan` - Architecture (Architect, Platform Eng)
3. `/flow:implement` - Code (Frontend/Backend Engineers)
4. `/flow:validate` - Quality (QA, Security Engineers)

### Supporting Workflows (Pre-Spec)
5. `/flow:assess` - Complexity scoring
6. `/flow:research` - Deep research

### Ad Hoc Utilities
7. `/flow:submit-n-watch-pr` - PR automation

**Note:** `/flow:operate` was removed (outer loop - belongs to falcondev)

## Logging and Observability

Every custom workflow execution creates:

```
.logs/
  decisions/
    session-YYYYMMDD-HHMMSS.jsonl  # Decision log
  events/
    session-YYYYMMDD-HHMMSS.jsonl  # Event log
```

### Decision Log Format
```json
{
  "timestamp": "2025-12-26T10:00:00-05:00",
  "session": "001",
  "decision": "WORKFLOW_INVOCATION_POINT",
  "context": "Would invoke workflow 'specify'",
  "reasoning": "Real workflow invocation would happen here",
  "alternatives_considered": [],
  "outcome": "Integration point identified"
}
```

### Event Log Format
```json
{
  "timestamp": "2025-12-26T10:00:01-05:00",
  "session": "001",
  "event_type": "WORKFLOW_STEP_START",
  "event": "Starting step 1/3: specify",
  "workflow": "specify",
  "details": {"step": {...}, "context": {...}}
}
```

## Schema Validation

Custom workflows are validated against `schemas/flowspec_workflow.schema.json`.

Common validation errors:

### Missing Required Fields
```
Error: rigor.log_decisions must be true
```
**Fix:** Set all rigor rules to `true`

### Invalid Condition Syntax
```
Error: condition: "complexity > 5" - invalid operator
```
**Fix:** Use valid operators (`>=`, `<=`, `==`, `!=`, `>`, `<`)

### Unknown Workflow Reference
```
Error: workflow 'deploy' not found in workflows section
```
**Fix:** Reference only defined workflows (specify, plan, implement, validate, assess, research, submit-n-watch-pr)

## Integration Points

Custom workflows use the `WorkflowOrchestrator` class:

```python
from pathlib import Path
from flowspec_cli.workflow.orchestrator import WorkflowOrchestrator

workspace_root = Path.cwd()
session_id = "001"

orchestrator = WorkflowOrchestrator(workspace_root, session_id)
result = orchestrator.execute_custom_workflow("quick_build")

if result.success:
    print(f"✓ Completed {result.steps_executed} steps")
else:
    print(f"✗ Failed: {result.error}")
```

### Dispatch Integration (Pending)

The orchestrator identifies the integration point for dispatching to actual workflow handlers at `src/flowspec_cli/workflow/orchestrator.py:373-416`.

Full integration requires wiring dispatch logic:

```python
# Example dispatch pattern (to be implemented):
workflow_handlers = {
    "specify": specify_module.execute,
    "plan": plan_module.execute,
    "implement": implement_module.execute,
    "validate": validate_module.execute,
}

handler = workflow_handlers.get(workflow_name)
if handler:
    handler(workspace_root, ...)
```

## See Also

- `flowspec_workflow.yml` - Define custom workflows here
- `schemas/flowspec_workflow.schema.json` - Custom workflow schema
- `src/flowspec_cli/workflow/orchestrator.py` - Orchestrator implementation
- `src/flowspec_cli/workflow/rigor.py` - Rigor enforcement
- `build-docs/simplify/flowspec-loop.md` - Inner loop architecture
- `templates/commands/flow/custom.md` - `/flow:custom` command reference
