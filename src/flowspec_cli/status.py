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
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Optional

from flowspec_cli.logging.config import get_config as get_logging_config


def get_flowspec_version() -> str:
    """Get flowspec CLI version using importlib.metadata."""
    try:
        from importlib.metadata import version

        return version("flowspec-cli")
    except Exception:
        # Fallback: try pyproject.toml for development/source installs
        try:
            import tomllib

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
        # Use existing backlog shim to get tasks
        from flowspec_cli.backlog.shim import task_list

        # Get tasks in "In Progress" status
        result = task_list(status="In Progress", plain=True)

        if result and result.strip():
            lines = result.strip().split("\n")
            if lines:
                # Parse first in-progress task (format: "task-123  Description  [In Progress]")
                first_task = lines[0]
                parts = first_task.split()
                if parts:
                    task_id = parts[0]
                    # Extract description (everything between task_id and status)
                    desc_match = re.search(r"task-\d+\s+(.+?)\s+\[", first_task)
                    description = desc_match.group(1) if desc_match else "Unknown"

                    # Try to infer phase from task labels or content
                    phase_keywords = {
                        "assess": "assess",
                        "specify": "specify",
                        "research": "research",
                        "plan": "plan",
                        "implement": "implement",
                        "validate": "validate",
                    }

                    first_task_lower = first_task.lower()
                    for keyword, phase in phase_keywords.items():
                        if keyword in first_task_lower:
                            return (phase, f"{task_id} — {description}")

                    # Default to "implement" if no phase keyword found
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
        # Use existing backlog shim to get tasks
        from flowspec_cli.backlog.shim import task_list

        # Get tasks by status and count them
        in_progress_result = task_list(status="In Progress", plain=True)
        todo_result = task_list(status="To Do", plain=True)
        done_result = task_list(status="Done", plain=True)

        # Count lines (each line is a task)
        if in_progress_result and in_progress_result.strip():
            counts["in_progress"] = len([l for l in in_progress_result.strip().split("\n") if l.strip()])

        if todo_result and todo_result.strip():
            counts["todo"] = len([l for l in todo_result.strip().split("\n") if l.strip()])

        if done_result and done_result.strip():
            counts["done"] = len([l for l in done_result.strip().split("\n") if l.strip()])

    except Exception:
        # Fallback: try to parse from backlog/tasks/ directory
        try:
            tasks_dir = Path.cwd() / "backlog" / "tasks"
            if tasks_dir.exists():
                for task_file in tasks_dir.glob("task-*.md"):
                    try:
                        content = task_file.read_text(encoding="utf-8")
                        # Look for status in frontmatter or body
                        if "status: In Progress" in content or "[In Progress]" in content:
                            counts["in_progress"] += 1
                        elif "status: To Do" in content or "[To Do]" in content:
                            counts["todo"] += 1
                        elif "status: Done" in content or "[Done]" in content:
                            counts["done"] += 1
                    except Exception:
                        pass
        except Exception:
            pass

    return counts


def get_recent_decisions(days: int = 1) -> int:
    """Count recent decisions logged in the last N days."""
    count = 0

    try:
        config = get_logging_config()
        decisions_dir = config.decisions_dir

        if decisions_dir.exists():
            # Check for date-named files (YYYY-MM-DD.jsonl)
            for day_offset in range(days):
                check_date = date.today() - timedelta(days=day_offset)
                log_file = decisions_dir / f"{check_date.isoformat()}.jsonl"

                if log_file.exists():
                    with open(log_file, encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                count += 1

            # Also check session-*.jsonl files (vibe mode)
            for session_file in decisions_dir.glob("session-*.jsonl"):
                try:
                    with open(session_file, encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                count += 1
                except Exception:
                    pass

    except Exception:
        pass

    # Also check .logs/decisions/ (vibe mode location)
    try:
        vibe_decisions_dir = Path.cwd() / ".logs" / "decisions"
        if vibe_decisions_dir.exists():
            # Check date-named files
            for day_offset in range(days):
                check_date = date.today() - timedelta(days=day_offset)
                log_file = vibe_decisions_dir / f"{check_date.isoformat()}.jsonl"

                if log_file.exists():
                    with open(log_file, encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                count += 1

            # Check session files
            for session_file in vibe_decisions_dir.glob("session-*.jsonl"):
                try:
                    with open(session_file, encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                count += 1
                except Exception:
                    pass
    except Exception:
        pass

    return count


def get_recent_events(days: int = 1) -> int:
    """Count recent events logged in the last N days."""
    count = 0

    try:
        config = get_logging_config()
        events_dir = config.events_dir

        if events_dir.exists():
            # Check for date-named files (YYYY-MM-DD.jsonl)
            for day_offset in range(days):
                check_date = date.today() - timedelta(days=day_offset)
                log_file = events_dir / f"{check_date.isoformat()}.jsonl"

                if log_file.exists():
                    with open(log_file, encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                count += 1

            # Also check session-*.jsonl files (vibe mode)
            for session_file in events_dir.glob("session-*.jsonl"):
                try:
                    with open(session_file, encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                count += 1
                except Exception:
                    pass

    except Exception:
        pass

    # Also check .logs/events/ (vibe mode location)
    try:
        vibe_events_dir = Path.cwd() / ".logs" / "events"
        if vibe_events_dir.exists():
            # Check date-named files
            for day_offset in range(days):
                check_date = date.today() - timedelta(days=day_offset)
                log_file = vibe_events_dir / f"{check_date.isoformat()}.jsonl"

                if log_file.exists():
                    with open(log_file, encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                count += 1

            # Check session files
            for session_file in vibe_events_dir.glob("session-*.jsonl"):
                try:
                    with open(session_file, encoding="utf-8") as f:
                        for line in f:
                            if line.strip():
                                count += 1
                except Exception:
                    pass
    except Exception:
        pass

    return count


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

    lines.append(f"Project:   {data['project']}")
    lines.append(f"Version:   {data['version']}")
    lines.append(f"Mode:      {data['mode']}")

    if data['phase']:
        lines.append(f"Phase:     {data['phase']}  ({data['current_task']})")
    else:
        lines.append("Phase:     (no active work)")

    tasks = data['tasks']
    lines.append(
        f"Tasks:     {tasks['in_progress']} in progress, "
        f"{tasks['todo']} to do, "
        f"{tasks['done']} done"
    )

    if data['decisions_today'] > 0:
        lines.append(f"Decisions: {data['decisions_today']} logged today")

    if data['events_today'] > 0:
        lines.append(f"Events:    {data['events_today']} logged today")

    lines.append(f"Next:      {data['next_action']}")

    return "\n".join(lines)


def format_status_json(data: dict[str, Any]) -> str:
    """Format status data as JSON."""
    return json.dumps(data, indent=2)
