"""JSONL event writer with daily rotation for flowspec event system.

This module provides the core emit_event function and JSONL file writer
with daily rotation and configurable retention.

Based on: task-486 - Implement JSONL Event Writer Library
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schema import FlowspecEvent


def get_event_log_path(base_dir: Path | str | None = None) -> Path:
    """Get the path for today's event log file.

    Args:
        base_dir: Base directory for event logs (defaults to .logs/events)

    Returns:
        Path to today's JSONL event log file
    """
    if base_dir is None:
        base_dir = Path.cwd() / ".logs" / "events"
    else:
        base_dir = Path(base_dir)

    # Daily rotation: YYYY-MM-DD.jsonl
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return base_dir / f"{today}.jsonl"


def emit_event(
    event: FlowspecEvent, base_dir: Path | str | None = None, validate: bool = True
) -> bool:
    """Emit a flowspec event to the JSONL event log.

    This is the primary entry point for event emission. Events are
    automatically written to daily-rotated JSONL files.

    Args:
        event: The flowspec event to emit
        base_dir: Base directory for event logs (defaults to .logs/events)
        validate: Whether to validate event before writing (default: True)

    Returns:
        True if the event was emitted successfully, False otherwise

    Example:
        >>> from flowspec_cli.telemetry.schema import FlowspecEvent
        >>> event = FlowspecEvent.create(
        ...     event_type="lifecycle.started",
        ...     agent_id="@backend-engineer",
        ...     source="cli",
        ...     message="Starting implementation"
        ... )
        >>> emit_event(event)
        True
    """
    try:
        log_path = get_event_log_path(base_dir)

        # Ensure parent directory exists
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Validate event schema version
        if validate and event.version != "1.1.0":
            if os.environ.get("FLOWSPEC_EVENT_DEBUG"):
                print(f"Event version mismatch: {event.version} != 1.1.0")
            return False

        # Convert event to JSON line
        event_dict = event.to_dict()
        json_line = json.dumps(event_dict, separators=(",", ":"))

        # Append to file (atomic append on most systems)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json_line + "\n")

        return True
    except OSError as e:
        # Log error but don't fail - event emission should be non-blocking
        if os.environ.get("FLOWSPEC_EVENT_DEBUG"):
            print(f"Event write error: {e}")
        return False
    except Exception as e:
        if os.environ.get("FLOWSPEC_EVENT_DEBUG"):
            print(f"Event emission error: {e}")
        return False


def emit_event_async(
    event: FlowspecEvent, base_dir: Path | str | None = None
) -> bool:
    """Emit an event asynchronously (non-blocking).

    This is a placeholder for future async implementation.
    Currently delegates to synchronous emit_event.

    Args:
        event: The flowspec event to emit
        base_dir: Base directory for event logs

    Returns:
        True if the event was emitted successfully
    """
    # TODO: Implement true async emission with asyncio
    return emit_event(event, base_dir, validate=True)


def read_events(
    date_str: str | None = None,
    base_dir: Path | str | None = None,
    limit: int | None = None,
) -> list[dict]:
    """Read events from a specific date's log file.

    Args:
        date_str: Date in YYYY-MM-DD format (defaults to today)
        base_dir: Base directory for event logs
        limit: Maximum number of events to read (from end of file)

    Returns:
        List of event dictionaries (most recent first if limit is specified)

    Example:
        >>> events = read_events("2025-12-13", limit=100)
        >>> len(events)
        42
    """
    if base_dir is None:
        base_dir = Path.cwd() / ".logs" / "events"
    else:
        base_dir = Path(base_dir)

    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    log_path = base_dir / f"{date_str}.jsonl"

    if not log_path.exists():
        return []

    try:
        with log_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Apply limit if specified
        if limit is not None:
            lines = lines[-limit:]

        # Parse JSON lines
        events = []
        for line in reversed(lines) if limit else lines:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return events
    except OSError:
        return []


def count_events(
    date_str: str | None = None, base_dir: Path | str | None = None
) -> int:
    """Count events in a specific date's log file.

    Args:
        date_str: Date in YYYY-MM-DD format (defaults to today)
        base_dir: Base directory for event logs

    Returns:
        Number of events in the log file
    """
    if base_dir is None:
        base_dir = Path.cwd() / ".logs" / "events"
    else:
        base_dir = Path(base_dir)

    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    log_path = base_dir / f"{date_str}.jsonl"

    if not log_path.exists():
        return 0

    try:
        with log_path.open("r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    except OSError:
        return 0


def cleanup_old_logs(
    base_dir: Path | str | None = None, retention_days: int = 30
) -> int:
    """Clean up event logs older than retention period.

    Args:
        base_dir: Base directory for event logs
        retention_days: Number of days to retain logs (default: 30)

    Returns:
        Number of log files deleted

    Example:
        >>> cleanup_old_logs(retention_days=7)
        5
    """
    if base_dir is None:
        base_dir = Path.cwd() / ".logs" / "events"
    else:
        base_dir = Path(base_dir)

    if not base_dir.exists():
        return 0

    deleted = 0
    now = datetime.now(timezone.utc)

    try:
        for log_file in base_dir.glob("*.jsonl"):
            # Parse date from filename
            try:
                file_date = datetime.strptime(log_file.stem, "%Y-%m-%d")
                file_date = file_date.replace(tzinfo=timezone.utc)
                age_days = (now - file_date).days

                if age_days > retention_days:
                    log_file.unlink()
                    deleted += 1
            except (ValueError, OSError):
                continue

        return deleted
    except OSError:
        return 0


__all__ = [
    "emit_event",
    "emit_event_async",
    "read_events",
    "count_events",
    "cleanup_old_logs",
    "get_event_log_path",
]
