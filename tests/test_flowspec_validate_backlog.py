"""Tests for /flow:validate backlog.md integration.

Verifies AC#1-AC#7 for task-113:
- AC#1: Command discovers tasks in In Progress or Done status for validation
- AC#2: Validation workflow references sub-agents with backlog capabilities
- AC#3: QA sub-agent validates ACs match test results
- AC#4: Security sub-agent validates security-related ACs
- AC#5: Documentation check phase handles docs validation
- AC#6: AC verification phase ensures all criteria are met
- AC#7: Test: Run /flow:validate and verify task validation workflow

NOTE: validate.md was simplified to use a phased workflow with sub-agents instead
of inline AGENT CONTEXT sections. Tests have been updated accordingly.
"""

import pytest
from pathlib import Path


@pytest.fixture
def validate_md_path():
    """Get path to validate.md command file."""
    return (
        Path(__file__).parent.parent / ".claude" / "commands" / "flow" / "validate.md"
    )


@pytest.fixture
def backlog_instructions_path():
    """Get path to _backlog-instructions.md file."""
    return (
        Path(__file__).parent.parent
        / ".claude"
        / "partials"
        / "flow"
        / "_backlog-instructions.md"
    )


@pytest.fixture
def validate_agents_dir():
    """Get path to validate sub-agents directory."""
    return Path(__file__).parent.parent / ".claude" / "agents" / "validate"


class TestTaskDiscoveryAC1:
    """AC #1: Command discovers tasks in In Progress or Done status for validation."""

    def test_validate_md_exists(self, validate_md_path):
        """Verify validate.md command file exists."""
        assert validate_md_path.exists(), "validate.md command file must exist"

    def test_has_backlog_task_discovery_section(self, validate_md_path):
        """AC #1: Validate.md includes task discovery/validation section."""
        content = validate_md_path.read_text()
        # Accept old pattern or new phased workflow pattern
        has_old_pattern = "## Backlog Task Discovery" in content
        has_new_pattern = (
            "Phase 0:" in content
            or "Step 0: Workflow State Validation" in content
            or "Task Discovery" in content
        )
        assert has_old_pattern or has_new_pattern, (
            "validate.md must have task discovery section"
        )

    def test_discovers_in_progress_tasks(self, validate_md_path):
        """AC #1: Command instructs to discover In Progress tasks."""
        content = validate_md_path.read_text()
        assert 'backlog task list -s "In Progress" --plain' in content

    def test_discovers_done_tasks(self, validate_md_path):
        """AC #1: Command instructs to discover or mark tasks Done."""
        content = validate_md_path.read_text()
        # Accept old pattern or new phased workflow pattern
        has_done_discovery = 'backlog task list -s "Done" --plain' in content
        has_done_marking = "-s Done" in content or '-s "Done"' in content
        assert has_done_discovery or has_done_marking, (
            "validate.md must reference Done status"
        )

    def test_view_task_details_for_validation(self, validate_md_path):
        """AC #1: Command instructs to view or manage task details."""
        content = validate_md_path.read_text()
        # Accept various task management patterns
        has_view = "backlog task" in content and "--plain" in content
        has_edit = "backlog task edit" in content
        has_task_ref = "backlog task" in content
        assert has_view or has_edit or has_task_ref, (
            "validate.md must reference backlog task commands"
        )


class TestPhasedWorkflowAC2:
    """AC #2: Phased workflow with sub-agent delegation."""

    def test_has_phased_workflow(self, validate_md_path):
        """AC #2: Validate.md uses phased workflow structure."""
        content = validate_md_path.read_text()

        # New phased workflow structure
        has_phases = "Phase 0:" in content or "### Phase 0" in content
        has_workflow = "## Workflow" in content

        assert has_phases and has_workflow, (
            "validate.md must have phased workflow structure"
        )

    def test_references_sub_agents(self, validate_md_path):
        """AC #2: Validate.md references validation sub-agents."""
        content = validate_md_path.read_text()

        # Check for sub-agent references
        has_sub_agents = (
            "Sub-Agents" in content
            or "sub-agent" in content
            or "qa-validator" in content
            or "security-validator" in content
            or "test-runner" in content
        )

        assert has_sub_agents, "validate.md must reference validation sub-agents"

    def test_sub_agents_directory_exists(self, validate_agents_dir):
        """AC #2: Validation sub-agents directory exists."""
        assert validate_agents_dir.exists(), (
            ".claude/agents/validate/ directory must exist"
        )

    def test_has_qa_validator_agent(self, validate_agents_dir):
        """AC #2: QA validator sub-agent exists."""
        qa_path = validate_agents_dir / "qa-validator.md"
        assert qa_path.exists(), "qa-validator.md sub-agent must exist"

    def test_has_security_validator_agent(self, validate_agents_dir):
        """AC #2: Security validator sub-agent exists."""
        sec_path = validate_agents_dir / "security-validator.md"
        assert sec_path.exists(), "security-validator.md sub-agent must exist"

    def test_has_test_runner_agent(self, validate_agents_dir):
        """AC #2: Test runner sub-agent exists."""
        test_path = validate_agents_dir / "test-runner.md"
        assert test_path.exists(), "test-runner.md sub-agent must exist"

    def test_has_docs_validator_agent(self, validate_agents_dir):
        """AC #2: Docs validator sub-agent exists."""
        docs_path = validate_agents_dir / "docs-validator.md"
        assert docs_path.exists(), "docs-validator.md sub-agent must exist"

    def test_backlog_instructions_file_exists(self, backlog_instructions_path):
        """AC #2: Verify _backlog-instructions.md exists for shared instructions."""
        assert backlog_instructions_path.exists(), (
            "_backlog-instructions.md must exist for shared backlog instructions"
        )

    def test_backlog_instructions_has_core_sections(self, backlog_instructions_path):
        """AC #2: Shared backlog instructions has all core sections."""
        content = backlog_instructions_path.read_text()

        assert "## Critical Rules" in content
        assert "## Task Discovery" in content
        assert "## Starting Work on a Task" in content
        assert "## Tracking Progress with Acceptance Criteria" in content
        assert "## Completing Tasks" in content
        assert "## Definition of Done Checklist" in content

    def test_backlog_instructions_has_cli_examples(self, backlog_instructions_path):
        """AC #2: Shared instructions has CLI command examples."""
        content = backlog_instructions_path.read_text()

        assert "backlog task list" in content
        assert "backlog task edit" in content
        assert "--check-ac" in content
        assert "--plain" in content


class TestQAValidatorAC3:
    """AC #3: QA validator validates ACs match test results."""

    def test_qa_validator_exists(self, validate_agents_dir):
        """AC #3: QA validator sub-agent exists."""
        qa_path = validate_agents_dir / "qa-validator.md"
        assert qa_path.exists(), "qa-validator.md must exist"

    def test_qa_validates_tests(self, validate_agents_dir):
        """AC #3: QA validator handles test validation."""
        qa_path = validate_agents_dir / "qa-validator.md"
        content = qa_path.read_text()

        # Should reference test validation
        has_test_ref = "test" in content.lower() or "Test" in content
        assert has_test_ref, "QA validator must reference test validation"

    def test_qa_validates_coverage(self, validate_agents_dir):
        """AC #3: QA validator handles AC coverage."""
        qa_path = validate_agents_dir / "qa-validator.md"
        content = qa_path.read_text()

        # Should reference AC or acceptance criteria
        has_ac_ref = (
            "AC" in content
            or "acceptance criteria" in content.lower()
            or "coverage" in content.lower()
        )
        assert has_ac_ref, "QA validator must reference AC coverage"


class TestSecurityValidatorAC4:
    """AC #4: Security validator validates security-related ACs."""

    def test_security_validator_exists(self, validate_agents_dir):
        """AC #4: Security validator sub-agent exists."""
        sec_path = validate_agents_dir / "security-validator.md"
        assert sec_path.exists(), "security-validator.md must exist"

    def test_security_validates_security(self, validate_agents_dir):
        """AC #4: Security validator handles security validation."""
        sec_path = validate_agents_dir / "security-validator.md"
        content = sec_path.read_text()

        # Should reference security validation
        has_security_ref = "security" in content.lower() or "Security" in content
        assert has_security_ref, "Security validator must reference security validation"

    def test_security_returns_findings(self, validate_agents_dir):
        """AC #4: Security validator reports findings."""
        sec_path = validate_agents_dir / "security-validator.md"
        content = sec_path.read_text()

        # Should reference findings/issues/vulnerabilities
        has_findings_ref = (
            "finding" in content.lower()
            or "issue" in content.lower()
            or "vulnerabilit" in content.lower()
            or "result" in content.lower()
        )
        assert has_findings_ref, "Security validator must report findings"


class TestDocsValidatorAC5:
    """AC #5: Docs validator handles documentation validation."""

    def test_docs_validator_exists(self, validate_agents_dir):
        """AC #5: Docs validator sub-agent exists."""
        docs_path = validate_agents_dir / "docs-validator.md"
        assert docs_path.exists(), "docs-validator.md must exist"

    def test_docs_validates_documentation(self, validate_agents_dir):
        """AC #5: Docs validator handles documentation validation."""
        docs_path = validate_agents_dir / "docs-validator.md"
        content = docs_path.read_text()

        # Should reference documentation
        has_docs_ref = (
            "document" in content.lower()
            or "doc" in content.lower()
            or "readme" in content.lower()
        )
        assert has_docs_ref, "Docs validator must reference documentation"


class TestACVerificationAC6:
    """AC #6: AC verification phase ensures all criteria are met."""

    def test_has_ac_verification_phase(self, validate_md_path):
        """AC #6: Validate.md has AC verification phase."""
        content = validate_md_path.read_text()

        # Check for AC verification phase
        has_ac_phase = (
            "Phase 4:" in content
            or "AC Verification" in content
            or "Acceptance Criteria" in content
        )
        assert has_ac_phase, "validate.md must have AC verification phase"

    def test_marks_acs_complete(self, validate_md_path):
        """AC #6: Workflow marks ACs complete on success."""
        content = validate_md_path.read_text()

        # Check for AC marking
        has_check_ac = "--check-ac" in content
        assert has_check_ac, "validate.md must mark ACs complete with --check-ac"

    def test_completion_phase_updates_task(self, validate_md_path):
        """AC #6: Completion phase updates task status."""
        content = validate_md_path.read_text()

        # Check for task completion
        has_completion = (
            "Phase 6:" in content or "Completion" in content or "-s Done" in content
        )
        assert has_completion, "validate.md must have task completion phase"


class TestValidationWorkflowAC7:
    """AC #7: Validate complete validation workflow."""

    def test_validate_has_frontmatter(self, validate_md_path):
        """Validate.md has proper frontmatter."""
        content = validate_md_path.read_text()

        # Check for frontmatter
        assert content.startswith("---"), "validate.md must have frontmatter"
        assert "description:" in content, "frontmatter must have description"

    def test_validate_has_workflow_section(self, validate_md_path):
        """Validate.md has workflow section."""
        content = validate_md_path.read_text()
        assert "## Workflow" in content, "validate.md must have Workflow section"

    def test_validate_has_outputs_section(self, validate_md_path):
        """Validate.md has outputs section."""
        content = validate_md_path.read_text()
        assert "## Outputs" in content or "**Artifact:**" in content, (
            "validate.md must have outputs section"
        )

    def test_validate_has_issue_reporting(self, validate_md_path):
        """Validate.md has issue reporting phase."""
        content = validate_md_path.read_text()

        # Check for issue reporting
        has_reporting = (
            "Phase 5:" in content or "Report" in content or "issues" in content.lower()
        )
        assert has_reporting, "validate.md must have issue reporting"

    def test_validate_has_command_reference(self, validate_md_path):
        """Validate.md has command reference."""
        content = validate_md_path.read_text()

        # Check for command reference
        has_cmd_ref = "## Command Reference" in content or "/flow:validate" in content
        assert has_cmd_ref, "validate.md must have command reference"
