"""Tests for hook event model schema.

Tests event creation, serialization, factory functions, and event matching.
"""

import json


from specify_cli.hooks.events import (
    Artifact,
    Event,
    EventType,
    create_implement_completed_event,
    create_spec_created_event,
    create_task_completed_event,
)


class TestArtifact:
    """Test Artifact dataclass."""

    def test_artifact_creation(self):
        """Test creating an artifact."""
        artifact = Artifact(
            type="source_code",
            path="./src/auth/",
            files_changed=12,
        )
        assert artifact.type == "source_code"
        assert artifact.path == "./src/auth/"
        assert artifact.files_changed == 12

    def test_artifact_to_dict(self):
        """Test artifact serialization to dict."""
        artifact = Artifact(type="report", path="./report.html")
        result = artifact.to_dict()
        assert result["type"] == "report"
        assert result["path"] == "./report.html"
        assert "files_changed" not in result  # None fields excluded

    def test_artifact_from_dict(self):
        """Test artifact deserialization from dict."""
        data = {"type": "prd", "path": "./docs/spec.md", "files_changed": 1}
        artifact = Artifact.from_dict(data)
        assert artifact.type == "prd"
        assert artifact.path == "./docs/spec.md"
        assert artifact.files_changed == 1


class TestEvent:
    """Test Event dataclass."""

    def test_event_creation_minimal(self):
        """Test creating event with minimal required fields."""
        event = Event(
            event_type="spec.created",
            project_root="/tmp/project",
        )
        assert event.event_type == "spec.created"
        assert event.project_root == "/tmp/project"
        assert event.event_id.startswith("evt_")
        assert event.schema_version == "1.0"
        assert event.timestamp.endswith("Z")  # UTC timestamp

    def test_event_creation_full(self):
        """Test creating event with all fields."""
        artifact = Artifact(type="prd", path="./docs/spec.md")
        event = Event(
            event_type="spec.created",
            project_root="/tmp/project",
            feature="user-auth",
            context={"agent": "pm-planner"},
            artifacts=[artifact],
            metadata={"cli_version": "0.0.179"},
        )
        assert event.feature == "user-auth"
        assert event.context == {"agent": "pm-planner"}
        assert len(event.artifacts) == 1
        assert event.metadata == {"cli_version": "0.0.179"}

    def test_event_to_dict(self):
        """Test event serialization to dict."""
        event = Event(
            event_type="task.completed",
            project_root="/tmp/project",
            context={"task_id": "task-189"},
        )
        result = event.to_dict()
        assert result["event_type"] == "task.completed"
        assert result["project_root"] == "/tmp/project"
        assert result["context"] == {"task_id": "task-189"}
        assert "feature" not in result  # None fields excluded

    def test_event_to_json(self):
        """Test event serialization to JSON."""
        event = Event(
            event_type="spec.created",
            project_root="/tmp/project",
        )
        json_str = event.to_json()
        data = json.loads(json_str)
        assert data["event_type"] == "spec.created"
        assert data["project_root"] == "/tmp/project"

    def test_event_from_dict(self):
        """Test event deserialization from dict."""
        data = {
            "event_type": "plan.created",
            "project_root": "/tmp/project",
            "feature": "auth",
        }
        event = Event.from_dict(data)
        assert event.event_type == "plan.created"
        assert event.project_root == "/tmp/project"
        assert event.feature == "auth"

    def test_event_from_json(self):
        """Test event deserialization from JSON."""
        json_str = '{"event_type": "task.created", "project_root": "/tmp"}'
        event = Event.from_json(json_str)
        assert event.event_type == "task.created"
        assert event.project_root == "/tmp"

    def test_event_roundtrip(self):
        """Test event serialization and deserialization roundtrip."""
        original = Event(
            event_type="implement.completed",
            project_root="/tmp/project",
            feature="auth",
            context={"agent": "backend-engineer"},
        )
        json_str = original.to_json()
        restored = Event.from_json(json_str)

        assert restored.event_type == original.event_type
        assert restored.project_root == original.project_root
        assert restored.feature == original.feature
        assert restored.context == original.context


class TestEventType:
    """Test EventType enum."""

    def test_workflow_event_types(self):
        """Test workflow event types are defined."""
        assert EventType.SPEC_CREATED.value == "spec.created"
        assert EventType.SPEC_UPDATED.value == "spec.updated"
        assert EventType.PLAN_CREATED.value == "plan.created"
        assert EventType.IMPLEMENT_STARTED.value == "implement.started"
        assert EventType.IMPLEMENT_COMPLETED.value == "implement.completed"
        assert EventType.VALIDATE_COMPLETED.value == "validate.completed"

    def test_task_event_types(self):
        """Test task event types are defined."""
        assert EventType.TASK_CREATED.value == "task.created"
        assert EventType.TASK_UPDATED.value == "task.updated"
        assert EventType.TASK_COMPLETED.value == "task.completed"
        assert EventType.TASK_AC_CHECKED.value == "task.ac_checked"


class TestEventFactories:
    """Test event factory functions."""

    def test_create_spec_created_event(self):
        """Test creating spec.created event."""
        event = create_spec_created_event(
            project_root="/tmp/project",
            feature="user-auth",
            spec_path="docs/prd/auth-spec.md",
        )
        assert event.event_type == "spec.created"
        assert event.feature == "user-auth"
        assert event.context["agent"] == "pm-planner"
        assert len(event.artifacts) == 1
        assert event.artifacts[0].type == "prd"

    def test_create_task_completed_event(self):
        """Test creating task.completed event."""
        event = create_task_completed_event(
            project_root="/tmp/project",
            task_id="task-189",
            task_title="Implement auth",
            priority="high",
            labels=["backend", "security"],
        )
        assert event.event_type == "task.completed"
        assert event.context["task_id"] == "task-189"
        assert event.context["priority"] == "high"
        assert event.context["labels"] == ["backend", "security"]

    def test_create_implement_completed_event(self):
        """Test creating implement.completed event."""
        event = create_implement_completed_event(
            project_root="/tmp/project",
            feature="auth",
            task_id="task-189",
            files_changed=15,
            source_path="./src/auth/",
        )
        assert event.event_type == "implement.completed"
        assert event.feature == "auth"
        assert event.context["task_id"] == "task-189"
        assert len(event.artifacts) == 1
        assert event.artifacts[0].files_changed == 15


class TestEventIdGeneration:
    """Test event ID generation."""

    def test_event_id_format(self):
        """Test event ID format is correct."""
        event = Event(event_type="test", project_root="/tmp")
        assert event.event_id.startswith("evt_")
        # ULID is 26 characters, so total is 30 (evt_ + 26)
        # Fallback is evt_ + 16 hex chars = 20
        assert len(event.event_id) >= 20

    def test_event_ids_unique(self):
        """Test event IDs are unique."""
        import time

        event1 = Event(event_type="test", project_root="/tmp")
        time.sleep(0.001)  # Ensure different timestamp
        event2 = Event(event_type="test", project_root="/tmp")
        assert event1.event_id != event2.event_id


class TestTimestampGeneration:
    """Test timestamp generation."""

    def test_timestamp_format(self):
        """Test timestamp is ISO 8601 UTC."""
        event = Event(event_type="test", project_root="/tmp")
        assert event.timestamp.endswith("Z")
        assert "T" in event.timestamp
        # Should be parseable as ISO format
        from datetime import datetime

        datetime.fromisoformat(event.timestamp.replace("Z", "+00:00"))
