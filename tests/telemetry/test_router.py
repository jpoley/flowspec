"""Tests for the event router module."""

from __future__ import annotations

from flowspec_cli.telemetry.router import EventRouter, get_router, register_handler, reset_router, route_event
from flowspec_cli.telemetry.schema import FlowspecEvent


def test_register_handler() -> None:
    """Test registering an event handler."""
    router = EventRouter()
    events_received = []

    def handler(event: FlowspecEvent) -> None:
        events_received.append(event)

    router.register_handler("lifecycle.*", handler)

    event = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@test-agent",
    )

    router.route(event)
    assert len(events_received) == 1
    assert events_received[0].event_type == "lifecycle.started"


def test_pattern_matching() -> None:
    """Test wildcard pattern matching."""
    router = EventRouter()
    lifecycle_events = []
    task_events = []
    all_events = []

    def lifecycle_handler(event: FlowspecEvent) -> None:
        lifecycle_events.append(event)

    def task_handler(event: FlowspecEvent) -> None:
        task_events.append(event)

    def all_handler(event: FlowspecEvent) -> None:
        all_events.append(event)

    router.register_handler("lifecycle.*", lifecycle_handler)
    router.register_handler("task.*", task_handler)
    router.register_handler("*", all_handler)

    # Route lifecycle event
    event1 = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@agent1",
    )
    router.route(event1)

    assert len(lifecycle_events) == 1
    assert len(task_events) == 0
    assert len(all_events) == 1

    # Route task event
    event2 = FlowspecEvent.create(
        event_type="task.created",
        agent_id="@agent2",
    )
    router.route(event2)

    assert len(lifecycle_events) == 1
    assert len(task_events) == 1
    assert len(all_events) == 2


def test_multiple_handlers_per_pattern() -> None:
    """Test multiple handlers for the same pattern."""
    router = EventRouter()
    handler1_events = []
    handler2_events = []

    def handler1(event: FlowspecEvent) -> None:
        handler1_events.append(event)

    def handler2(event: FlowspecEvent) -> None:
        handler2_events.append(event)

    router.register_handler("git.*", handler1)
    router.register_handler("git.*", handler2)

    event = FlowspecEvent.create(
        event_type="git.commit",
        agent_id="@agent1",
    )

    count = router.route(event)
    assert count == 2
    assert len(handler1_events) == 1
    assert len(handler2_events) == 1


def test_unregister_handler() -> None:
    """Test unregistering a handler."""
    router = EventRouter()
    events_received = []

    def handler(event: FlowspecEvent) -> None:
        events_received.append(event)

    router.register_handler("lifecycle.*", handler)

    # Route event - should be received
    event1 = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@agent1",
    )
    router.route(event1)
    assert len(events_received) == 1

    # Unregister handler
    router.unregister_handler("lifecycle.*", handler)

    # Route event - should not be received
    event2 = FlowspecEvent.create(
        event_type="lifecycle.completed",
        agent_id="@agent1",
    )
    router.route(event2)
    assert len(events_received) == 1  # Still 1, not 2


def test_unregister_all_handlers_for_pattern() -> None:
    """Test unregistering all handlers for a pattern."""
    router = EventRouter()
    handler1_events = []
    handler2_events = []

    def handler1(event: FlowspecEvent) -> None:
        handler1_events.append(event)

    def handler2(event: FlowspecEvent) -> None:
        handler2_events.append(event)

    router.register_handler("task.*", handler1)
    router.register_handler("task.*", handler2)

    # Unregister all handlers
    router.unregister_handler("task.*")

    event = FlowspecEvent.create(
        event_type="task.created",
        agent_id="@agent1",
    )

    count = router.route(event)
    assert count == 0
    assert len(handler1_events) == 0
    assert len(handler2_events) == 0


def test_get_matching_handlers() -> None:
    """Test getting matching handlers."""
    router = EventRouter()

    def handler1(event: FlowspecEvent) -> None:
        pass

    def handler2(event: FlowspecEvent) -> None:
        pass

    router.register_handler("lifecycle.*", handler1)
    router.register_handler("lifecycle.started", handler2)

    # Should match both patterns
    handlers = router.get_matching_handlers("lifecycle.started")
    assert len(handlers) == 2


def test_clear_handlers() -> None:
    """Test clearing all handlers."""
    router = EventRouter()

    def handler(event: FlowspecEvent) -> None:
        pass

    router.register_handler("lifecycle.*", handler)
    router.register_handler("task.*", handler)

    assert len(router.list_patterns()) == 2

    router.clear_handlers()

    assert len(router.list_patterns()) == 0


def test_list_patterns() -> None:
    """Test listing registered patterns."""
    router = EventRouter()

    def handler(event: FlowspecEvent) -> None:
        pass

    router.register_handler("lifecycle.*", handler)
    router.register_handler("task.*", handler)
    router.register_handler("git.*", handler)

    patterns = router.list_patterns()
    assert len(patterns) == 3
    assert "lifecycle.*" in patterns
    assert "task.*" in patterns
    assert "git.*" in patterns


def test_global_router() -> None:
    """Test global router instance."""
    reset_router()

    events_received = []

    def handler(event: FlowspecEvent) -> None:
        events_received.append(event)

    register_handler("lifecycle.*", handler)

    event = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@test-agent",
    )

    count = route_event(event)
    assert count == 1
    assert len(events_received) == 1


def test_handler_error_handling() -> None:
    """Test that handler errors don't stop routing."""
    router = EventRouter()
    handler1_called = []
    handler2_called = []

    def failing_handler(event: FlowspecEvent) -> None:
        handler1_called.append(True)
        raise ValueError("Handler error")

    def working_handler(event: FlowspecEvent) -> None:
        handler2_called.append(True)

    router.register_handler("lifecycle.*", failing_handler)
    router.register_handler("lifecycle.*", working_handler)

    event = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@agent1",
    )

    # Should still route to both handlers
    count = router.route(event)
    assert count == 2
    assert len(handler1_called) == 1
    assert len(handler2_called) == 1


def test_exact_match() -> None:
    """Test exact event type matching."""
    router = EventRouter()
    events_received = []

    def handler(event: FlowspecEvent) -> None:
        events_received.append(event)

    # Register exact match
    router.register_handler("lifecycle.started", handler)

    # Should match
    event1 = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@agent1",
    )
    router.route(event1)
    assert len(events_received) == 1

    # Should not match
    event2 = FlowspecEvent.create(
        event_type="lifecycle.completed",
        agent_id="@agent1",
    )
    router.route(event2)
    assert len(events_received) == 1  # Still 1


def test_namespace_matching() -> None:
    """Test namespace-level pattern matching."""
    router = EventRouter()
    git_events = []
    task_events = []

    def git_handler(event: FlowspecEvent) -> None:
        git_events.append(event)

    def task_handler(event: FlowspecEvent) -> None:
        task_events.append(event)

    router.register_handler("git.*", git_handler)
    router.register_handler("task.*", task_handler)

    # Create various events
    events = [
        FlowspecEvent.create(event_type="git.commit", agent_id="@agent1"),
        FlowspecEvent.create(event_type="git.pushed", agent_id="@agent1"),
        FlowspecEvent.create(event_type="task.created", agent_id="@agent1"),
        FlowspecEvent.create(event_type="lifecycle.started", agent_id="@agent1"),
    ]

    for event in events:
        router.route(event)

    assert len(git_events) == 2
    assert len(task_events) == 1
