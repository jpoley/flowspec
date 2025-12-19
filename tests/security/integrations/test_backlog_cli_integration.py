"""Tests for backlog CLI integration with task creation."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from flowspec_cli.security.integrations.backlog import (
    FindingTask,
    create_backlog_tasks_via_cli,
    create_tasks_from_findings,
)
from flowspec_cli.security.models import Finding, Location, Severity


@pytest.fixture
def sample_findings():
    """Create sample findings for testing."""
    return [
        Finding(
            id="SEMGREP-001",
            scanner="semgrep",
            severity=Severity.CRITICAL,
            title="SQL Injection",
            description="SQL injection vulnerability",
            location=Location(file=Path("src/db.py"), line_start=42, line_end=45),
            cwe_id="CWE-89",
        ),
        Finding(
            id="SEMGREP-002",
            scanner="semgrep",
            severity=Severity.HIGH,
            title="XSS Vulnerability",
            description="Cross-site scripting",
            location=Location(file=Path("src/web.py"), line_start=100, line_end=102),
            cwe_id="CWE-79",
        ),
    ]


@pytest.fixture
def sample_task():
    """Create a sample FindingTask."""
    return FindingTask(
        title="Fix CRITICAL: SQL Injection",
        description="SQL injection in db.py",
        severity="critical",
        cwe_id="CWE-89",
        location="src/db.py:42",
        finding_id="SEMGREP-001",
        priority="high",
        labels=["security", "critical", "cwe89", "semgrep"],
        acceptance_criteria=[
            "Fix vulnerability at src/db.py:42",
            "Add security test",
            "Re-scan shows resolved",
        ],
    )


class TestCreateBacklogTasksViaCli:
    """Tests for create_backlog_tasks_via_cli function."""

    @patch("subprocess.run")
    def test_create_task_success(self, mock_run, sample_task):
        """Test successful task creation via CLI."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        tasks = [sample_task]
        created, failed = create_backlog_tasks_via_cli(tasks)

        assert created == 1
        assert failed == 0
        assert mock_run.called

        # Verify command structure
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "backlog"
        assert call_args[1] == "task"
        assert call_args[2] == "create"
        assert "Fix CRITICAL: SQL Injection" in call_args

    @patch("subprocess.run")
    def test_create_multiple_tasks(self, mock_run, sample_task):
        """Test creating multiple tasks."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        task2 = FindingTask(
            title="Fix HIGH: XSS",
            description="XSS in web.py",
            severity="high",
            cwe_id="CWE-79",
            location="src/web.py:100",
            finding_id="SEMGREP-002",
            priority="high",
            labels=["security", "high"],
            acceptance_criteria=["Fix XSS"],
        )

        tasks = [sample_task, task2]
        created, failed = create_backlog_tasks_via_cli(tasks)

        assert created == 2
        assert failed == 0
        assert mock_run.call_count == 2

    @patch("subprocess.run")
    def test_dry_run_mode(self, mock_run, sample_task, capsys):
        """Test dry run mode doesn't actually create tasks."""
        tasks = [sample_task]
        created, failed = create_backlog_tasks_via_cli(tasks, dry_run=True)

        assert created == 1
        assert failed == 0
        assert not mock_run.called  # Should NOT call subprocess in dry run

        captured = capsys.readouterr()
        assert "[DRY RUN]" in captured.out
        assert "Fix CRITICAL: SQL Injection" in captured.out

    @patch("subprocess.run")
    def test_task_creation_failure(self, mock_run, sample_task):
        """Test handling of task creation failure."""
        mock_run.side_effect = Exception("Backlog CLI error")

        tasks = [sample_task]

        # Should not raise exception, but track failure
        created, failed = create_backlog_tasks_via_cli(tasks)

        assert created == 0
        assert failed == 1

    @patch("subprocess.run")
    def test_command_includes_all_fields(self, mock_run, sample_task):
        """Test that CLI command includes all task fields."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        tasks = [sample_task]
        create_backlog_tasks_via_cli(tasks)

        call_args = mock_run.call_args[0][0]

        # Check for description
        assert "--description" in call_args

        # Check for priority
        assert "--priority" in call_args
        assert "high" in call_args

        # Check for labels
        assert "--label" in call_args
        assert any("security" in str(arg) for arg in call_args)

        # Check for acceptance criteria
        assert "--ac" in call_args

    @patch("subprocess.run")
    def test_labels_added_correctly(self, mock_run, sample_task):
        """Test that labels are added correctly."""
        mock_run.return_value = MagicMock(returncode=0)

        sample_task.labels = ["security", "critical", "backend"]
        tasks = [sample_task]

        create_backlog_tasks_via_cli(tasks)

        call_args = mock_run.call_args[0][0]
        # Each label should have --label flag
        label_count = call_args.count("--label")
        assert label_count == 3

    @patch("subprocess.run")
    def test_acceptance_criteria_added_correctly(self, mock_run, sample_task):
        """Test that acceptance criteria are added correctly."""
        mock_run.return_value = MagicMock(returncode=0)

        sample_task.acceptance_criteria = ["AC 1", "AC 2", "AC 3"]
        tasks = [sample_task]

        create_backlog_tasks_via_cli(tasks)

        call_args = mock_run.call_args[0][0]
        # Each AC should have --ac flag
        ac_count = call_args.count("--ac")
        assert ac_count == 3


class TestIntegrationWithFindings:
    """Integration tests with actual findings."""

    def test_end_to_end_task_creation(self, sample_findings):
        """Test complete flow from findings to tasks."""
        # Create tasks from findings
        tasks = create_tasks_from_findings(sample_findings)

        assert len(tasks) == 2
        assert all(isinstance(t, FindingTask) for t in tasks)

        # Verify critical finding comes first
        assert tasks[0].severity == "critical"
        assert tasks[0].priority == "high"
        assert "security" in tasks[0].labels

    def test_grouped_task_creation(self, sample_findings):
        """Test grouped task creation from findings."""
        # Add another SQL injection to test grouping
        sample_findings.append(
            Finding(
                id="SEMGREP-003",
                scanner="semgrep",
                severity=Severity.HIGH,
                title="SQL Injection in API",
                description="Another SQL injection",
                location=Location(file=Path("src/api.py"), line_start=50, line_end=52),
                cwe_id="CWE-89",
            )
        )

        tasks = create_tasks_from_findings(sample_findings, group_by_cwe=True)

        # Should have fewer tasks due to grouping
        assert len(tasks) == 2  # CWE-89 (2 findings) and CWE-79 (1 finding)

        # Find CWE-89 group
        sql_task = next(t for t in tasks if "CWE-89" in str(t.cwe_id))
        assert "(2 occurrences)" in sql_task.title

    @patch("subprocess.run")
    def test_severity_filtering_for_task_creation(self, mock_run, sample_findings):
        """Test creating tasks only for specific severities."""
        mock_run.return_value = MagicMock(returncode=0)

        # Filter to only critical
        critical_findings = [
            f for f in sample_findings if f.severity == Severity.CRITICAL
        ]

        tasks = create_tasks_from_findings(critical_findings)
        created, failed = create_backlog_tasks_via_cli(tasks)

        assert created == 1
        assert failed == 0
        # Only one task should be created (critical finding)


class TestTaskFormatting:
    """Tests for task formatting and structure."""

    def test_task_description_includes_severity(self, sample_task):
        """Test task description includes severity."""
        assert (
            "CRITICAL" in sample_task.description or "critical" in sample_task.severity
        )

    def test_task_description_includes_location(self, sample_task):
        """Test task description includes file location."""
        assert "src/db.py" in sample_task.location

    def test_task_description_includes_cwe(self, sample_task):
        """Test task description includes CWE reference."""
        assert sample_task.cwe_id == "CWE-89"

    def test_task_has_security_label(self, sample_task):
        """Test all tasks have security label."""
        assert "security" in sample_task.labels

    def test_task_priority_matches_severity(self, sample_task):
        """Test task priority is appropriate for severity."""
        # Critical severity should map to high priority
        assert sample_task.severity == "critical"
        assert sample_task.priority == "high"
