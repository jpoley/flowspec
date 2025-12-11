"""
Backlog.md integration module for flowspec.

This module provides task generation and management integration between
flowspec specs and Backlog.md task management system.
"""

from .parser import TaskParser
from .writer import BacklogWriter
from .mapper import TaskMapper
from .dependency_graph import DependencyGraphBuilder

__all__ = [
    "TaskParser",
    "BacklogWriter",
    "TaskMapper",
    "DependencyGraphBuilder",
]
