#!/usr/bin/env python3
"""PostToolUse hook for Task Memory lifecycle management.

This hook intercepts Bash commands containing 'backlog task edit' and triggers
the appropriate task memory lifecycle operations when task status changes.

Trigger: Bash tool calls containing 'backlog task edit <id> -s <status>'

Lifecycle Operations:
- To Do → In Progress: Create task memory file
- In Progress → Done: Archive task memory file
- Done → In Progress: Restore task memory from archive
- In Progress → To Do: Delete task memory file
- Done → Archive: Delete archived task memory

Design: Fail-open (always exits 0) to prevent blocking backlog operations.
"""

import json
import logging
import re
import subprocess
import sys
from pathlib import Path

# Configure logging to file for debugging (don't pollute stdout)
LOG_FILE = Path(".specify/logs/task-memory-hook.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_backlog_command(command: str) -> dict | None:
    """Parse a backlog task edit command to extract task ID and status.

    Args:
        command: The Bash command string

    Returns:
        Dict with 'task_id' and 'new_status' if valid command, None otherwise
    """
    # Match: backlog task edit <task-id> -s "<status>" or -s <status>
    # Also match: backlog task edit <task-id> --status "<status>"
    pattern = r'backlog\s+task\s+edit\s+(task-\d+|\d+)\s+.*(?:-s|--status)\s+["\']?([^"\']+)["\']?'

    match = re.search(pattern, command, re.IGNORECASE)
    if not match:
        return None

    task_id = match.group(1)
    new_status = match.group(2).strip()

    # Normalize task_id to task-XXX format
    if not task_id.startswith("task-"):
        task_id = f"task-{task_id}"

    return {"task_id": task_id, "new_status": new_status}


def get_task_old_status(task_id: str) -> str | None:
    """Query backlog CLI to get current task status (before change).

    Note: This runs AFTER the command, so we need to query the backlog
    task and infer the old status from the context.

    Args:
        task_id: Task identifier

    Returns:
        Current status string, or None if query fails
    """
    try:
        result = subprocess.run(
            ["backlog", "task", task_id, "--plain"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            logger.warning(f"Failed to query task {task_id}: {result.stderr}")
            return None

        # Parse output for Status: line
        for line in result.stdout.split("\n"):
            if line.startswith("Status:"):
                return line.split(":", 1)[1].strip()

        return None
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout querying task {task_id}")
        return None
    except Exception as e:
        logger.error(f"Error querying task {task_id}: {e}")
        return None


def get_task_title(task_id: str) -> str:
    """Get task title from backlog CLI.

    Args:
        task_id: Task identifier

    Returns:
        Task title or empty string if not found
    """
    try:
        result = subprocess.run(
            ["backlog", "task", task_id, "--plain"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return ""

        # Parse first line for title
        lines = result.stdout.strip().split("\n")
        if lines:
            # First line format: "Task task-XXX - Title Here"
            first_line = lines[0]
            if " - " in first_line:
                return first_line.split(" - ", 1)[1].strip()

        return ""
    except Exception as e:
        logger.error(f"Error getting task title for {task_id}: {e}")
        return ""


def trigger_lifecycle_manager(
    task_id: str, old_status: str, new_status: str, task_title: str = ""
) -> bool:
    """Trigger the lifecycle manager for a state transition.

    Args:
        task_id: Task identifier
        old_status: Previous task status
        new_status: New task status
        task_title: Optional task title

    Returns:
        True if successful, False otherwise
    """
    try:
        # Import here to avoid import errors if memory module isn't available
        from specify_cli.memory.hooks import on_task_status_change

        on_task_status_change(task_id, old_status, new_status, task_title)
        logger.info(
            f"Lifecycle manager triggered: {task_id} ({old_status} → {new_status})"
        )
        return True
    except ImportError as e:
        logger.error(f"Failed to import memory module: {e}")
        return False
    except Exception as e:
        logger.error(f"Lifecycle manager error: {e}")
        return False


def infer_old_status(
    new_status: str, memory_exists: bool, archived_exists: bool
) -> str:
    """Infer old status based on new status and file state.

    Since we run after the command, we can't query the old status directly.
    We infer it from the new status and whether memory files exist.

    Args:
        new_status: The new status from the command
        memory_exists: Whether active memory file exists
        archived_exists: Whether archived memory file exists

    Returns:
        Inferred old status
    """
    new_normalized = new_status.lower().replace(" ", "_")

    if new_normalized == "in_progress":
        if archived_exists:
            return "Done"  # Restoring from Done
        else:
            return "To Do"  # Starting fresh
    elif new_normalized == "done":
        return "In Progress"
    elif new_normalized == "to_do":
        return "In Progress"  # Reset
    elif new_normalized in ("archive", "archived"):
        return "Done"

    return "To Do"  # Default fallback


def check_memory_files(task_id: str) -> tuple[bool, bool]:
    """Check if memory files exist for a task.

    Args:
        task_id: Task identifier

    Returns:
        Tuple of (active_exists, archived_exists)
    """
    base_path = Path.cwd()
    memory_path = base_path / "backlog" / "memory" / f"{task_id}.md"
    archive_path = base_path / "backlog" / "memory" / "archive" / f"{task_id}.md"

    return memory_path.exists(), archive_path.exists()


def main():
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        input_data = sys.stdin.read()
        if not input_data:
            logger.debug("No input received")
            sys.exit(0)

        # Parse JSON input
        try:
            hook_input = json.loads(input_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse input JSON: {e}")
            sys.exit(0)  # Fail open

        # Check if this is a Bash tool call
        tool_name = hook_input.get("tool_name", "")
        if tool_name != "Bash":
            logger.debug(f"Skipping non-Bash tool: {tool_name}")
            sys.exit(0)

        # Get the command that was executed
        tool_input = hook_input.get("tool_input", {})
        command = tool_input.get("command", "")

        if not command:
            logger.debug("No command in tool input")
            sys.exit(0)

        # Check if this is a backlog task edit command
        if "backlog" not in command or "task" not in command or "edit" not in command:
            logger.debug("Not a backlog task edit command")
            sys.exit(0)

        # Parse the command
        parsed = parse_backlog_command(command)
        if not parsed:
            logger.debug(f"Could not parse backlog command: {command}")
            sys.exit(0)

        task_id = parsed["task_id"]
        new_status = parsed["new_status"]

        logger.info(f"Detected task status change: {task_id} → {new_status}")

        # Check memory file state to infer old status
        memory_exists, archived_exists = check_memory_files(task_id)
        old_status = infer_old_status(new_status, memory_exists, archived_exists)

        logger.debug(
            f"Inferred state: {old_status} → {new_status} "
            f"(memory={memory_exists}, archived={archived_exists})"
        )

        # Get task title for memory creation
        task_title = get_task_title(task_id)

        # Trigger lifecycle manager
        success = trigger_lifecycle_manager(task_id, old_status, new_status, task_title)

        if success:
            logger.info(f"Task memory lifecycle completed for {task_id}")
        else:
            logger.warning(f"Task memory lifecycle failed for {task_id}")

    except Exception as e:
        logger.exception(f"Hook error: {e}")

    # Always exit 0 (fail open)
    sys.exit(0)


if __name__ == "__main__":
    main()
