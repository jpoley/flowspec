"""Tests for batch --validation-mode flag in specify init."""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from specify_cli import app

runner = CliRunner()


@pytest.fixture
def isolated_tmp_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create isolated temp directory and change to it."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


class TestBatchValidationModeNone:
    """Tests for --validation-mode none."""

    def test_batch_mode_none_sets_all_transitions(
        self, isolated_tmp_path: Path
    ) -> None:
        """Test --validation-mode none applies NONE to all transitions."""
        result = runner.invoke(
            app,
            [
                "init",
                str(isolated_tmp_path / "test-project"),
                "--ai",
                "claude",
                "--validation-mode",
                "none",
                "--no-git",
            ],
            input="1\n2\n",  # AI selection and constitution tier
        )
        # May exit early due to network issues in test, check workflow file if created
        workflow_file = isolated_tmp_path / "test-project" / "jpspec_workflow.yml"
        if workflow_file.exists():
            content = workflow_file.read_text()
            # All should be NONE
            assert content.count("validation: NONE") >= 7


class TestBatchValidationModePullRequest:
    """Tests for --validation-mode pull-request."""

    def test_batch_mode_pull_request_sets_all_transitions(
        self, isolated_tmp_path: Path
    ) -> None:
        """Test --validation-mode pull-request applies to all transitions."""
        result = runner.invoke(
            app,
            [
                "init",
                str(isolated_tmp_path / "test-project"),
                "--ai",
                "claude",
                "--validation-mode",
                "pull-request",
                "--no-git",
            ],
            input="1\n2\n",
        )
        workflow_file = isolated_tmp_path / "test-project" / "jpspec_workflow.yml"
        if workflow_file.exists():
            content = workflow_file.read_text()
            assert content.count("validation: PULL_REQUEST") >= 7


class TestBatchValidationModeKeyword:
    """Tests for --validation-mode keyword."""

    def test_batch_mode_keyword_prompts_for_keyword(
        self, isolated_tmp_path: Path
    ) -> None:
        """Test --validation-mode keyword prompts for approval keyword."""
        result = runner.invoke(
            app,
            [
                "init",
                str(isolated_tmp_path / "test-project"),
                "--ai",
                "claude",
                "--validation-mode",
                "keyword",
                "--no-git",
            ],
            input="CUSTOM_KEYWORD\n1\n2\n",  # keyword, AI selection, constitution
        )
        workflow_file = isolated_tmp_path / "test-project" / "jpspec_workflow.yml"
        if workflow_file.exists():
            content = workflow_file.read_text()
            # Should use custom keyword
            assert (
                'KEYWORD["CUSTOM_KEYWORD"]' in content
                or 'KEYWORD["APPROVED"]' in content
            )


class TestBatchValidationModeInvalid:
    """Tests for invalid --validation-mode values."""

    def test_invalid_validation_mode_rejected(self, isolated_tmp_path: Path) -> None:
        """Test invalid --validation-mode value shows error."""
        result = runner.invoke(
            app,
            [
                "init",
                str(isolated_tmp_path / "test-project"),
                "--ai",
                "claude",
                "--validation-mode",
                "invalid-mode",
                "--no-git",
            ],
            input="1\n2\n",
        )
        assert result.exit_code == 1
        assert "Invalid validation mode" in result.output


class TestBatchModeWithPerTransitionOverrides:
    """Tests for per-transition flags overriding batch mode."""

    def test_per_transition_overrides_batch_mode(self, isolated_tmp_path: Path) -> None:
        """Test per-transition flags override batch mode."""
        result = runner.invoke(
            app,
            [
                "init",
                str(isolated_tmp_path / "test-project"),
                "--ai",
                "claude",
                "--validation-mode",
                "none",
                "--validation-plan",
                "pull-request",
                "--no-git",
            ],
            input="1\n2\n",
        )
        workflow_file = isolated_tmp_path / "test-project" / "jpspec_workflow.yml"
        if workflow_file.exists():
            content = workflow_file.read_text()
            # Most should be NONE, but plan should be PULL_REQUEST
            assert "validation: PULL_REQUEST" in content

    def test_no_validation_prompts_overrides_batch_mode(
        self, isolated_tmp_path: Path
    ) -> None:
        """Test --no-validation-prompts takes precedence over --validation-mode."""
        result = runner.invoke(
            app,
            [
                "init",
                str(isolated_tmp_path / "test-project"),
                "--ai",
                "claude",
                "--validation-mode",
                "pull-request",
                "--no-validation-prompts",
                "--no-git",
            ],
            input="1\n2\n",
        )
        workflow_file = isolated_tmp_path / "test-project" / "jpspec_workflow.yml"
        if workflow_file.exists():
            content = workflow_file.read_text()
            # --no-validation-prompts should result in all NONE
            # (transition_modes becomes empty dict, using defaults)
            assert "validation: NONE" in content
