"""AI-powered vulnerability fix generation.

This module provides automated code patch generation for security findings.
It generates unified diffs that can be applied to fix vulnerabilities.

See ADR-006 for the AI triage engine that identifies vulnerabilities,
and this module for the fix generation that follows.
"""

from flowspec_cli.security.fixer.applicator import (
    ApplyResult,
    ApplyStatus,
    BatchApplyResult,
    PatchApplicator,
    PatchApplicatorConfig,
)
from flowspec_cli.security.fixer.generator import FixGenerator
from flowspec_cli.security.fixer.models import (
    FixPattern,
    FixResult,
    FixStatus,
    Patch,
)
from flowspec_cli.security.fixer.patterns import FixPatternLibrary

__all__ = [
    # Models
    "FixResult",
    "FixStatus",
    "Patch",
    "FixPattern",
    # Generator
    "FixGenerator",
    "FixPatternLibrary",
    # Applicator
    "ApplyResult",
    "ApplyStatus",
    "BatchApplyResult",
    "PatchApplicator",
    "PatchApplicatorConfig",
]
