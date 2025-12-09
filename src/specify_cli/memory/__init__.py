"""Task Memory module - Persistent storage for task implementation context.

This module provides components for managing task memory files that track:
- Implementation context and decisions
- Approaches tried and outcomes
- Open questions and resources
- Freeform notes during development
"""

from specify_cli.memory.store import TaskMemoryStore
from specify_cli.memory.injector import ContextInjector
from specify_cli.memory.mcp import register_memory_resources, create_memory_mcp_server

__all__ = [
    "TaskMemoryStore",
    "ContextInjector",
    "register_memory_resources",
    "create_memory_mcp_server",
]
