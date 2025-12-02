#!/usr/bin/env bash
# JP Spec Kit - Custom Statusline for Claude Code
# Format: [Phase] task-ID (N/M) | branch*
# Performance: Optimized for < 100ms execution

set -euo pipefail

# Exit early if not in a git repo
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# Get git branch with dirty indicator (fast - no external deps)
get_git_info() {
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || return

    # Check for uncommitted changes (staged, unstaged, untracked)
    if ! git diff-index --quiet HEAD -- 2>/dev/null || \
       [[ -n "$(git ls-files --others --exclude-standard 2>/dev/null | head -1)" ]]; then
        echo "${branch}*"
    else
        echo "$branch"
    fi
}

# Get task and phase info (requires backlog CLI)
get_task_phase() {
    command -v backlog >/dev/null 2>&1 || return

    # Parse backlog output - format is "  [PRIORITY] task-XXX - Title"
    local task_line task_id
    task_line=$(backlog task list --plain -s "In Progress" 2>/dev/null | grep -E '^\s*\[' | head -1) || return
    [[ -z "$task_line" ]] && return

    # Extract task ID (e.g., "task-188")
    task_id=$(echo "$task_line" | grep -oE 'task-[0-9]+') || return
    [[ -z "$task_id" ]] && return

    local details
    details=$(backlog task "$task_id" --plain 2>/dev/null) || return

    # Extract phase from workflow label
    local phase=""
    local labels
    labels=$(echo "$details" | grep "^Labels:" | cut -d: -f2-)

    for label in $labels; do
        label=$(echo "$label" | xargs | tr -d ',"'"'"')
        if [[ "$label" == workflow:* ]]; then
            local state="${label#workflow:}"
            case "$state" in
                "To Do"|"Assessed") phase="Assess" ;;
                "Specified") phase="Specify" ;;
                "Researched") phase="Research" ;;
                "Planned") phase="Plan" ;;
                "In Implementation") phase="Impl" ;;
                "Validated") phase="Valid" ;;
                "Deployed") phase="Deploy" ;;
                "Done") phase="Done" ;;
                *) phase="${state:0:8}" ;;
            esac
            break
        fi
    done

    # Count acceptance criteria (use wc -l for reliable counting)
    local checked total
    checked=$(echo "$details" | grep -E '^\- \[x\]' | wc -l)
    total=$(echo "$details" | grep -E '^\- \[[ x]\]' | wc -l)

    # Output phase and task info (pipe-delimited)
    local task_info="$task_id"
    [[ "$total" -gt 0 ]] && task_info="$task_id ($checked/$total)"

    printf "%s|%s" "$phase" "$task_info"
}

# Main - assemble statusline
main() {
    local git_info phase_task phase task output=""

    # Get git info (always fast)
    git_info=$(get_git_info 2>/dev/null || echo "")

    # Get task/phase info (single call for both)
    phase_task=$(get_task_phase 2>/dev/null || printf "none|none")
    phase="${phase_task%%|*}"
    task="${phase_task#*|}"

    # Build output
    [[ -n "$phase" && "$phase" != "none" ]] && output="[$phase]"
    [[ -n "$task" && "$task" != "none" ]] && output="${output:+$output }$task"
    [[ -n "$git_info" ]] && output="${output:+$output | }$git_info"

    echo "$output"
}

main
