"""Tests for flowspec doctor health checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from flowspec_cli.doctor.checks import (
    CheckResult,
    CheckStatus,
    _parse_version,
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


class TestParseVersion:
    def test_plain_version(self) -> None:
        assert _parse_version("1.2.3") == (1, 2, 3)

    def test_strips_v_prefix(self) -> None:
        assert _parse_version("v1.2.3") == (1, 2, 3)

    def test_zero_padded_equivalent(self) -> None:
        assert _parse_version("0.4.008") == _parse_version("0.4.8")


class TestCheckFlowspecVersion:
    def test_pass_when_up_to_date(self) -> None:
        result = check_flowspec_version("1.2.3", "1.2.3")
        assert result.status == CheckStatus.PASS
        assert "up to date" in result.message

    def test_pass_when_zero_padded_equivalent(self) -> None:
        result = check_flowspec_version("0.4.008", "0.4.8")
        assert result.status == CheckStatus.PASS

    def test_pass_when_current_ahead(self) -> None:
        result = check_flowspec_version("1.2.4", "1.2.3")
        assert result.status == CheckStatus.PASS

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

    def test_fail_when_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def raise_timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd=["backlog"], timeout=5)

        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", raise_timeout)
        result = check_backlog_installed()
        assert result.status == CheckStatus.FAIL, "Timeout should report as FAIL"

    def test_fail_when_nonzero_exit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        result = check_backlog_installed()
        assert result.status == CheckStatus.FAIL

    def test_fail_when_output_not_version_string(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(
            returncode=0, stdout="some unexpected output\n"
        )
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        result = check_backlog_installed()
        assert result.status == CheckStatus.FAIL

    def test_fail_when_version_string_has_trailing_dot(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=0, stdout="1.2.\n")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        result = check_backlog_installed()
        assert result.status == CheckStatus.FAIL, "'1.2.' is not a valid version string"


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

    def test_fail_when_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def raise_timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd=["bd"], timeout=5)

        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", raise_timeout)
        result = check_beads_installed()
        assert result.status == CheckStatus.FAIL, "Timeout should report as FAIL"

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
        # Mock schema+semantic validation so any valid YAML counts as passing
        mock_validation = MagicMock()
        mock_validation.is_valid = True
        mock_validation.errors = []
        with (
            patch("flowspec_cli.doctor.checks.WorkflowConfig") as mock_cfg,
            patch("flowspec_cli.doctor.checks.WorkflowValidator") as mock_val,
        ):
            mock_cfg.load.return_value = MagicMock()
            mock_val.return_value.validate.return_value = mock_validation
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

    def test_fail_empty_yaml(self, tmp_path: Path) -> None:
        (tmp_path / "flowspec_workflow.yml").write_text("", encoding="utf-8")
        result = check_workflow_config(tmp_path)
        assert result.status == CheckStatus.FAIL, "Empty YAML should fail"
        assert "empty or not a YAML mapping" in result.message

    def test_fail_yaml_not_mapping(self, tmp_path: Path) -> None:
        (tmp_path / "flowspec_workflow.yml").write_text(
            "- item1\n- item2\n", encoding="utf-8"
        )
        result = check_workflow_config(tmp_path)
        assert result.status == CheckStatus.FAIL, "YAML list (not mapping) should fail"
        assert "empty or not a YAML mapping" in result.message


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

    def test_pass_when_agents_path_is_file(self, tmp_path: Path) -> None:
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "agents").write_text("", encoding="utf-8")
        result = check_agent_naming(tmp_path)
        assert result.status == CheckStatus.PASS, (
            "A file named 'agents' should not crash or warn"
        )


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

    def test_warn_when_constitution_is_directory(self, tmp_path: Path) -> None:
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        (memory_dir / "constitution.md").mkdir()
        result = check_constitution(tmp_path)
        assert result.status == CheckStatus.WARN, (
            "A directory named constitution.md should not count"
        )


class TestCheckFlowspecDir:
    def test_pass_dir_exists(self, tmp_path: Path) -> None:
        (tmp_path / ".flowspec").mkdir()
        result = check_flowspec_dir(tmp_path)
        assert result.status == CheckStatus.PASS

    def test_warn_dir_missing(self, tmp_path: Path) -> None:
        result = check_flowspec_dir(tmp_path)
        assert result.status == CheckStatus.WARN
        assert result.fix_cmd is not None

    def test_warn_when_flowspec_is_file(self, tmp_path: Path) -> None:
        (tmp_path / ".flowspec").write_text("", encoding="utf-8")
        result = check_flowspec_dir(tmp_path)
        assert result.status == CheckStatus.WARN, (
            "A file named .flowspec should not count as directory"
        )


class TestRunAllChecks:
    def test_returns_eight_checks(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        backlog_result = MagicMock(returncode=0, stdout="1.21.0\n")
        beads_result = MagicMock(returncode=0, stdout="bd version 0.29.0 (abc123)\n")
        mock_run = MagicMock(side_effect=[backlog_result, beads_result])
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        results = run_all_checks(
            tmp_path, current_version="0.1.0", latest_version="0.1.0"
        )
        assert len(results) == 8, f"Expected 8 checks, got {len(results)}"

    def test_all_results_are_check_result(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        backlog_result = MagicMock(returncode=0, stdout="1.21.0\n")
        beads_result = MagicMock(returncode=0, stdout="bd version 0.29.0 (abc123)\n")
        mock_run = MagicMock(side_effect=[backlog_result, beads_result])
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        results = run_all_checks(tmp_path, current_version="0.1.0")
        for r in results:
            assert isinstance(r, CheckResult), f"Expected CheckResult, got {type(r)}"
            assert isinstance(r.status, CheckStatus), (
                f"Expected CheckStatus, got {type(r.status)}"
            )


class TestDoctorCli:
    """Integration tests for the doctor CLI command via CliRunner."""

    def _make_runner(self) -> CliRunner:
        return CliRunner()

    def test_exits_nonzero_on_fail(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Force a FAIL: backlog subprocess raises FileNotFoundError, no workflow yml
        def raise_fnf(*args, **kwargs):
            raise FileNotFoundError

        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", raise_fnf)
        monkeypatch.setattr(
            "flowspec_cli.get_github_latest_release", lambda *a, **k: None
        )
        monkeypatch.chdir(tmp_path)

        from flowspec_cli import app

        runner = self._make_runner()
        result = runner.invoke(app, ["doctor"], catch_exceptions=False)
        assert result.exit_code != 0, "Expected non-zero exit when checks fail"

    def test_exits_zero_all_pass(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        all_pass = [
            CheckResult(name=f"check-{i}", status=CheckStatus.PASS, message="ok")
            for i in range(8)
        ]
        monkeypatch.setattr(
            "flowspec_cli.doctor.cli.run_all_checks", lambda *a, **k: all_pass
        )
        monkeypatch.setattr(
            "flowspec_cli.get_github_latest_release", lambda *a, **k: "0.4.008"
        )
        monkeypatch.chdir(tmp_path)

        from flowspec_cli import app

        runner = self._make_runner()
        result = runner.invoke(app, ["doctor"], catch_exceptions=False)
        assert result.exit_code == 0, f"Expected zero exit; got: {result.output}"

    def test_fix_creates_constitution(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=0, stdout="1.0.0\n")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        monkeypatch.setattr(
            "flowspec_cli.get_github_latest_release", lambda *a, **k: None
        )
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".flowspec").mkdir()  # mark as flowspec project

        from flowspec_cli import app

        runner = self._make_runner()
        result = runner.invoke(app, ["doctor", "--fix"], catch_exceptions=False)
        assert (tmp_path / "memory" / "constitution.md").exists(), (
            "--fix should create memory/constitution.md"
        )
        assert result.exit_code != 0, (
            "--fix should exit non-zero when other checks still fail"
        )

    def test_fix_skips_constitution_in_non_project_dir(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_run = MagicMock()
        mock_run.return_value = MagicMock(returncode=0, stdout="1.21.0\n")
        monkeypatch.setattr("flowspec_cli.doctor.checks.subprocess.run", mock_run)
        monkeypatch.setattr(
            "flowspec_cli.get_github_latest_release", lambda *a, **k: None
        )
        monkeypatch.chdir(tmp_path)
        # No .flowspec or flowspec_workflow.yml — not a project directory

        from flowspec_cli import app

        runner = self._make_runner()
        runner.invoke(app, ["doctor", "--fix"], catch_exceptions=False)
        assert not (tmp_path / "memory" / "constitution.md").exists(), (
            "--fix must not create constitution.md outside a flowspec project"
        )
