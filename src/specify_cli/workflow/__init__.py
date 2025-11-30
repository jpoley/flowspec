"""Workflow configuration module for JP Spec Kit.

This module provides the WorkflowConfig class for loading, parsing, and querying
jpspec workflow configuration files. It enables the /jpspec commands to enforce
state-based transitions and agent assignments.

Example:
    >>> from specify_cli.workflow import WorkflowConfig
    >>> config = WorkflowConfig.load()
    >>> agents = config.get_agents("implement")
    >>> next_state = config.get_next_state("Planned", "implement")
"""

from .config import WorkflowConfig
from .exceptions import (
    WorkflowConfigError,
    WorkflowConfigNotFoundError,
    WorkflowConfigValidationError,
    WorkflowNotFoundError,
    WorkflowStateError,
)

__all__ = [
    "WorkflowConfig",
    "WorkflowConfigError",
    "WorkflowConfigNotFoundError",
    "WorkflowConfigValidationError",
    "WorkflowNotFoundError",
    "WorkflowStateError",
]
