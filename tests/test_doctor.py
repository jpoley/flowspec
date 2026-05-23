"""Tests for flowspec doctor health checks."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from flowspec_cli.doctor.checks import (
    CheckResult,
    CheckStatus,
    check_agent_naming,
    check_backlog_installed,
    check_beads_installed,
    check_constitution,
    check_flowspec_dir,
    check_flowspec_version,
    check_python_version,
    check_workflow_config,
    run_all_checks,
)


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


class TestCheckPythonVersion:
    def test_pass_current_version(self) -> None:
        result = check_python_version()
        # This test always runs on >= 3.11 (project requirement)
        assert result.status == CheckStatus.PASS
        assert "Python" in result.message

    def test_fail_old_version(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys, "version_info", (3, 10, 0, "final", 0))
        result = check_python_version()
        assert result.status == CheckStatus.FAIL
        assert "3.10" in result.message
        assert result.fix_cmd is not None


class TestCheckFlowspecVersion:
    def test_pass_when_up_to_date(self) -> None:
        result = check_flowspec_version("1.2.3", "1.2.3")
        assert result.status == CheckStatus.PASS
        assert "up to date" in result.message

    def test_warn_when_behind(self) -> None:
        result = check_flowspec_version("1.2.3", "1.2.4")
        assert result.status == CheckStatus.WARN
        assert "1.2.4" in result.message
        assert result.fix_cmd is not None

    def test_warn_when_latest_unknown(self) -> None:
        result = check_flowspec_version("1.2.3", None)
        assert result.status == CheckStatus.WARN
        assert "could not check" in result.message


class TestCheckBacklogInstalled:
    def test_pass_when_installed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=0, stdout="1.21.0\n")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        result = check_backlog_installed()
        assert result.status == CheckStatus.PASS
        assert "1.21.0" in result.message

    def test_fail_when_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def raise_fnf(*args, **kwargs):
            raise FileNotFoundError

        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", raise_fnf)
        result = check_backlog_installed()
        assert result.status == CheckStatus.FAIL
        assert result.fix_cmd is not None

    def test_fail_when_nonzero_exit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        result = check_backlog_installed()
        assert result.status == CheckStatus.FAIL


class TestCheckBeadsInstalled:
    def test_pass_when_installed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(
            returncode=0, stdout="bd version 0.29.0 (abc123)\n"
        )
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        result = check_beads_installed()
        assert result.status == CheckStatus.PASS
        assert "0.29.0" in result.message

    def test_fail_when_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def raise_fnf(*args, **kwargs):
            raise FileNotFoundError

        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", raise_fnf)
        result = check_beads_installed()
        assert result.status == CheckStatus.FAIL
        assert result.fix_cmd is not None

    def test_fail_when_nonzero_exit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        result = check_beads_installed()
        assert result.status == CheckStatus.FAIL


class TestCheckWorkflowConfig:
    def test_pass_valid_yml(self, tmp_path: Path) -> None:
        (tmp_path / "flowspec_workflow.yml").write_text(
            "version: 2\nname: test\n", encoding="utf-8"
        )
        result = check_workflow_config(tmp_path)
        assert result.status == CheckStatus.PASS
        assert "valid" in result.message

    def test_fail_missing(self, tmp_path: Path) -> None:
        result = check_workflow_config(tmp_path)
        assert result.status == CheckStatus.FAIL
        assert "not found" in result.message
        assert result.fix_cmd is not None

    def test_fail_invalid_yaml(self, tmp_path: Path) -> None:
        (tmp_path / "flowspec_workflow.yml").write_text(
            "key: [unclosed bracket\n", encoding="utf-8"
        )
        result = check_workflow_config(tmp_path)
        assert result.status == CheckStatus.FAIL
        assert "parse error" in result.message


class TestCheckAgentNaming:
    def test_pass_no_agents_dir(self, tmp_path: Path) -> None:
        result = check_agent_naming(tmp_path)
        assert result.status == CheckStatus.PASS

    def test_pass_no_old_files(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "qa.agent.md").write_text("", encoding="utf-8")
        result = check_agent_naming(tmp_path)
        assert result.status == CheckStatus.PASS

    def test_warn_old_hyphen_files(self, tmp_path: Path) -> None:
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "flow-qa.agent.md").write_text("", encoding="utf-8")
        (agents_dir / "flow-dev.agent.md").write_text("", encoding="utf-8")
        result = check_agent_naming(tmp_path)
        assert result.status == CheckStatus.WARN
        assert "2" in result.message
        assert result.fix_cmd == "flowspec upgrade-repo"


class TestCheckConstitution:
    def test_pass_constitution_exists(self, tmp_path: Path) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").write_text("# Constitution", encoding="utf-8")
        result = check_constitution(tmp_path)
        assert result.status == CheckStatus.PASS

    def test_warn_constitution_missing(self, tmp_path: Path) -> None:
        result = check_constitution(tmp_path)
        assert result.status == CheckStatus.WARN
        assert result.fix_cmd is not None


class TestCheckFlowspecDir:
    def test_pass_dir_exists(self, tmp_path: Path) -> None:
        (tmp_path / ".flowspec").mkdir()
        result = check_flowspec_dir(tmp_path)
        assert result.status == CheckStatus.PASS

    def test_warn_dir_missing(self, tmp_path: Path) -> None:
        result = check_flowspec_dir(tmp_path)
        assert result.status == CheckStatus.WARN
        assert result.fix_cmd is not None


class TestRunAllChecks:
    def test_returns_eight_checks(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=0, stdout="1.0.0\n")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        results = run_all_checks(
            tmp_path, current_version="0.1.0", latest_version="0.1.0"
        )
        assert len(results) == 8

    def test_all_results_are_check_result(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=0, stdout="1.0.0\n")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        results = run_all_checks(tmp_path, current_version="0.1.0")
        for r in results:
            assert isinstance(r, CheckResult)
            assert isinstance(r.status, CheckStatus)
