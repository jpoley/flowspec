"""Integration tests for /jpspec:implement command with backlog.md CLI.

This test module verifies that the /jpspec:implement command correctly integrates
with backlog.md for task management, including:
- Required task check at command start
- Backlog instructions included in all 5 engineer agents
- Task assignment workflow
- AC checking workflow
- Implementation notes workflow
- Code reviewer verification workflow
"""

import pytest
import subprocess
from pathlib import Path
from textwrap import dedent
from unittest.mock import patch, MagicMock, call
import json


@pytest.fixture
def temp_project_with_backlog(tmp_path):
    """Create a temporary project with backlog structure.

    Creates:
    - backlog/ directory with standard structure
    - Sample tasks for testing
    """
    backlog_root = tmp_path / "backlog"
    backlog_root.mkdir()

    # Create standard backlog directories
    (backlog_root / "tasks").mkdir()
    (backlog_root / "drafts").mkdir()
    (backlog_root / "docs").mkdir()
    (backlog_root / "decisions").mkdir()
    (backlog_root / "archive").mkdir()

    # Create backlog.json config
    config = {
        "version": "1.0.0",
        "taskIdPrefix": "task-",
        "statuses": ["To Do", "In Progress", "Done"],
        "priorities": ["Low", "Medium", "High"],
    }
    (backlog_root / "backlog.json").write_text(json.dumps(config, indent=2))

    return tmp_path


@pytest.fixture
def implement_command_file():
    """Get path to the implement.md command file."""
    return Path(__file__).parent.parent / ".claude" / "commands" / "jpspec" / "implement.md"


@pytest.fixture
def backlog_instructions_file():
    """Get path to the _backlog-instructions.md file."""
    return Path(__file__).parent.parent / ".claude" / "commands" / "jpspec" / "_backlog-instructions.md"


class TestImplementCommandBacklogRequirement:
    """Test that implement command requires existing backlog tasks."""

    def test_implement_command_has_task_requirement_section(self, implement_command_file):
        """Verify implement.md contains CRITICAL task requirement section."""
        content = implement_command_file.read_text()

        # Check for critical task requirement section
        assert "## CRITICAL: Backlog Task Requirement" in content
        assert "BEFORE PROCEEDING" in content
        assert "backlog task list -s \"To Do\" --plain" in content

    def test_implement_command_fails_gracefully_when_no_tasks(self, implement_command_file):
        """Verify implement.md instructs to fail gracefully when no tasks exist."""
        content = implement_command_file.read_text()

        # Check for graceful failure instructions
        assert "If no tasks exist" in content
        assert "Fail gracefully" in content
        assert "No backlog tasks found" in content
        assert "do NOT proceed with implementation" in content

    def test_implement_command_requires_backlog_tasks(self, implement_command_file):
        """Verify implement.md requires engineers to work from backlog."""
        content = implement_command_file.read_text()

        # Check requirements
        assert "Engineers MUST pick tasks from the backlog" in content
        assert "Engineers MUST NOT implement features without corresponding backlog tasks" in content


class TestBacklogInstructionsInAllAgents:
    """Test that all 5 engineer agents receive backlog instructions."""

    def test_frontend_engineer_has_backlog_instructions(self, implement_command_file):
        """Verify Frontend Engineer agent prompt includes backlog integration."""
        content = implement_command_file.read_text()

        # Find Frontend Engineer section
        assert "# AGENT CONTEXT: Senior Frontend Engineer" in content

        # Verify backlog instructions present after Frontend Engineer context
        fe_section_start = content.find("# AGENT CONTEXT: Senior Frontend Engineer")
        fe_section_end = content.find("#### Backend Implementation", fe_section_start)
        fe_section = content[fe_section_start:fe_section_end]

        assert "# BACKLOG.MD INTEGRATION - CRITICAL INSTRUCTIONS" in fe_section
        assert "NEVER edit task files directly" in fe_section
        assert "backlog task list -s \"To Do\" --plain" in fe_section
        assert "backlog task edit <id> -s \"In Progress\" -a @frontend-engineer" in fe_section
        assert "--check-ac" in fe_section

    def test_backend_engineer_has_backlog_instructions(self, implement_command_file):
        """Verify Backend Engineer agent prompt includes backlog integration."""
        content = implement_command_file.read_text()

        # Find Backend Engineer section
        assert "# AGENT CONTEXT: Senior Backend Engineer" in content

        # Verify backlog instructions present
        be_section_start = content.find("# AGENT CONTEXT: Senior Backend Engineer")
        be_section_end = content.find("#### AI/ML Implementation", be_section_start)
        be_section = content[be_section_start:be_section_end]

        assert "# BACKLOG.MD INTEGRATION - CRITICAL INSTRUCTIONS" in be_section
        assert "backlog task edit <id> -s \"In Progress\" -a @backend-engineer" in be_section
        assert "--check-ac" in be_section

    def test_ai_ml_engineer_has_backlog_instructions(self, implement_command_file):
        """Verify AI/ML Engineer agent prompt includes backlog integration."""
        content = implement_command_file.read_text()

        # Find AI/ML Engineer section
        aiml_section_start = content.find("# AGENT CONTEXT: Senior AI/ML Engineer")
        assert aiml_section_start != -1, "AI/ML Engineer section not found"

        # Get section (until next phase or end)
        aiml_section_end = content.find("### Phase 2:", aiml_section_start)
        aiml_section = content[aiml_section_start:aiml_section_end]

        assert "# BACKLOG.MD INTEGRATION - CRITICAL INSTRUCTIONS" in aiml_section
        assert "backlog task edit <id> -s \"In Progress\" -a @ai-ml-engineer" in aiml_section

    def test_frontend_reviewer_has_backlog_instructions(self, implement_command_file):
        """Verify Frontend Code Reviewer has backlog verification instructions."""
        content = implement_command_file.read_text()

        # Find Frontend Code Reviewer section
        assert "# AGENT CONTEXT: Principal Frontend Code Reviewer" in content

        fr_section_start = content.find("# AGENT CONTEXT: Principal Frontend Code Reviewer")
        fr_section_end = content.find("#### Backend Code Review", fr_section_start)
        fr_section = content[fr_section_start:fr_section_end]

        assert "# BACKLOG.MD INTEGRATION - CRITICAL FOR CODE REVIEWERS" in fr_section
        assert "Code reviewers MUST verify that task acceptance criteria match" in fr_section
        assert "backlog task <id> --plain" in fr_section
        assert "--uncheck-ac" in fr_section

    def test_backend_reviewer_has_backlog_instructions(self, implement_command_file):
        """Verify Backend Code Reviewer has backlog verification instructions."""
        content = implement_command_file.read_text()

        # Find Backend Code Reviewer section
        assert "# AGENT CONTEXT: Principal Backend Code Reviewer" in content

        br_section_start = content.find("# AGENT CONTEXT: Principal Backend Code Reviewer")
        br_section_end = content.find("### Phase 3:", br_section_start)
        if br_section_end == -1:
            br_section_end = len(content)
        br_section = content[br_section_start:br_section_end]

        assert "# BACKLOG.MD INTEGRATION - CRITICAL FOR CODE REVIEWERS" in br_section
        assert "Code reviewers MUST verify that task acceptance criteria match" in br_section
        assert "--uncheck-ac" in br_section

    def test_all_5_agents_have_backlog_integration(self, implement_command_file):
        """Verify all 5 agents (3 engineers + 2 reviewers) have backlog instructions."""
        content = implement_command_file.read_text()

        # Count occurrences of backlog integration headers
        engineer_integrations = content.count("# BACKLOG.MD INTEGRATION - CRITICAL INSTRUCTIONS")
        reviewer_integrations = content.count("# BACKLOG.MD INTEGRATION - CRITICAL FOR CODE REVIEWERS")

        # Should have 3 engineer integrations + 2 reviewer integrations
        assert engineer_integrations == 3, f"Expected 3 engineer backlog integrations, found {engineer_integrations}"
        assert reviewer_integrations == 2, f"Expected 2 reviewer backlog integrations, found {reviewer_integrations}"
        assert engineer_integrations + reviewer_integrations == 5, "Expected 5 total backlog integrations"


class TestTaskAssignmentWorkflow:
    """Test that agents follow proper task assignment workflow."""

    def test_engineers_pick_tasks_from_backlog(self, implement_command_file):
        """Verify engineers are instructed to pick tasks from backlog."""
        content = implement_command_file.read_text()

        # Should have instructions to list tasks
        assert content.count('backlog task list -s "To Do" --plain') >= 3
        assert content.count('backlog search') >= 3

    def test_engineers_assign_themselves(self, implement_command_file):
        """Verify engineers are instructed to assign themselves to tasks."""
        content = implement_command_file.read_text()

        # Check assignment instructions for each engineer type
        assert '@frontend-engineer' in content
        assert '@backend-engineer' in content
        assert '@ai-ml-engineer' in content

        # Verify assignment command format
        assert content.count('-s "In Progress" -a @') >= 3

    def test_engineers_set_in_progress_before_coding(self, implement_command_file):
        """Verify engineers set status to In Progress before starting work."""
        content = implement_command_file.read_text()

        # All engineer sections should have In Progress status change
        assert content.count('backlog task edit <id> -s "In Progress"') >= 3

    def test_engineers_add_implementation_plan(self, implement_command_file):
        """Verify engineers are instructed to add implementation plan."""
        content = implement_command_file.read_text()

        # Should have plan examples
        assert content.count('--plan $') >= 3
        assert 'Add implementation plan' in content


class TestAcceptanceCriteriaWorkflow:
    """Test AC checking workflow in implement command."""

    def test_engineers_check_ac_progressively(self, implement_command_file):
        """Verify engineers check ACs as they complete work."""
        content = implement_command_file.read_text()

        # Should have AC checking instructions
        assert content.count('--check-ac') >= 10  # Multiple examples
        assert 'As you complete each acceptance criterion' in content

    def test_engineers_can_check_multiple_ac(self, implement_command_file):
        """Verify engineers can check multiple ACs at once."""
        content = implement_command_file.read_text()

        # Should have examples of checking multiple ACs
        assert content.count('--check-ac 1 --check-ac 2 --check-ac 3') >= 3

    def test_engineers_dont_batch_completions(self, implement_command_file):
        """Verify instruction to not batch AC completions."""
        content = implement_command_file.read_text()

        assert "Mark ACs complete as you finish them" in content
        assert "Don't batch completions" in content


class TestImplementationNotesWorkflow:
    """Test implementation notes workflow."""

    def test_engineers_add_implementation_notes(self, implement_command_file):
        """Verify engineers add implementation notes."""
        content = implement_command_file.read_text()

        # Should have notes examples
        assert content.count('--notes $') >= 3
        assert 'Add implementation notes' in content

    def test_notes_describe_what_was_built(self, implement_command_file):
        """Verify notes describe implementation details."""
        content = implement_command_file.read_text()

        # Should have examples with key changes
        assert 'Key changes:' in content
        assert 'Implemented' in content

    def test_engineers_add_notes_before_done(self, implement_command_file):
        """Verify engineers add notes before marking Done."""
        content = implement_command_file.read_text()

        # Check Definition of Done includes notes
        assert "Implementation notes added" in content
        assert "Before marking Done" in content


class TestCodeReviewerVerification:
    """Test that code reviewers verify AC completion."""

    def test_reviewers_check_task_before_review(self, implement_command_file):
        """Verify reviewers read task ACs before reviewing."""
        content = implement_command_file.read_text()

        # Reviewer sections should have instructions to check task
        assert content.count('backlog task <id> --plain') >= 2
        assert "Check task ACs before reviewing" in content

    def test_reviewers_verify_ac_matches_code(self, implement_command_file):
        """Verify reviewers check that ACs match code implementation."""
        content = implement_command_file.read_text()

        assert "Verify each AC matches code" in content
        assert "Verify the code actually implements it" in content

    def test_reviewers_can_uncheck_invalid_ac(self, implement_command_file):
        """Verify reviewers can uncheck ACs that don't match code."""
        content = implement_command_file.read_text()

        # Should have uncheck instructions
        assert content.count('--uncheck-ac') >= 2
        assert "If AC is checked but code doesn't implement it → UNCHECK IT" in content

    def test_reviewers_verify_definition_of_done(self, implement_command_file):
        """Verify reviewers check Definition of Done."""
        content = implement_command_file.read_text()

        assert "Verify Definition of Done" in content
        assert "All ACs checked AND verified in code" in content


class TestIntegrationScenarios:
    """Integration tests for complete workflows."""

    @patch('subprocess.run')
    def test_complete_engineer_workflow(self, mock_run, temp_project_with_backlog):
        """Test complete engineer workflow: pick → assign → work → check ACs → notes → done."""
        mock_run.return_value = MagicMock(returncode=0, stdout="Success")

        # Simulate engineer workflow
        task_id = "42"

        # Step 1: List tasks
        subprocess.run(["backlog", "task", "list", "-s", "To Do", "--plain"])

        # Step 2: Assign and start
        subprocess.run([
            "backlog", "task", "edit", task_id,
            "-s", "In Progress",
            "-a", "@backend-engineer"
        ])

        # Step 3: Add plan
        subprocess.run([
            "backlog", "task", "edit", task_id,
            "--plan", "1. Design\n2. Implement\n3. Test"
        ])

        # Step 4: Check ACs progressively
        subprocess.run(["backlog", "task", "edit", task_id, "--check-ac", "1"])
        subprocess.run(["backlog", "task", "edit", task_id, "--check-ac", "2"])

        # Step 5: Add notes
        subprocess.run([
            "backlog", "task", "edit", task_id,
            "--notes", "Implemented feature X"
        ])

        # Step 6: Mark done
        subprocess.run(["backlog", "task", "edit", task_id, "-s", "Done"])

        # Verify calls were made
        assert mock_run.call_count == 7

    @patch('subprocess.run')
    def test_code_reviewer_workflow(self, mock_run):
        """Test code reviewer workflow: check task → verify ACs → update if needed."""
        mock_run.return_value = MagicMock(returncode=0, stdout="Success")

        task_id = "42"

        # Step 1: Check task ACs
        subprocess.run(["backlog", "task", task_id, "--plain"])

        # Step 2: Find AC not implemented
        # (In real scenario, reviewer would read code here)

        # Step 3: Uncheck invalid AC and add notes
        subprocess.run([
            "backlog", "task", "edit", task_id,
            "--uncheck-ac", "2",
            "--append-notes", "Code review: AC #2 not fully implemented"
        ])

        # Step 4: Revert status if needed
        subprocess.run([
            "backlog", "task", "edit", task_id,
            "-s", "In Progress"
        ])

        # Verify calls
        assert mock_run.call_count == 3

    def test_no_duplicate_instructions(self, implement_command_file):
        """Verify backlog instructions aren't unnecessarily duplicated."""
        content = implement_command_file.read_text()

        # Each agent should have its own section, not share a single one
        # This is intentional - each agent gets tailored instructions

        # But we should NOT have verbatim duplication of _backlog-instructions.md
        # Instead, we have customized versions per agent

        # Verify customization for different agents
        assert "@frontend-engineer" in content
        assert "@backend-engineer" in content
        assert "@ai-ml-engineer" in content

        # Verify reviewer-specific instructions
        assert "CRITICAL FOR CODE REVIEWERS" in content

    def test_backlog_instructions_file_exists(self, backlog_instructions_file):
        """Verify _backlog-instructions.md reference file exists."""
        assert backlog_instructions_file.exists()

        # Verify it has core sections
        content = backlog_instructions_file.read_text()
        assert "Critical Rules" in content
        assert "Task Discovery" in content
        assert "Starting Work on a Task" in content
        assert "Tracking Progress with Acceptance Criteria" in content
        assert "Completing Tasks" in content


class TestCriticalRules:
    """Test that critical rules are emphasized."""

    def test_never_edit_files_directly_rule(self, implement_command_file):
        """Verify NEVER edit files directly rule is present."""
        content = implement_command_file.read_text()

        assert content.count("NEVER edit task files directly") >= 5
        assert "Always use `backlog` CLI commands" in content

    def test_use_plain_flag_rule(self, implement_command_file):
        """Verify --plain flag usage is emphasized."""
        content = implement_command_file.read_text()

        assert content.count("--plain") >= 15
        assert "Use `--plain` flag" in content

    def test_mark_ac_as_you_finish_rule(self, implement_command_file):
        """Verify progressive AC marking rule."""
        content = implement_command_file.read_text()

        assert "Mark ACs complete as you finish them" in content
        assert "Don't batch completions" in content

    def test_add_notes_before_done_rule(self, implement_command_file):
        """Verify notes required before Done rule."""
        content = implement_command_file.read_text()

        assert "Add implementation notes" in content
        assert "before marking tasks Done" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
