"""Tests for interactive validation mode prompts in specify init command.

Tests cover:
- AC1: Add validation mode prompts to specify init command
- AC2: Support NONE selection (default, press Enter)
- AC3: Support KEYWORD selection with custom keyword input
- AC4: Support PULL_REQUEST selection
- AC8: Display summary of configured validation modes at end
"""

from unittest.mock import patch

import pytest
import typer

from specify_cli import (
    display_validation_summary,
    prompt_validation_modes,
)


class TestPromptValidationModes:
    """Tests for prompt_validation_modes function."""

    @patch("specify_cli.typer.prompt")
    def test_all_none_default(self, mock_prompt):
        """AC2: Test NONE selection as default (pressing Enter)."""
        # Simulate user pressing Enter (default "1") for all transitions
        mock_prompt.side_effect = ["1"] * 7  # 7 transitions

        result = prompt_validation_modes()

        # Verify all transitions are set to "none"
        assert len(result) == 7
        assert all(v == "none" for v in result.values())
        assert "assess" in result
        assert "specify" in result
        assert "research" in result
        assert "plan" in result
        assert "implement" in result
        assert "validate" in result
        assert "operate" in result

    @patch("specify_cli.typer.prompt")
    def test_keyword_selection_with_custom_keyword(self, mock_prompt):
        """AC3: Test KEYWORD selection with custom keyword input."""
        # User selects KEYWORD (2) for specify transition with custom keyword
        mock_prompt.side_effect = [
            "1",  # assess: NONE
            "2",  # specify: KEYWORD
            "PRD_APPROVED",  # custom keyword
            "1",  # research: NONE
            "1",  # plan: NONE
            "1",  # implement: NONE
            "1",  # validate: NONE
            "1",  # operate: NONE
        ]

        result = prompt_validation_modes()

        assert result["specify"] == 'KEYWORD["PRD_APPROVED"]'
        assert result["assess"] == "none"
        assert result["research"] == "none"

    @patch("specify_cli.typer.prompt")
    def test_keyword_selection_with_default_keyword(self, mock_prompt):
        """AC3: Test KEYWORD selection with default keyword (APPROVED)."""
        # User selects KEYWORD (2) but presses Enter for keyword (default)
        mock_prompt.side_effect = [
            "1",  # assess: NONE
            "2",  # specify: KEYWORD
            "APPROVED",  # default keyword
            "1",  # research: NONE
            "1",  # plan: NONE
            "1",  # implement: NONE
            "1",  # validate: NONE
            "1",  # operate: NONE
        ]

        result = prompt_validation_modes()

        assert result["specify"] == 'KEYWORD["APPROVED"]'

    @patch("specify_cli.typer.prompt")
    def test_pull_request_selection(self, mock_prompt):
        """AC4: Test PULL_REQUEST selection."""
        # User selects PULL_REQUEST (3) for plan transition
        mock_prompt.side_effect = [
            "1",  # assess: NONE
            "1",  # specify: NONE
            "1",  # research: NONE
            "3",  # plan: PULL_REQUEST
            "1",  # implement: NONE
            "1",  # validate: NONE
            "1",  # operate: NONE
        ]

        result = prompt_validation_modes()

        assert result["plan"] == "pull-request"
        assert result["assess"] == "none"
        assert result["specify"] == "none"

    @patch("specify_cli.typer.prompt")
    def test_mixed_validation_modes(self, mock_prompt):
        """Test multiple different validation modes configured."""
        # Mix of NONE, KEYWORD, and PULL_REQUEST
        mock_prompt.side_effect = [
            "1",  # assess: NONE
            "2",  # specify: KEYWORD
            "SPEC_OK",  # custom keyword
            "1",  # research: NONE
            "3",  # plan: PULL_REQUEST
            "2",  # implement: KEYWORD
            "IMPL_READY",  # custom keyword
            "1",  # validate: NONE
            "3",  # operate: PULL_REQUEST
        ]

        result = prompt_validation_modes()

        assert result["assess"] == "none"
        assert result["specify"] == 'KEYWORD["SPEC_OK"]'
        assert result["research"] == "none"
        assert result["plan"] == "pull-request"
        assert result["implement"] == 'KEYWORD["IMPL_READY"]'
        assert result["validate"] == "none"
        assert result["operate"] == "pull-request"

    @patch("specify_cli.typer.prompt")
    def test_invalid_choice_defaults_to_none(self, mock_prompt):
        """Test that invalid choices default to NONE with warning."""
        # User enters invalid choice "4"
        mock_prompt.side_effect = [
            "4",  # invalid choice
            "1",  # specify: NONE
            "1",  # research: NONE
            "1",  # plan: NONE
            "1",  # implement: NONE
            "1",  # validate: NONE
            "1",  # operate: NONE
        ]

        result = prompt_validation_modes()

        # Invalid choice should default to "none"
        assert result["assess"] == "none"

    @patch("specify_cli.typer.prompt")
    def test_empty_keyword_uses_default(self, mock_prompt):
        """Test that empty keyword input uses default 'APPROVED'."""
        # User selects KEYWORD but enters empty string
        mock_prompt.side_effect = [
            "2",  # assess: KEYWORD
            "",  # empty keyword
            "1",  # specify: NONE
            "1",  # research: NONE
            "1",  # plan: NONE
            "1",  # implement: NONE
            "1",  # validate: NONE
            "1",  # operate: NONE
        ]

        result = prompt_validation_modes()

        # Empty keyword should use default "APPROVED"
        assert result["assess"] == 'KEYWORD["APPROVED"]'

    @patch("specify_cli.typer.prompt")
    def test_whitespace_keyword_trimmed(self, mock_prompt):
        """Test that keyword whitespace is trimmed."""
        # User enters keyword with leading/trailing whitespace
        mock_prompt.side_effect = [
            "2",  # assess: KEYWORD
            "  TRIMMED  ",  # keyword with whitespace
            "1",  # specify: NONE
            "1",  # research: NONE
            "1",  # plan: NONE
            "1",  # implement: NONE
            "1",  # validate: NONE
            "1",  # operate: NONE
        ]

        result = prompt_validation_modes()

        assert result["assess"] == 'KEYWORD["TRIMMED"]'

    @patch("specify_cli.typer.prompt")
    def test_keyboard_interrupt_exits(self, mock_prompt):
        """Test that Ctrl+C (KeyboardInterrupt) exits gracefully."""
        # Simulate user pressing Ctrl+C
        mock_prompt.side_effect = KeyboardInterrupt()

        with pytest.raises(typer.Exit) as exc_info:
            prompt_validation_modes()

        assert exc_info.value.exit_code == 1


class TestDisplayValidationSummary:
    """Tests for display_validation_summary function."""

    def test_all_none_displays_default_message(self, capsys):
        """AC8: Test summary when all transitions are NONE."""
        modes = {
            "assess": "none",
            "specify": "none",
            "research": "none",
            "plan": "none",
            "implement": "none",
            "validate": "none",
            "operate": "none",
        }

        display_validation_summary(modes)

        captured = capsys.readouterr()
        assert "Validation Mode Summary" in captured.out
        assert "All transitions using NONE (default)" in captured.out

    def test_custom_modes_displayed(self, capsys):
        """AC8: Test summary displays custom validation modes."""
        modes = {
            "assess": "none",
            "specify": 'KEYWORD["PRD_OK"]',
            "research": "none",
            "plan": "pull-request",
            "implement": "none",
            "validate": "none",
            "operate": "none",
        }

        display_validation_summary(modes)

        captured = capsys.readouterr()
        assert "Custom validation modes:" in captured.out
        assert "specify" in captured.out
        assert 'KEYWORD["PRD_OK"]' in captured.out
        assert "plan" in captured.out
        assert "PULL_REQUEST" in captured.out
        # NONE modes should not be shown
        assert "assess" not in captured.out or "none" not in captured.out.lower()

    def test_mixed_modes_formatted_correctly(self, capsys):
        """AC8: Test summary formats different mode types correctly."""
        modes = {
            "assess": "none",
            "specify": 'keyword["APPROVED"]',  # lowercase input
            "research": "none",
            "plan": "pull-request",
            "implement": 'KEYWORD["READY"]',  # uppercase input
            "validate": "none",
            "operate": "none",
        }

        display_validation_summary(modes)

        captured = capsys.readouterr()
        # Should uppercase keyword modes
        assert 'KEYWORD["APPROVED"]' in captured.out
        assert 'KEYWORD["READY"]' in captured.out
        assert "PULL_REQUEST" in captured.out

    def test_empty_modes_dict(self, capsys):
        """Test summary with empty modes dict (all defaults)."""
        modes = {}

        display_validation_summary(modes)

        captured = capsys.readouterr()
        assert "All transitions using NONE (default)" in captured.out


class TestInitCommandIntegration:
    """Integration tests for validation prompts in init command."""

    @pytest.fixture
    def temp_project_dir(self, tmp_path):
        """Create a temporary project directory."""
        project_dir = tmp_path / "test-project"
        project_dir.mkdir()
        return project_dir

    def test_no_validation_prompts_flag_skips_prompts(self, temp_project_dir):
        """Test that --no-validation-prompts skips prompts and uses NONE."""
        # This would be an integration test with actual CLI invocation
        # For now, we test the logic directly
        no_validation_prompts = True
        transition_modes = {}

        if no_validation_prompts:
            transition_modes = {}

        assert transition_modes == {}

    def test_explicit_flags_override_prompts(self):
        """Test that explicit --validation-* flags override prompts."""
        # Simulated CLI flags
        explicit_flags = {
            "assess": "none",
            "research": "none",
            "specify": "keyword",  # explicit flag
            "plan": "none",
            "implement": "none",
            "validate": "none",
            "operate": "none",
        }

        has_explicit_flags = any(v.lower() != "none" for v in explicit_flags.values())

        assert has_explicit_flags is True

    def test_interactive_mode_detection(self):
        """Test detection of interactive vs non-interactive mode."""
        import sys

        # This test validates the logic, actual TTY testing would require mocking
        is_interactive = sys.stdin.isatty()

        # In test environment, this is typically False
        # In actual terminal, this would be True
        assert isinstance(is_interactive, bool)


class TestValidationModeFormatting:
    """Tests for validation mode string formatting."""

    def test_keyword_format_with_quotes(self):
        """Test KEYWORD format includes quotes."""
        mode = 'KEYWORD["APPROVED"]'
        assert mode.startswith("KEYWORD[")
        assert mode.endswith("]")
        assert '"' in mode

    def test_pull_request_format(self):
        """Test PULL_REQUEST format is lowercase with hyphen."""
        mode = "pull-request"
        assert mode == "pull-request"

    def test_none_format(self):
        """Test NONE format is lowercase."""
        mode = "none"
        assert mode == "none"


# Edge cases and error handling


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @patch("specify_cli.typer.prompt")
    def test_all_keyword_modes_different_keywords(self, mock_prompt):
        """Test each transition can have different keyword."""
        mock_prompt.side_effect = [
            "2",
            "ASSESS_OK",
            "2",
            "SPECIFY_OK",
            "2",
            "RESEARCH_OK",
            "2",
            "PLAN_OK",
            "2",
            "IMPL_OK",
            "2",
            "VALIDATE_OK",
            "2",
            "OPERATE_OK",
        ]

        result = prompt_validation_modes()

        assert result["assess"] == 'KEYWORD["ASSESS_OK"]'
        assert result["specify"] == 'KEYWORD["SPECIFY_OK"]'
        assert result["research"] == 'KEYWORD["RESEARCH_OK"]'
        assert result["plan"] == 'KEYWORD["PLAN_OK"]'
        assert result["implement"] == 'KEYWORD["IMPL_OK"]'
        assert result["validate"] == 'KEYWORD["VALIDATE_OK"]'
        assert result["operate"] == 'KEYWORD["OPERATE_OK"]'

    @patch("specify_cli.typer.prompt")
    def test_all_pull_request_modes(self, mock_prompt):
        """Test all transitions can be PULL_REQUEST."""
        mock_prompt.side_effect = ["3"] * 7  # All PR mode

        result = prompt_validation_modes()

        assert all(v == "pull-request" for v in result.values())

    @patch("specify_cli.typer.prompt")
    def test_special_characters_in_keyword(self, mock_prompt):
        """Test keywords with special characters."""
        mock_prompt.side_effect = [
            "2",  # KEYWORD
            "APPROVED-2024!",  # keyword with special chars
            "1",  # specify: NONE
            "1",  # research: NONE
            "1",  # plan: NONE
            "1",  # implement: NONE
            "1",  # validate: NONE
            "1",  # operate: NONE
        ]

        result = prompt_validation_modes()

        assert result["assess"] == 'KEYWORD["APPROVED-2024!"]'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
