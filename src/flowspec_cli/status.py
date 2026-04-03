"""Flowspec status command - workflow orientation dashboard.

Provides instant project orientation showing:
- Project name and flowspec version
- Active workflow mode (vibe / light / full SDD)
- Current workflow phase
- In-progress backlog tasks
- Recent decisions and events
- Next recommended action
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from flowspec_cli.logging.config import get_config as get_logging_config
from flowspec_cli.workflow.config import WorkflowConfig


def get_flowspec_version() -> str:
    """Get flowspec CLI version from pyproject.toml."""
    try:
        import tomllib

        # Try to find pyproject.toml
        current_dir = Path(__file__).parent
        while current_dir.parent != current_dir:
            pyproject = current_dir / "pyproject.toml"
            if pyproject.exists():
                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                    return data.get("project", {}).get("version", "unknown")
            current_dir = current_dir.parent
    except Exception:
        pass
    return "unknown"


def get_project_name() -> str:
    """Get project name from directory or constitution."""
    cwd = Path.cwd()

    # Try to read from constitution
    constitution_paths = [
        cwd / "memory" / "constitution.md",
        cwd / ".flowspec" / "constitution.md",
    ]

    for const_path in constitution_paths:
        if const_path.exists():
            try:
                content = const_path.read_text(encoding="utf-8")
                # Look for project name in first heading or title
                for line in content.split("\n")[:20]:
                    if line.startswith("# "):
                        return line[2:].strip()
            except Exception:
                pass

    # Fallback to directory name
    return cwd.name


def get_workflow_mode() -> str:
    """Detect workflow mode: vibe / light / full SDD.

    Full SDD: Has flowspec_workflow.yml
    Vibe: Has .logs/ directory but no workflow config
    Light: Somewhere in between
    """
    cwd = Path.cwd()

    # Check for workflow config
    config_exists = any([
        (cwd / "flowspec_workflow.yml").exists(),
        (cwd / "flowspec_workflow.yaml").exists(),
        (cwd / "memory" / "flowspec_workflow.yml").exists(),
    ])

    if config_exists:
        return "Full SDD"

    # Check for .logs directory (vibe mode)
    if (cwd / ".logs").exists():
        return "Vibe"

    return "Light"


def get_current_phase() -> tuple[Optional[str], Optional[str]]:
    """Get current workflow phase from active backlog tasks.

    Returns:
        (phase_name, task_description) or (None, None)
    """
    try:
        # Try to use backlog MCP client to get tasks
        from flowspec_cli.backlog.mcp_client import get_backlog_tasks

        tasks = get_backlog_tasks(status="In Progress")
        if tasks:
            # Get first in-progress task
            task = tasks[0]
            task_id = task.get("id", "")
            description = task.get("title", "")

            # Try to infer phase from task metadata or labels
            metadata = task.get("metadata", {})
            labels = metadata.get("labels", [])

            # Map labels to phases
            phase_map = {
                "assess": "assess",
                "specify": "specify",
                "research": "research",
                "plan": "plan",
                "implement": "implement",
                "validate": "validate",
            }

            for label in labels:
                label_lower = label.lower()
                for key, phase in phase_map.items():
                    if key in label_lower:
                        return (phase, f"{task_id} — {description}")

            # Default to "implement" if no phase label found
            return ("implement", f"{task_id} — {description}")

    except Exception:
        pass

    return (None, None)


def get_task_counts() -> dict[str, int]:
    """Get counts of tasks by status.

    Returns:
        {"in_progress": N, "todo": N, "done": N}
    """
    counts = {"in_progress": 0, "todo": 0, "done": 0}

    try:
        from flowspec_cli.backlog.mcp_client import get_backlog_tasks

        # Get tasks by status
        in_progress = get_backlog_tasks(status="In Progress")
        todo = get_backlog_tasks(status="To Do")
        done = get_backlog_tasks(status="Done")

        counts["in_progress"] = len(in_progress) if in_progress else 0
        counts["todo"] = len(todo) if todo else 0
        counts["done"] = len(done) if done else 0

    except Exception:
        # Fallback: try to parse backlog.md directly
        try:
            backlog_path = Path.cwd() / "backlog" / "backlog.md"
            if backlog_path.exists():
                content = backlog_path.read_text(encoding="utf-8")

                # Simple regex counting
                import re
                in_progress_matches = re.findall(r'\[In Progress\]', content)
                todo_matches = re.findall(r'\[To Do\]', content)
                done_matches = re.findall(r'\[Done\]', content)

                counts["in_progress"] = len(in_progress_matches)
                counts["todo"] = len(todo_matches)
                counts["done"] = len(done_matches)
        except Exception:
            pass

    return counts


def get_recent_decisions(days: int = 1) -> int:
    """Count recent decisions logged in the last N days."""
    try:
        config = get_logging_config()
        decisions_dir = config.decisions_dir

        if not decisions_dir.exists():
            return 0

        count = 0
        cutoff_date = date.today() - timedelta(days=days - 1)

        # Check decision log files for recent days
        for day_offset in range(days):
            check_date = date.today() - timedelta(days=day_offset)
            log_file = decisions_dir / f"{check_date.isoformat()}.jsonl"

            if log_file.exists():
                with open(log_file, encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            count += 1

        return count
    except Exception:
        return 0


def get_recent_events(days: int = 1) -> int:
    """Count recent events logged in the last N days."""
    try:
        config = get_logging_config()
        events_dir = config.events_dir

        if not events_dir.exists():
            return 0

        count = 0

        # Check event log files for recent days
        for day_offset in range(days):
            check_date = date.today() - timedelta(days=day_offset)
            log_file = events_dir / f"{check_date.isoformat()}.jsonl"

            if log_file.exists():
                with open(log_file, encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            count += 1

        return count
    except Exception:
        return 0


def get_next_action(phase: Optional[str], task_counts: dict[str, int]) -> str:
    """Determine next recommended action based on current state."""
    # If there's an in-progress task, continue it
    if phase:
        phase_commands = {
            "assess": "/flow:assess",
            "specify": "/flow:specify",
            "research": "/flow:research",
            "plan": "/flow:plan",
            "implement": "/flow:implement",
            "validate": "/flow:validate",
        }
        return phase_commands.get(phase, "/flow:implement")

    # If there are todo tasks, start one
    if task_counts.get("todo", 0) > 0:
        return "/flow:assess (start new task)"

    # No tasks
    return "Create tasks with /flow:specify"


def get_status_data() -> dict[str, Any]:
    """Gather all status information.

    Returns:
        Dictionary containing all status data.
    """
    project_name = get_project_name()
    version = get_flowspec_version()
    mode = get_workflow_mode()
    phase, task_desc = get_current_phase()
    task_counts = get_task_counts()
    decisions_count = get_recent_decisions(days=1)
    events_count = get_recent_events(days=1)
    next_action = get_next_action(phase, task_counts)

    return {
        "project": project_name,
        "version": version,
        "mode": mode,
        "phase": phase,
        "current_task": task_desc,
        "tasks": task_counts,
        "decisions_today": decisions_count,
        "events_today": events_count,
        "next_action": next_action,
    }


def format_status_human(data: dict[str, Any]) -> str:
    """Format status data for human-readable output."""
    lines = []

    lines.append(f"Project:  {data['project']}")
    lines.append(f"Mode:     {data['mode']}")

    if data['phase']:
        lines.append(f"Phase:    {data['phase']}  ({data['current_task']})")
    else:
        lines.append("Phase:    (no active work)")

    tasks = data['tasks']
    lines.append(
        f"Tasks:    {tasks['in_progress']} in progress, "
        f"{tasks['todo']} to do, "
        f"{tasks['done']} done"
    )

    if data['decisions_today'] > 0:
        lines.append(f"Decisions: {data['decisions_today']} logged today")

    if data['events_today'] > 0:
        lines.append(f"Events:    {data['events_today']} logged today")

    lines.append(f"Next:     {data['next_action']}")

    return "\n".join(lines)


def format_status_json(data: dict[str, Any]) -> str:
    """Format status data as JSON."""
    return json.dumps(data, indent=2)
