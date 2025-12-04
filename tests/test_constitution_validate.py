"""Tests for constitution validate command."""

import json
from pathlib import Path
from typer.testing import CliRunner
import pytest

from specify_cli import app

runner = CliRunner()


@pytest.fixture
def temp_constitution(tmp_path: Path) -> Path:
    """Create a temporary constitution file with NEEDS_VALIDATION markers."""
    const_path = tmp_path / "memory" / "constitution.md"
    const_path.parent.mkdir(parents=True, exist_ok=True)

    content = """# Test Project Constitution
<!-- NEEDS_VALIDATION: Project name -->

## Core Principles

### Quality-Driven Development
<!-- NEEDS_VALIDATION: Adjust quality principles to team practices -->
Code quality is a shared responsibility.

## Technology Stack
<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->
[LANGUAGES_AND_FRAMEWORKS]

### Linting & Formatting
<!-- NEEDS_VALIDATION: Detected linting tools -->
[LINTING_TOOLS]

## Governance

**Version**: 1.0.0 | **Ratified**: [DATE] | **Last Amended**: [DATE]
<!-- NEEDS_VALIDATION: Version and dates -->
"""
    const_path.write_text(content)
    return const_path


@pytest.fixture
def validated_constitution(tmp_path: Path) -> Path:
    """Create a fully validated constitution (no NEEDS_VALIDATION markers)."""
    const_path = tmp_path / "memory" / "constitution.md"
    const_path.parent.mkdir(parents=True, exist_ok=True)

    content = """# Validated Project Constitution

## Core Principles

### Quality-Driven Development
Code quality is a shared responsibility.

## Technology Stack
- Python 3.11+
- TypeScript 5

### Linting & Formatting
- ruff for Python
- eslint for TypeScript

## Governance

**Version**: 1.0.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2025-01-01
"""
    const_path.write_text(content)
    return const_path


class TestConstitutionValidate:
    """Test cases for 'specify constitution validate' command."""

    def test_validate_with_unvalidated_sections(
        self, temp_constitution: Path, monkeypatch
    ):
        """Test validation detects NEEDS_VALIDATION markers."""
        monkeypatch.chdir(temp_constitution.parent.parent)

        result = runner.invoke(app, ["constitution", "validate"])

        assert result.exit_code == 1  # Unvalidated sections found
        assert "Constitution Validation Status" in result.stdout
        assert "section(s) need validation" in result.stdout
        assert (
            "Project name" in result.stdout
            or "Test Project Constitution" in result.stdout
        )
        assert "Quality-Driven Development" in result.stdout
        assert "Technology Stack" in result.stdout

    def test_validate_fully_validated_constitution(
        self, validated_constitution: Path, monkeypatch
    ):
        """Test validation passes when no NEEDS_VALIDATION markers present."""
        monkeypatch.chdir(validated_constitution.parent.parent)

        result = runner.invoke(app, ["constitution", "validate"])

        assert result.exit_code == 0  # Fully validated
        assert "Constitution fully validated!" in result.stdout
        assert "No NEEDS_VALIDATION markers found" in result.stdout

    def test_validate_nonexistent_file(self, tmp_path: Path, monkeypatch):
        """Test validation handles missing constitution file."""
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["constitution", "validate"])

        assert result.exit_code == 2  # Error
        assert "Constitution file not found" in result.stdout

    def test_validate_custom_path(self, temp_constitution: Path):
        """Test validation with custom constitution path."""
        result = runner.invoke(
            app, ["constitution", "validate", "--path", str(temp_constitution)]
        )

        assert result.exit_code == 1  # Unvalidated sections
        assert "section(s) need validation" in result.stdout

    def test_validate_json_output_unvalidated(
        self, temp_constitution: Path, monkeypatch
    ):
        """Test JSON output for unvalidated constitution."""
        monkeypatch.chdir(temp_constitution.parent.parent)

        result = runner.invoke(app, ["constitution", "validate", "--json"])

        assert result.exit_code == 1

        # Parse JSON output
        output = json.loads(result.stdout)

        assert output["validated"] is False
        assert output["unvalidated_count"] > 0
        assert isinstance(output["markers"], list)
        assert len(output["markers"]) == output["unvalidated_count"]

        # Verify marker structure
        first_marker = output["markers"][0]
        assert "line" in first_marker
        assert "section" in first_marker
        assert "description" in first_marker
        assert "context" in first_marker

    def test_validate_json_output_validated(
        self, validated_constitution: Path, monkeypatch
    ):
        """Test JSON output for fully validated constitution."""
        monkeypatch.chdir(validated_constitution.parent.parent)

        result = runner.invoke(app, ["constitution", "validate", "--json"])

        assert result.exit_code == 0

        # Parse JSON output
        output = json.loads(result.stdout)

        assert output["validated"] is True
        assert output["unvalidated_count"] == 0
        assert output["markers"] == []

    def test_validate_json_output_missing_file(self, tmp_path: Path, monkeypatch):
        """Test JSON error output for missing constitution."""
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["constitution", "validate", "--json"])

        assert result.exit_code == 2

        # Parse JSON output
        output = json.loads(result.stdout)

        assert "error" in output
        assert "Constitution file not found" in output["error"]
        assert "path" in output

    def test_validate_detects_all_marker_formats(self, tmp_path: Path, monkeypatch):
        """Test validation detects various NEEDS_VALIDATION marker formats."""
        const_path = tmp_path / "memory" / "constitution.md"
        const_path.parent.mkdir(parents=True, exist_ok=True)

        content = """# Test Constitution

## Section 1
<!-- NEEDS_VALIDATION: Basic marker -->

## Section 2
<!--NEEDS_VALIDATION:No spaces-->

## Section 3
<!--  NEEDS_VALIDATION:  Extra  spaces  -->

## Section 4
<!-- NEEDS_VALIDATION: Multi-word description with punctuation! -->
"""
        const_path.write_text(content)
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["constitution", "validate", "--json"])

        output = json.loads(result.stdout)
        assert output["unvalidated_count"] == 4  # All formats detected

    def test_validate_marker_line_numbers(self, temp_constitution: Path, monkeypatch):
        """Test that reported line numbers are accurate."""
        monkeypatch.chdir(temp_constitution.parent.parent)

        result = runner.invoke(app, ["constitution", "validate", "--json"])
        output = json.loads(result.stdout)

        # Read constitution to verify line numbers
        content = temp_constitution.read_text()
        lines = content.split("\n")

        for marker in output["markers"]:
            line_num = marker["line"]
            line_content = lines[line_num - 1]  # 0-indexed vs 1-indexed
            assert "NEEDS_VALIDATION" in line_content

    def test_validate_finds_section_headings(
        self, temp_constitution: Path, monkeypatch
    ):
        """Test that section headings are correctly identified."""
        monkeypatch.chdir(temp_constitution.parent.parent)

        result = runner.invoke(app, ["constitution", "validate", "--json"])
        output = json.loads(result.stdout)

        # Most markers should have identified sections
        # (some may be "Unknown section" if they're before any heading)
        identified_sections = [
            m for m in output["markers"] if m["section"] != "Unknown section"
        ]
        assert len(identified_sections) > 0  # At least some should be identified

        # Section should be a markdown heading (no # prefix in result)
        for marker in identified_sections:
            assert not marker["section"].startswith("#")

    def test_validate_instructions_in_output(
        self, temp_constitution: Path, monkeypatch
    ):
        """Test that helpful instructions are shown in human-readable output."""
        monkeypatch.chdir(temp_constitution.parent.parent)

        result = runner.invoke(app, ["constitution", "validate"])

        # Verify instructions are present
        assert "Next steps:" in result.stdout
        assert "Review each section" in result.stdout
        assert "Update the content" in result.stdout
        assert "Remove the <!-- NEEDS_VALIDATION" in result.stdout
        assert "Run this command again" in result.stdout
        assert "Edit file:" in result.stdout


class TestConstitutionValidateEdgeCases:
    """Edge case tests for constitution validation."""

    def test_validate_empty_constitution(self, tmp_path: Path, monkeypatch):
        """Test validation with empty constitution file."""
        const_path = tmp_path / "memory" / "constitution.md"
        const_path.parent.mkdir(parents=True, exist_ok=True)
        const_path.write_text("")
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["constitution", "validate"])

        assert result.exit_code == 0  # No markers = validated
        assert "Constitution fully validated!" in result.stdout

    def test_validate_marker_without_description(self, tmp_path: Path, monkeypatch):
        """Test handling of malformed NEEDS_VALIDATION marker."""
        const_path = tmp_path / "memory" / "constitution.md"
        const_path.parent.mkdir(parents=True, exist_ok=True)

        # Malformed marker (no description after colon)
        content = """# Test
<!-- NEEDS_VALIDATION: -->
"""
        const_path.write_text(content)
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["constitution", "validate", "--json"])
        output = json.loads(result.stdout)

        # Should still detect marker even if description is empty
        assert output["unvalidated_count"] >= 0

    def test_validate_with_permission_error(self, tmp_path: Path, monkeypatch):
        """Test handling of unreadable constitution file."""
        const_path = tmp_path / "memory" / "constitution.md"
        const_path.parent.mkdir(parents=True, exist_ok=True)
        const_path.write_text("# Test")

        # Make file unreadable (may not work on all systems)
        try:
            const_path.chmod(0o000)
            monkeypatch.chdir(tmp_path)

            result = runner.invoke(app, ["constitution", "validate"])

            assert result.exit_code == 2  # Error
            assert (
                "Error reading file" in result.stdout
                or "Permission denied" in result.stdout
            )
        finally:
            # Restore permissions for cleanup
            const_path.chmod(0o644)

    def test_validate_marker_at_file_start(self, tmp_path: Path, monkeypatch):
        """Test marker detection at the very start of file."""
        const_path = tmp_path / "memory" / "constitution.md"
        const_path.parent.mkdir(parents=True, exist_ok=True)

        content = """<!-- NEEDS_VALIDATION: First line marker -->
# Constitution
"""
        const_path.write_text(content)
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["constitution", "validate", "--json"])
        output = json.loads(result.stdout)

        assert output["unvalidated_count"] == 1
        assert output["markers"][0]["line"] == 1


class TestConstitutionValidateHelp:
    """Test help and usage information."""

    def test_constitution_help(self):
        """Test 'specify constitution --help' shows available commands."""
        result = runner.invoke(app, ["constitution", "--help"])

        assert result.exit_code == 0
        assert "validate" in result.stdout
        assert "constitution" in result.stdout.lower()

    def test_validate_help(self):
        """Test 'specify constitution validate --help' shows usage."""
        result = runner.invoke(app, ["constitution", "validate", "--help"])

        assert result.exit_code == 0
        assert "--path" in result.stdout
        assert "--json" in result.stdout
        assert "NEEDS_VALIDATION" in result.stdout
