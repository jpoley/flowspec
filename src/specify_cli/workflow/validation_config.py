"""Validation configuration management for workflow transitions.

This module provides configuration management for validation modes applied to
workflow transitions. It supports loading, saving, and managing validation
configuration for the `specify init` command and related workflow operations.

Example:
    >>> from specify_cli.workflow.validation_config import (
    ...     ValidationConfig, get_default_config, save_config, load_config
    ... )
    >>> config = get_default_config()
    >>> config.transitions["specify"] = "KEYWORD[PRD_APPROVED]"
    >>> save_config(config, Path("jpspec_workflow.yml"))
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from specify_cli.workflow.transition import (
    WORKFLOW_TRANSITIONS,
    ValidationMode,
    format_validation_mode,
    parse_validation_mode,
)


@dataclass
class ValidationConfig:
    """Configuration for workflow transition validation modes.

    This class stores validation modes for each workflow transition,
    allowing users to configure how transitions are gated (NONE, KEYWORD,
    or PULL_REQUEST).

    Attributes:
        version: Configuration schema version (default: "1.0").
        transitions: Mapping of transition names to validation mode strings.

    Example:
        >>> config = ValidationConfig()
        >>> config.transitions["specify"] = "KEYWORD[PRD_APPROVED]"
        >>> config.transitions["plan"] = "PULL_REQUEST"
    """

    version: str = "1.0"
    transitions: dict[str, str] = field(default_factory=dict)

    def get_validation_mode(self, transition_name: str) -> str:
        """Get validation mode for a specific transition.

        Args:
            transition_name: Name of the transition (e.g., "specify", "plan").

        Returns:
            Validation mode string (e.g., "NONE", "KEYWORD[APPROVED]").
            Returns "NONE" if transition not configured.
        """
        return self.transitions.get(transition_name, "NONE")

    def set_validation_mode(self, transition_name: str, mode: str) -> None:
        """Set validation mode for a specific transition.

        Args:
            transition_name: Name of the transition.
            mode: Validation mode string (e.g., "NONE", "KEYWORD[APPROVED]").

        Raises:
            ValueError: If mode string is invalid.
        """
        # Validate mode string by parsing
        parse_validation_mode(mode)
        self.transitions[transition_name] = mode

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary format.

        Returns:
            Dictionary with version and transitions.
        """
        return {
            "version": self.version,
            "transitions": [
                {
                    "name": name,
                    "validation": mode,
                }
                for name, mode in self.transitions.items()
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ValidationConfig:
        """Create configuration from dictionary format.

        Args:
            data: Dictionary with version and transitions.

        Returns:
            ValidationConfig instance.

        Raises:
            ValueError: If data format is invalid.
        """
        version = data.get("version", "1.0")
        transitions_list = data.get("transitions", [])

        transitions = {}
        for transition in transitions_list:
            if not isinstance(transition, dict):
                raise ValueError(f"Invalid transition format: {transition}")

            name = transition.get("name")
            validation = transition.get("validation", "NONE")

            if not name:
                raise ValueError("Transition missing 'name' field")

            transitions[name] = validation

        return cls(version=version, transitions=transitions)


def get_default_config() -> ValidationConfig:
    """Get default validation configuration with all transitions set to NONE.

    Returns:
        ValidationConfig with all known transitions set to ValidationMode.NONE.

    Example:
        >>> config = get_default_config()
        >>> config.get_validation_mode("specify")
        'NONE'
    """
    config = ValidationConfig()

    # Initialize all known transitions to NONE
    for transition in WORKFLOW_TRANSITIONS:
        config.transitions[transition.name] = format_validation_mode(
            ValidationMode.NONE
        )

    return config


def load_config(path: Path) -> ValidationConfig:
    """Load validation configuration from YAML file.

    Args:
        path: Path to configuration file (e.g., jpspec_workflow.yml).

    Returns:
        ValidationConfig loaded from file.

    Raises:
        FileNotFoundError: If configuration file does not exist.
        ValueError: If configuration file has invalid format.

    Example:
        >>> config = load_config(Path(".specify/jpspec_workflow.yml"))
    """
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid configuration format in {path}")

    return ValidationConfig.from_dict(data)


def save_config(config: ValidationConfig, path: Path) -> None:
    """Save validation configuration to YAML file.

    Args:
        config: ValidationConfig to save.
        path: Path to output file (e.g., jpspec_workflow.yml).

    Example:
        >>> config = get_default_config()
        >>> save_config(config, Path(".specify/jpspec_workflow.yml"))
    """
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    data = config.to_dict()

    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
