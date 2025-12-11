"""Integration tests for Task Memory lifecycle hooks.

These tests verify the integration between backlog CLI commands and
Task Memory lifecycle management via Claude Code PostToolUse hooks.
"""

import json
import os
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def integration_project(tmp_path):
    """Create full integration test project structure."""
    # Create directory structure
    backlog_dir = tmp_path / "backlog"
    memory_dir = backlog_dir / "memory"
    archive_dir = memory_dir / "archive"
    template_dir = tmp_path / "templates" / "memory"
    specify_logs_dir = tmp_path / ".specify" / "logs"
    backlog_hooks_dir = tmp_path / ".backlog" / "hooks"
    claude_hooks_dir = tmp_path / ".claude" / "hooks"

    for d in [
        backlog_dir,
        memory_dir,
        archive_dir,
        template_dir,
        specify_logs_dir,
        backlog_hooks_dir,
        claude_hooks_dir,
    ]:
        d.mkdir(parents=True, exist_ok=True)

    # Create default template
    template_content = """# Task Memory: {task_id}

**Created**: {created_date}
**Last Updated**: {updated_date}
**Task**: {task_title}

## Context

## Key Decisions

## Approaches Tried

## Open Questions

## Resources

## Notes
"""
    (template_dir / "default.md").write_text(template_content)

    # Create backlog/CLAUDE.md
    backlog_claude_md = backlog_dir / "CLAUDE.md"
    backlog_claude_md.write_text("# Backlog Task Management\n\n")

    # Create .backlog/config.yml
    config_content = """hooks:
  post_task_update:
    enabled: true
    command: ".backlog/hooks/post-task-update.sh"
    timeout: 10
    fail_open: true

memory:
  storage:
    active_dir: "backlog/memory"
    archive_dir: "backlog/memory/archive"
    template_dir: "templates/memory"
"""
    (tmp_path / ".backlog" / "config.yml").write_text(config_content)

    return tmp_path


class TestPostToolUseHook:
    """Tests for the PostToolUse hook."""

    def test_parse_backlog_command_basic(self, integration_project):
        """Test parsing of basic backlog task edit command."""
        hook_path = (
            Path(__file__).parent.parent.parent
            / ".claude"
            / "hooks"
            / "post-tool-use-task-memory-lifecycle.py"
        )

        hook_code = hook_path.read_text()
        hook_globals = {"__name__": "test_hook"}
        # Use compile and exec to load the parse function
        compiled = compile(hook_code, str(hook_path), "exec")
        exec(compiled, hook_globals)  # noqa: S102

        parse_fn = hook_globals.get("parse_backlog_command")
        assert parse_fn is not None

        # Test various command formats
        test_cases = [
            (
                'backlog task edit task-42 -s "In Progress"',
                {"task_id": "task-42", "new_status": "In Progress"},
            ),
            (
                "backlog task edit task-100 -s Done",
                {"task_id": "task-100", "new_status": "Done"},
            ),
            (
                'backlog task edit 55 -s "To Do"',
                {"task_id": "task-55", "new_status": "To Do"},
            ),
            (
                "backlog task edit task-999 --status 'In Progress'",
                {"task_id": "task-999", "new_status": "In Progress"},
            ),
        ]

        for command, expected in test_cases:
            result = parse_fn(command)
            assert result == expected, f"Failed for: {command}"

    def test_parse_backlog_command_invalid(self, integration_project):
        """Test parsing of invalid commands."""
        hook_path = (
            Path(__file__).parent.parent.parent
            / ".claude"
            / "hooks"
            / "post-tool-use-task-memory-lifecycle.py"
        )

        hook_code = hook_path.read_text()
        hook_globals = {"__name__": "test_hook"}
        compiled = compile(hook_code, str(hook_path), "exec")
        exec(compiled, hook_globals)  # noqa: S102

        parse_fn = hook_globals.get("parse_backlog_command")

        invalid_commands = [
            "git commit -m 'message'",
            "backlog task list",
            "backlog task 42 --plain",
            "npm install",
            "",
        ]

        for command in invalid_commands:
            result = parse_fn(command)
            assert result is None, f"Should be None for: {command}"


class TestBashHook:
    """Tests for the bash wrapper hook."""

    def test_hook_script_exists(self, integration_project):
        """Test that hook script exists and is executable."""
        hook_path = (
            Path(__file__).parent.parent.parent
            / ".backlog"
            / "hooks"
            / "post-task-update.sh"
        )
        assert hook_path.exists(), f"Hook script not found: {hook_path}"

        # Check if executable
        assert os.access(hook_path, os.X_OK), "Hook script is not executable"

    def test_hook_script_syntax(self, integration_project):
        """Test hook script has valid bash syntax."""
        hook_path = (
            Path(__file__).parent.parent.parent
            / ".backlog"
            / "hooks"
            / "post-task-update.sh"
        )

        result = subprocess.run(
            ["bash", "-n", str(hook_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"Bash syntax error: {result.stderr}"


class TestConfigFile:
    """Tests for .backlog/config.yml."""

    def test_config_file_exists(self, integration_project):
        """Test that config file exists."""
        config_path = Path(__file__).parent.parent.parent / ".backlog" / "config.yml"
        assert config_path.exists(), f"Config file not found: {config_path}"

    def test_config_file_valid_yaml(self, integration_project):
        """Test config file is valid YAML."""
        import yaml

        config_path = Path(__file__).parent.parent.parent / ".backlog" / "config.yml"
        config_content = config_path.read_text()

        try:
            config = yaml.safe_load(config_content)
            assert config is not None
            assert "hooks" in config
            assert "memory" in config
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML: {e}")


class TestLifecycleIntegration:
    """Tests for full lifecycle integration."""

    def test_lifecycle_manager_import(self, integration_project):
        """Test that lifecycle manager can be imported."""
        from specify_cli.memory.hooks import on_task_status_change

        assert callable(on_task_status_change)

    def test_state_change_to_in_progress(self, integration_project):
        """Test memory creation on transition to In Progress."""
        from specify_cli.memory import LifecycleManager, TaskMemoryStore

        store = TaskMemoryStore(base_path=integration_project)
        manager = LifecycleManager(store=store)

        task_id = "task-999"

        # Should not exist initially
        assert not store.exists(task_id)

        # Trigger state change
        manager.on_state_change(task_id, "To Do", "In Progress", "Test Task")

        # Memory should be created
        assert store.exists(task_id)
        content = store.read(task_id)
        assert "task-999" in content

    def test_state_change_to_done(self, integration_project):
        """Test memory archival on transition to Done."""
        from specify_cli.memory import LifecycleManager, TaskMemoryStore

        store = TaskMemoryStore(base_path=integration_project)
        manager = LifecycleManager(store=store)

        task_id = "task-888"

        # Create memory first
        manager.on_state_change(task_id, "To Do", "In Progress", "Test Task")
        assert store.exists(task_id)

        # Transition to Done
        manager.on_state_change(task_id, "In Progress", "Done", "Test Task")

        # Should be archived, not active
        assert not store.exists(task_id)
        assert store.exists(task_id, check_archive=True)

    def test_state_change_restore(self, integration_project):
        """Test memory restoration on Done to In Progress."""
        from specify_cli.memory import LifecycleManager, TaskMemoryStore

        store = TaskMemoryStore(base_path=integration_project)
        manager = LifecycleManager(store=store)

        task_id = "task-777"

        # Create, archive, restore
        manager.on_state_change(task_id, "To Do", "In Progress", "Test Task")
        store.append(task_id, "Important context")
        manager.on_state_change(task_id, "In Progress", "Done", "Test Task")
        manager.on_state_change(task_id, "Done", "In Progress", "Test Task")

        # Should be restored with content
        assert store.exists(task_id)
        content = store.read(task_id)
        assert "Important context" in content

    def test_state_change_reset(self, integration_project):
        """Test memory deletion on In Progress to To Do."""
        from specify_cli.memory import LifecycleManager, TaskMemoryStore

        store = TaskMemoryStore(base_path=integration_project)
        manager = LifecycleManager(store=store)

        task_id = "task-666"

        # Create then reset
        manager.on_state_change(task_id, "To Do", "In Progress", "Test Task")
        assert store.exists(task_id)

        manager.on_state_change(task_id, "In Progress", "To Do", "Test Task")
        assert not store.exists(task_id)


class TestHookInput:
    """Tests for hook input processing."""

    def test_hook_processes_bash_tool_call(self, integration_project):
        """Test hook correctly processes Bash tool call input."""
        hook_path = (
            Path(__file__).parent.parent.parent
            / ".claude"
            / "hooks"
            / "post-tool-use-task-memory-lifecycle.py"
        )

        # Create simulated hook input
        hook_input = {
            "tool_name": "Bash",
            "tool_input": {"command": 'backlog task edit task-123 -s "In Progress"'},
        }

        # Run hook with simulated input using subprocess.run safely
        result = subprocess.run(
            ["python3", str(hook_path)],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(integration_project),
            check=False,
        )

        # Should exit 0 (fail open)
        assert result.returncode == 0

    def test_hook_ignores_non_bash_tools(self, integration_project):
        """Test hook ignores non-Bash tool calls."""
        hook_path = (
            Path(__file__).parent.parent.parent
            / ".claude"
            / "hooks"
            / "post-tool-use-task-memory-lifecycle.py"
        )

        hook_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": "/some/file.txt"},
        }

        result = subprocess.run(
            ["python3", str(hook_path)],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        assert result.returncode == 0

    def test_hook_handles_empty_input(self, integration_project):
        """Test hook handles empty input gracefully."""
        hook_path = (
            Path(__file__).parent.parent.parent
            / ".claude"
            / "hooks"
            / "post-tool-use-task-memory-lifecycle.py"
        )

        result = subprocess.run(
            ["python3", str(hook_path)],
            input="",
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        assert result.returncode == 0

    def test_hook_handles_invalid_json(self, integration_project):
        """Test hook handles invalid JSON gracefully."""
        hook_path = (
            Path(__file__).parent.parent.parent
            / ".claude"
            / "hooks"
            / "post-tool-use-task-memory-lifecycle.py"
        )

        result = subprocess.run(
            ["python3", str(hook_path)],
            input="not valid json {{{}",
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        assert result.returncode == 0
