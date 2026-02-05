#!/usr/bin/env bash
#
# Hook wrapper: Ensures hooks always run from project root
#
# Usage: run-hook.sh <command> [args...]
#
# This wrapper:
# - Finds the project root (directory containing .claude/)
# - Changes to project root before executing command
# - Uses FAIL-OPEN principle: errors output valid JSON and exit 0
# - Never blocks Claude Code workflow
#
# IMPORTANT: No strict mode (set -euo pipefail) - we must never block AI tools!

# Fail-open helper: output valid JSON and exit 0
fail_open() {
    local reason="${1:-wrapper error}"
    echo "{\"decision\":\"allow\",\"reason\":\"$reason\"}"
    exit 0
}

# Find project root by looking for .claude directory
# Note: Searches up to 10 parent directories. Projects nested deeper than 10 levels
# from the execution directory will fail. Increase max_depth if needed for deeper nesting.
find_project_root() {
    local current_dir="$PWD"
    local max_depth=10  # Maximum directory traversal depth
    local depth=0

    while [[ "$depth" -lt "$max_depth" ]]; do
        if [[ -d "$current_dir/.claude" ]]; then
            echo "$current_dir"
            return 0
        fi

        # Move up one directory
        local parent_dir
        parent_dir="$(dirname "$current_dir" 2>/dev/null)" || return 1
        if [[ "$parent_dir" == "$current_dir" ]]; then
            # Reached filesystem root
            break
        fi
        current_dir="$parent_dir"
        depth=$((depth + 1))
    done

    # Fallback: try to find .claude relative to this script
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}" 2>/dev/null)" 2>/dev/null && pwd 2>/dev/null)" || return 1
    if [[ -d "$script_dir/../.." ]] && [[ -d "$script_dir/../../.claude" ]]; then
        (cd "$script_dir/../.." && pwd) 2>/dev/null
        return 0
    fi

    return 1
}

# Check if command provided - fail open if not
if [[ $# -lt 1 ]]; then
    fail_open "no command specified"
fi

# Find and change to project root - fail open if not found
PROJECT_ROOT="$(find_project_root 2>/dev/null)" || fail_open "could not find project root"
if [[ -z "$PROJECT_ROOT" ]]; then
    fail_open "empty project root"
fi

cd "$PROJECT_ROOT" 2>/dev/null || fail_open "could not cd to project root"

# Execute command with all arguments from project root
# If command fails, output valid JSON and exit 0
"$@" || fail_open "command failed"
