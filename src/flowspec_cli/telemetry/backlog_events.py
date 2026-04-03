"""Backlog event emission helpers.

This module provides utilities for emitting events from backlog operations.
"""

from __future__ import annotations

from .event_writer import emit_event
from .schema import Context, FlowspecEvent, TaskObject


def emit_task_created_event(
    task_id: str,
    title: str,
    labels: list[str] | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a task created event.

    Args:
        task_id: Task identifier
        title: Task title
        labels: Task labels
        agent_id: Agent who created the task

    Returns:
        True if event was emitted successfully
    """
    task_obj = TaskObject(task_id=task_id, title=title, labels=labels)
    context = Context(task_id=task_id)

    event = FlowspecEvent.create(
        event_type="task.created",
        agent_id=agent_id,
        source="cli",
        message=f"Task created: {task_id}",
        task=task_obj,
        context=context,
    )

    return emit_event(event)


def emit_task_assigned_event(
    task_id: str,
    assigned_to: str,
    agent_id: str = "system",
) -> bool:
    """Emit a task assigned event.

    Args:
        task_id: Task identifier
        assigned_to: Agent assigned to task
        agent_id: Agent who assigned the task

    Returns:
        True if event was emitted successfully
    """
    task_obj = TaskObject(task_id=task_id, assigned_to=assigned_to)
    context = Context(task_id=task_id)

    event = FlowspecEvent.create(
        event_type="task.assigned",
        agent_id=agent_id,
        source="cli",
        message=f"Task assigned to {assigned_to}",
        task=task_obj,
        context=context,
    )

    return emit_event(event)


def emit_task_state_changed_event(
    task_id: str,
    from_state: str,
    to_state: str,
    agent_id: str = "system",
) -> bool:
    """Emit a task state changed event.

    Args:
        task_id: Task identifier
        from_state: Previous state
        to_state: New state
        agent_id: Agent who changed the state

    Returns:
        True if event was emitted successfully
    """
    task_obj = TaskObject(task_id=task_id, from_state=from_state, to_state=to_state)
    context = Context(task_id=task_id)

    event = FlowspecEvent.create(
        event_type="task.state_changed",
        agent_id=agent_id,
        source="cli",
        message=f"Task {task_id}: {from_state} → {to_state}",
        task=task_obj,
        context=context,
    )

    return emit_event(event)


def emit_task_ac_checked_event(
    task_id: str,
    ac_index: int,
    ac_text: str,
    agent_id: str = "system",
) -> bool:
    """Emit a task acceptance criterion checked event.

    Args:
        task_id: Task identifier
        ac_index: Acceptance criterion index
        ac_text: Acceptance criterion text
        agent_id: Agent who checked the AC

    Returns:
        True if event was emitted successfully
    """
    task_obj = TaskObject(task_id=task_id, ac_index=ac_index, ac_text=ac_text)
    context = Context(task_id=task_id)

    event = FlowspecEvent.create(
        event_type="task.ac_checked",
        agent_id=agent_id,
        source="cli",
        message=f"Task {task_id}: AC #{ac_index} checked",
        task=task_obj,
        context=context,
    )

    return emit_event(event)


def emit_task_blocked_event(
    task_id: str,
    reason: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a task blocked event.

    Args:
        task_id: Task identifier
        reason: Reason for blocking
        agent_id: Agent who blocked the task

    Returns:
        True if event was emitted successfully
    """
    task_obj = TaskObject(task_id=task_id)
    context = Context(task_id=task_id)

    message = f"Task {task_id} blocked"
    if reason:
        message += f": {reason}"

    event = FlowspecEvent.create(
        event_type="task.blocked",
        agent_id=agent_id,
        source="cli",
        message=message,
        task=task_obj,
        context=context,
        metadata={"reason": reason} if reason else None,
    )

    return emit_event(event)


def emit_task_unblocked_event(
    task_id: str,
    agent_id: str = "system",
) -> bool:
    """Emit a task unblocked event.

    Args:
        task_id: Task identifier
        agent_id: Agent who unblocked the task

    Returns:
        True if event was emitted successfully
    """
    task_obj = TaskObject(task_id=task_id)
    context = Context(task_id=task_id)

    event = FlowspecEvent.create(
        event_type="task.unblocked",
        agent_id=agent_id,
        source="cli",
        message=f"Task {task_id} unblocked",
        task=task_obj,
        context=context,
    )

    return emit_event(event)


def emit_task_completed_event(
    task_id: str,
    agent_id: str = "system",
) -> bool:
    """Emit a task completed event.

    Args:
        task_id: Task identifier
        agent_id: Agent who completed the task

    Returns:
        True if event was emitted successfully
    """
    task_obj = TaskObject(task_id=task_id)
    context = Context(task_id=task_id)

    event = FlowspecEvent.create(
        event_type="task.completed",
        agent_id=agent_id,
        source="cli",
        message=f"Task {task_id} completed",
        task=task_obj,
        context=context,
    )

    return emit_event(event)


def emit_task_archived_event(
    task_id: str,
    agent_id: str = "system",
) -> bool:
    """Emit a task archived event.

    Args:
        task_id: Task identifier
        agent_id: Agent who archived the task

    Returns:
        True if event was emitted successfully
    """
    task_obj = TaskObject(task_id=task_id)
    context = Context(task_id=task_id)

    event = FlowspecEvent.create(
        event_type="task.archived",
        agent_id=agent_id,
        source="cli",
        message=f"Task {task_id} archived",
        task=task_obj,
        context=context,
    )

    return emit_event(event)


__all__ = [
    "emit_task_created_event",
    "emit_task_assigned_event",
    "emit_task_state_changed_event",
    "emit_task_ac_checked_event",
    "emit_task_blocked_event",
    "emit_task_unblocked_event",
    "emit_task_completed_event",
    "emit_task_archived_event",
]
