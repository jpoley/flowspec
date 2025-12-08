"""Janitor - Repository cleanup state management.

This module provides state tracking for the github-janitor agent,
including pending cleanup items, last run timestamps, and audit logging.

Example:
    >>> from specify_cli.janitor import JanitorState, read_janitor_state
    >>> state = read_janitor_state(Path(".specify/state"))
    >>> print(f"Last run: {state.last_run}")
"""

from .reader import (
    JanitorState,
    PendingCleanup,
    read_janitor_state,
    read_pending_cleanup,
)
from .state import (
    add_pending_branch,
    add_pending_worktree,
    clear_pending_cleanup,
    record_janitor_run,
    update_pending_cleanup,
    write_audit_log,
)

__all__ = [
    # Reader
    "JanitorState",
    "PendingCleanup",
    "read_janitor_state",
    "read_pending_cleanup",
    # Writer
    "record_janitor_run",
    "update_pending_cleanup",
    "add_pending_branch",
    "add_pending_worktree",
    "clear_pending_cleanup",
    "write_audit_log",
]
