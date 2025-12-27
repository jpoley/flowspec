---
description: Execute a user-defined custom workflow sequence from flowspec_workflow.yml
loop: inner
# Loop Classification: INNER LOOP
# Custom workflows orchestrate inner loop commands (specify, plan, implement, validate)
---

## User Input

```text
$ARGUMENTS
```

You **MUST** parse the workflow name from the arguments. If no workflow name provided, list available custom workflows.

## Execution Instructions

This command executes user-customizable workflow sequences defined in `flowspec_workflow.yml`.

{{INCLUDE:.claude/commands/flow/_constitution-check.md}}

### Overview

The custom command:
1. Loads custom workflow definitions from `flowspec_workflow.yml`
2. Validates rigor enforcement rules
3. Executes workflow steps in sequence
4. Handles conditional logic (e.g., `complexity >= 7`)
5. Manages checkpoints for spec-ing mode
6. Logs all decisions and events to `.logs/`

### Usage

```bash
# List available custom workflows
/flow:custom

# Execute a specific custom workflow
/flow:custom quick_build
/flow:custom full_design
/flow:custom ship_it
```

### Implementation

Use the `WorkflowOrchestrator` to execute custom workflows:

```python
from pathlib import Path
from flowspec_cli.workflow.orchestrator import WorkflowOrchestrator

# Get workspace root
workspace_root = Path.cwd()

# Generate unique session ID
import datetime
session_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Initialize orchestrator
orchestrator = WorkflowOrchestrator(workspace_root, session_id)

# Parse workflow name from arguments
workflow_name = "$ARGUMENTS".strip()

if not workflow_name:
    # List available workflows
    workflows = orchestrator.list_custom_workflows()
    if not workflows:
        print("No custom workflows defined in flowspec_workflow.yml")
        print("\nExample custom_workflows section:")
        print("""
custom_workflows:
  quick_build:
    name: "Quick Build"
    mode: "vibing"
    steps:
      - workflow: "specify"
      - workflow: "implement"
      - workflow: "validate"
    rigor:
      log_decisions: true
      log_events: true
      backlog_integration: true
      memory_tracking: true
      follow_constitution: true
""")
    else:
        print(f"Available custom workflows ({len(workflows)}):\n")
        for wf_name in workflows:
            wf_def = orchestrator.custom_workflows[wf_name]
            print(f"  {wf_name}")
            print(f"    Name: {wf_def.get('name', 'N/A')}")
            print(f"    Mode: {wf_def.get('mode', 'N/A')}")
            print(f"    Steps: {len(wf_def.get('steps', []))}")
            if 'description' in wf_def:
                print(f"    Description: {wf_def['description']}")
            print()
else:
    # Execute the custom workflow
    try:
        # Optional: Get context for condition evaluation
        # For example, if assess was run, load complexity score
        context = {}

        # Execute workflow
        result = orchestrator.execute_custom_workflow(workflow_name, context)

        if result.success:
            print(f"✓ Custom workflow '{workflow_name}' completed successfully")
            print(f"  Steps executed: {result.steps_executed}")
            print(f"  Steps skipped: {result.steps_skipped}")
            print(f"\nDecision log: .logs/decisions/session-{session_id}.jsonl")
            print(f"Event log: .logs/events/session-{session_id}.jsonl")
        else:
            print(f"✗ Custom workflow '{workflow_name}' failed")
            print(f"  Error: {result.error}")
            print(f"  Steps completed before failure: {result.steps_executed}")

    except ValueError as e:
        print(f"✗ Error: {e}")
        print(f"\nAvailable workflows:")
        for wf_name in orchestrator.list_custom_workflows():
            print(f"  - {wf_name}")
```

### Custom Workflow Definition

Custom workflows are defined in the `custom_workflows` section of `flowspec_workflow.yml`:

```yaml
custom_workflows:
  my_workflow:
    name: "My Custom Workflow"
    description: "Optional description"
    mode: "vibing"  # or "spec-ing"
    steps:
      - workflow: "specify"
      - workflow: "research"
        condition: "complexity >= 7"  # conditional execution
      - workflow: "plan"
        checkpoint: "Review architecture?"  # approval point in spec-ing mode
      - workflow: "implement"
    rigor:  # REQUIRED - cannot be disabled
      log_decisions: true
      log_events: true
      backlog_integration: true
      memory_tracking: true
      follow_constitution: true
```

### Execution Modes

- **vibing**: Autonomous execution, no checkpoints, full logging
- **spec-ing**: Stop at checkpoints for user approval

### Conditional Execution

Steps can include conditions evaluated against context:

```yaml
- workflow: "research"
  condition: "complexity >= 7"  # only run if complexity score >= 7
```

Supported operators: `>=`, `<=`, `==`, `!=`, `>`, `<`

### Rigor Enforcement

All custom workflows MUST have rigor rules set to `true`. This is enforced by the schema and cannot be disabled:

- `log_decisions`: Log to `.logs/decisions/*.jsonl`
- `log_events`: Log to `.logs/events/*.jsonl`
- `backlog_integration`: Integrate with backlog.md via MCP
- `memory_tracking`: Track task state across sessions
- `follow_constitution`: Follow `.specify/memory/constitution.md`

### Integration Point

The orchestrator reaches the workflow invocation point at `src/flowspec_cli/workflow/orchestrator.py:373-416`.

For full integration, wire dispatch logic to actual workflow modules:

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

### See Also

- `build-docs/simplify/flowspec-loop.md` - Inner loop architecture
- `schemas/flowspec_workflow.schema.json` - Custom workflow schema
- `src/flowspec_cli/workflow/orchestrator.py` - Orchestrator implementation
- `src/flowspec_cli/workflow/rigor.py` - Rigor enforcement
