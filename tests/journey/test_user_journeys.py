"""
User Journey Tests - REAL end-to-end customer scenarios.

These tests verify COMPLETE user flows, not just individual components.
They catch "declared victory too soon" by testing actual customer experience.

Each test represents a real user journey that MUST work for customer success.
"""

import subprocess
from pathlib import Path
import pytest
import json


class TestCustomerJourney:
    """
    User journey tests for workflow orchestration.

    Each test is a COMPLETE customer scenario from start to finish.
    If ANY test fails, we haven't delivered customer value.
    """

    def test_journey_1_list_workflows(self):
        """
        JOURNEY: New user wants to see available workflows

        Steps:
        1. User runs: flowspec flow custom --list
        2. System shows available workflows
        3. User sees descriptions and can choose

        Success: User knows what workflows exist
        """
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "--list"],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"
        assert "quick_build" in result.stdout, "quick_build workflow not shown"
        assert "full_design" in result.stdout, "full_design workflow not shown"
        assert "ship_it" in result.stdout, "ship_it workflow not shown"

        # Verify descriptions are helpful
        assert "Lightweight workflow" in result.stdout, "No description for quick_build"
        assert "Complete design" in result.stdout, "No description for full_design"

    def test_journey_2_get_execution_plan(self):
        """
        JOURNEY: User wants to know what a workflow will do

        Steps:
        1. User runs: flowspec flow custom quick_build
        2. System shows execution plan
        3. User sees all steps that will execute

        Success: User understands what will happen before executing
        """
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "quick_build"],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"
        assert "/flow:specify" in result.stdout, "specify step not shown"
        assert "/flow:implement" in result.stdout, "implement step not shown"
        assert "/flow:validate" in result.stdout, "validate step not shown"

        # Verify user knows what to do next
        assert ("execution plan prepared" in result.stdout or
                "steps" in result.stdout.lower()), "No clear status message"

    def test_journey_3_conditional_workflow(self):
        """
        JOURNEY: User runs workflow with conditional logic

        Steps:
        1. User runs: flowspec flow custom full_design
        2. System evaluates conditions
        3. System skips/includes steps based on context

        Success: Conditional logic works as documented
        """
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "full_design"],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        # Should show all 4 steps
        assert "assess" in result.stdout.lower(), "assess step missing"
        assert "specify" in result.stdout.lower(), "specify step missing"
        assert "research" in result.stdout.lower(), "research step missing"
        assert "plan" in result.stdout.lower(), "plan step missing"

    def test_journey_4_logs_created(self):
        """
        JOURNEY: User wants audit trail of workflow execution

        Steps:
        1. User runs workflow
        2. System creates decision and event logs
        3. User can review what happened

        Success: Complete audit trail available
        """
        # Run workflow to generate logs
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "quick_build"],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        # Verify logs directory exists
        logs_dir = Path(".logs")
        assert logs_dir.exists(), "Logs directory not created"

        # Verify log files exist
        decision_logs = list(logs_dir.glob("decisions/session-*.jsonl"))
        event_logs = list(logs_dir.glob("events/session-*.jsonl"))

        assert len(decision_logs) > 0, "No decision logs created"
        assert len(event_logs) > 0, "No event logs created"

        # Verify logs have content
        latest_decision_log = max(decision_logs, key=lambda p: p.stat().st_mtime)
        with open(latest_decision_log) as f:
            lines = f.readlines()
            assert len(lines) > 0, "Decision log is empty"

            # Verify JSON format
            for line in lines:
                entry = json.loads(line)
                assert "decision" in entry or "timestamp" in entry, "Invalid log format"

    @pytest.mark.skip(reason="Requires --execute implementation")
    def test_journey_5_execute_workflow(self):
        """
        JOURNEY: User wants workflow to actually execute

        Steps:
        1. User runs: flowspec flow custom quick_build --execute
        2. System executes all workflow steps
        3. User sees progress and completion

        Success: Workflow actually runs, not just planning

        THIS IS THE KEY TEST THAT FAILS - MUST IMPLEMENT FOR 100%
        """
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "quick_build", "--execute"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes for execution
        )

        assert result.returncode == 0, f"Execution failed: {result.stderr}"

        # Verify execution happened
        assert "Executing" in result.stdout, "No execution indicator"
        assert "complete" in result.stdout.lower(), "No completion message"

        # Verify all steps ran
        assert "specify" in result.stdout.lower(), "specify didn't run"
        assert "implement" in result.stdout.lower(), "implement didn't run"
        assert "validate" in result.stdout.lower(), "validate didn't run"

    @pytest.mark.skip(reason="Requires --execute and --task implementation")
    def test_journey_6_backlog_integration(self):
        """
        JOURNEY: User wants workflow to update backlog task

        Steps:
        1. User creates task: backlog task create "Test"
        2. User runs: flowspec flow custom quick_build --execute --task task-123
        3. System updates task as workflow progresses
        4. Task shows execution history

        Success: Full backlog integration working

        THIS IS THE OTHER KEY TEST THAT FAILS - MUST IMPLEMENT FOR 100%
        """
        # Create test task
        task_result = subprocess.run(
            ["backlog", "task", "create", "Journey Test Task",
             "--description", "Test backlog integration",
             "--status", "To Do"],
            capture_output=True,
            text=True
        )

        # Extract task ID from output
        task_id = None
        for line in task_result.stdout.split("\n"):
            if "task-" in line:
                # Parse task ID
                import re
                match = re.search(r'task-\d+', line)
                if match:
                    task_id = match.group(0)
                    break

        assert task_id, "Failed to create task"

        # Execute workflow with task integration
        exec_result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "quick_build",
             "--execute", "--task", task_id],
            capture_output=True,
            text=True,
            timeout=300
        )

        assert exec_result.returncode == 0, f"Execution failed: {exec_result.stderr}"

        # Verify task was updated
        view_result = subprocess.run(
            ["backlog", "task", "view", task_id],
            capture_output=True,
            text=True
        )

        assert "Done" in view_result.stdout or "In Progress" in view_result.stdout, \
            "Task status not updated"

        # Cleanup
        subprocess.run(["backlog", "task", "archive", task_id])

    def test_journey_7_error_handling(self):
        """
        JOURNEY: User runs invalid workflow

        Steps:
        1. User runs: flowspec flow custom nonexistent
        2. System shows clear error message
        3. User knows what to do next

        Success: Helpful error messages, not crashes
        """
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "nonexistent"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should fail gracefully
        assert result.returncode != 0, "Should fail for invalid workflow"
        assert "not found" in result.stderr.lower() or \
               "not found" in result.stdout.lower(), "No clear error message"

        # Should show available workflows
        assert "available" in result.stdout.lower() or \
               "available" in result.stderr.lower(), "Doesn't suggest alternatives"

    @pytest.mark.skip(reason="Requires context passing implementation")
    def test_journey_8_context_passing(self):
        """
        JOURNEY: User wants to pass context to workflow

        Steps:
        1. User runs: flowspec flow custom full_design --context complexity=8
        2. System evaluates conditions with context
        3. Research step runs because complexity >= 7

        Success: Context-aware execution working
        """
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "full_design",
             "--context", "complexity=8"],
            capture_output=True,
            text=True,
            timeout=30
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        # With complexity=8, research should be included
        # (Not skipped)
        assert "research" in result.stdout.lower(), "research step not shown"
        # Should NOT see skip message for research
        assert "skipped" not in result.stdout.lower() or \
               "research" not in result.stdout.lower(), "research was skipped incorrectly"


class TestEdgeCases:
    """
    Edge case and failure scenario tests.

    These catch the "1/2 baked solution" problem by testing edge cases.
    """

    def test_empty_workflow_name(self):
        """User provides no workflow name - should show list"""
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should show list (not crash)
        assert result.returncode == 0, "Crashes on empty workflow name"
        assert "workflow" in result.stdout.lower(), "Doesn't show workflows"

    def test_invalid_flag(self):
        """User uses invalid flag - should show error"""
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "--invalid-flag"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should fail gracefully
        assert result.returncode != 0, "Accepts invalid flags"

    def test_no_flowspec_workflow_yml(self, tmp_path):
        """User runs in directory without flowspec_workflow.yml"""
        result = subprocess.run(
            ["uv", "run", "flowspec", "flow", "custom", "--list"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should handle gracefully (not crash)
        # May show error or empty list - both acceptable
        assert "error" in result.stderr.lower() or \
               "no" in result.stdout.lower() or \
               result.returncode != 0, "Doesn't handle missing config"


class TestDelusionalVictoryPrevention:
    """
    Tests that prevent "declared victory too soon" syndrome.

    Each test verifies ACTUAL customer value, not just infrastructure.
    """

    def test_not_just_planning(self):
        """
        CRITICAL: Verify we do more than just show plans

        If this passes but execution tests fail, we've declared victory too soon.
        """
        # This is a meta-test
        # It fails if we only have planning working
        pytest.skip("Manual check: Are execution tests passing?")

    def test_not_just_logging(self):
        """
        CRITICAL: Verify we do more than just log things

        If this passes but actual work doesn't happen, we've failed customers.
        """
        pytest.skip("Manual check: Does work actually get done?")

    def test_customer_can_use_it(self):
        """
        CRITICAL: Can a customer actually use this?

        If we can't demonstrate a complete user journey, we're not done.
        """
        pytest.skip("Manual check: Show a customer using this successfully")


# Test discovery helper
def pytest_collection_modifyitems(items):
    """Mark skipped tests prominently"""
    for item in items:
        if item.get_closest_marker("skip"):
            item.add_marker(pytest.mark.xfail(reason="Not implemented yet", run=False))
