"""PRD (Product Requirements Document) validator for workflow transitions.

This module validates PRD artifacts before workflow transitions can proceed.
It checks for:
- File existence at expected path
- Required sections present in the document
- Content is not a stub/placeholder

The validator integrates with the transition schema from task-172 to gate
transitions requiring PRD artifacts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PRDValidationResult:
    """Result of PRD validation.

    Attributes:
        valid: Whether the PRD passed all validation checks.
        errors: List of validation error messages.
        warnings: List of validation warning messages.
        sections_found: List of required sections that were found.
        sections_missing: List of required sections that are missing.
    """

    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    sections_found: list[str] = field(default_factory=list)
    sections_missing: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error message and mark validation as failed.

        Args:
            message: Error message to add.
        """
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning message.

        Args:
            message: Warning message to add.
        """
        self.warnings.append(message)


class PRDValidator:
    """Validator for PRD artifacts.

    Validates that PRD files meet quality requirements before
    workflow transitions can proceed.
    """

    # Required sections that must appear in a valid PRD
    REQUIRED_SECTIONS = [
        "Executive Summary",
        "Problem Statement",
        "User Stories",
        "Functional Requirements",
        "Non-Functional Requirements",
        "Success Metrics",
    ]

    # Optional but recommended sections
    RECOMMENDED_SECTIONS = [
        "Dependencies",
        "Risks and Mitigations",
        "Out of Scope",
    ]

    # Patterns that indicate placeholder/stub content
    STUB_PATTERNS = [
        r"\[TODO\]",
        r"\[TBD\]",
        r"\[To be determined\]",
        r"Lorem ipsum",
        r"PLACEHOLDER",
        r"XXX",
    ]

    def __init__(
        self,
        required_sections: list[str] | None = None,
        stub_patterns: list[str] | None = None,
    ):
        """Initialize the PRD validator.

        Args:
            required_sections: Override default required sections.
            stub_patterns: Override default stub detection patterns.
        """
        self.required_sections = required_sections or self.REQUIRED_SECTIONS
        self.stub_patterns = stub_patterns or self.STUB_PATTERNS

    def validate_exists(self, prd_path: Path) -> PRDValidationResult:
        """Validate that PRD file exists.

        Args:
            prd_path: Path to the PRD file.

        Returns:
            PRDValidationResult with existence check results.
        """
        result = PRDValidationResult()

        if not prd_path.exists():
            result.add_error(f"PRD file not found: {prd_path}")
            return result

        if not prd_path.is_file():
            result.add_error(f"PRD path is not a file: {prd_path}")
            return result

        # Check file is not empty
        if prd_path.stat().st_size == 0:
            result.add_error(f"PRD file is empty: {prd_path}")
            return result

        return result

    def validate_sections(self, content: str) -> PRDValidationResult:
        """Validate that PRD contains required sections.

        Checks for the presence of required section headers in the document.
        Section headers are expected in Markdown format (## Section Name).

        Args:
            content: PRD file content as string.

        Returns:
            PRDValidationResult with section validation results.
        """
        result = PRDValidationResult()

        # Extract all markdown headers (## Header or # Header)
        header_pattern = r"^#{1,3}\s+(.+)$"
        headers = []
        for line in content.split("\n"):
            match = re.match(header_pattern, line.strip())
            if match:
                headers.append(match.group(1).strip())

        # Check for required sections
        for required_section in self.required_sections:
            found = any(
                required_section.lower() in header.lower() for header in headers
            )
            if found:
                result.sections_found.append(required_section)
            else:
                result.sections_missing.append(required_section)
                result.add_error(f"Missing required section: {required_section}")

        # Check for recommended sections (warnings only)
        for recommended_section in self.RECOMMENDED_SECTIONS:
            found = any(
                recommended_section.lower() in header.lower() for header in headers
            )
            if not found:
                result.add_warning(
                    f"Recommended section not found: {recommended_section}"
                )

        return result

    def validate_not_stub(self, content: str) -> PRDValidationResult:
        """Validate that PRD is not a placeholder/stub.

        Checks for common placeholder patterns that indicate the PRD
        has not been properly filled out.

        Args:
            content: PRD file content as string.

        Returns:
            PRDValidationResult with stub detection results.
        """
        result = PRDValidationResult()

        # Check for stub patterns
        for pattern in self.stub_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                result.add_error(f"PRD contains placeholder content: {pattern}")

        # Check for minimum content length (excluding headers and whitespace)
        # Strip markdown headers and count remaining content
        content_lines = [
            line
            for line in content.split("\n")
            if line.strip() and not re.match(r"^#{1,3}\s+", line.strip())
        ]
        content_text = " ".join(content_lines)

        if len(content_text) < 200:
            result.add_error(
                "PRD appears to be a stub (insufficient content, minimum 200 characters)"
            )

        return result

    def validate_prd(self, prd_path: Path) -> PRDValidationResult:
        """Perform complete PRD validation.

        Combines all validation checks:
        1. File exists
        2. Contains required sections
        3. Is not a stub/placeholder

        Args:
            prd_path: Path to the PRD file.

        Returns:
            PRDValidationResult with all validation results.
        """
        # Check existence first
        result = self.validate_exists(prd_path)
        if not result.valid:
            return result

        # Read content
        try:
            content = prd_path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(f"Failed to read PRD file: {e}")
            return result

        # Validate sections
        section_result = self.validate_sections(content)
        result.errors.extend(section_result.errors)
        result.warnings.extend(section_result.warnings)
        result.sections_found.extend(section_result.sections_found)
        result.sections_missing.extend(section_result.sections_missing)

        # Validate not stub
        stub_result = self.validate_not_stub(content)
        result.errors.extend(stub_result.errors)
        result.warnings.extend(stub_result.warnings)

        # Update valid flag
        result.valid = len(result.errors) == 0

        return result


def validate_prd_for_transition(
    feature_name: str, base_path: Path | None = None
) -> PRDValidationResult:
    """Validate PRD for a feature transition.

    Convenience function that constructs the expected PRD path and
    validates it using the standard validator.

    Args:
        feature_name: Feature slug (e.g., "user-authentication").
        base_path: Base project directory (defaults to current directory).

    Returns:
        PRDValidationResult with validation results.

    Example:
        >>> result = validate_prd_for_transition("user-auth")
        >>> if not result.valid:
        ...     print(f"Errors: {result.errors}")
    """
    if base_path is None:
        base_path = Path.cwd()

    prd_path = base_path / "docs" / "prd" / f"{feature_name}.md"
    validator = PRDValidator()
    return validator.validate_prd(prd_path)
