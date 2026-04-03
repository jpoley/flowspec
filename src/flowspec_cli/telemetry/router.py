"""Event routing system with namespace dispatch for flowspec events.

This module provides the EventRouter for dispatching events to handlers
based on namespace patterns with support for wildcards.

Based on: task-487 - Implement Event Router with Namespace Dispatch
"""

from __future__ import annotations

import fnmatch
import re
from typing import TYPE_CHECKING, Callable, Protocol

if TYPE_CHECKING:
    from .schema import FlowspecEvent


class EventHandler(Protocol):
    """Protocol for event handlers."""

    def __call__(self, event: FlowspecEvent) -> bool:
        """Handle an event.

        Args:
            event: The flowspec event to handle

        Returns:
            True if handled successfully, False otherwise
        """
        ...


class EventFilter:
    """Filter events by various criteria."""

    def __init__(
        self,
        task_id: str | None = None,
        agent_id: str | None = None,
        time_range: tuple[str, str] | None = None,
        event_types: list[str] | None = None,
    ):
        """Initialize event filter.

        Args:
            task_id: Filter by task ID
            agent_id: Filter by agent ID
            time_range: Filter by time range (start, end) ISO 8601
            event_types: Filter by event types (supports wildcards)
        """
        self.task_id = task_id
        self.agent_id = agent_id
        self.time_range = time_range
        self.event_types = event_types or []

    def matches(self, event: FlowspecEvent) -> bool:
        """Check if event matches filter criteria.

        Args:
            event: The event to check

        Returns:
            True if event matches all filter criteria
        """
        # Filter by task_id
        if self.task_id:
            if not event.context or event.context.task_id != self.task_id:
                return False

        # Filter by agent_id
        if self.agent_id:
            if event.agent_id != self.agent_id:
                return False

        # Filter by time range
        if self.time_range:
            start, end = self.time_range
            if event.timestamp < start or event.timestamp > end:
                return False

        # Filter by event types (with wildcard support)
        if self.event_types:
            matched = False
            for pattern in self.event_types:
                if fnmatch.fnmatch(event.event_type, pattern):
                    matched = True
                    break
            if not matched:
                return False

        return True


class EventRouter:
    """Route events to handlers based on namespace patterns.

    The router supports:
    - Pattern matching with wildcards (e.g., git.* matches all git events)
    - Multiple handlers per pattern
    - Event filtering by task_id, agent_id, time_range
    - Built-in handlers for JSONL file and MCP server

    Example:
        >>> router = EventRouter()
        >>> router.register_handler("git.*", git_event_handler)
        >>> router.register_handler("lifecycle.*", lifecycle_handler)
        >>> router.dispatch(event)
    """

    def __init__(self):
        """Initialize the event router."""
        self._handlers: dict[str, list[EventHandler]] = {}
        self._filters: dict[str, EventFilter] = {}

    def register_handler(
        self,
        pattern: str,
        handler: EventHandler,
        event_filter: EventFilter | None = None,
    ) -> None:
        """Register an event handler for a pattern.

        Args:
            pattern: Event type pattern (supports wildcards like git.*)
            handler: Handler function to call
            event_filter: Optional filter to apply before calling handler

        Example:
            >>> def my_handler(event: FlowspecEvent) -> bool:
            ...     print(f"Got event: {event.event_type}")
            ...     return True
            >>> router.register_handler("git.*", my_handler)
        """
        if pattern not in self._handlers:
            self._handlers[pattern] = []

        self._handlers[pattern].append(handler)

        if event_filter:
            self._filters[pattern] = event_filter

    def unregister_handler(self, pattern: str, handler: EventHandler) -> bool:
        """Unregister a specific handler from a pattern.

        Args:
            pattern: Event type pattern
            handler: Handler function to remove

        Returns:
            True if handler was removed, False if not found
        """
        if pattern not in self._handlers:
            return False

        try:
            self._handlers[pattern].remove(handler)
            return True
        except ValueError:
            return False

    def dispatch(self, event: FlowspecEvent) -> int:
        """Dispatch an event to all matching handlers.

        Args:
            event: The flowspec event to dispatch

        Returns:
            Number of handlers that successfully processed the event

        Example:
            >>> event = FlowspecEvent.create(
            ...     event_type="git.commit",
            ...     agent_id="@backend-engineer",
            ...     source="cli"
            ... )
            >>> router.dispatch(event)
            2
        """
        handled_count = 0

        for pattern, handlers in self._handlers.items():
            # Check if event type matches pattern
            if not self._matches_pattern(event.event_type, pattern):
                continue

            # Apply filter if configured
            if pattern in self._filters:
                if not self._filters[pattern].matches(event):
                    continue

            # Call all handlers for this pattern
            for handler in handlers:
                try:
                    if handler(event):
                        handled_count += 1
                except Exception:
                    # Handlers should not fail the dispatch
                    continue

        return handled_count

    def _matches_pattern(self, event_type: str, pattern: str) -> bool:
        """Check if event type matches a pattern.

        Supports:
        - Exact match: "git.commit" matches "git.commit"
        - Wildcard: "git.*" matches all git.* events
        - Prefix: "lifecycle" matches "lifecycle.*"

        Args:
            event_type: The event type to check
            pattern: The pattern to match against

        Returns:
            True if event type matches pattern
        """
        # Exact match
        if event_type == pattern:
            return True

        # Wildcard match
        if "*" in pattern:
            return fnmatch.fnmatch(event_type, pattern)

        # Prefix match (pattern without .* matches namespace)
        if "." not in pattern:
            return event_type.startswith(f"{pattern}.")

        return False

    def list_patterns(self) -> list[str]:
        """List all registered patterns.

        Returns:
            List of registered event patterns
        """
        return list(self._handlers.keys())

    def count_handlers(self, pattern: str | None = None) -> int:
        """Count handlers for a pattern or all handlers.

        Args:
            pattern: Event type pattern (None for all)

        Returns:
            Number of handlers
        """
        if pattern is None:
            return sum(len(handlers) for handlers in self._handlers.values())

        return len(self._handlers.get(pattern, []))

    def clear(self) -> None:
        """Clear all handlers and filters."""
        self._handlers.clear()
        self._filters.clear()


# Global router instance
_router: EventRouter | None = None


def get_router() -> EventRouter:
    """Get the global event router.

    Returns:
        The global EventRouter instance
    """
    global _router
    if _router is None:
        _router = EventRouter()
    return _router


# Built-in handler: JSONL file writer
def jsonl_file_handler(event: FlowspecEvent) -> bool:
    """Built-in handler that writes events to JSONL file.

    Args:
        event: The flowspec event to write

    Returns:
        True if written successfully
    """
    from .event_writer import emit_event

    return emit_event(event)


# Built-in handler: MCP server (placeholder)
def mcp_server_handler(event: FlowspecEvent) -> bool:
    """Built-in handler that sends events to MCP server.

    This is a placeholder for future MCP integration.

    Args:
        event: The flowspec event to send

    Returns:
        True if sent successfully
    """
    # TODO: Implement MCP server integration
    return True


def setup_default_router() -> EventRouter:
    """Setup router with default handlers.

    Registers:
    - JSONL file handler for all events (*.*)
    - MCP server handler for coordination events (coordination.*)

    Returns:
        Configured EventRouter instance
    """
    router = get_router()

    # Register JSONL handler for all events
    router.register_handler("*.*", jsonl_file_handler)

    # Register MCP handler for coordination events
    # router.register_handler("coordination.*", mcp_server_handler)

    return router


__all__ = [
    "EventHandler",
    "EventFilter",
    "EventRouter",
    "get_router",
    "jsonl_file_handler",
    "mcp_server_handler",
    "setup_default_router",
]
