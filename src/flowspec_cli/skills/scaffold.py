"""Skill deployment for flowspec init.

This module provides skill directory copying functionality
that deploys skills from templates/skills/ to .claude/skills/
when users run `flowspec init`.
"""

from __future__ import annotations

import shutil
from pathlib import Path


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

    # Find templates/skills directory
    # Check if we're in a package installation or source repo
    templates_skills_dir = None

    # Try package resources first (for installed flowspec-cli)
    try:
        import importlib.resources

        # For Python 3.11+, use files() API
        if hasattr(importlib.resources, "files"):
            templates_ref = importlib.resources.files("flowspec_cli").joinpath(
                "templates/skills"
            )
            if templates_ref.is_dir():
                # Convert to Path - we need to copy from this location
                templates_skills_dir = Path(str(templates_ref))
    except (ImportError, AttributeError, TypeError):
        pass

    # Fallback: look for templates in source repo structure
    if templates_skills_dir is None or not templates_skills_dir.exists():
        # Assume we're in development mode - find templates relative to this file
        src_dir = Path(__file__).parent.parent.parent.parent  # Go up to repo root
        potential_templates = src_dir / "templates" / "skills"
        if potential_templates.exists():
            templates_skills_dir = potential_templates

    # If still not found, return empty list
    if templates_skills_dir is None or not templates_skills_dir.exists():
        return []

    # Create .claude/skills directory
    skills_dir = project_root / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    deployed = []

    # Copy each skill directory from templates/skills/ to .claude/skills/
    for skill_dir in templates_skills_dir.iterdir():
        # Skip symlinks (like context-extractor which points back to .claude/skills)
        if skill_dir.is_symlink():
            continue

        # Only process directories that contain SKILL.md
        if not skill_dir.is_dir():
            continue

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
            shutil.rmtree(dest_skill_dir)

        shutil.copytree(skill_dir, dest_skill_dir)
        deployed.append(dest_skill_dir)

    return deployed


__all__ = ["deploy_skills"]
