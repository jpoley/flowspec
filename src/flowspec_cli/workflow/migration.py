"""Workflow configuration migration utilities.

This module provides utilities for detecting and migrating flowspec_workflow.yml
from v1.0 to v2.0 format. It handles:
- Version detection
- Schema migration (adding roles, custom_workflows, agent_loops sections)
- Removal of deprecated 'operate' workflow and transitions
- Preservation of custom configurations

The migration is designed to be non-destructive - it creates a backup before
making any changes and preserves custom configurations where possible.
"""

from __future__ import annotations

import copy
import logging
import shutil
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# Current target version for migration
TARGET_VERSION = "2.0"

# Default v2.0 sections that should be added if missing
DEFAULT_ROLES = {
    "primary": "dev",
    "show_all_commands": False,
    "definitions": {
        "arch": {
            "display_name": "Architect",
            "icon": "\U0001f3d7\ufe0f",
            "commands": ["decide", "model"],
            "agents": ["@software-architect", "@platform-engineer"],
        },
        "dev": {
            "display_name": "Developer",
            "icon": "\U0001f4bb",
            "commands": ["cleanup", "debug", "refactor"],
            "agents": [
                "@frontend-engineer",
                "@backend-engineer",
                "@ai-ml-engineer",
            ],
        },
        "sec": {
            "display_name": "Security Engineer",
            "icon": "\U0001f512",
            "commands": ["fix", "report", "scan", "triage"],
            "agents": ["@secure-by-design-engineer"],
        },
        "qa": {
            "display_name": "QA Engineer",
            "icon": "\u2705",
            "commands": ["review", "test"],
            "agents": ["@quality-guardian", "@release-manager"],
        },
        "ops": {
            "display_name": "SRE/DevOps",
            "icon": "\U0001f680",
            "commands": ["monitor", "respond", "scale"],
            "agents": ["@sre-agent"],
        },
        "all": {
            "display_name": "All Roles",
            "icon": "\U0001f310",
            "commands": [],
            "agents": [],
        },
    },
}

DEFAULT_AGENT_LOOPS = {
    "inner": {
        "description": "Fast execution - optimized for developer velocity",
        "agents": [
            "frontend-engineer",
            "backend-engineer",
            "ai-ml-engineer",
            "frontend-code-reviewer",
            "backend-code-reviewer",
        ],
    },
    "outer": {
        "description": "Governance-focused - optimized for safety and reliability",
        "agents": [
            "workflow-assessor",
            "product-requirements-manager",
            "researcher",
            "business-validator",
            "software-architect",
            "platform-engineer",
            "quality-guardian",
            "secure-by-design-engineer",
            "tech-writer",
            "release-manager",
            "sre-agent",
            "pr-monitor",
        ],
    },
}

DEFAULT_CUSTOM_WORKFLOWS = {
    "quick_build": {
        "name": "Quick Build",
        "description": "Lightweight workflow for simple features",
        "mode": "vibing",
        "steps": [
            {"workflow": "specify"},
            {"workflow": "implement"},
            {"workflow": "validate"},
        ],
        "rigor": {
            "log_decisions": True,
            "log_events": True,
            "backlog_integration": True,
            "memory_tracking": True,
            "follow_constitution": True,
            "create_adrs": True,
        },
    },
    "full_design": {
        "name": "Full Design Workflow",
        "description": "Complete design workflow with conditional research",
        "mode": "spec-ing",
        "steps": [
            {"workflow": "assess"},
            {"workflow": "specify", "checkpoint": "Review PRD before continuing?"},
            {"workflow": "research", "condition": "complexity >= 7"},
            {
                "workflow": "plan",
                "checkpoint": "Review architecture before implementing?",
            },
        ],
        "rigor": {
            "log_decisions": True,
            "log_events": True,
            "backlog_integration": True,
            "memory_tracking": True,
            "follow_constitution": True,
            "create_adrs": True,
        },
    },
    "ship_it": {
        "name": "Build and Ship",
        "description": "Implementation to validation with PR submission",
        "mode": "vibing",
        "steps": [
            {"workflow": "implement"},
            {"workflow": "validate"},
            {"workflow": "submit-n-watch-pr"},
        ],
        "rigor": {
            "log_decisions": True,
            "log_events": True,
            "backlog_integration": True,
            "memory_tracking": True,
            "follow_constitution": True,
            "create_adrs": True,
        },
    },
}

# Deprecated elements to remove in v2.0
DEPRECATED_WORKFLOWS = ["operate"]
DEPRECATED_STATES = ["Deployed"]
DEPRECATED_TRANSITIONS = [
    "operate",
    "complete_from_deployed",
    "rollback",
    "complete_from_operated",
]


@dataclass
class WorkflowMigrationResult:
    """Result of a workflow configuration migration.

    Attributes:
        migrated: Whether migration was performed
        from_version: Original version before migration
        to_version: Version after migration
        changes: List of changes made
        backup_path: Path to backup file (if created)
        errors: List of error messages
    """

    migrated: bool = False
    from_version: str | None = None
    to_version: str | None = None
    changes: list[str] = field(default_factory=list)
    backup_path: Path | None = None
    errors: list[str] = field(default_factory=list)

    def summary(self) -> str:
        """Generate a human-readable summary of the migration."""
        if not self.migrated:
            if self.from_version == TARGET_VERSION:
                return "already at v2.0"
            if self.errors:
                return f"{len(self.errors)} errors"
            return "no migration needed"

        parts = []
        if self.from_version and self.to_version:
            parts.append(f"v{self.from_version} -> v{self.to_version}")
        if self.changes:
            parts.append(f"{len(self.changes)} changes")
        return ", ".join(parts) if parts else "migrated"


def detect_workflow_version(config: dict[str, Any]) -> str:
    """Detect the version of a workflow configuration.

    Args:
        config: Parsed workflow configuration dictionary

    Returns:
        Version string (e.g., "1.0", "2.0")
    """
    # Check explicit version field
    version = config.get("version")
    if version:
        return str(version)

    # Infer version from structure
    # v2.0 indicators: roles, custom_workflows, agent_loops sections
    has_roles = "roles" in config
    has_custom_workflows = "custom_workflows" in config
    has_agent_loops = "agent_loops" in config

    if has_roles or has_custom_workflows or has_agent_loops:
        return "2.0"

    # v1.0 indicators: operate workflow, Deployed state
    workflows = config.get("workflows", {})
    if "operate" in workflows:
        return "1.0"

    states = config.get("states", [])
    if "Deployed" in states:
        return "1.0"

    # Default to 1.0 if unknown
    return "1.0"


def migrate_workflow_config(
    project_root: Path,
    backup_dir: Path | None = None,
    dry_run: bool = False,
) -> WorkflowMigrationResult:
    """Migrate workflow configuration from v1.0 to v2.0.

    Args:
        project_root: Root directory of the project
        backup_dir: Directory to store backup (if None, uses project_root)
        dry_run: If True, only report changes without applying

    Returns:
        WorkflowMigrationResult with details of the migration
    """
    result = WorkflowMigrationResult()

    # Find workflow config file
    workflow_file = project_root / "flowspec_workflow.yml"
    if not workflow_file.exists():
        workflow_file = project_root / "flowspec_workflow.yaml"
        if not workflow_file.exists():
            # No workflow config to migrate
            logger.debug("No flowspec_workflow.yml found")
            return result

    # Load existing config
    try:
        with open(workflow_file) as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        result.errors.append(f"Failed to parse {workflow_file}: {e}")
        return result

    if not isinstance(config, dict):
        result.errors.append(f"Invalid config format in {workflow_file}")
        return result

    # Detect version
    result.from_version = detect_workflow_version(config)

    # Already at target version?
    if result.from_version == TARGET_VERSION:
        result.to_version = TARGET_VERSION
        logger.debug("Workflow config already at v2.0")
        return result

    # Create backup
    if not dry_run:
        backup_location = backup_dir if backup_dir else project_root
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = backup_location / f"flowspec_workflow.yml.backup-{timestamp}"
        try:
            shutil.copy2(workflow_file, backup_path)
            result.backup_path = backup_path
            logger.debug(f"Created backup at {backup_path}")
        except OSError as e:
            result.errors.append(f"Failed to create backup: {e}")
            return result

    # Perform migration
    migrated_config = _migrate_v1_to_v2(config, result.changes)

    # Update metadata
    migrated_config["version"] = TARGET_VERSION
    if "metadata" in migrated_config:
        migrated_config["metadata"]["schema_version"] = TARGET_VERSION
        migrated_config["metadata"]["last_updated"] = datetime.now().strftime(
            "%Y-%m-%d"
        )

    result.to_version = TARGET_VERSION
    result.migrated = True

    # Write migrated config
    if not dry_run:
        try:
            with open(workflow_file, "w") as f:
                yaml.dump(
                    migrated_config,
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                    width=100,
                )
            logger.info(f"Migrated {workflow_file} to v2.0")
        except OSError as e:
            result.errors.append(f"Failed to write migrated config: {e}")
            result.migrated = False

    return result


def _migrate_v1_to_v2(config: dict[str, Any], changes: list[str]) -> dict[str, Any]:
    """Perform the actual v1.0 to v2.0 migration.

    Args:
        config: Original v1.0 configuration
        changes: List to append change descriptions to

    Returns:
        Migrated v2.0 configuration
    """
    migrated = copy.deepcopy(config)

    # 1. Add version field
    migrated["version"] = TARGET_VERSION
    changes.append("Added version: 2.0")

    # 2. Remove deprecated 'operate' workflow
    workflows = migrated.get("workflows", {})
    if isinstance(workflows, dict):
        for deprecated in DEPRECATED_WORKFLOWS:
            if deprecated in workflows:
                del workflows[deprecated]
                changes.append(f"Removed deprecated workflow: {deprecated}")
        migrated["workflows"] = workflows

    # 3. Remove deprecated states
    states = migrated.get("states", [])
    if isinstance(states, list):
        original_count = len(states)
        states = [s for s in states if s not in DEPRECATED_STATES]
        if len(states) < original_count:
            changes.append(f"Removed deprecated states: {DEPRECATED_STATES}")
        migrated["states"] = states

    # 4. Remove deprecated transitions
    transitions = migrated.get("transitions", [])
    if isinstance(transitions, list):
        original_count = len(transitions)
        transitions = [
            t
            for t in transitions
            if t.get("name") not in DEPRECATED_TRANSITIONS
            and t.get("via") not in DEPRECATED_WORKFLOWS
        ]
        if len(transitions) < original_count:
            removed_count = original_count - len(transitions)
            changes.append(f"Removed {removed_count} deprecated transitions")
        migrated["transitions"] = transitions

    # 5. Add roles section if missing
    if "roles" not in migrated:
        migrated["roles"] = DEFAULT_ROLES
        changes.append("Added roles section with default configuration")

    # 6. Add agent_loops section if missing
    if "agent_loops" not in migrated:
        migrated["agent_loops"] = DEFAULT_AGENT_LOOPS
        changes.append("Added agent_loops section")

    # 7. Add custom_workflows section if missing
    if "custom_workflows" not in migrated:
        migrated["custom_workflows"] = DEFAULT_CUSTOM_WORKFLOWS
        changes.append("Added custom_workflows section with default workflows")

    # 8. Update metadata
    metadata = migrated.get("metadata", {})
    if isinstance(metadata, dict):
        metadata["schema_version"] = TARGET_VERSION
        # Remove deprecated Deployed state from state_count
        if "state_count" in metadata:
            metadata["state_count"] = len(migrated.get("states", []))
        # Update workflow_count (removed operate)
        if "workflow_count" in metadata:
            metadata["workflow_count"] = len(migrated.get("workflows", {}))
        migrated["metadata"] = metadata
        changes.append("Updated metadata to reflect v2.0 schema")

    return migrated


def compare_workflow_after_extraction(
    project_root: Path,
    backup_dir: Path,
) -> WorkflowMigrationResult:
    """Compare workflow config after extraction to generate a migration report.

    This is called after upgrade-repo extracts the release package.
    It compares the new workflow config with the backed-up version.

    Args:
        project_root: Root directory of the project (with newly extracted config)
        backup_dir: Directory containing the backup (before extraction)

    Returns:
        WorkflowMigrationResult with comparison details
    """
    result = WorkflowMigrationResult()

    new_workflow_file = project_root / "flowspec_workflow.yml"
    old_workflow_file = backup_dir / "flowspec_workflow.yml"

    # Check if files exist
    if not new_workflow_file.exists():
        logger.debug("No new flowspec_workflow.yml found")
        return result

    # Load new config
    try:
        with open(new_workflow_file) as f:
            new_config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        result.errors.append(f"Failed to parse new config: {e}")
        return result

    result.to_version = detect_workflow_version(new_config)

    # Load old config if exists
    if old_workflow_file.exists():
        try:
            with open(old_workflow_file) as f:
                old_config = yaml.safe_load(f) or {}
            result.from_version = detect_workflow_version(old_config)
        except yaml.YAMLError:
            result.from_version = None
    else:
        result.from_version = None
        result.changes.append("New flowspec_workflow.yml added")
        result.migrated = True
        return result

    # Compare versions
    if result.from_version != result.to_version:
        result.migrated = True
        result.changes.append(
            f"Version updated: {result.from_version} -> {result.to_version}"
        )

    # Compare key sections
    for section in [
        "workflows",
        "states",
        "transitions",
        "roles",
        "agent_loops",
        "custom_workflows",
    ]:
        old_has = section in old_config
        new_has = section in new_config

        if not old_has and new_has:
            result.changes.append(f"Added section: {section}")
            result.migrated = True
        elif old_has and not new_has:
            result.changes.append(f"Removed section: {section}")
            result.migrated = True

    # Check for deprecated elements removed
    old_workflows = old_config.get("workflows", {})
    new_workflows = new_config.get("workflows", {})

    for deprecated in DEPRECATED_WORKFLOWS:
        if deprecated in old_workflows and deprecated not in new_workflows:
            result.changes.append(f"Removed deprecated workflow: {deprecated}")
            result.migrated = True

    return result


__all__ = [
    "WorkflowMigrationResult",
    "detect_workflow_version",
    "migrate_workflow_config",
    "compare_workflow_after_extraction",
    "TARGET_VERSION",
]
