"""Tests for flowspec doctor health check command."""

from unittest.mock import MagicMock, patch

import yaml

from flowspec_cli.doctor import (
    CheckResult,
    CheckStatus,
    check_agent_files,
    check_constitution,
    check_flowspec_version,
    check_python_version,
    check_tool_installed,
    check_workflow_config,
    run_all_checks,
)


class TestCheckFlowspecVersion:
    """Tests for flowspec version check."""

    @patch("httpx.get", side_effect=Exception("no network"))
    def test_returns_version(self, _mock_httpx):
        """Should return current flowspec version."""
        result = check_flowspec_version()
        assert result.name == "flowspec CLI"
        assert result.status in (CheckStatus.PASS, CheckStatus.WARN)


class TestCheckPythonVersion:
    """Tests for Python version check."""

    def test_compatible_version(self):
        """Should pass for Python 3.11+."""
        # Current test is running on 3.11+ since that's a requirement
        result = check_python_version()
        assert result.name == "Python version"
        assert result.status == CheckStatus.PASS
        assert "Python" in result.message

    @patch("flowspec_cli.doctor.sys.version_info", (3, 10, 0))
    def test_incompatible_version(self):
        """Should fail for Python < 3.11."""
        result = check_python_version()
        assert result.status == CheckStatus.FAIL
        assert "3.10" in result.message
        assert "requires 3.11+" in result.message


class TestCheckToolInstalled:
    """Tests for tool installation checks."""

    @patch("flowspec_cli.doctor.shutil.which")
    def test_tool_not_found(self, mock_which):
        """Should fail when tool not in PATH."""
        mock_which.return_value = None
        result = check_tool_installed("nonexistent-tool")
        assert result.status == CheckStatus.FAIL
        assert "not found in PATH" in result.message
        assert result.fix_command is not None

    @patch("flowspec_cli.doctor.shutil.which")
    @patch("flowspec_cli.doctor.subprocess.run")
    def test_tool_found_with_version(self, mock_run, mock_which):
        """Should pass when tool is found and can get version."""
        mock_which.return_value = "/usr/bin/backlog"
        mock_run.return_value = MagicMock(stdout="backlog 1.28.1\n", stderr="")
        result = check_tool_installed("backlog")
        assert result.status == CheckStatus.PASS
        assert "1.28.1" in result.message

    @patch("flowspec_cli.doctor.shutil.which")
    @patch("flowspec_cli.doctor.subprocess.run")
    def test_tool_found_version_fails(self, mock_run, mock_which):
        """Should still pass if tool found but version check fails."""
        mock_which.return_value = "/usr/bin/tool"
        mock_run.side_effect = Exception("Version check failed")
        result = check_tool_installed("tool")
        assert result.status == CheckStatus.PASS
        assert "installed" in result.message


class TestCheckWorkflowConfig:
    """Tests for workflow configuration check."""

    def test_no_config_file(self, tmp_path, monkeypatch):
        """Should warn when no workflow config exists."""
        monkeypatch.chdir(tmp_path)
        result = check_workflow_config()
        assert result.status == CheckStatus.WARN
        assert "No workflow configuration found" in result.message
        assert result.fix_command == "Run: /flow:init"

    def test_valid_config(self, tmp_path, monkeypatch):
        """Should pass for valid workflow config."""
        monkeypatch.chdir(tmp_path)
        config_path = tmp_path / "flowspec_workflow.yml"
        valid_config = {
            "states": ["To Do", "Done"],
            "workflows": {
                "complete": {
                    "input_states": ["To Do"],
                    "output_state": "Done",
                }
            },
            "transitions": [{"from": "To Do", "to": "Done", "via": "complete"}],
        }
        config_path.write_text(yaml.dump(valid_config))

        result = check_workflow_config()
        assert result.status == CheckStatus.PASS
        assert "Valid" in result.message

    def test_invalid_yaml(self, tmp_path, monkeypatch):
        """Should fail for invalid YAML."""
        monkeypatch.chdir(tmp_path)
        config_path = tmp_path / "flowspec_workflow.yml"
        config_path.write_text("invalid: yaml: content: [")

        result = check_workflow_config()
        assert result.status == CheckStatus.FAIL
        assert "Invalid YAML" in result.message

    def test_config_with_errors(self, tmp_path, monkeypatch):
        """Should fail for config with validation errors."""
        monkeypatch.chdir(tmp_path)
        config_path = tmp_path / "flowspec_workflow.yml"
        # Config missing initial state "To Do"
        invalid_config = {
            "states": ["In Progress", "Done"],
            "workflows": {},
            "transitions": [],
        }
        config_path.write_text(yaml.dump(invalid_config))

        result = check_workflow_config()
        assert result.status == CheckStatus.FAIL
        assert "Invalid" in result.message
        assert result.details is not None
        assert "errors" in result.details

    def test_config_with_warnings(self, tmp_path, monkeypatch):
        """Should warn for config with validation warnings only."""
        monkeypatch.chdir(tmp_path)
        config_path = tmp_path / "flowspec_workflow.yml"
        # Config with warnings but no errors
        config_with_warnings = {
            "states": ["To Do", "In Progress"],  # No terminal states (warning)
            "workflows": {
                "start": {
                    "input_states": ["To Do"],
                    "output_state": "In Progress",
                }
            },
            "transitions": [{"from": "To Do", "to": "In Progress", "via": "start"}],
        }
        config_path.write_text(yaml.dump(config_with_warnings))

        result = check_workflow_config()
        # Should pass with warnings (warnings don't make config invalid)
        assert result.status in (CheckStatus.PASS, CheckStatus.WARN)


class TestCheckAgentFiles:
    """Tests for agent file naming check."""

    def test_no_agent_files(self, tmp_path, monkeypatch):
        """Should warn when no agent files found."""
        monkeypatch.chdir(tmp_path)
        result = check_agent_files()
        assert result.status == CheckStatus.WARN
        assert "No agent files found" in result.message

    def test_old_hyphen_convention(self, tmp_path, monkeypatch):
        """Should warn for files using old hyphen naming."""
        monkeypatch.chdir(tmp_path)
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "backend-engineer.md").write_text("# Backend Engineer")
        (agents_dir / "frontend-engineer.md").write_text("# Frontend Engineer")

        result = check_agent_files()
        assert result.status == CheckStatus.WARN
        assert "not matching flow.*.agent.md" in result.message
        assert result.fix_command == "Run: flowspec upgrade-repo"
        assert result.details is not None
        assert len(result.details["files"]) == 2

    def test_correct_flow_agent_convention(self, tmp_path, monkeypatch):
        """Should pass for files using flow.*.agent.md naming."""
        monkeypatch.chdir(tmp_path)
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "flow.assess.agent.md").write_text("# Assess")
        (agents_dir / "flow.specify.agent.md").write_text("# Specify")

        result = check_agent_files()
        assert result.status == CheckStatus.PASS

    def test_mixed_convention(self, tmp_path, monkeypatch):
        """Should warn when mixing compliant and non-compliant names."""
        monkeypatch.chdir(tmp_path)
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "backend-engineer.md").write_text("# Old")
        (agents_dir / "frontend.engineer.md").write_text("# Wrong pattern")
        (agents_dir / "flow.assess.agent.md").write_text("# Correct")

        result = check_agent_files()
        assert result.status == CheckStatus.WARN
        # Both non-compliant files should be reported
        assert len(result.details["files"]) == 2

    def test_dot_separated_but_not_flow_pattern(self, tmp_path, monkeypatch):
        """Should warn for dot-separated names that don't match flow.*.agent.md."""
        monkeypatch.chdir(tmp_path)
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "backend.engineer.md").write_text("# Backend Engineer")

        result = check_agent_files()
        assert result.status == CheckStatus.WARN
        assert len(result.details["files"]) == 1

    def test_skips_special_files(self, tmp_path, monkeypatch):
        """Should skip README and underscore-prefixed files."""
        monkeypatch.chdir(tmp_path)
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "README.md").write_text("# README")
        (agents_dir / "_template.md").write_text("# Template")
        (agents_dir / "flow.assess.agent.md").write_text("# Assess")

        result = check_agent_files()
        assert result.status == CheckStatus.PASS


class TestCheckConstitution:
    """Tests for constitution file check."""

    def test_no_constitution(self, tmp_path, monkeypatch):
        """Should warn when constitution not found."""
        monkeypatch.chdir(tmp_path)
        result = check_constitution()
        assert result.status == CheckStatus.WARN
        assert "Constitution not found" in result.message
        assert result.fix_command == "Run: /flow:init"

    def test_constitution_with_placeholders(self, tmp_path, monkeypatch):
        """Should warn for constitution with placeholders."""
        monkeypatch.chdir(tmp_path)
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        constitution = memory_dir / "constitution.md"
        constitution.write_text("# [PROJECT_NAME]\n\nPrinciple: [PRINCIPLE_1_NAME]")

        result = check_constitution()
        assert result.status == CheckStatus.WARN
        assert "placeholders" in result.message
        assert result.fix_command == "Run: /flow:init"

    def test_valid_constitution(self, tmp_path, monkeypatch):
        """Should pass for properly configured constitution."""
        monkeypatch.chdir(tmp_path)
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        constitution = memory_dir / "constitution.md"
        constitution.write_text("# My Project\n\nPrinciple: Security First")

        result = check_constitution()
        assert result.status == CheckStatus.PASS
        assert "Present" in result.message


class TestRunAllChecks:
    """Tests for run_all_checks function."""

    @patch("httpx.get", side_effect=Exception("no network"))
    def test_returns_all_check_results(self, _mock_httpx):
        """Should return results for all checks."""
        results = run_all_checks()
        assert len(results) == 7  # 7 checks defined
        assert all(isinstance(r, CheckResult) for r in results)

    @patch("httpx.get", side_effect=Exception("no network"))
    def test_check_names(self, _mock_httpx):
        """Should include all expected check names."""
        results = run_all_checks()
        names = {r.name for r in results}
        expected = {
            "flowspec CLI",
            "Python version",
            "backlog CLI",
            "beads CLI",
            "Workflow config",
            "Agent file naming",
            "Constitution",
        }
        assert names == expected
