"""Telemetry module for flowspec role and workflow tracking.

This module provides telemetry collection with PII protection:
- RoleEvent enum for event types
- track_role_event() for logging events
- JSONL writer for persistent storage
- Configuration with opt-in consent

All PII (project names, paths, usernames) is automatically hashed.

Example:
    from flowspec_cli.telemetry import RoleEvent, track_role_event

    # Track a role selection
    track_role_event(
        RoleEvent.ROLE_SELECTED,
        role="dev",
        command="/flow:implement"
    )

    # Track an agent invocation
    track_role_event(
        RoleEvent.AGENT_INVOKED,
        role="dev",
        agent="backend-engineer",
        context={"task_id": "task-123"}
    )

New Event System (v1.1.0):
    from flowspec_cli.telemetry import FlowspecEvent, emit_event

    # Emit a structured event
    event = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@backend-engineer",
        source="cli",
        message="Starting implementation"
    )
    emit_event(event)

Environment Variables:
    FLOWSPEC_TELEMETRY_DISABLED: Set to "1" to disable telemetry
    FLOWSPEC_TELEMETRY_DEBUG: Set to "1" for debug output on errors
    FLOWSPEC_EVENT_DEBUG: Set to "1" for event system debug output
"""

from .config import (
    TelemetryConfig,
    disable_telemetry,
    enable_telemetry,
    is_telemetry_enabled,
    load_telemetry_config,
    save_telemetry_config,
)
from .event_writer import (
    cleanup_old_logs,
    count_events,
    emit_event,
    emit_event_async,
    get_event_log_path,
    read_events,
)
from .events import RoleEvent, TelemetryEvent
from .integration import (
    track_agent_invocation,
    track_agent_invocation_decorator,
    track_command_execution,
    track_handoff,
    track_role_change,
    track_role_selection,
    track_workflow,
)
from .router import EventFilter, EventRouter, get_router, setup_default_router
from .schema import (
    ActionObject,
    AgentId,
    ContextObject,
    ContainerObject,
    CorrelationObject,
    DecisionObject,
    EventSource,
    EventType,
    FlowspecEvent,
    GitObject,
    HookObject,
    SecurityObject,
    SessionId,
    TaskId,
    TaskObject,
    ToolObject,
)
from .tracker import (
    hash_pii,
    reset_writer,
    sanitize_path,
    sanitize_value,
    track_role_event,
)
from .writer import TelemetryWriter

__all__ = [
    # Legacy Events
    "RoleEvent",
    "TelemetryEvent",
    # New Event System (v1.1.0)
    "FlowspecEvent",
    "EventType",
    "AgentId",
    "SessionId",
    "TaskId",
    "EventSource",
    "ToolObject",
    "HookObject",
    "GitObject",
    "TaskObject",
    "ContainerObject",
    "DecisionObject",
    "ActionObject",
    "SecurityObject",
    "ContextObject",
    "CorrelationObject",
    # Event Writer
    "emit_event",
    "emit_event_async",
    "read_events",
    "count_events",
    "cleanup_old_logs",
    "get_event_log_path",
    # Event Router
    "EventRouter",
    "EventFilter",
    "get_router",
    "setup_default_router",
    # Config
    "TelemetryConfig",
    "is_telemetry_enabled",
    "enable_telemetry",
    "disable_telemetry",
    "load_telemetry_config",
    "save_telemetry_config",
    # Tracking
    "track_role_event",
    "hash_pii",
    "sanitize_path",
    "sanitize_value",
    "reset_writer",
    # Integration helpers
    "track_role_selection",
    "track_role_change",
    "track_agent_invocation",
    "track_agent_invocation_decorator",
    "track_handoff",
    "track_command_execution",
    "track_workflow",
    # Writer
    "TelemetryWriter",
]
