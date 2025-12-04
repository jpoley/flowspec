"""Tests for constitution validate command."""

import pytest
from typer.testing import CliRunner

from specify_cli import app

runner = CliRunner()


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project directory."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    return tmp_path


def test_constitution_validate_file_not_found(tmp_path, monkeypatch):
    """Test validation when constitution file doesn't exist."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Constitution not found" in result.stdout
    assert "specify init --here" in result.stdout


def test_constitution_validate_no_markers(temp_project, monkeypatch):
    """Test validation passes when no NEEDS_VALIDATION markers present."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text(
        """# Project Constitution

## Quality Standards

All code must be tested.

## Git Workflow

Use feature branches.
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "Constitution is fully validated" in result.stdout
    assert "No NEEDS_VALIDATION markers found" in result.stdout


def test_constitution_validate_with_markers(temp_project, monkeypatch):
    """Test validation fails when NEEDS_VALIDATION markers present."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text(
        """<!-- NEEDS_VALIDATION: Project name -->
# [PROJECT_NAME] Constitution

<!-- NEEDS_VALIDATION: Quality standards -->
## Quality Standards

All code must be tested.

<!-- NEEDS_VALIDATION: Git workflow -->
## Git Workflow

Use feature branches.
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Found 3 section(s) requiring validation" in result.stdout
    assert "Project name" in result.stdout
    assert "Quality standards" in result.stdout
    assert "Git workflow" in result.stdout
    assert "Action Required:" in result.stdout
    assert "Remove the NEEDS_VALIDATION comment" in result.stdout


def test_constitution_validate_single_marker(temp_project, monkeypatch):
    """Test validation with single marker."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text(
        """# Project Constitution

<!-- NEEDS_VALIDATION: Version and date -->
Version: 1.0.0
Date: TBD
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Found 1 section(s) requiring validation" in result.stdout
    assert "Version and date" in result.stdout


def test_constitution_validate_custom_path(tmp_path):
    """Test validation with custom constitution path."""
    custom_path = tmp_path / "custom" / "my-constitution.md"
    custom_path.parent.mkdir()
    custom_path.write_text(
        """# Custom Constitution

No validation markers here.
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate", "--path", str(custom_path)],
        env={"PWD": str(tmp_path)},
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "Constitution is fully validated" in result.stdout


def test_constitution_validate_custom_path_not_found(tmp_path, monkeypatch):
    """Test validation with custom path that doesn't exist."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["constitution", "validate", "--path", str(tmp_path / "nonexistent.md")],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Constitution not found" in result.stdout


def test_constitution_validate_verbose_mode(temp_project, monkeypatch):
    """Test verbose mode output."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text(
        """<!-- NEEDS_VALIDATION: Project name -->
# [PROJECT_NAME] Constitution
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate", "--verbose"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Project name" in result.stdout
    # Note: verbose flag is defined but doesn't add extra output yet
    # This test is for future enhancement


def test_constitution_validate_multiline_markers(temp_project, monkeypatch):
    """Test that markers on multiple lines are all detected."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text(
        """<!-- NEEDS_VALIDATION: Section 1 -->
Content 1

<!-- NEEDS_VALIDATION: Section 2 -->
Content 2

<!-- NEEDS_VALIDATION: Section 3 -->
Content 3

<!-- NEEDS_VALIDATION: Section 4 -->
Content 4

<!-- NEEDS_VALIDATION: Section 5 -->
Content 5
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Found 5 section(s) requiring validation" in result.stdout
    for i in range(1, 6):
        assert f"Section {i}" in result.stdout


def test_constitution_validate_partial_completion(temp_project, monkeypatch):
    """Test validation with some markers removed (partial completion)."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text(
        """# My Project Constitution

This section is complete (marker removed).

<!-- NEEDS_VALIDATION: Technology stack -->
## Technology Stack

Still needs review.

<!-- NEEDS_VALIDATION: Version -->
Version: TBD
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Found 2 section(s) requiring validation" in result.stdout
    assert "Technology stack" in result.stdout
    assert "Version" in result.stdout


def test_constitution_validate_marker_format_variations(temp_project, monkeypatch):
    """Test that only properly formatted markers are detected."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text(
        """<!-- NEEDS_VALIDATION: Valid marker -->
Valid section

<!-- NEEDS_VALIDATION:No space after colon -->
Should not match (no space)

<!-- NEEDS VALIDATION: Missing underscore -->
Should not match (missing underscore)

<!--NEEDS_VALIDATION: No space before -->
Should not match (no leading space)
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    # Should only find the properly formatted marker
    assert result.exit_code == 1
    assert "Found 1 section(s) requiring validation" in result.stdout
    assert "Valid marker" in result.stdout


def test_constitution_validate_empty_file(temp_project, monkeypatch):
    """Test validation with empty constitution file."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text("")

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "Constitution is fully validated" in result.stdout


def test_constitution_validate_guidance_content(temp_project, monkeypatch):
    """Test that guidance panel has helpful content."""
    monkeypatch.chdir(temp_project)

    constitution_path = temp_project / "memory" / "constitution.md"
    constitution_path.write_text(
        """<!-- NEEDS_VALIDATION: Test marker -->
Content
"""
    )

    result = runner.invoke(
        app,
        ["constitution", "validate"],
        catch_exceptions=False,
    )

    # Check for key guidance elements
    assert "Action Required:" in result.stdout
    assert "Review each section" in result.stdout
    assert "Update the values" in result.stdout
    assert "Remove the NEEDS_VALIDATION comment" in result.stdout
    assert "Example:" in result.stdout
    assert "Before:" in result.stdout
    assert "After:" in result.stdout
