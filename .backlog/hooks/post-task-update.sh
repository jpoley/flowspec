#!/usr/bin/env bash
#
# Post-task-update hook for Task Memory lifecycle management
#
# This hook is called after a task status change via backlog CLI.
# It triggers the appropriate task memory lifecycle operations.
#
# Usage: post-task-update.sh <task-id> <old-status> <new-status>
#
# Arguments:
#   task-id     : Task identifier (e.g., "task-42" or "42")
#   old-status  : Previous task status
#   new-status  : New task status
#
# Example:
#   ./post-task-update.sh task-42 "To Do" "In Progress"
#
# Exit codes:
#   0 - Always (fail-open design)
#

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
readonly LOG_FILE="${PROJECT_ROOT}/.specify/logs/task-memory-hook.log"

# Ensure log directory exists
mkdir -p "$(dirname "${LOG_FILE}")"

log() {
    local level="$1"
    shift
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ${level} - $*" >> "${LOG_FILE}"
}

# Parse arguments
if [[ $# -lt 3 ]]; then
    log "ERROR" "Usage: post-task-update.sh <task-id> <old-status> <new-status>"
    exit 0  # Fail open
fi

TASK_ID="$1"
OLD_STATUS="$2"
NEW_STATUS="$3"

# Normalize task ID to task-XXX format
if [[ ! "${TASK_ID}" =~ ^task- ]]; then
    TASK_ID="task-${TASK_ID}"
fi

log "INFO" "Hook triggered: ${TASK_ID} (${OLD_STATUS} → ${NEW_STATUS})"

# Get task title from backlog
get_task_title() {
    local task_id="$1"
    local output

    if output=$(backlog task "${task_id}" --plain 2>/dev/null); then
        # Parse first line: "Task task-XXX - Title Here"
        echo "${output}" | head -1 | sed 's/.*- //'
    else
        echo ""
    fi
}

TASK_TITLE=$(get_task_title "${TASK_ID}")

# Call Python lifecycle manager
call_lifecycle_manager() {
    cd "${PROJECT_ROOT}"

    # Try using uv run first (preferred), fall back to direct python
    if command -v uv &>/dev/null; then
        uv run python -c "
from specify_cli.memory.hooks import on_task_status_change
on_task_status_change('${TASK_ID}', '${OLD_STATUS}', '${NEW_STATUS}', '${TASK_TITLE}')
" 2>>"${LOG_FILE}"
    elif command -v python3 &>/dev/null; then
        python3 -c "
from specify_cli.memory.hooks import on_task_status_change
on_task_status_change('${TASK_ID}', '${OLD_STATUS}', '${NEW_STATUS}', '${TASK_TITLE}')
" 2>>"${LOG_FILE}"
    else
        log "ERROR" "No Python interpreter found"
        return 1
    fi
}

# Execute lifecycle management
if call_lifecycle_manager; then
    log "INFO" "Lifecycle manager completed for ${TASK_ID}"
else
    log "WARNING" "Lifecycle manager failed for ${TASK_ID}"
fi

# Always exit 0 (fail open)
exit 0
