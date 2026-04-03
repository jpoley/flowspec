"""Tests for the event writer module."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from flowspec_cli.telemetry.event_writer import EventWriter, emit_event, get_writer, reset_writer
from flowspec_cli.telemetry.schema import FlowspecEvent


@pytest.fixture
def temp_events_dir(tmp_path: Path) -> Path:
    """Create a temporary events directory."""
    events_dir = tmp_path / "events"
    events_dir.mkdir()
    return events_dir


@pytest.fixture
def writer(temp_events_dir: Path) -> EventWriter:
    """Create an event writer with a temporary directory."""
    return EventWriter(events_dir=temp_events_dir, enable_daily_rotation=False)


def test_write_event(writer: EventWriter) -> None:
    """Test writing a single event."""
    event = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@test-agent",
        message="Test event",
    )

    result = writer.write_event(event)
    assert result is True

    # Verify event was written
    event_file = writer._get_event_file()
    assert event_file.exists()

    with event_file.open("r") as f:
        line = f.readline().strip()
        parsed = json.loads(line)
        assert parsed["event_type"] == "lifecycle.started"
        assert parsed["agent_id"] == "@test-agent"
        assert parsed["message"] == "Test event"
        assert parsed["version"] == "1.1.0"


def test_write_multiple_events(writer: EventWriter) -> None:
    """Test writing multiple events."""
    events = [
        FlowspecEvent.create(
            event_type="lifecycle.started",
            agent_id="@agent1",
        ),
        FlowspecEvent.create(
            event_type="lifecycle.completed",
            agent_id="@agent1",
        ),
        FlowspecEvent.create(
            event_type="task.created",
            agent_id="@agent2",
        ),
    ]

    written = writer.write_events(events)
    assert written == 3

    # Verify all events were written
    assert writer.count_events() == 3


def test_read_events(writer: EventWriter) -> None:
    """Test reading events from the file."""
    # Write some events
    for i in range(5):
        event = FlowspecEvent.create(
            event_type="lifecycle.started",
            agent_id=f"@agent{i}",
        )
        writer.write_event(event)

    # Read events
    events = writer.read_events(limit=3)
    assert len(events) == 3

    # Events should be in reverse order (most recent first)
    assert events[0]["agent_id"] == "@agent4"
    assert events[1]["agent_id"] == "@agent3"
    assert events[2]["agent_id"] == "@agent2"


def test_count_events(writer: EventWriter) -> None:
    """Test counting events."""
    assert writer.count_events() == 0

    # Write some events
    for i in range(10):
        event = FlowspecEvent.create(
            event_type="lifecycle.started",
            agent_id=f"@agent{i}",
        )
        writer.write_event(event)

    assert writer.count_events() == 10


def test_daily_rotation(temp_events_dir: Path) -> None:
    """Test daily rotation of event files."""
    writer = EventWriter(events_dir=temp_events_dir, enable_daily_rotation=True)

    event = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@test-agent",
    )

    writer.write_event(event)

    # Verify daily-rotated file exists
    event_file = writer._get_event_file()
    assert "events-" in event_file.name
    assert ".jsonl" in event_file.name


def test_list_event_files(temp_events_dir: Path) -> None:
    """Test listing event files."""
    writer = EventWriter(events_dir=temp_events_dir, enable_daily_rotation=True)

    # Create multiple event files
    for i in range(3):
        event = FlowspecEvent.create(
            event_type="lifecycle.started",
            agent_id=f"@agent{i}",
        )
        writer.write_event(event)

    event_files = writer.list_event_files()
    assert len(event_files) >= 1


def test_global_writer(temp_events_dir: Path) -> None:
    """Test global writer instance."""
    reset_writer(events_dir=temp_events_dir, enable_daily_rotation=False)

    writer = get_writer()
    assert isinstance(writer, EventWriter)

    event = FlowspecEvent.create(
        event_type="lifecycle.started",
        agent_id="@test-agent",
    )

    result = emit_event(event)
    assert result is True

    # Verify event was written
    assert writer.count_events() == 1


def test_event_with_all_fields(writer: EventWriter) -> None:
    """Test writing an event with all optional fields."""
    from flowspec_cli.telemetry.schema import Context, GitObject, ToolObject

    event = FlowspecEvent.create(
        event_type="git.commit",
        agent_id="@backend-engineer",
        session_id="sess-123",
        source="cli",
        status="progress",
        message="Commit made",
        progress=0.5,
        tool=ToolObject(tool_name="Bash", tool_input={"command": "git commit"}),
        git=GitObject(
            operation="commit",
            sha="abc123",
            branch_name="feat/test",
            message="Test commit",
        ),
        context=Context(task_id="task-123", branch_name="feat/test"),
        metadata={"custom": "data"},
    )

    result = writer.write_event(event)
    assert result is True

    # Read and verify
    events = writer.read_events(limit=1)
    assert len(events) == 1
    parsed = events[0]

    assert parsed["event_type"] == "git.commit"
    assert parsed["agent_id"] == "@backend-engineer"
    assert parsed["session_id"] == "sess-123"
    assert parsed["source"] == "cli"
    assert parsed["status"] == "progress"
    assert parsed["message"] == "Commit made"
    assert parsed["progress"] == 0.5
    assert parsed["tool"]["tool_name"] == "Bash"
    assert parsed["git"]["sha"] == "abc123"
    assert parsed["context"]["task_id"] == "task-123"
    assert parsed["metadata"]["custom"] == "data"
