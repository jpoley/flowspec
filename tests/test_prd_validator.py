"""Tests for PRD validation module."""

import tempfile
from pathlib import Path

from specify_cli.workflow.prd_validator import (
    PRDValidationResult,
    PRDValidator,
    validate_prd_for_transition,
)


def test_prd_validator_exists():
    """Test PRD validator can be imported and instantiated."""
    validator = PRDValidator()
    assert validator is not None
    assert len(validator.REQUIRED_SECTIONS) > 0


def test_prd_validation_result():
    """Test PRD validation result basics."""
    result = PRDValidationResult()
    assert result.valid is True

    result.add_error("Test error")
    assert result.valid is False
    assert "Test error" in result.errors


def test_validate_prd_file_not_found():
    """Test validation fails for missing file."""
    validator = PRDValidator()
    with tempfile.TemporaryDirectory() as tmpdir:
        prd_path = Path(tmpdir) / "missing.md"
        result = validator.validate_prd(prd_path)
        assert result.valid is False
        assert any("not found" in e.lower() for e in result.errors)


def test_validate_prd_success():
    """Test validation succeeds for valid PRD."""
    validator = PRDValidator()
    with tempfile.TemporaryDirectory() as tmpdir:
        prd_path = Path(tmpdir) / "valid.md"
        prd_path.write_text(
            """
# PRD: Test Feature

## Executive Summary
This feature implements a comprehensive testing framework with advanced capabilities.
The system will provide automated testing, reporting, and integration with CI/CD pipelines.

## Problem Statement
Current testing infrastructure lacks automation and comprehensive coverage.
Teams spend significant time on manual testing, leading to delays and inconsistent quality.

## User Stories
US1: As a developer, I want automated test execution so that I can validate changes quickly.
US2: As a QA engineer, I want comprehensive test reports for better analysis.

## Functional Requirements
FR1: System shall execute automated tests on code commits.
FR2: System shall generate detailed test reports with pass/fail status.
FR3: System shall integrate with popular CI/CD platforms.

## Non-Functional Requirements
NFR1: Test execution time shall be under 5 minutes for standard test suites.
NFR2: System shall support concurrent test execution for improved performance.

## Success Metrics
- 95% test automation coverage
- 50% reduction in manual testing time
- Zero false positive test failures
"""
        )
        result = validator.validate_prd(prd_path)
        assert result.valid is True
        assert len(result.errors) == 0


def test_validate_prd_missing_sections():
    """Test validation fails when sections are missing."""
    validator = PRDValidator()
    with tempfile.TemporaryDirectory() as tmpdir:
        prd_path = Path(tmpdir) / "incomplete.md"
        prd_path.write_text("# PRD\n\n## Executive Summary\nSummary only.")
        result = validator.validate_prd(prd_path)
        assert result.valid is False
        assert len(result.sections_missing) > 0


def test_validate_prd_with_placeholders():
    """Test validation fails for placeholder content."""
    validator = PRDValidator()
    with tempfile.TemporaryDirectory() as tmpdir:
        prd_path = Path(tmpdir) / "stub.md"
        prd_path.write_text("# PRD\n\n[TODO] Write this later.")
        result = validator.validate_prd(prd_path)
        assert result.valid is False
        assert any("placeholder" in e.lower() for e in result.errors)


def test_validate_prd_for_transition():
    """Test convenience function."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        prd_dir = base / "docs" / "prd"
        prd_dir.mkdir(parents=True)

        prd_path = prd_dir / "test-feature.md"
        prd_path.write_text(
            """
# PRD: Test Feature

## Executive Summary
This PRD describes the test feature implementation with full details on requirements and success criteria.
The feature will deliver significant value through improved automation and efficiency.

## Problem Statement
Current manual processes are inefficient and error-prone, requiring automation.
The lack of standardization leads to inconsistent results and wasted effort across teams.

## User Stories
US1: As a user, I want automated processes so I can focus on higher-value work.
US2: As an administrator, I want consistent results across all operations for reliability.

## Functional Requirements
FR1: System shall automate common tasks with configurable workflows and templates.
FR2: System shall provide detailed logging and audit trails for compliance purposes.

## Non-Functional Requirements
NFR1: Operations shall complete within acceptable performance thresholds and SLAs.
NFR2: System shall maintain 99.9% uptime with proper error handling and recovery.

## Success Metrics
- 80% reduction in manual effort compared to baseline
- 99% process consistency across all operations
- Zero security incidents or compliance violations
"""
        )

        result = validate_prd_for_transition("test-feature", base)
        assert result.valid is True
