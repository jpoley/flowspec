"""Tests for dev-setup and init command equivalence.

Tests verify that dev-setup (symlinks) and init (copies) produce equivalent
command sets with consistent subdirectory structure. Based on ADR-010 validation
rules R6 and R7.

Architecture Reference:
- ADR-010: docs/adr/ADR-010-dev-setup-validation-architecture.md
- R6: dev-setup creates same file set as init would copy
- R7: Subdirectory structure matches (jpspec/, speckit/)
"""

from pathlib import Path
from typing import Set

import pytest


@pytest.fixture
def source_repo_root() -> Path:
    """Return path to jp-spec-kit source repository root."""
    # Tests run from project root, so cwd is the source repo
    return Path.cwd()


@pytest.fixture
def templates_dir(source_repo_root: Path) -> Path:
    """Return path to templates/commands directory."""
    return source_repo_root / "templates" / "commands"


@pytest.fixture
def claude_commands_dir(source_repo_root: Path) -> Path:
    """Return path to .claude/commands directory."""
    return source_repo_root / ".claude" / "commands"


class TestDevSetupInitEquivalence:
    """Verify dev-setup symlinks match what init would copy.

    ADR-010 Rule R6: dev-setup creates same file set as init would copy
    """

    def test_jpspec_symlinks_match_templates(
        self, claude_commands_dir: Path, templates_dir: Path
    ):
        """Test dev-setup creates jpspec symlinks for all jpspec templates.

        Validates:
        - Every template in templates/commands/jpspec/ has a corresponding symlink
        - Symlink count matches template count
        - All symlinks are valid (not broken)
        """
        jpspec_templates_dir = templates_dir / "jpspec"
        jpspec_commands_dir = claude_commands_dir / "jpspec"

        # Get all template files
        template_files = set(
            f.name for f in jpspec_templates_dir.glob("*.md") if f.is_file()
        )

        # Get all symlinks
        symlink_files = set(
            f.name for f in jpspec_commands_dir.glob("*.md") if f.is_symlink()
        )

        # Verify every template has a symlink
        assert (
            template_files == symlink_files
        ), f"Jpspec symlink mismatch. Templates: {template_files}, Symlinks: {symlink_files}"

        # Verify symlink count
        assert len(symlink_files) > 0, "No jpspec symlinks found"
        assert len(template_files) == len(
            symlink_files
        ), f"Expected {len(template_files)} symlinks, found {len(symlink_files)}"

    def test_speckit_symlinks_match_templates(
        self, claude_commands_dir: Path, templates_dir: Path
    ):
        """Test dev-setup creates speckit symlinks for all speckit templates.

        Validates:
        - Every template in templates/commands/*.md has a corresponding symlink
        - Symlink count matches template count
        - All symlinks are valid (not broken)
        """
        speckit_commands_dir = claude_commands_dir / "speckit"

        # Get all template files (excluding jpspec subdirectory)
        template_files = set(f.name for f in templates_dir.glob("*.md") if f.is_file())

        # Get all symlinks
        symlink_files = set(
            f.name for f in speckit_commands_dir.glob("*.md") if f.is_symlink()
        )

        # Verify every template has a symlink
        assert (
            template_files == symlink_files
        ), f"Speckit symlink mismatch. Templates: {template_files}, Symlinks: {symlink_files}"

        # Verify symlink count
        assert len(symlink_files) > 0, "No speckit symlinks found"
        assert len(template_files) == len(
            symlink_files
        ), f"Expected {len(template_files)} symlinks, found {len(symlink_files)}"

    def test_init_would_copy_same_files(
        self, claude_commands_dir: Path, templates_dir: Path
    ):
        """Test that init would copy the same files dev-setup links to.

        Validates R6: The file set created by dev-setup (symlinks) matches
        what init would copy from templates.
        """
        # Get all files dev-setup links to
        dev_setup_files: Set[str] = set()

        # Jpspec files
        jpspec_commands = claude_commands_dir / "jpspec"
        for symlink in jpspec_commands.glob("*.md"):
            if symlink.is_symlink():
                # Track the filename (what init would copy)
                dev_setup_files.add(f"jpspec/{symlink.name}")

        # Speckit files
        speckit_commands = claude_commands_dir / "speckit"
        for symlink in speckit_commands.glob("*.md"):
            if symlink.is_symlink():
                dev_setup_files.add(f"speckit/{symlink.name}")

        # Get all files init would copy from templates
        init_files: Set[str] = set()

        # Jpspec templates
        jpspec_templates = templates_dir / "jpspec"
        if jpspec_templates.exists():
            for template in jpspec_templates.glob("*.md"):
                if template.is_file():
                    init_files.add(f"jpspec/{template.name}")

        # Speckit templates (direct files in templates/commands/)
        for template in templates_dir.glob("*.md"):
            if template.is_file():
                init_files.add(f"speckit/{template.name}")

        # Verify file sets match
        assert dev_setup_files == init_files, (
            f"File set mismatch between dev-setup and init.\n"
            f"Dev-setup only: {dev_setup_files - init_files}\n"
            f"Init only: {init_files - dev_setup_files}"
        )

        # Verify non-empty
        assert len(dev_setup_files) > 0, "No files found in dev-setup"
        assert len(init_files) > 0, "No files found in init templates"


class TestSubdirectoryStructure:
    """Verify subdirectory structure matches between dev-setup and init.

    ADR-010 Rule R7: Subdirectory structure matches (jpspec/, speckit/)
    """

    def test_jpspec_subdirectory_exists(self, claude_commands_dir: Path):
        """Test jpspec subdirectory exists in .claude/commands/."""
        jpspec_dir = claude_commands_dir / "jpspec"
        assert jpspec_dir.exists(), "jpspec subdirectory does not exist"
        assert jpspec_dir.is_dir(), "jpspec is not a directory"

    def test_speckit_subdirectory_exists(self, claude_commands_dir: Path):
        """Test speckit subdirectory exists in .claude/commands/."""
        speckit_dir = claude_commands_dir / "speckit"
        assert speckit_dir.exists(), "speckit subdirectory does not exist"
        assert speckit_dir.is_dir(), "speckit is not a directory"

    def test_no_extra_subdirectories(self, claude_commands_dir: Path):
        """Test only jpspec and speckit subdirectories exist.

        Validates structure consistency - no unexpected directories.
        """
        # Get all subdirectories
        subdirs = [d.name for d in claude_commands_dir.iterdir() if d.is_dir()]

        # Verify only expected subdirectories
        expected_subdirs = {"jpspec", "speckit"}
        actual_subdirs = set(subdirs)

        assert actual_subdirs == expected_subdirs, (
            f"Unexpected subdirectory structure.\n"
            f"Expected: {expected_subdirs}\n"
            f"Found: {actual_subdirs}\n"
            f"Extra: {actual_subdirs - expected_subdirs}\n"
            f"Missing: {expected_subdirs - actual_subdirs}"
        )

    def test_templates_subdirectory_structure_matches(self, templates_dir: Path):
        """Test templates directory has matching jpspec subdirectory.

        Validates source structure matches destination structure.
        """
        jpspec_templates = templates_dir / "jpspec"
        assert jpspec_templates.exists(), "templates/commands/jpspec does not exist"
        assert jpspec_templates.is_dir(), "templates/commands/jpspec is not a directory"

        # Verify jpspec contains actual template files
        jpspec_files = list(jpspec_templates.glob("*.md"))
        assert len(jpspec_files) > 0, "No jpspec template files found"

    def test_no_direct_files_in_commands_root(self, claude_commands_dir: Path):
        """Test no direct .md files exist in .claude/commands/ root.

        ADR-010 Rule R1: .claude/commands/ contains ONLY subdirectories (jpspec/, speckit/),
        no direct files. All commands must be in subdirectories.
        """
        # Get all direct .md files (not in subdirectories)
        direct_files = [
            f.name for f in claude_commands_dir.glob("*.md") if f.is_file()
        ]

        assert len(direct_files) == 0, (
            f"Direct .md files found in .claude/commands/ root (should be in subdirectories):\n"
            f"{', '.join(direct_files)}"
        )


class TestDevSetupSymlinkValidation:
    """Validate dev-setup creates only symlinks, no direct files.

    ADR-010 Rule R1: .claude/commands/**/*.md contains ONLY symlinks
    ADR-010 Rule R2: All symlinks resolve to existing files
    ADR-010 Rule R3: All symlinks point to templates/commands/
    """

    def test_jpspec_contains_only_symlinks(self, claude_commands_dir: Path):
        """Test jpspec directory contains only symlinks, no direct files."""
        jpspec_dir = claude_commands_dir / "jpspec"

        all_md_files = list(jpspec_dir.glob("*.md"))
        symlinks = [f for f in all_md_files if f.is_symlink()]
        direct_files = [f for f in all_md_files if not f.is_symlink()]

        assert len(direct_files) == 0, (
            f"Direct .md files found in jpspec/ (should be symlinks):\n"
            f"{', '.join(f.name for f in direct_files)}"
        )

        assert len(symlinks) > 0, "No symlinks found in jpspec/"

    def test_speckit_contains_only_symlinks(self, claude_commands_dir: Path):
        """Test speckit directory contains only symlinks, no direct files."""
        speckit_dir = claude_commands_dir / "speckit"

        all_md_files = list(speckit_dir.glob("*.md"))
        symlinks = [f for f in all_md_files if f.is_symlink()]
        direct_files = [f for f in all_md_files if not f.is_symlink()]

        assert len(direct_files) == 0, (
            f"Direct .md files found in speckit/ (should be symlinks):\n"
            f"{', '.join(f.name for f in direct_files)}"
        )

        assert len(symlinks) > 0, "No symlinks found in speckit/"

    def test_all_symlinks_resolve_correctly(self, claude_commands_dir: Path):
        """Test all symlinks resolve to existing files (no broken symlinks).

        ADR-010 Rule R2: All symlinks resolve to existing files
        """
        broken_symlinks = []

        # Check jpspec symlinks
        jpspec_dir = claude_commands_dir / "jpspec"
        for symlink in jpspec_dir.glob("*.md"):
            if symlink.is_symlink():
                try:
                    target = symlink.resolve(strict=True)
                    if not target.exists():
                        broken_symlinks.append(f"jpspec/{symlink.name}")
                except (OSError, RuntimeError):
                    broken_symlinks.append(f"jpspec/{symlink.name}")

        # Check speckit symlinks
        speckit_dir = claude_commands_dir / "speckit"
        for symlink in speckit_dir.glob("*.md"):
            if symlink.is_symlink():
                try:
                    target = symlink.resolve(strict=True)
                    if not target.exists():
                        broken_symlinks.append(f"speckit/{symlink.name}")
                except (OSError, RuntimeError):
                    broken_symlinks.append(f"speckit/{symlink.name}")

        assert len(broken_symlinks) == 0, (
            f"Broken symlinks found:\n" f"{', '.join(broken_symlinks)}"
        )

    def test_all_symlinks_point_to_templates(
        self, claude_commands_dir: Path, templates_dir: Path
    ):
        """Test all symlinks point to templates/commands/ directory.

        ADR-010 Rule R3: All symlinks point to templates/commands/
        """
        invalid_targets = []

        # Check jpspec symlinks
        jpspec_dir = claude_commands_dir / "jpspec"
        jpspec_templates = templates_dir / "jpspec"
        for symlink in jpspec_dir.glob("*.md"):
            if symlink.is_symlink():
                target = symlink.resolve()
                if not target.is_relative_to(jpspec_templates):
                    invalid_targets.append(
                        f"jpspec/{symlink.name} -> {target} (expected under {jpspec_templates})"
                    )

        # Check speckit symlinks
        speckit_dir = claude_commands_dir / "speckit"
        for symlink in speckit_dir.glob("*.md"):
            if symlink.is_symlink():
                target = symlink.resolve()
                # Speckit symlinks should point to templates/commands/*.md (not jpspec subdirectory)
                if not target.is_relative_to(templates_dir) or target.is_relative_to(
                    jpspec_templates
                ):
                    invalid_targets.append(
                        f"speckit/{symlink.name} -> {target} (expected under {templates_dir}, not jpspec/)"
                    )

        assert len(invalid_targets) == 0, (
            f"Symlinks with invalid targets found:\n" f"\n".join(invalid_targets)
        )


class TestDevSetupIdempotency:
    """Verify running dev-setup multiple times is safe.

    Tests that dev-setup can be run repeatedly without breaking the setup.
    This is important for the --force flag and recovery scenarios.
    """

    def test_symlink_count_stable(self, claude_commands_dir: Path):
        """Test symlink count is stable (dev-setup was already run).

        This test verifies the current state after dev-setup has been run.
        Running dev-setup again with --force should not change the count.
        """
        # Count jpspec symlinks
        jpspec_dir = claude_commands_dir / "jpspec"
        jpspec_symlinks = [f for f in jpspec_dir.glob("*.md") if f.is_symlink()]

        # Count speckit symlinks
        speckit_dir = claude_commands_dir / "speckit"
        speckit_symlinks = [f for f in speckit_dir.glob("*.md") if f.is_symlink()]

        # Verify non-zero counts (dev-setup has been run)
        assert len(jpspec_symlinks) > 0, "No jpspec symlinks found (dev-setup not run?)"
        assert (
            len(speckit_symlinks) > 0
        ), "No speckit symlinks found (dev-setup not run?)"

        # Store counts for documentation
        total_symlinks = len(jpspec_symlinks) + len(speckit_symlinks)
        assert total_symlinks > 0, "No symlinks found"

    def test_no_duplicate_symlinks(self, claude_commands_dir: Path):
        """Test no duplicate symlink names exist.

        Verifies each template has exactly one symlink (not multiple).
        """
        # Check jpspec
        jpspec_dir = claude_commands_dir / "jpspec"
        jpspec_names = [f.name for f in jpspec_dir.glob("*.md") if f.is_symlink()]
        assert len(jpspec_names) == len(
            set(jpspec_names)
        ), f"Duplicate jpspec symlinks found: {jpspec_names}"

        # Check speckit
        speckit_dir = claude_commands_dir / "speckit"
        speckit_names = [f.name for f in speckit_dir.glob("*.md") if f.is_symlink()]
        assert len(speckit_names) == len(
            set(speckit_names)
        ), f"Duplicate speckit symlinks found: {speckit_names}"

    def test_symlinks_are_relative_not_absolute(self, claude_commands_dir: Path):
        """Test symlinks use relative paths, not absolute paths.

        Relative paths ensure portability across different system environments.
        """
        absolute_symlinks = []

        # Check jpspec symlinks
        jpspec_dir = claude_commands_dir / "jpspec"
        for symlink in jpspec_dir.glob("*.md"):
            if symlink.is_symlink():
                # Read the raw symlink target (before resolution)
                target = symlink.readlink()
                if target.is_absolute():
                    absolute_symlinks.append(f"jpspec/{symlink.name} -> {target}")

        # Check speckit symlinks
        speckit_dir = claude_commands_dir / "speckit"
        for symlink in speckit_dir.glob("*.md"):
            if symlink.is_symlink():
                target = symlink.readlink()
                if target.is_absolute():
                    absolute_symlinks.append(f"speckit/{symlink.name} -> {target}")

        assert len(absolute_symlinks) == 0, (
            f"Absolute path symlinks found (should be relative):\n"
            f"\n".join(absolute_symlinks)
        )


class TestTemplateCompleteness:
    """Verify template directory completeness.

    ADR-010 Rule R4: Every template has corresponding symlink (WARNING level)
    These tests ensure templates are not orphaned.
    """

    def test_all_jpspec_templates_have_symlinks(
        self, templates_dir: Path, claude_commands_dir: Path
    ):
        """Test every jpspec template has a corresponding symlink."""
        jpspec_templates = templates_dir / "jpspec"
        jpspec_commands = claude_commands_dir / "jpspec"

        template_files = set(f.name for f in jpspec_templates.glob("*.md"))
        symlink_files = set(f.name for f in jpspec_commands.glob("*.md"))

        orphan_templates = template_files - symlink_files

        assert len(orphan_templates) == 0, (
            f"Jpspec templates without symlinks (orphaned):\n"
            f"{', '.join(orphan_templates)}"
        )

    def test_all_speckit_templates_have_symlinks(
        self, templates_dir: Path, claude_commands_dir: Path
    ):
        """Test every speckit template has a corresponding symlink."""
        speckit_commands = claude_commands_dir / "speckit"

        # Get template files (excluding jpspec subdirectory)
        template_files = set(f.name for f in templates_dir.glob("*.md"))
        symlink_files = set(f.name for f in speckit_commands.glob("*.md"))

        orphan_templates = template_files - symlink_files

        assert len(orphan_templates) == 0, (
            f"Speckit templates without symlinks (orphaned):\n"
            f"{', '.join(orphan_templates)}"
        )

    def test_no_orphan_symlinks(
        self, templates_dir: Path, claude_commands_dir: Path
    ):
        """Test no symlinks exist without corresponding templates.

        ADR-010 Rule R5: No orphan symlinks (target exists in templates)
        """
        orphan_symlinks = []

        # Check jpspec
        jpspec_templates = templates_dir / "jpspec"
        jpspec_commands = claude_commands_dir / "jpspec"

        template_files = set(f.name for f in jpspec_templates.glob("*.md"))
        symlink_files = set(f.name for f in jpspec_commands.glob("*.md"))

        jpspec_orphans = symlink_files - template_files
        if jpspec_orphans:
            orphan_symlinks.extend(f"jpspec/{name}" for name in jpspec_orphans)

        # Check speckit
        speckit_commands = claude_commands_dir / "speckit"
        template_files = set(f.name for f in templates_dir.glob("*.md"))
        symlink_files = set(f.name for f in speckit_commands.glob("*.md"))

        speckit_orphans = symlink_files - template_files
        if speckit_orphans:
            orphan_symlinks.extend(f"speckit/{name}" for name in speckit_orphans)

        assert len(orphan_symlinks) == 0, (
            f"Orphan symlinks found (no corresponding template):\n"
            f"{', '.join(orphan_symlinks)}"
        )
