"""Janitor state writer module.

This module provides functions to write janitor state files including
recording run timestamps, updating pending cleanup items, and audit logging.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .reader import PendingCleanup, read_pending_cleanup


def ensure_state_dir(project_root: Path) -> Path:
    """Ensure the state directory exists.

    Args:
        project_root: Root directory of the project.

    Returns:
        Path to .specify/state/ directory.
    """
    state_dir = project_root / ".specify" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def record_janitor_run(
    state_dir: Path,
    *,
    timestamp: Optional[datetime] = None,
) -> datetime:
    """Record that janitor was run successfully.

    Args:
        state_dir: Path to .specify/state/ directory.
        timestamp: Optional timestamp (defaults to now).

    Returns:
        The recorded timestamp.
    """
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    timestamp_file = state_dir / "janitor-last-run"
    timestamp_file.write_text(timestamp.isoformat(), encoding="utf-8")

    return timestamp


def update_pending_cleanup(
    state_dir: Path,
    pending: PendingCleanup,
) -> None:
    """Write pending cleanup items to state file.

    Args:
        state_dir: Path to .specify/state/ directory.
        pending: Pending cleanup items to write.
    """
    cleanup_file = state_dir / "pending-cleanup.json"

    # Build JSON structure
    data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "merged_branches": [
            {
                "name": b.name,
                "reason": b.reason,
                "identified_at": b.identified_at.isoformat()
                if b.identified_at
                else None,
            }
            for b in pending.merged_branches
        ],
        "orphaned_worktrees": [
            {
                "path": w.path,
                "identified_at": w.identified_at.isoformat()
                if w.identified_at
                else None,
            }
            for w in pending.orphaned_worktrees
        ],
        "non_compliant_branches": pending.non_compliant_branches,
    }

    cleanup_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


def add_pending_branch(
    state_dir: Path,
    branch_name: str,
    reason: str,
) -> None:
    """Add a branch to pending cleanup.

    Args:
        state_dir: Path to .specify/state/ directory.
        branch_name: Name of the branch.
        reason: Why it's pending cleanup.
    """
    from .reader import PendingBranch

    pending = read_pending_cleanup(state_dir)

    # Check if already in list
    existing_names = {b.name for b in pending.merged_branches}
    if branch_name in existing_names:
        return

    pending.merged_branches.append(
        PendingBranch(
            name=branch_name,
            reason=reason,
            identified_at=datetime.now(timezone.utc),
        )
    )

    update_pending_cleanup(state_dir, pending)


def add_pending_worktree(
    state_dir: Path,
    worktree_path: str,
) -> None:
    """Add a worktree to pending cleanup.

    Args:
        state_dir: Path to .specify/state/ directory.
        worktree_path: Path to the worktree.
    """
    from .reader import PendingWorktree

    pending = read_pending_cleanup(state_dir)

    # Check if already in list
    existing_paths = {w.path for w in pending.orphaned_worktrees}
    if worktree_path in existing_paths:
        return

    pending.orphaned_worktrees.append(
        PendingWorktree(
            path=worktree_path,
            identified_at=datetime.now(timezone.utc),
        )
    )

    update_pending_cleanup(state_dir, pending)


def add_non_compliant_branch(
    state_dir: Path,
    branch_name: str,
    reason: str,
) -> None:
    """Add a branch with naming issues to pending state.

    Args:
        state_dir: Path to .specify/state/ directory.
        branch_name: Name of the branch.
        reason: Why it's non-compliant.
    """
    pending = read_pending_cleanup(state_dir)
    pending.non_compliant_branches[branch_name] = reason
    update_pending_cleanup(state_dir, pending)


def clear_pending_cleanup(
    state_dir: Path,
    *,
    clear_branches: bool = True,
    clear_worktrees: bool = True,
    clear_non_compliant: bool = False,
) -> None:
    """Clear pending cleanup items after successful cleanup.

    Args:
        state_dir: Path to .specify/state/ directory.
        clear_branches: Whether to clear merged branches.
        clear_worktrees: Whether to clear orphaned worktrees.
        clear_non_compliant: Whether to clear non-compliant branches (usually not).
    """
    pending = read_pending_cleanup(state_dir)

    if clear_branches:
        pending.merged_branches = []

    if clear_worktrees:
        pending.orphaned_worktrees = []

    if clear_non_compliant:
        pending.non_compliant_branches = {}

    update_pending_cleanup(state_dir, pending)


def write_audit_log(
    project_root: Path,
    action: str,
    details: Optional[str] = None,
) -> None:
    """Append an entry to the janitor audit log.

    Args:
        project_root: Root directory of the project.
        action: Short description of the action (e.g., "Pruned 3 branches").
        details: Optional additional details.
    """
    audit_file = project_root / ".specify" / "audit.log"
    audit_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = f"[{timestamp}] JANITOR: {action}"

    if details:
        entry += f"\n[{timestamp}] JANITOR: {details}"

    with audit_file.open("a", encoding="utf-8") as f:
        f.write(entry + "\n")


def generate_cleanup_report(
    pruned_branches: list[tuple[str, str]],
    cleaned_worktrees: list[str],
    non_compliant: dict[str, str],
    protected_skipped: list[str],
) -> str:
    """Generate a human-readable cleanup report.

    Args:
        pruned_branches: List of (branch_name, reason) tuples for pruned branches.
        cleaned_worktrees: List of worktree paths that were cleaned.
        non_compliant: Dict of branch_name -> reason for non-compliant branches.
        protected_skipped: List of protected branches that were skipped.

    Returns:
        Formatted report string.
    """
    lines = [
        "JANITOR CLEANUP REPORT",
        "======================",
        "",
    ]

    # Pruned branches
    lines.append(f"Branches Pruned: {len(pruned_branches)}")
    for name, reason in pruned_branches:
        lines.append(f"  - {name} ({reason})")
    if not pruned_branches:
        lines.append("  (none)")
    lines.append("")

    # Cleaned worktrees
    lines.append(f"Worktrees Cleaned: {len(cleaned_worktrees)}")
    for path in cleaned_worktrees:
        lines.append(f"  - {path}")
    if not cleaned_worktrees:
        lines.append("  (none)")
    lines.append("")

    # Non-compliant branches (warnings only)
    lines.append(f"Non-Compliant Branches: {len(non_compliant)}")
    for name, reason in non_compliant.items():
        lines.append(f"  - {name} ({reason})")
    if not non_compliant:
        lines.append("  (none)")
    lines.append("")

    # Protected branches skipped
    lines.append(f"Protected Branches Skipped: {len(protected_skipped)}")
    for name in protected_skipped:
        lines.append(f"  - {name}")
    if not protected_skipped:
        lines.append("  (none)")

    return "\n".join(lines)
