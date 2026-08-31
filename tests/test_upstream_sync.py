"""Tests for the spec-kit and Backlog.md upstream sync.

Covers:
- The pinned backlog-md version constants.
- The install/upgrade minimum-version guard.
- Template content ported from upstream spec-kit.
- Definition of Done guidance in the deployed backlog partials.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pytest

from flowspec_cli import (
    compare_semver,
    get_backlog_validated_version,
    warn_if_backlog_version_below_minimum,
)
from flowspec_cli.versions import (
    BACKLOG_MIN_VERSION,
    BACKLOG_RECOMMENDED_VERSION,
)

# Minimum length for a template section to count as real content, not a stub.
MIN_SECTION_LENGTH = 40


def get_project_root() -> Path:
    """Get the project root directory reliably."""
    return Path(__file__).resolve().parent.parent


def safe_read_file(file_path: Path) -> Optional[str]:
    """Safely read file, returning None on missing/error."""
    try:
        if file_path.exists() and file_path.is_file():
            return file_path.read_text(encoding="utf-8")
    except OSError:
        pass
    return None


def read_template(*parts: str) -> str:
    """Read a bundled template, asserting it exists."""
    path = get_project_root().joinpath("src", "flowspec_cli", "templates", *parts)
    content = safe_read_file(path)
    assert content is not None, f"Template not found: {path}"
    return content


class TestBacklogVersionConstants:
    def test_recommended_is_at_least_minimum(self) -> None:
        assert compare_semver(BACKLOG_RECOMMENDED_VERSION, BACKLOG_MIN_VERSION) >= 0, (
            f"recommended {BACKLOG_RECOMMENDED_VERSION} is below "
            f"minimum {BACKLOG_MIN_VERSION}"
        )

    def test_minimum_supports_definition_of_done(self) -> None:
        # backlog-md gained --dod/--check-dod in 1.34.0.
        assert compare_semver(BACKLOG_MIN_VERSION, "1.34.0") >= 0

    def test_validated_version_returns_recommended(self) -> None:
        assert get_backlog_validated_version() == BACKLOG_RECOMMENDED_VERSION

    def test_recommended_is_newer_than_the_old_pin(self) -> None:
        # Guards against silently regressing to the long-stale 1.21.0 pin.
        assert compare_semver(BACKLOG_RECOMMENDED_VERSION, "1.21.0") > 0


class TestMinimumVersionGuard:
    def test_warns_below_minimum(self, capsys: pytest.CaptureFixture[str]) -> None:
        warn_if_backlog_version_below_minimum("1.21.0")
        out = capsys.readouterr().out
        assert "Warning" in out
        assert BACKLOG_MIN_VERSION in out

    def test_silent_at_minimum(self, capsys: pytest.CaptureFixture[str]) -> None:
        warn_if_backlog_version_below_minimum(BACKLOG_MIN_VERSION)
        assert capsys.readouterr().out == ""

    def test_silent_above_minimum(self, capsys: pytest.CaptureFixture[str]) -> None:
        warn_if_backlog_version_below_minimum(BACKLOG_RECOMMENDED_VERSION)
        assert capsys.readouterr().out == ""


class TestSpecKitTemplatePorts:
    def test_spec_template_has_assumptions_section(self) -> None:
        content = read_template("spec-template.md")
        assert "## Assumptions" in content
        section = content.split("## Assumptions", 1)[1]
        assert len(section) > MIN_SECTION_LENGTH, "Assumptions section is a stub"

    def test_plan_template_project_type_lists_concrete_options(self) -> None:
        content = read_template("plan-template.md")
        assert "web-service" in content
        assert "[single/web/mobile - determines source structure]" not in content

    def test_plan_template_complexity_tracking_is_a_callout(self) -> None:
        content = read_template("plan-template.md")
        assert (
            "> **Fill ONLY if Constitution Check has violations that must be justified**"
            in content
        )

    def test_checklist_template_declares_marker_semantics(self) -> None:
        content = read_template("checklist-template.md")
        assert "**Review Ownership**" in content
        assert "**Marker Semantics**" in content
        assert "must not modify markers" in content

    def test_checklist_template_uses_flow_namespace(self) -> None:
        content = read_template("checklist-template.md")
        assert "/spec.checklist" not in content
        assert "/flow:gate" in content

    def test_templates_carry_no_speckit_placeholder_tokens(self) -> None:
        # Upstream uses __SPECKIT_COMMAND_*__ tokens; flowspec resolves command
        # names directly, so the tokens must never be copied in.
        for name in (
            "spec-template.md",
            "plan-template.md",
            "tasks-template.md",
            "checklist-template.md",
        ):
            assert "__SPECKIT_COMMAND_" not in read_template(name), (
                f"{name} contains an unresolved spec-kit placeholder token"
            )


class TestDefinitionOfDoneGuidance:
    def test_flow_partial_documents_dod_flags(self) -> None:
        content = read_template("partials", "flow", "_backlog-instructions.md")
        for flag in ("--check-dod", "--dod", "--no-dod-defaults", "--final-summary"):
            assert flag in content, f"{flag} missing from flow backlog partial"

    def test_flow_partial_mentions_config_key(self) -> None:
        content = read_template("partials", "flow", "_backlog-instructions.md")
        assert "definitionOfDone" in content

    def test_root_partial_requires_dod_check_before_done(self) -> None:
        content = read_template("partials", "backlog-instructions.md")
        assert "--check-dod" in content
        assert "definitionOfDone" in content
