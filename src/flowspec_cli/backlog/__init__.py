"""
Backlog.md integration module for flowspec.

This module provides task generation and management integration between
flowspec specs and Backlog.md task management system.

Components:
    - TaskParser: Parse task files into Task objects
    - BacklogWriter: Write tasks to backlog.md format files
    - TaskMapper: Map spec tasks to backlog format
    - DependencyGraphBuilder: Build task dependency graphs
    - shim: CLI wrapper with automatic event emission (recommended for agents)

Example using shim (recommended for agents):
    >>> from flowspec_cli.backlog.shim import task_edit, complete_task
    >>> result = task_edit("task-123", status="In Progress")
    >>> # Later...
    >>> result = complete_task("task-123")  # Emits task.completed event
"""

from .dependency_graph import DependencyGraphBuilder
from .mapper import TaskMapper
from .parser import TaskParser

# Import shim functions for convenience
from .shim import (
    ShimResult,
    check_acceptance_criteria,
    complete_task,
    # Convenience aliases
    create_task,
    edit_task,
    start_task,
    task_archive,
    task_create,
    task_edit,
    task_list,
    task_search,
    task_view,
)
from .writer import BacklogWriter

__all__ = [
    # Legacy components
    "TaskParser",
    "BacklogWriter",
    "TaskMapper",
    "DependencyGraphBuilder",
    # Shim (recommended for agents)
    "ShimResult",
    "task_create",
    "task_edit",
    "task_view",
    "task_list",
    "task_search",
    "task_archive",
    # Convenience aliases
    "create_task",
    "edit_task",
    "complete_task",
    "start_task",
    "check_acceptance_criteria",
]
