"""Git event emission helpers.

This module provides utilities for emitting events from git operations.
"""

from __future__ import annotations

from typing import Literal

from .event_writer import emit_event
from .schema import Context, FlowspecEvent, GitObject


def emit_branch_created_event(
    branch_name: str,
    from_branch: str | None = None,
    task_id: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a branch created event.

    Args:
        branch_name: Name of the created branch
        from_branch: Source branch (e.g., "main")
        task_id: Associated task ID
        agent_id: Agent who created the branch

    Returns:
        True if event was emitted successfully
    """
    git_obj = GitObject(
        operation="branch",
        branch_name=branch_name,
        from_branch=from_branch,
    )
    context = Context(branch_name=branch_name, task_id=task_id)

    event = FlowspecEvent.create(
        event_type="git.branch_created",
        agent_id=agent_id,
        source="cli",
        message=f"Branch created: {branch_name}",
        git=git_obj,
        context=context,
    )

    return emit_event(event)


def emit_branch_deleted_event(
    branch_name: str,
    task_id: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a branch deleted event.

    Args:
        branch_name: Name of the deleted branch
        task_id: Associated task ID
        agent_id: Agent who deleted the branch

    Returns:
        True if event was emitted successfully
    """
    git_obj = GitObject(operation="branch", branch_name=branch_name)
    context = Context(branch_name=branch_name, task_id=task_id)

    event = FlowspecEvent.create(
        event_type="git.branch_deleted",
        agent_id=agent_id,
        source="cli",
        message=f"Branch deleted: {branch_name}",
        git=git_obj,
        context=context,
    )

    return emit_event(event)


def emit_commit_event(
    sha: str,
    message: str,
    branch_name: str | None = None,
    files_changed: int | None = None,
    insertions: int | None = None,
    deletions: int | None = None,
    gpg_key_id: str | None = None,
    signer_agent_id: str | None = None,
    task_id: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a commit event.

    Args:
        sha: Commit SHA
        message: Commit message
        branch_name: Branch where commit was made
        files_changed: Number of files changed
        insertions: Number of insertions
        deletions: Number of deletions
        gpg_key_id: GPG key ID used for signing
        signer_agent_id: Agent who signed the commit
        task_id: Associated task ID
        agent_id: Agent who made the commit

    Returns:
        True if event was emitted successfully
    """
    git_obj = GitObject(
        operation="commit",
        sha=sha,
        branch_name=branch_name,
        message=message,
        files_changed=files_changed,
        insertions=insertions,
        deletions=deletions,
        gpg_key_id=gpg_key_id,
        signer_agent_id=signer_agent_id,
    )
    context = Context(branch_name=branch_name, task_id=task_id)

    event = FlowspecEvent.create(
        event_type="git.commit",
        agent_id=agent_id,
        source="cli",
        message=f"Commit: {sha[:7]} - {message[:50]}",
        git=git_obj,
        context=context,
    )

    return emit_event(event)


def emit_worktree_created_event(
    worktree_path: str,
    branch_name: str,
    task_id: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a worktree created event.

    Args:
        worktree_path: Path to the worktree
        branch_name: Branch associated with worktree
        task_id: Associated task ID
        agent_id: Agent who created the worktree

    Returns:
        True if event was emitted successfully
    """
    context = Context(
        worktree_path=worktree_path,
        branch_name=branch_name,
        task_id=task_id,
    )

    event = FlowspecEvent.create(
        event_type="git.worktree_created",
        agent_id=agent_id,
        source="cli",
        message=f"Worktree created: {worktree_path}",
        context=context,
    )

    return emit_event(event)


def emit_worktree_removed_event(
    worktree_path: str,
    task_id: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a worktree removed event.

    Args:
        worktree_path: Path to the worktree
        task_id: Associated task ID
        agent_id: Agent who removed the worktree

    Returns:
        True if event was emitted successfully
    """
    context = Context(worktree_path=worktree_path, task_id=task_id)

    event = FlowspecEvent.create(
        event_type="git.worktree_removed",
        agent_id=agent_id,
        source="cli",
        message=f"Worktree removed: {worktree_path}",
        context=context,
    )

    return emit_event(event)


def emit_pushed_event(
    branch_name: str,
    task_id: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a pushed event.

    Args:
        branch_name: Branch that was pushed
        task_id: Associated task ID
        agent_id: Agent who pushed

    Returns:
        True if event was emitted successfully
    """
    git_obj = GitObject(operation="push", branch_name=branch_name)
    context = Context(branch_name=branch_name, task_id=task_id)

    event = FlowspecEvent.create(
        event_type="git.pushed",
        agent_id=agent_id,
        source="cli",
        message=f"Pushed: {branch_name}",
        git=git_obj,
        context=context,
    )

    return emit_event(event)


def emit_pr_created_event(
    pr_number: int,
    branch_name: str,
    task_id: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a PR created event.

    Args:
        pr_number: PR number
        branch_name: Branch for the PR
        task_id: Associated task ID
        agent_id: Agent who created the PR

    Returns:
        True if event was emitted successfully
    """
    context = Context(
        pr_number=pr_number,
        branch_name=branch_name,
        task_id=task_id,
    )

    event = FlowspecEvent.create(
        event_type="git.pr_created",
        agent_id=agent_id,
        source="cli",
        message=f"PR #{pr_number} created",
        context=context,
    )

    return emit_event(event)


def emit_merged_event(
    branch_name: str,
    merge_method: Literal["merge", "squash", "rebase"] = "merge",
    pr_number: int | None = None,
    task_id: str | None = None,
    agent_id: str = "system",
) -> bool:
    """Emit a merged event.

    Args:
        branch_name: Branch that was merged
        merge_method: Method used for merge
        pr_number: PR number (if applicable)
        task_id: Associated task ID
        agent_id: Agent who merged

    Returns:
        True if event was emitted successfully
    """
    git_obj = GitObject(
        operation="merge",
        branch_name=branch_name,
        merge_method=merge_method,
    )
    context = Context(
        branch_name=branch_name,
        pr_number=pr_number,
        task_id=task_id,
    )

    event = FlowspecEvent.create(
        event_type="git.merged",
        agent_id=agent_id,
        source="cli",
        message=f"Merged: {branch_name}",
        git=git_obj,
        context=context,
    )

    return emit_event(event)


__all__ = [
    "emit_branch_created_event",
    "emit_branch_deleted_event",
    "emit_commit_event",
    "emit_worktree_created_event",
    "emit_worktree_removed_event",
    "emit_pushed_event",
    "emit_pr_created_event",
    "emit_merged_event",
]
