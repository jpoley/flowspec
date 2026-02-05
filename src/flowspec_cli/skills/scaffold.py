"""Skill deployment for flowspec init and upgrade-repo.

This module provides skill directory copying functionality
that deploys skills from templates/skills/ to .claude/skills/
when users run `flowspec init`, and syncs skills during
`flowspec upgrade-repo`.
"""

from __future__ import annotations

import filecmp
import logging
import shutil
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SkillSyncResult:
    """Result of a skills sync operation.

    Attributes:
        added: List of skill names that were newly added
        updated: List of skill names that were updated (with backup)
        unchanged: List of skill names that were already up to date
        backup_dir: Path to the backup directory (if any updates were made)
        errors: List of error messages for skills that failed to sync
    """

    added: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    backup_dir: Path | None = None
    errors: list[str] = field(default_factory=list)

    @property
    def total_synced(self) -> int:
        """Total number of skills that were added or updated."""
        return len(self.added) + len(self.updated)

    @property
    def has_changes(self) -> bool:
        """Whether any skills were added or updated."""
        return self.total_synced > 0

    def summary(self) -> str:
        """Generate a human-readable summary of the sync operation."""
        parts = []
        if self.added:
            parts.append(f"{len(self.added)} added")
        if self.updated:
            parts.append(f"{len(self.updated)} updated")
        if self.unchanged:
            parts.append(f"{len(self.unchanged)} unchanged")
        if self.errors:
            parts.append(f"{len(self.errors)} errors")
        return ", ".join(parts) if parts else "no skills found"


def _find_templates_dir(subdir: str) -> Path | None:
    """Locate a templates subdirectory.

    Templates are bundled with the flowspec_cli package at
    flowspec_cli/templates/{subdir}/. Falls back to source repo
    structure for development mode.

    Args:
        subdir: Name of the subdirectory under templates/ (e.g., "skills", "commands", "partials")

    Returns:
        Path to templates/{subdir} directory, or None if not found.
    """
    # First, check for bundled templates in the package
    # This is the primary location for standalone flowspec
    package_templates = Path(__file__).parent.parent / "templates" / subdir
    if package_templates.exists():
        return package_templates

    # Fallback: Look for templates in source repo structure
    # This handles development mode where templates are at repo root.
    src_dir = Path(__file__).parent.parent.parent.parent  # Go up to repo root
    potential_templates = src_dir / "templates" / subdir
    if potential_templates.exists():
        return potential_templates

    return None


def deploy_skills(
    project_root: Path,
    *,
    force: bool = False,
    skip_skills: bool = False,
) -> list[Path]:
    """Deploy skills from templates/skills/ to .claude/skills/.

    Args:
        project_root: Root directory of the project
        force: If True, overwrite existing skills
        skip_skills: If True, skip skill deployment entirely

    Returns:
        List of paths to deployed skill directories
    """
    if skip_skills:
        return []

    templates_skills_dir = _find_templates_dir("skills")
    if templates_skills_dir is None:
        logger.warning(
            "Skills templates directory not found. "
            "This may indicate an installation issue if running from a package."
        )
        return []

    # Create .claude/skills directory
    skills_dir = project_root / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    deployed = []

    # Copy each skill directory from templates/skills/ to .claude/skills/
    for skill_dir in templates_skills_dir.iterdir():
        # Skip symlinks first - important because symlinks to directories
        # would pass is_dir() check. Example: context-extractor symlink
        # points back to .claude/skills, which we don't want to copy.
        if skill_dir.is_symlink():
            continue

        # Only process directories (non-symlinks already filtered above)
        if not skill_dir.is_dir():
            continue

        # Only process directories that contain SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        # Destination path
        dest_skill_dir = skills_dir / skill_dir.name

        # Check if skill already exists
        if dest_skill_dir.exists() and not force:
            # Skip existing skills unless --force
            continue

        # Copy skill directory
        if dest_skill_dir.exists():
            # Remove existing if force=True
            try:
                shutil.rmtree(dest_skill_dir)
            except OSError as exc:
                raise RuntimeError(
                    f"Failed to remove existing skill directory '{dest_skill_dir}'. "
                    "Please check file permissions and whether any files are in use."
                ) from exc

        try:
            shutil.copytree(skill_dir, dest_skill_dir)
        except OSError as exc:
            raise RuntimeError(
                f"Failed to copy skill directory '{skill_dir}' to '{dest_skill_dir}'. "
                "Please check file permissions, available disk space, and whether any "
                "files are in use."
            ) from exc
        deployed.append(dest_skill_dir)

    return deployed


def _dirs_are_equal(dir1: Path, dir2: Path) -> bool:
    """Compare two directories for equality (file contents only).

    Args:
        dir1: First directory to compare
        dir2: Second directory to compare

    Returns:
        True if directories have identical file contents, False otherwise
    """
    # Get list of files in each directory
    files1 = {f.relative_to(dir1) for f in dir1.rglob("*") if f.is_file()}
    files2 = {f.relative_to(dir2) for f in dir2.rglob("*") if f.is_file()}

    # If file sets differ, directories are not equal
    if files1 != files2:
        return False

    # Compare each file's contents
    for rel_path in files1:
        file1 = dir1 / rel_path
        file2 = dir2 / rel_path
        if not filecmp.cmp(file1, file2, shallow=False):
            return False

    return True


def sync_skills_directory(
    project_root: Path,
    source_skills_dir: Path,
    backup_dir: Path | None = None,
) -> SkillSyncResult:
    """Sync skills from source directory to project's .claude/skills/.

    This is used by upgrade-repo to sync skills from the extracted
    release package to the target project.

    Args:
        project_root: Root directory of the target project
        source_skills_dir: Directory containing source skills (from release package)
        backup_dir: Directory to backup existing skills before updating.
                   If None, no backups are created for updated skills.

    Returns:
        SkillSyncResult with details of what was added, updated, or unchanged
    """
    result = SkillSyncResult()

    # Validate source directory
    if not source_skills_dir.exists():
        logger.debug(f"Source skills directory not found: {source_skills_dir}")
        return result

    # Target skills directory
    target_skills_dir = project_root / ".claude" / "skills"
    target_skills_dir.mkdir(parents=True, exist_ok=True)

    # Track backup directory if we create backups
    skills_backup_dir = None
    if backup_dir:
        skills_backup_dir = backup_dir / ".claude" / "skills"

    # Process each skill in source directory
    for skill_dir in source_skills_dir.iterdir():
        # Skip non-directories and symlinks
        if skill_dir.is_symlink() or not skill_dir.is_dir():
            continue

        # Skip directories without SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        skill_name = skill_dir.name
        target_skill_dir = target_skills_dir / skill_name

        try:
            if not target_skill_dir.exists():
                # New skill - copy it
                shutil.copytree(skill_dir, target_skill_dir)
                result.added.append(skill_name)
                logger.debug(f"Added new skill: {skill_name}")

            elif _dirs_are_equal(skill_dir, target_skill_dir):
                # Skill exists and is identical - no action needed
                result.unchanged.append(skill_name)
                logger.debug(f"Skill unchanged: {skill_name}")

            else:
                # Skill exists but differs - backup and update
                if skills_backup_dir:
                    # Create backup
                    skills_backup_dir.mkdir(parents=True, exist_ok=True)
                    backup_skill_dir = skills_backup_dir / skill_name
                    if backup_skill_dir.exists():
                        shutil.rmtree(backup_skill_dir)
                    shutil.copytree(target_skill_dir, backup_skill_dir)
                    result.backup_dir = backup_dir
                    logger.debug(f"Backed up skill: {skill_name}")

                # Remove existing and copy new
                shutil.rmtree(target_skill_dir)
                shutil.copytree(skill_dir, target_skill_dir)
                result.updated.append(skill_name)
                logger.debug(f"Updated skill: {skill_name}")

        except OSError as exc:
            error_msg = f"Failed to sync skill '{skill_name}': {exc}"
            result.errors.append(error_msg)
            logger.warning(error_msg)

    return result


def compare_skills_after_extraction(
    project_root: Path,
    backup_dir: Path,
) -> SkillSyncResult:
    """Compare skills after extraction to generate a sync report.

    This is called after upgrade-repo extracts the release package.
    It compares the new skills in project_root/.claude/skills/ with
    the backed-up skills in backup_dir/.claude/skills/ to determine
    which skills were added, updated, or remained unchanged.

    Args:
        project_root: Root directory of the project (with newly extracted skills)
        backup_dir: Directory containing the backup (before extraction)

    Returns:
        SkillSyncResult with details of what was added, updated, or unchanged
    """
    result = SkillSyncResult()
    result.backup_dir = backup_dir

    new_skills_dir = project_root / ".claude" / "skills"
    old_skills_dir = backup_dir / ".claude" / "skills"

    # If no new skills directory exists, nothing was synced
    if not new_skills_dir.exists():
        logger.debug("No .claude/skills/ directory in project after extraction")
        return result

    # Get sets of skill names
    new_skills = set()
    if new_skills_dir.exists():
        for skill_dir in new_skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.is_symlink():
                if (skill_dir / "SKILL.md").exists():
                    new_skills.add(skill_dir.name)

    old_skills = set()
    if old_skills_dir.exists():
        for skill_dir in old_skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.is_symlink():
                if (skill_dir / "SKILL.md").exists():
                    old_skills.add(skill_dir.name)

    # Categorize skills
    for skill_name in new_skills:
        new_skill_path = new_skills_dir / skill_name
        old_skill_path = old_skills_dir / skill_name

        if skill_name not in old_skills:
            # Newly added skill
            result.added.append(skill_name)
        elif not old_skill_path.exists():
            # Old directory exists but no matching skill (edge case)
            result.added.append(skill_name)
        elif _dirs_are_equal(new_skill_path, old_skill_path):
            # Unchanged
            result.unchanged.append(skill_name)
        else:
            # Updated
            result.updated.append(skill_name)

    # Sort for consistent output
    result.added.sort()
    result.updated.sort()
    result.unchanged.sort()

    return result


def _deploy_template_directory(
    project_root: Path,
    template_subdir: str,
    dest_subdir: str,
    *,
    force: bool = False,
    skip: bool = False,
) -> list[Path]:
    """Deploy a template directory to .claude/{dest_subdir}/.

    This is a shared helper function used by deploy_commands and deploy_partials
    to reduce code duplication. Both functions follow the same pattern of copying
    template files/directories to .claude/{dest_subdir}/.

    Args:
        project_root: Root directory of the project
        template_subdir: Name of the template subdirectory (e.g., "commands", "partials")
        dest_subdir: Name of the destination subdirectory under .claude/
        force: If True, overwrite existing items
        skip: If True, skip deployment entirely

    Returns:
        List of paths to deployed files/directories
    """
    if skip:
        return []

    templates_dir = _find_templates_dir(template_subdir)
    if templates_dir is None:
        logger.warning(
            f"{template_subdir.capitalize()} templates directory not found. "
            "This may indicate an installation issue if running from a package."
        )
        return []

    # Create .claude/{dest_subdir} directory
    dest_dir = project_root / ".claude" / dest_subdir
    dest_dir.mkdir(parents=True, exist_ok=True)

    deployed = []

    # Copy each item from templates/{template_subdir}/ to .claude/{dest_subdir}/
    for item in templates_dir.iterdir():
        # Skip symlinks
        if item.is_symlink():
            continue

        # Destination path
        dest_item = dest_dir / item.name

        # Check if item already exists
        if dest_item.exists() and not force:
            # Skip existing items unless --force
            continue

        # Copy item
        if dest_item.exists():
            # Remove existing if force=True
            try:
                if dest_item.is_dir():
                    shutil.rmtree(dest_item)
                else:
                    dest_item.unlink()
            except OSError as exc:
                raise RuntimeError(
                    f"Failed to remove existing item '{dest_item}'. "
                    "Please check file permissions and whether any files are in use."
                ) from exc

        try:
            if item.is_dir():
                shutil.copytree(item, dest_item)
            else:
                shutil.copy2(item, dest_item)
        except OSError as exc:
            raise RuntimeError(
                f"Failed to copy '{item}' to '{dest_item}'. "
                "Please check file permissions, available disk space, and whether any "
                "files are in use."
            ) from exc
        deployed.append(dest_item)

    return deployed


def deploy_commands(
    project_root: Path,
    *,
    force: bool = False,
    skip_commands: bool = False,
) -> list[Path]:
    """Deploy commands from templates/commands/ to .claude/commands/.

    Args:
        project_root: Root directory of the project
        force: If True, overwrite existing commands
        skip_commands: If True, skip command deployment entirely

    Returns:
        List of paths to deployed command files/directories
    """
    return _deploy_template_directory(
        project_root,
        "commands",
        "commands",
        force=force,
        skip=skip_commands,
    )


def deploy_partials(
    project_root: Path,
    *,
    force: bool = False,
    skip_partials: bool = False,
) -> list[Path]:
    """Deploy partials from templates/partials/ to .claude/partials/.

    Args:
        project_root: Root directory of the project
        force: If True, overwrite existing partials
        skip_partials: If True, skip partials deployment entirely

    Returns:
        List of paths to deployed partial files/directories
    """
    return _deploy_template_directory(
        project_root,
        "partials",
        "partials",
        force=force,
        skip=skip_partials,
    )


def deploy_claude_hooks(
    project_root: Path,
    project_name: str = "",
    *,
    force: bool = False,
    skip_hooks: bool = False,
) -> list[Path]:
    """Deploy Claude Code hooks from templates/hooks/ to .claude/hooks/.

    This deploys the fail-open hooks for Claude Code that provide:
    - Session startup with environment verification
    - Auto-approval for safe read operations
    - Git command safety checks
    - Sensitive file protection
    - Auto-formatting and linting for Python files
    - Quality gate on PR creation

    Args:
        project_root: Root directory of the project
        project_name: Name of the project (for settings.json template)
        force: If True, overwrite existing hooks
        skip_hooks: If True, skip hook deployment entirely

    Returns:
        List of paths to deployed hook files
    """
    if skip_hooks:
        return []

    templates_hooks_dir = _find_templates_dir("hooks")
    if templates_hooks_dir is None:
        logger.warning(
            "Hooks templates directory not found. "
            "This may indicate an installation issue if running from a package."
        )
        return []

    # Create .claude/hooks directory
    hooks_dir = project_root / ".claude" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    deployed = []

    # Copy each hook file from templates/hooks/ to .claude/hooks/
    for item in templates_hooks_dir.iterdir():
        # Skip symlinks and the template file
        if item.is_symlink():
            continue
        if item.name == "settings.json.template":
            continue

        # Only process files (hooks are individual scripts)
        if not item.is_file():
            continue

        # Destination path
        dest_item = hooks_dir / item.name

        # Check if item already exists
        if dest_item.exists() and not force:
            # Skip existing items unless --force
            continue

        # Copy file
        if dest_item.exists():
            try:
                dest_item.unlink()
            except OSError as exc:
                raise RuntimeError(
                    f"Failed to remove existing hook '{dest_item}'. "
                    "Please check file permissions."
                ) from exc

        try:
            shutil.copy2(item, dest_item)
            # Make shell scripts executable
            if item.suffix == ".sh":
                dest_item.chmod(0o755)
        except OSError as exc:
            raise RuntimeError(
                f"Failed to copy hook '{item}' to '{dest_item}'. "
                "Please check file permissions and available disk space."
            ) from exc
        deployed.append(dest_item)

    # Generate settings.json from template if it doesn't exist
    settings_file = project_root / ".claude" / "settings.json"
    settings_template = templates_hooks_dir / "settings.json.template"

    if settings_template.exists() and (not settings_file.exists() or force):
        try:
            template_content = settings_template.read_text(encoding="utf-8")

            # Determine project-specific settings
            if not project_name:
                project_name = project_root.name

            # Detect tech stack for preferences
            # Priority: Python > Node.js (flowspec is Python-first)
            has_python = (project_root / "pyproject.toml").exists()
            has_nodejs = (project_root / "package.json").exists()

            if has_python:
                # Python project (or hybrid - Python takes precedence)
                code_style = "ruff"
                test_framework = "pytest"
                if (project_root / "uv.lock").exists():
                    package_manager = "uv"
                elif (project_root / "poetry.lock").exists():
                    package_manager = "poetry"
                else:
                    package_manager = "pip"
            elif has_nodejs:
                # Pure Node.js project
                code_style = "prettier"
                test_framework = "jest"
                package_manager = "npm"
            else:
                # Default to Python tooling
                code_style = "ruff"
                test_framework = "pytest"
                package_manager = "uv"

            # Replace placeholders
            content = template_content.replace("{{PROJECT_NAME}}", project_name)
            content = content.replace("{{CODE_STYLE}}", code_style)
            content = content.replace("{{TEST_FRAMEWORK}}", test_framework)
            content = content.replace("{{PACKAGE_MANAGER}}", package_manager)

            settings_file.write_text(content, encoding="utf-8")
            deployed.append(settings_file)
        except OSError as exc:
            raise RuntimeError(
                f"Failed to create settings.json: {exc}. Please check file permissions."
            ) from exc

    return deployed


__all__ = [
    "deploy_skills",
    "deploy_commands",
    "deploy_partials",
    "deploy_claude_hooks",
    "sync_skills_directory",
    "compare_skills_after_extraction",
    "SkillSyncResult",
]
