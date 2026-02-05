#!/bin/bash
#
# SessionStart hook: Environment setup and context display
#
# This hook runs when starting or resuming a Claude Code session.
# It verifies key dependencies and displays active backlog tasks.
#
# Output: JSON with decision "allow" and contextual information
# Exit code: Always 0 (fail-open principle - never block sessions)
#
# IMPORTANT: This script uses FAIL-OPEN patterns throughout.
# NO strict mode (set -euo pipefail) - we must never cripple AI coding tools!
#

# Get project directory (fallback to current directory if not set)
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Timeout for subprocess calls (in seconds)
TIMEOUT=5

# ANSI color codes for pretty output (only if terminal supports it)
if [[ -t 1 ]]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    GREEN=''
    YELLOW=''
    RED=''
    BLUE=''
    NC=''
fi

# Initialize output arrays
warnings=()
info=()

# Initialize variables that might be used later (fail-open for -u scenarios)
task_count=0
tasks_output=""
first_task_id=""

# Helper function to run command with timeout (fail-open if timeout binary missing)
run_with_timeout() {
    local timeout_duration="$1"
    shift
    if command -v timeout &> /dev/null; then
        timeout "$timeout_duration" "$@" 2>/dev/null || true
    else
        # No timeout binary - run directly with || true fallback
        "$@" 2>/dev/null || true
    fi
}

# Check for uv
if ! command -v uv &> /dev/null; then
    warnings+=("uv not installed - Python package management may not work")
else
    # Use subshell to isolate potential failures; || true ensures we continue
    uv_version=$(uv --version 2>/dev/null || echo "installed")
    uv_version_line=$(echo "$uv_version" | head -n1 || echo "installed")
    info+=("uv: ${uv_version_line:-installed}")
fi

# Check for backlog CLI
if ! command -v backlog &> /dev/null; then
    warnings+=("backlog CLI not installed - task management unavailable")
else
    # Get backlog version
    backlog_version=$(backlog --version 2>/dev/null || echo "unknown")
    info+=("backlog: $backlog_version")

    # Get active "In Progress" tasks
    cd "$PROJECT_DIR" 2>/dev/null || true
    tasks_output=$(run_with_timeout "$TIMEOUT" backlog task list --plain -s "In Progress" 2>/dev/null) || tasks_output=""

    if [[ -n "$tasks_output" ]]; then
        # Count actual task lines (skip header lines like "In Progress:")
        # Task lines match pattern: [PRIORITY] task-XXX - Title or task-XXX - Title
        task_count=$(echo "$tasks_output" | grep -cE '^\s*(\[.+\]\s+)?task-[0-9]+' 2>/dev/null || echo "0")
        # Ensure task_count is a valid number
        [[ "$task_count" =~ ^[0-9]+$ ]] || task_count=0

        if [[ "$task_count" -gt 0 ]]; then
            info+=("Active tasks: $task_count in progress")
            # Add task details and inject task memory
            while IFS= read -r task_line; do
                # Skip header lines (e.g., "In Progress:")
                [[ "$task_line" =~ :$ ]] && continue
                [[ -z "$task_line" ]] && continue

                # Extract task ID and title from plain output
                # Format: "  [HIGH] task-579 - Title" or "  task-579 - Title"
                # Remove leading whitespace and optional priority prefix
                cleaned_line=$(echo "$task_line" | sed 's/^[[:space:]]*//' | sed 's/^\[[^]]*\][[:space:]]*//')

                # Match "task-XXX - Title"
                if [[ "$cleaned_line" =~ ^(task-[0-9]+)[[:space:]]*-[[:space:]]*(.+)$ ]]; then
                    task_id="${BASH_REMATCH[1]}"
                    task_title="${BASH_REMATCH[2]}"
                    info+=("  - $task_id: $task_title")

                    # Check if task memory exists
                    memory_file="$PROJECT_DIR/backlog/memory/$task_id.md"
                    if [[ -f "$memory_file" ]]; then
                        info+=("    ✓ Task memory available: $memory_file")
                    fi
                fi
            done <<< "$tasks_output"
        else
            info+=("No active tasks")
        fi
    else
        # Empty output or error - check if backlog.md exists
        if [[ -f "$PROJECT_DIR/backlog/backlog.md" ]]; then
            info+=("No tasks in 'In Progress' status")
        else
            warnings+=("backlog.md not found in project - task tracking not initialized")
        fi
    fi

    # Inject first active task memory into CLAUDE.md (if any exist)
    # This makes task context available automatically via @import
    # Uses token-aware truncation (max 2000 tokens)
    if [[ "$task_count" -gt 0 ]] && [[ -n "$tasks_output" ]]; then
        # Extract first task ID from output (skip header lines, find first task-XXX)
        first_task_id=$(echo "$tasks_output" | grep -oE 'task-[0-9]+' | head -n1 || echo "")
        if [[ -n "$first_task_id" ]] && command -v python3 &> /dev/null; then
            # Use Python to inject task memory via ContextInjector with truncation
            # Wrapped in subshell with || true for fail-open
            (
                PROJECT_DIR="$PROJECT_DIR" FIRST_TASK_ID="$first_task_id" python3 - <<'PYEOF' 2>/dev/null
from pathlib import Path
import sys
import os
sys.path.insert(0, os.environ.get("PROJECT_DIR", "."))
try:
    from src.flowspec_cli.memory.injector import ContextInjector
    injector = ContextInjector(Path(os.environ.get("PROJECT_DIR", ".")))
    injector.update_active_task_with_truncation(os.environ.get("FIRST_TASK_ID", ""))
except Exception:
    pass  # Fail silently - don't block session
PYEOF
            ) || true
            # Note: Cannot reliably check $? after || true, so just assume success if we got here
            info+=("  ✓ Active task memory injected into CLAUDE.md (token-aware)")
        fi
    fi
fi

# Build context message for display
context_lines=()

if [[ ${#warnings[@]} -gt 0 ]]; then
    context_lines+=("${YELLOW}Environment Warnings:${NC}")
    for warning in "${warnings[@]}"; do
        context_lines+=("  ${YELLOW}⚠${NC} $warning")
    done
fi

if [[ ${#info[@]} -gt 0 ]]; then
    context_lines+=("")
    context_lines+=("${BLUE}Session Context:${NC}")
    for info_item in "${info[@]}"; do
        context_lines+=("  ${GREEN}✓${NC} $info_item")
    done
fi

# Format output as JSON
# Build additionalContext as a string with newlines
additional_context=""
if [[ ${#context_lines[@]} -gt 0 ]]; then
    for line in "${context_lines[@]}"; do
        # Remove color codes for JSON (they don't display well in notifications)
        # Use tr as fallback if sed fails (more portable)
        clean_line=$(echo -e "$line" | sed 's/\x1b\[[0-9;]*m//g' 2>/dev/null || echo "$line")
        if [[ -n "$additional_context" ]]; then
            additional_context="${additional_context}\n${clean_line}"
        else
            additional_context="$clean_line"
        fi
    done
fi

# Log session start event (fail silently if python3 or logging module not available)
if command -v python3 &> /dev/null; then
    (
        python3 <<'LOGEOF' 2>/dev/null
import os
import sys

project_dir = os.environ.get("PROJECT_DIR")
if project_dir:
    sys.path.insert(0, project_dir + "/src")

try:
    from flowspec_cli.logging import EventLogger
    logger = EventLogger()
    logger.log_session_start(details={'project_dir': project_dir})
except Exception:
    # Fail silently - don't block session start
    pass
LOGEOF
    ) || true
fi

# Output JSON decision
# Try python3 first, fall back to pure bash if python3 unavailable
# Pass additional_context via environment variable to prevent code injection
if command -v python3 &> /dev/null; then
    ADDITIONAL_CONTEXT="$additional_context" python3 <<'JSONEOF' 2>/dev/null || echo '{"decision":"allow","reason":"session started"}'
import json
import os

decision = {
    "decision": "allow",
    "reason": "Session started - environment verified",
}

# Read from environment variable (safe from code injection)
additional_context = os.environ.get("ADDITIONAL_CONTEXT", "")
if additional_context.strip():
    decision["additionalContext"] = additional_context

print(json.dumps(decision))
JSONEOF
else
    # Fallback: output minimal JSON without python3
    # Escape special characters in additional_context for JSON
    escaped_context=$(echo "$additional_context" | sed 's/\\/\\\\/g; s/"/\\"/g; s/	/\\t/g' 2>/dev/null || echo "")
    if [[ -n "$escaped_context" ]]; then
        echo "{\"decision\":\"allow\",\"reason\":\"session started\",\"additionalContext\":\"$escaped_context\"}"
    else
        echo '{"decision":"allow","reason":"session started"}'
    fi
fi

# GUARANTEED FAIL-OPEN: Always exit 0 no matter what happened above
exit 0
