"""Unit tests for janitor module.

Tests cover:
- State reading (timestamps, pending cleanup)
- State writing (recording runs, updating pending)
- Audit logging
- Cleanup report generation
"""

import json
from datetime import datetime, timezone
from pathlib import Path


from specify_cli.janitor import (
    JanitorState,
    PendingCleanup,
    add_pending_branch,
    clear_pending_cleanup,
    read_janitor_state,
    read_pending_cleanup,
    record_janitor_run,
    update_pending_cleanup,
    write_audit_log,
)
from specify_cli.janitor.reader import (
    PendingBranch,
    PendingWorktree,
    format_janitor_warning,
    read_janitor_timestamp,
)
from specify_cli.janitor.state import ensure_state_dir, generate_cleanup_report


class TestReadJanitorTimestamp:
    """Tests for read_janitor_timestamp function."""

    def test_read_existing_timestamp(self, tmp_path: Path) -> None:
        """Test reading an existing timestamp file."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        timestamp_file = state_dir / "janitor-last-run"
        timestamp_file.write_text("2025-12-07T21:30:00+00:00")

        result = read_janitor_timestamp(state_dir)

        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 7

    def test_read_missing_file(self, tmp_path: Path) -> None:
        """Test reading when file doesn't exist."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)

        result = read_janitor_timestamp(state_dir)

        assert result is None

    def test_read_invalid_timestamp(self, tmp_path: Path) -> None:
        """Test handling invalid timestamp content."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        timestamp_file = state_dir / "janitor-last-run"
        timestamp_file.write_text("not-a-timestamp")

        result = read_janitor_timestamp(state_dir)

        assert result is None

    def test_read_zulu_timestamp(self, tmp_path: Path) -> None:
        """Test reading Z suffix timestamp."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        timestamp_file = state_dir / "janitor-last-run"
        timestamp_file.write_text("2025-12-07T21:30:00Z")

        result = read_janitor_timestamp(state_dir)

        assert result is not None
        assert result.tzinfo is not None


class TestReadPendingCleanup:
    """Tests for read_pending_cleanup function."""

    def test_read_empty_file(self, tmp_path: Path) -> None:
        """Test reading empty pending cleanup."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        cleanup_file = state_dir / "pending-cleanup.json"
        cleanup_file.write_text("{}")

        result = read_pending_cleanup(state_dir)

        assert result.merged_branches == []
        assert result.orphaned_worktrees == []
        assert result.non_compliant_branches == {}

    def test_read_with_branches(self, tmp_path: Path) -> None:
        """Test reading pending cleanup with branches."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        cleanup_file = state_dir / "pending-cleanup.json"
        cleanup_file.write_text(
            json.dumps(
                {
                    "merged_branches": [
                        {"name": "feature/old", "reason": "upstream gone"},
                        {"name": "fix/done", "reason": "merged"},
                    ]
                }
            )
        )

        result = read_pending_cleanup(state_dir)

        assert len(result.merged_branches) == 2
        assert result.merged_branches[0].name == "feature/old"
        assert result.merged_branches[0].reason == "upstream gone"

    def test_read_with_worktrees(self, tmp_path: Path) -> None:
        """Test reading pending cleanup with worktrees."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        cleanup_file = state_dir / "pending-cleanup.json"
        cleanup_file.write_text(
            json.dumps(
                {
                    "orphaned_worktrees": [
                        {"path": "/tmp/worktree1"},
                        {"path": "/tmp/worktree2"},
                    ]
                }
            )
        )

        result = read_pending_cleanup(state_dir)

        assert len(result.orphaned_worktrees) == 2
        assert result.orphaned_worktrees[0].path == "/tmp/worktree1"

    def test_read_missing_file(self, tmp_path: Path) -> None:
        """Test reading when file doesn't exist."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)

        result = read_pending_cleanup(state_dir)

        assert result.merged_branches == []
        assert not result.has_pending

    def test_read_invalid_json(self, tmp_path: Path) -> None:
        """Test handling invalid JSON."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        cleanup_file = state_dir / "pending-cleanup.json"
        cleanup_file.write_text("not valid json")

        result = read_pending_cleanup(state_dir)

        assert result.merged_branches == []


class TestPendingCleanup:
    """Tests for PendingCleanup dataclass."""

    def test_total_pending(self) -> None:
        """Test total_pending property."""
        pending = PendingCleanup(
            merged_branches=[
                PendingBranch("a", "gone"),
                PendingBranch("b", "merged"),
            ],
            orphaned_worktrees=[PendingWorktree("/tmp/wt")],
        )

        assert pending.total_pending == 3

    def test_has_pending_true(self) -> None:
        """Test has_pending when items exist."""
        pending = PendingCleanup(
            merged_branches=[PendingBranch("a", "gone")],
        )

        assert pending.has_pending is True

    def test_has_pending_false(self) -> None:
        """Test has_pending when empty."""
        pending = PendingCleanup()

        assert pending.has_pending is False

    def test_has_pending_with_non_compliant(self) -> None:
        """Test has_pending with only non-compliant branches."""
        pending = PendingCleanup(
            non_compliant_branches={"bad-branch": "doesn't match pattern"},
        )

        assert pending.has_pending is True

    def test_summary(self) -> None:
        """Test summary property."""
        pending = PendingCleanup(
            merged_branches=[PendingBranch("a", "gone")],
            orphaned_worktrees=[PendingWorktree("/tmp/wt")],
        )

        summary = pending.summary
        assert "1 branch(es) to prune" in summary
        assert "1 worktree(s) to clean" in summary


class TestJanitorState:
    """Tests for JanitorState dataclass."""

    def test_needs_run_true(self) -> None:
        """Test needs_run when pending items exist."""
        state = JanitorState(
            pending=PendingCleanup(
                merged_branches=[PendingBranch("a", "gone")],
            )
        )

        assert state.needs_run is True

    def test_needs_run_false(self) -> None:
        """Test needs_run when no pending items."""
        state = JanitorState(pending=PendingCleanup())

        assert state.needs_run is False

    def test_hours_since_last_run(self) -> None:
        """Test hours_since_last_run calculation."""
        # 2 hours ago
        two_hours_ago = datetime.now(timezone.utc).replace(microsecond=0)
        state = JanitorState(last_run=two_hours_ago)

        hours = state.hours_since_last_run
        assert hours is not None
        assert hours >= 0  # Should be very close to 0

    def test_hours_since_last_run_never_run(self) -> None:
        """Test hours_since_last_run when never run."""
        state = JanitorState()

        assert state.hours_since_last_run is None


class TestRecordJanitorRun:
    """Tests for record_janitor_run function."""

    def test_records_timestamp(self, tmp_path: Path) -> None:
        """Test recording current timestamp."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)

        result = record_janitor_run(state_dir)

        assert result is not None
        timestamp_file = state_dir / "janitor-last-run"
        assert timestamp_file.exists()
        content = timestamp_file.read_text()
        assert "T" in content  # ISO format

    def test_records_custom_timestamp(self, tmp_path: Path) -> None:
        """Test recording custom timestamp."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        custom_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        result = record_janitor_run(state_dir, timestamp=custom_time)

        assert result == custom_time
        content = (state_dir / "janitor-last-run").read_text()
        assert "2025-01-01" in content


class TestUpdatePendingCleanup:
    """Tests for update_pending_cleanup function."""

    def test_writes_pending_items(self, tmp_path: Path) -> None:
        """Test writing pending cleanup items."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)

        pending = PendingCleanup(
            merged_branches=[PendingBranch("feature/old", "gone")],
            orphaned_worktrees=[PendingWorktree("/tmp/wt")],
            non_compliant_branches={"bad": "reason"},
        )

        update_pending_cleanup(state_dir, pending)

        cleanup_file = state_dir / "pending-cleanup.json"
        assert cleanup_file.exists()
        data = json.loads(cleanup_file.read_text())
        assert len(data["merged_branches"]) == 1
        assert len(data["orphaned_worktrees"]) == 1
        assert "bad" in data["non_compliant_branches"]


class TestAddPendingBranch:
    """Tests for add_pending_branch function."""

    def test_adds_branch(self, tmp_path: Path) -> None:
        """Test adding a pending branch."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        (state_dir / "pending-cleanup.json").write_text("{}")

        add_pending_branch(state_dir, "feature/old", "upstream gone")

        pending = read_pending_cleanup(state_dir)
        assert len(pending.merged_branches) == 1
        assert pending.merged_branches[0].name == "feature/old"

    def test_no_duplicate(self, tmp_path: Path) -> None:
        """Test that duplicates are not added."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)
        (state_dir / "pending-cleanup.json").write_text("{}")

        add_pending_branch(state_dir, "feature/old", "gone")
        add_pending_branch(state_dir, "feature/old", "gone")

        pending = read_pending_cleanup(state_dir)
        assert len(pending.merged_branches) == 1


class TestClearPendingCleanup:
    """Tests for clear_pending_cleanup function."""

    def test_clears_all(self, tmp_path: Path) -> None:
        """Test clearing all pending items."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)

        pending = PendingCleanup(
            merged_branches=[PendingBranch("a", "gone")],
            orphaned_worktrees=[PendingWorktree("/tmp/wt")],
        )
        update_pending_cleanup(state_dir, pending)

        clear_pending_cleanup(state_dir)

        result = read_pending_cleanup(state_dir)
        assert result.merged_branches == []
        assert result.orphaned_worktrees == []

    def test_clears_selectively(self, tmp_path: Path) -> None:
        """Test clearing only branches."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)

        pending = PendingCleanup(
            merged_branches=[PendingBranch("a", "gone")],
            orphaned_worktrees=[PendingWorktree("/tmp/wt")],
        )
        update_pending_cleanup(state_dir, pending)

        clear_pending_cleanup(state_dir, clear_branches=True, clear_worktrees=False)

        result = read_pending_cleanup(state_dir)
        assert result.merged_branches == []
        assert len(result.orphaned_worktrees) == 1


class TestWriteAuditLog:
    """Tests for write_audit_log function."""

    def test_creates_log_file(self, tmp_path: Path) -> None:
        """Test creating audit log file."""
        write_audit_log(tmp_path, "Pruned 3 branches")

        audit_file = tmp_path / ".specify" / "audit.log"
        assert audit_file.exists()
        content = audit_file.read_text()
        assert "JANITOR" in content
        assert "Pruned 3 branches" in content

    def test_appends_to_existing(self, tmp_path: Path) -> None:
        """Test appending to existing log."""
        audit_file = tmp_path / ".specify" / "audit.log"
        audit_file.parent.mkdir(parents=True)
        audit_file.write_text("[existing entry]\n")

        write_audit_log(tmp_path, "New action")

        content = audit_file.read_text()
        assert "[existing entry]" in content
        assert "New action" in content

    def test_includes_details(self, tmp_path: Path) -> None:
        """Test including optional details."""
        write_audit_log(tmp_path, "Pruned branches", details="feature/a, fix/b")

        content = (tmp_path / ".specify" / "audit.log").read_text()
        assert "feature/a, fix/b" in content


class TestGenerateCleanupReport:
    """Tests for generate_cleanup_report function."""

    def test_report_with_all_sections(self) -> None:
        """Test report with all sections populated."""
        report = generate_cleanup_report(
            pruned_branches=[("feature/old", "gone"), ("fix/done", "merged")],
            cleaned_worktrees=["/tmp/wt1"],
            non_compliant={"bad-name": "no prefix"},
            protected_skipped=["main", "develop"],
        )

        assert "Branches Pruned: 2" in report
        assert "feature/old" in report
        assert "Worktrees Cleaned: 1" in report
        assert "Non-Compliant Branches: 1" in report
        assert "Protected Branches Skipped: 2" in report

    def test_report_empty(self) -> None:
        """Test report when nothing to clean."""
        report = generate_cleanup_report(
            pruned_branches=[],
            cleaned_worktrees=[],
            non_compliant={},
            protected_skipped=[],
        )

        assert "Branches Pruned: 0" in report
        assert "(none)" in report


class TestFormatJanitorWarning:
    """Tests for format_janitor_warning function."""

    def test_no_warning_when_clean(self) -> None:
        """Test no warning when nothing pending."""
        state = JanitorState(pending=PendingCleanup())

        result = format_janitor_warning(state)

        assert result is None

    def test_warning_with_branches(self) -> None:
        """Test warning with pending branches."""
        state = JanitorState(
            pending=PendingCleanup(
                merged_branches=[PendingBranch("a", "gone")],
            )
        )

        result = format_janitor_warning(state)

        assert result is not None
        assert "cleanup pending" in result
        assert "1 merged branch" in result

    def test_warning_with_all_types(self) -> None:
        """Test warning with all pending types."""
        state = JanitorState(
            pending=PendingCleanup(
                merged_branches=[PendingBranch("a", "gone")],
                orphaned_worktrees=[PendingWorktree("/tmp/wt")],
                non_compliant_branches={"bad": "reason"},
            )
        )

        result = format_janitor_warning(state)

        assert result is not None
        assert "branch(es) to prune" in result
        assert "worktree(s)" in result
        assert "naming issues" in result


class TestEnsureStateDir:
    """Tests for ensure_state_dir function."""

    def test_creates_directory(self, tmp_path: Path) -> None:
        """Test creating state directory."""
        result = ensure_state_dir(tmp_path)

        assert result == tmp_path / ".specify" / "state"
        assert result.exists()
        assert result.is_dir()

    def test_idempotent(self, tmp_path: Path) -> None:
        """Test that function is idempotent."""
        ensure_state_dir(tmp_path)
        result = ensure_state_dir(tmp_path)

        assert result.exists()


class TestReadJanitorState:
    """Tests for read_janitor_state function."""

    def test_reads_complete_state(self, tmp_path: Path) -> None:
        """Test reading complete janitor state."""
        state_dir = tmp_path / ".specify" / "state"
        state_dir.mkdir(parents=True)

        # Write timestamp
        (state_dir / "janitor-last-run").write_text("2025-12-07T21:30:00Z")

        # Write pending cleanup
        (state_dir / "pending-cleanup.json").write_text(
            json.dumps(
                {
                    "merged_branches": [{"name": "old", "reason": "gone"}],
                }
            )
        )

        result = read_janitor_state(state_dir)

        assert result.last_run is not None
        assert len(result.pending.merged_branches) == 1
        assert result.state_dir == state_dir
