# Claude-Trace Observability Guide

**Task**: task-136 - Add Primary Support for claude-trace Observability Tool

This guide documents how to use claude-trace for debugging and profiling JP Spec Kit workflows.

## Overview

[claude-trace](https://github.com/anthropics/claude-trace) provides distributed tracing for Claude Code sessions, enabling:

- **Workflow Debugging**: Trace agent decisions and tool calls
- **Token Usage Tracking**: Attribute costs to specific operations
- **Performance Profiling**: Identify bottlenecks in complex workflows
- **Audit Logging**: Track all file operations and commands

## Installation

```bash
# Install claude-trace
pip install claude-trace

# Or with uv
uv pip install claude-trace
```

## Basic Usage

### Starting a Traced Session

```bash
# Start Claude Code with tracing enabled
claude-trace start claude

# Or enable for an existing session
export CLAUDE_TRACE_ENABLED=1
```

### Viewing Traces

```bash
# List recent traces
claude-trace list

# View specific trace
claude-trace show <trace-id>

# Query traces by agent
claude-trace query --agent "frontend-engineer"

# Query traces by task
claude-trace query --task "task-123"
```

## Debugging /jpspec Commands

### Trace a Workflow

```bash
# Trace a specify workflow
claude-trace start claude
/jpspec:implement

# After completion, view the trace
claude-trace show --last
```

### Common Debugging Scenarios

#### 1. Understanding Agent Decisions

```bash
# See which agents were invoked
claude-trace query --last --filter "agent_type"

# Output shows decision chain:
# - pm-planner: Created PRD
# - architect: Designed system
# - backend-engineer: Implemented API
```

#### 2. Finding Performance Bottlenecks

```bash
# Show timing breakdown
claude-trace show --last --timing

# Output:
# Total: 45s
# - Tool calls: 30s (67%)
#   - Read: 10s
#   - Grep: 5s
#   - Write: 15s
# - API calls: 15s (33%)
```

#### 3. Token Usage Attribution

```bash
# See token usage by operation
claude-trace show --last --tokens

# Output:
# Total tokens: 125,000
# - Context: 80,000 (64%)
# - Generation: 45,000 (36%)
# - By agent:
#   - backend-engineer: 50,000
#   - frontend-engineer: 40,000
#   - qa-engineer: 35,000
```

## Integration with JP Spec Kit

### Automatic Tracing

JP Spec Kit emits trace events automatically when configured:

```json
// .claude/settings.json
{
  "tracing": {
    "enabled": true,
    "level": "detailed",
    "retention_days": 30
  }
}
```

### Task-Level Tracing

Each `/jpspec` command emits structured events:

```bash
# Events emitted during /jpspec:specify
spec.workflow.started   - Workflow begins
spec.agent.invoked      - Agent started (pm-planner)
spec.artifact.created   - PRD created
spec.task.created       - Backlog tasks generated
spec.workflow.completed - Workflow finished
```

### Query Examples

```bash
# Find failed workflows
claude-trace query --status "failed" --since "1d"

# Find slow operations (>10s)
claude-trace query --duration ">10s" --since "1h"

# Find specific task work
claude-trace query --metadata "task_id=task-123"
```

## Privacy and Security

### Local-Only by Default

- Traces stored locally in `~/.claude-trace/`
- No data sent to external services
- Configurable retention period

### Secret Redaction

Sensitive data is automatically redacted:

```bash
# Redaction patterns (default)
- API keys: sk-*, xoxb-*, ghp_*
- Passwords: password=*, secret=*
- Tokens: Bearer *, token=*
```

### Configuring Redaction

```json
// .claude/settings.json
{
  "tracing": {
    "redact_patterns": [
      "MY_SECRET_*",
      "*_API_KEY"
    ]
  }
}
```

## Troubleshooting

### Traces Not Appearing

1. Verify tracing is enabled:
   ```bash
   echo $CLAUDE_TRACE_ENABLED
   ```

2. Check trace storage:
   ```bash
   ls ~/.claude-trace/
   ```

3. Verify permissions:
   ```bash
   chmod 755 ~/.claude-trace/
   ```

### Missing Events

1. Check trace level:
   ```bash
   # Use detailed level for all events
   claude-trace config set level detailed
   ```

2. Verify hook configuration in `.claude/settings.json`

### Performance Impact

Tracing adds <5% overhead. For minimal impact:

```json
{
  "tracing": {
    "level": "summary",  // Less detail, less overhead
    "async": true        // Non-blocking writes
  }
}
```

## Best Practices

1. **Enable during debugging only**: Disable tracing in production for performance
2. **Set retention policy**: Default 30 days prevents unbounded growth
3. **Use query filters**: Avoid loading full traces for large sessions
4. **Redact secrets**: Always verify sensitive data is redacted

## Related Documentation

- [claude-trace GitHub](https://github.com/anthropics/claude-trace)
- [JP Spec Kit Hooks](../reference/hooks.md)
- [Workflow Troubleshooting](./workflow-troubleshooting.md)
