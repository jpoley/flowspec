"""Tests for flowspec status command."""
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from flowspec_cli.status import (
    format_status_human,
    format_status_json,
    get_current_phase,
    get_flowspec_version,
    get_next_action,
    get_project_name,
    get_status_data,
    get_task_counts,
    get_workflow_mode,
)


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


def test_get_flowspec_version():
    """Test version detection using importlib.metadata."""
    version = get_flowspec_version()
    assert isinstance(version, str)
    assert len(version) > 0


def test_get_project_name_from_directory(temp_project_dir: Path, monkeypatch):
    """Test project name from directory name."""
    monkeypatch.chdir(temp_project_dir)
    name = get_project_name()
    assert name == "test_project"


def test_get_workflow_mode_light(temp_project_dir: Path, monkeypatch):
    """Test Light mode detection (no workflow config, no .logs)."""
    monkeypatch.chdir(temp_project_dir)
    mode = get_workflow_mode()
    assert mode == "Light"


@patch("flowspec_cli.status.task_list")
def test_get_current_phase_no_task(mock_task_list, temp_project_dir: Path, monkeypatch):
    """Test phase detection with no in-progress tasks."""
    monkeypatch.chdir(temp_project_dir)
    mock_task_list.return_value = ""

    phase, desc = get_current_phase()
    assert phase is None
    assert desc is None


@patch("flowspec_cli.status.task_list")
def test_get_task_counts_empty(mock_task_list, temp_project_dir: Path, monkeypatch):
    """Test task counting with no tasks."""
    monkeypatch.chdir(temp_project_dir)
    mock_task_list.return_value = ""

    counts = get_task_counts()
    assert counts["in_progress"] == 0
    assert counts["todo"] == 0
    assert counts["done"] == 0


def test_get_next_action_no_tasks():
    """Test next action when there are no tasks."""
    task_counts = {"in_progress": 0, "todo": 0, "done": 0}
    action = get_next_action(None, task_counts)
    assert "specify" in action.lower()


def test_format_status_human():
    """Test human-readable formatting."""
    data = {
        "project": "Test Project",
        "version": "1.0.0",
        "mode": "Full SDD",
        "phase": None,
        "current_task": None,
        "tasks": {"in_progress": 0, "todo": 0, "done": 0},
        "decisions_today": 0,
        "events_today": 0,
        "next_action": "Create tasks with /flow:specify",
    }

    output = format_status_human(data)

    assert "Test Project" in output
    assert "1.0.0" in output
    assert "Full SDD" in output
    assert "no active work" in output


def test_format_status_json():
    """Test JSON formatting."""
    data = {
        "project": "Test Project",
        "version": "1.0.0",
        "mode": "Vibe",
        "phase": None,
        "current_task": None,
        "tasks": {"in_progress": 0, "todo": 0, "done": 0},
        "decisions_today": 0,
        "events_today": 0,
        "next_action": "Create tasks with /flow:specify",
    }

    output = format_status_json(data)
    parsed = json.loads(output)

    assert parsed["project"] == "Test Project"
    assert parsed["version"] == "1.0.0"
    assert parsed["mode"] == "Vibe"
