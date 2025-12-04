"""Tests for constitution version tracking command."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from specify_cli import CONSTITUTION_VERSION, app

runner = CliRunner()


@pytest.fixture
def temp_constitution(tmp_path: Path) -> Path:
    """Create a temporary constitution file with version info."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    constitution = memory_dir / "constitution.md"
    constitution.write_text(
        """# Test Constitution
<!-- TIER: Medium - Standard controls for typical business projects -->

## Core Principles
Test content...

## Governance

This constitution guides team practices.

**Version**: 1.0.0
**Ratified**: 2025-01-01
**Last Amended**: 2025-01-15
<!-- NEEDS_VALIDATION: Version and dates -->
"""
    )
    return constitution


@pytest.fixture
def temp_outdated_constitution(tmp_path: Path) -> Path:
    """Create a temporary constitution file with outdated version."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(exist_ok=True)
    constitution = memory_dir / "constitution.md"
    constitution.write_text(
        """# Test Constitution
<!-- TIER: Light - Minimal controls -->

## Core Principles
Test content...

## Governance

This constitution is a living document.

**Version**: 0.9.0
**Ratified**: 2024-01-01
**Last Amended**: 2024-01-15
<!-- NEEDS_VALIDATION: Version and dates -->
"""
    )
    return constitution


@pytest.fixture
def temp_heavy_constitution(tmp_path: Path) -> Path:
    """Create a temporary heavy tier constitution file."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(exist_ok=True)
    constitution = memory_dir / "constitution.md"
    constitution.write_text(
        """# Test Constitution
<!-- TIER: Heavy - Strict controls for enterprise/regulated environments -->

## Core Principles
Test content...

## Governance

This constitution supersedes all other practices.

**Version**: 1.0.0
**Ratified**: 2025-01-01
**Last Amended**: 2025-01-15
<!-- NEEDS_VALIDATION: Version and dates -->
"""
    )
    return constitution


def test_constitution_version_displays_info(temp_constitution: Path, monkeypatch):
    """Test that constitution-version displays version information."""
    monkeypatch.chdir(temp_constitution.parent.parent)

    result = runner.invoke(app, ["constitution-version"])

    assert result.exit_code == 0
    assert "1.0.0" in result.stdout
    assert "Medium" in result.stdout
    assert "2025-01-01" in result.stdout
    assert "2025-01-15" in result.stdout
    assert CONSTITUTION_VERSION in result.stdout


def test_constitution_version_custom_path(temp_constitution: Path):
    """Test that constitution-version works with custom path."""
    result = runner.invoke(
        app, ["constitution-version", "--path", str(temp_constitution)]
    )

    assert result.exit_code == 0
    assert "1.0.0" in result.stdout
    assert "Medium" in result.stdout


def test_constitution_version_detects_medium_tier(temp_constitution: Path):
    """Test that constitution-version correctly detects Medium tier."""
    result = runner.invoke(
        app, ["constitution-version", "--path", str(temp_constitution)]
    )
    assert result.exit_code == 0
    assert "Medium" in result.stdout


def test_constitution_version_detects_light_tier(temp_outdated_constitution: Path):
    """Test that constitution-version correctly detects Light tier."""
    result = runner.invoke(
        app, ["constitution-version", "--path", str(temp_outdated_constitution)]
    )
    assert result.exit_code == 0
    assert "Light" in result.stdout


def test_constitution_version_detects_heavy_tier(temp_heavy_constitution: Path):
    """Test that constitution-version correctly detects Heavy tier."""
    result = runner.invoke(
        app, ["constitution-version", "--path", str(temp_heavy_constitution)]
    )
    assert result.exit_code == 0
    assert "Heavy" in result.stdout


def test_constitution_version_shows_upgrade_available(
    temp_outdated_constitution: Path, monkeypatch
):
    """Test that constitution-version shows upgrade message when outdated."""
    monkeypatch.chdir(temp_outdated_constitution.parent.parent)

    result = runner.invoke(app, ["constitution-version"])

    assert result.exit_code == 0
    assert "0.9.0" in result.stdout
    assert "Template version" in result.stdout
    assert CONSTITUTION_VERSION in result.stdout
    assert "⚠" in result.stdout or "available" in result.stdout.lower()


def test_constitution_version_missing_file(tmp_path: Path, monkeypatch):
    """Test that constitution-version errors when file is missing."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["constitution-version"])

    assert result.exit_code == 1
    assert "not found" in result.stdout.lower() or "Error" in result.stdout


def test_constitution_version_missing_custom_path():
    """Test that constitution-version errors with missing custom path."""
    result = runner.invoke(
        app, ["constitution-version", "--path", "/nonexistent/path/constitution.md"]
    )

    assert result.exit_code == 1
    assert "not found" in result.stdout.lower() or "Error" in result.stdout


def test_constitution_version_unknown_fields(tmp_path: Path, monkeypatch):
    """Test that constitution-version handles missing version fields gracefully."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    constitution = memory_dir / "constitution.md"
    constitution.write_text(
        """# Test Constitution

## Core Principles
Test content without version info...
"""
    )

    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["constitution-version"])

    assert result.exit_code == 0
    assert "Unknown" in result.stdout
