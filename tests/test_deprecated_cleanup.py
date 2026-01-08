"""Tests for deprecated file and directory cleanup functionality.

Tests cover:
- Detection of deprecated directories (.specify/)
- Detection of deprecated files (_DEPRECATED_*.md)
- Backup creation before removal
- Dry run mode
- Cleanup result reporting
- Integration with upgrade-repo command
"""

from pathlib import Path

from flowspec_cli.deprecated import (
    DEPRECATED_DIRECTORIES,
    DEPRECATED_FILE_PATTERNS,
    DeprecatedCleanupResult,
    cleanup_deprecated_files,
    detect_deprecated_items,
)


class TestDeprecatedCleanupResult:
    """Tests for DeprecatedCleanupResult dataclass."""

    def test_empty_result_has_no_changes(self):
        """Empty result reports no changes."""
        result = DeprecatedCleanupResult()
        assert result.has_changes is False
        assert result.total_removed == 0

    def test_result_with_directories_has_changes(self):
        """Result with directories reports changes."""
        result = DeprecatedCleanupResult(directories_removed=[".specify"])
        assert result.has_changes is True
        assert result.total_removed == 1

    def test_result_with_files_has_changes(self):
        """Result with files reports changes."""
        result = DeprecatedCleanupResult(files_removed=["_DEPRECATED_foo.md"])
        assert result.has_changes is True
        assert result.total_removed == 1

    def test_result_total_removed_counts_both(self):
        """Total removed counts both directories and files."""
        result = DeprecatedCleanupResult(
            directories_removed=[".specify"],
            files_removed=["_DEPRECATED_a.md", "_DEPRECATED_b.md"],
        )
        assert result.total_removed == 3

    def test_summary_no_changes(self):
        """Summary for no changes."""
        result = DeprecatedCleanupResult()
        assert result.summary() == "no deprecated items found"

    def test_summary_directories_only(self):
        """Summary for directories only."""
        result = DeprecatedCleanupResult(directories_removed=[".specify"])
        assert "dirs: .specify" in result.summary()

    def test_summary_files_only(self):
        """Summary for files only."""
        result = DeprecatedCleanupResult(
            files_removed=["_DEPRECATED_a.md", "_DEPRECATED_b.md"]
        )
        assert "2 files" in result.summary()

    def test_summary_both(self):
        """Summary for both directories and files."""
        result = DeprecatedCleanupResult(
            directories_removed=[".specify"],
            files_removed=["_DEPRECATED_a.md"],
        )
        summary = result.summary()
        assert ".specify" in summary
        assert "1 files" in summary


class TestDeprecatedDirectoriesConstant:
    """Tests for DEPRECATED_DIRECTORIES constant."""

    def test_contains_specify(self):
        """.specify is a deprecated directory."""
        assert ".specify" in DEPRECATED_DIRECTORIES


class TestDeprecatedFilePatternsConstant:
    """Tests for DEPRECATED_FILE_PATTERNS constant."""

    def test_contains_deprecated_pattern(self):
        """_DEPRECATED_*.md pattern is included."""
        assert "_DEPRECATED_*.md" in DEPRECATED_FILE_PATTERNS


class TestDetectDeprecatedItems:
    """Tests for detect_deprecated_items function."""

    def test_detects_specify_directory(self, tmp_path: Path):
        """Detects .specify/ directory when present."""
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()

        dirs, files = detect_deprecated_items(tmp_path)

        assert len(dirs) == 1
        assert dirs[0] == specify_dir

    def test_no_deprecated_directory(self, tmp_path: Path):
        """Returns empty list when no deprecated directories exist."""
        dirs, files = detect_deprecated_items(tmp_path)
        assert len(dirs) == 0

    def test_detects_deprecated_files_in_claude_commands(self, tmp_path: Path):
        """Detects _DEPRECATED_*.md files in .claude/commands/."""
        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        deprecated_file = commands_dir / "_DEPRECATED_old-command.md"
        deprecated_file.write_text("# Deprecated")

        dirs, files = detect_deprecated_items(tmp_path)

        assert len(files) == 1
        assert files[0] == deprecated_file

    def test_detects_deprecated_files_in_github_copilot(self, tmp_path: Path):
        """Detects _DEPRECATED_*.md files in .github/copilot/commands/."""
        commands_dir = tmp_path / ".github" / "copilot" / "commands"
        commands_dir.mkdir(parents=True)
        deprecated_file = commands_dir / "_DEPRECATED_legacy.md"
        deprecated_file.write_text("# Deprecated")

        dirs, files = detect_deprecated_items(tmp_path)

        assert len(files) == 1
        assert files[0] == deprecated_file

    def test_detects_deprecated_files_in_cursor(self, tmp_path: Path):
        """Detects _DEPRECATED_*.md files in .cursor/commands/."""
        commands_dir = tmp_path / ".cursor" / "commands"
        commands_dir.mkdir(parents=True)
        deprecated_file = commands_dir / "_DEPRECATED_old.md"
        deprecated_file.write_text("# Deprecated")

        dirs, files = detect_deprecated_items(tmp_path)

        assert len(files) == 1
        assert files[0] == deprecated_file

    def test_detects_multiple_deprecated_files(self, tmp_path: Path):
        """Detects multiple _DEPRECATED_*.md files."""
        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "_DEPRECATED_a.md").write_text("# A")
        (commands_dir / "_DEPRECATED_b.md").write_text("# B")
        (commands_dir / "valid-command.md").write_text("# Valid")

        dirs, files = detect_deprecated_items(tmp_path)

        assert len(files) == 2
        filenames = [f.name for f in files]
        assert "_DEPRECATED_a.md" in filenames
        assert "_DEPRECATED_b.md" in filenames
        assert "valid-command.md" not in filenames

    def test_ignores_non_deprecated_files(self, tmp_path: Path):
        """Ignores files that don't match deprecated patterns."""
        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "commit.md").write_text("# Commit")
        (commands_dir / "review.md").write_text("# Review")

        dirs, files = detect_deprecated_items(tmp_path)

        assert len(files) == 0


class TestCleanupDeprecatedFiles:
    """Tests for cleanup_deprecated_files function."""

    def test_removes_specify_directory(self, tmp_path: Path):
        """Removes .specify/ directory and creates backup."""
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()
        (specify_dir / "config.yaml").write_text("config: true")

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        assert not specify_dir.exists()
        assert ".specify" in result.directories_removed
        assert ".specify" in result.directories_backed_up
        # Verify backup exists
        backup_path = result.directories_backed_up[".specify"]
        assert backup_path.exists()
        assert (backup_path / "config.yaml").exists()

    def test_removes_deprecated_files(self, tmp_path: Path):
        """Removes _DEPRECATED_*.md files and creates backup."""
        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        deprecated_file = commands_dir / "_DEPRECATED_old.md"
        deprecated_file.write_text("# Old Command")

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        assert not deprecated_file.exists()
        assert ".claude/commands/_DEPRECATED_old.md" in result.files_removed
        # Verify backup exists
        rel_path = ".claude/commands/_DEPRECATED_old.md"
        assert rel_path in result.files_backed_up

    def test_dry_run_does_not_remove(self, tmp_path: Path):
        """Dry run detects but does not remove items."""
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir, dry_run=True)

        # Directory still exists
        assert specify_dir.exists()
        # But result shows what would be removed
        assert ".specify" in result.directories_removed

    def test_no_deprecated_items(self, tmp_path: Path):
        """Returns empty result when no deprecated items exist."""
        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        assert not result.has_changes
        assert result.summary() == "no deprecated items found"

    def test_backup_dir_created_if_needed(self, tmp_path: Path):
        """Creates _deprecated subdirectory in backup dir."""
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        cleanup_deprecated_files(tmp_path, backup_dir)

        deprecated_backup = backup_dir / "_deprecated"
        assert deprecated_backup.exists()

    def test_handles_multiple_items(self, tmp_path: Path):
        """Handles multiple deprecated directories and files."""
        # Create .specify directory
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()

        # Create deprecated files
        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        (commands_dir / "_DEPRECATED_a.md").write_text("# A")
        (commands_dir / "_DEPRECATED_b.md").write_text("# B")

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        assert result.total_removed == 3
        assert len(result.directories_removed) == 1
        assert len(result.files_removed) == 2

    def test_preserves_file_content_in_backup(self, tmp_path: Path):
        """Backup preserves original file content."""
        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        deprecated_file = commands_dir / "_DEPRECATED_test.md"
        original_content = "# Original Content\n\nSome important stuff."
        deprecated_file.write_text(original_content)

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        rel_path = ".claude/commands/_DEPRECATED_test.md"
        backup_path = result.files_backed_up[rel_path]
        assert backup_path.read_text() == original_content

    def test_preserves_directory_structure_in_backup(self, tmp_path: Path):
        """Backup preserves directory structure with subdirectories."""
        specify_dir = tmp_path / ".specify"
        subdir = specify_dir / "templates" / "nested"
        subdir.mkdir(parents=True)
        (subdir / "file.txt").write_text("nested content")

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        backup_path = result.directories_backed_up[".specify"]
        nested_backup = backup_path / "templates" / "nested" / "file.txt"
        assert nested_backup.exists()
        assert nested_backup.read_text() == "nested content"


class TestCleanupErrorHandling:
    """Tests for error handling in cleanup operations."""

    def test_errors_added_to_result(self, tmp_path: Path, monkeypatch):
        """Errors during removal are captured in result."""
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        # Make the directory unremovable by patching shutil.rmtree
        import shutil

        original_rmtree = shutil.rmtree

        def failing_rmtree(path, *args, **kwargs):
            if ".specify" in str(path):
                raise OSError("Permission denied")
            return original_rmtree(path, *args, **kwargs)

        monkeypatch.setattr(shutil, "rmtree", failing_rmtree)

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        assert len(result.errors) == 1
        assert "Permission denied" in result.errors[0]
        # Directory should still exist since removal failed
        assert specify_dir.exists()

    def test_continues_after_single_error(self, tmp_path: Path, monkeypatch):
        """Continues processing after a single item fails."""
        # Create multiple deprecated items
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()

        commands_dir = tmp_path / ".claude" / "commands"
        commands_dir.mkdir(parents=True)
        deprecated_file = commands_dir / "_DEPRECATED_test.md"
        deprecated_file.write_text("content")

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        # Make only directory removal fail
        import shutil

        original_rmtree = shutil.rmtree

        def failing_rmtree(path, *args, **kwargs):
            if ".specify" in str(path):
                raise OSError("Permission denied")
            return original_rmtree(path, *args, **kwargs)

        monkeypatch.setattr(shutil, "rmtree", failing_rmtree)

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        # File should still be removed even though directory failed
        assert not deprecated_file.exists()
        assert len(result.files_removed) == 1
        assert len(result.errors) == 1


class TestDeprecatedGithubAgentPatterns:
    """Tests for deprecated .github/agents/ file patterns (ADR-001)."""

    def test_contains_hyphenated_flow_pattern(self):
        """flow-*.agent.md pattern is included for deprecation."""
        from flowspec_cli.deprecated import DEPRECATED_GITHUB_AGENT_PATTERNS

        assert "flow-*.agent.md" in DEPRECATED_GITHUB_AGENT_PATTERNS

    def test_detects_hyphenated_agent_files(self, tmp_path: Path):
        """Detects flow-*.agent.md files in .github/agents/."""
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)

        # Create deprecated hyphenated files
        (agents_dir / "flow-specify.agent.md").write_text("# Deprecated")
        (agents_dir / "flow-implement.agent.md").write_text("# Deprecated")
        (agents_dir / "flow-plan.agent.md").write_text("# Deprecated")

        # Create current dot-notation file (should NOT be detected)
        (agents_dir / "flow.specify.agent.md").write_text("# Current")

        dirs, files = detect_deprecated_items(tmp_path)

        assert len(files) == 3
        filenames = [f.name for f in files]
        assert "flow-specify.agent.md" in filenames
        assert "flow-implement.agent.md" in filenames
        assert "flow-plan.agent.md" in filenames
        assert "flow.specify.agent.md" not in filenames

    def test_removes_hyphenated_agent_files(self, tmp_path: Path):
        """Removes flow-*.agent.md files and creates backup."""
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        deprecated_file = agents_dir / "flow-specify.agent.md"
        deprecated_file.write_text("# Deprecated Agent")

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        assert not deprecated_file.exists()
        assert ".github/agents/flow-specify.agent.md" in result.files_removed

    def test_preserves_dot_notation_agent_files(self, tmp_path: Path):
        """Does NOT remove flow.*.agent.md files (current format)."""
        agents_dir = tmp_path / ".github" / "agents"
        agents_dir.mkdir(parents=True)
        current_file = agents_dir / "flow.specify.agent.md"
        current_file.write_text("# Current Agent")

        backup_dir = tmp_path / ".backup"
        backup_dir.mkdir()

        result = cleanup_deprecated_files(tmp_path, backup_dir)

        # File should still exist
        assert current_file.exists()
        # Should not be in removed list
        assert not result.has_changes
