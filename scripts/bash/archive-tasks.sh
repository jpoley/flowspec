#!/usr/bin/env bash
set -euo pipefail

# archive-tasks.sh - Archive backlog tasks with flexible filtering
# Usage: ./scripts/bash/archive-tasks.sh [OPTIONS]

# Configuration
BACKLOG_DIR="backlog"
ARCHIVE_DIR="backlog/archive"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Flags
DRY_RUN=false
ARCHIVE_ALL=false
DONE_BY_DATE=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Statistics
TOTAL_ARCHIVED=0
FAILED_TASKS=()

#######################################
# Display usage information
#######################################
show_help() {
    cat <<EOF
archive-tasks.sh - Archive backlog tasks with flexible filtering

USAGE:
    ./scripts/bash/archive-tasks.sh [OPTIONS]

OPTIONS:
    --all, -a           Archive ALL tasks regardless of status
    --done-by DATE      Archive Done tasks updated on or before DATE (YYYY-MM-DD)
    --dry-run           Show what would be archived without making changes
    --help, -h          Show this help message

FILTERING MODES:
    Default (no flags): Archive tasks with status "Done" only
    --all / -a:         Archive ALL tasks (ignores status)
    --done-by DATE:     Archive Done tasks with updated date <= DATE

    Note: --all and --done-by are mutually exclusive

EXIT CODES:
    0 - Success (tasks archived)
    1 - Validation error (CLI missing, invalid args, invalid date)
    2 - No tasks to archive (informational, not an error)
    3 - Partial failures (some tasks failed to archive)

EXAMPLES:
    # Dry run to see what would be archived (Done tasks only)
    ./scripts/bash/archive-tasks.sh --dry-run

    # Archive all Done tasks
    ./scripts/bash/archive-tasks.sh

    # Archive ALL tasks regardless of status
    ./scripts/bash/archive-tasks.sh --all

    # Archive Done tasks updated on or before 2025-12-01
    ./scripts/bash/archive-tasks.sh --done-by 2025-12-01

    # Dry run with date filter
    ./scripts/bash/archive-tasks.sh --done-by 2025-11-01 --dry-run

DATE FORMAT:
    DATE must be in ISO 8601 format: YYYY-MM-DD (e.g., 2025-12-03)

EOF
}

#######################################
# Print colored message
# Arguments:
#   $1 - color code
#   $2 - message
#######################################
print_color() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

#######################################
# Validate date format and parseability
# Arguments:
#   $1 - date string to validate (YYYY-MM-DD)
# Returns:
#   0 if valid, 1 otherwise
#######################################
validate_date() {
    local date_str="$1"

    # Check format with regex
    if ! [[ "$date_str" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        print_color "${RED}" "ERROR: Invalid date format: ${date_str}"
        print_color "${RED}" "Expected format: YYYY-MM-DD (e.g., 2025-12-03)"
        return 1
    fi

    # Platform-specific date validation
    if date --version &>/dev/null; then
        # GNU date
        if ! date -d "$date_str" &>/dev/null; then
            print_color "${RED}" "ERROR: Invalid date: ${date_str}"
            print_color "${RED}" "Date must be a valid calendar date"
            return 1
        fi
    else
        # BSD/macOS date
        if ! date -j -f "%Y-%m-%d" "$date_str" "+%Y-%m-%d" &>/dev/null; then
            print_color "${RED}" "ERROR: Invalid date: ${date_str}"
            print_color "${RED}" "Date must be a valid calendar date"
            return 1
        fi
    fi

    return 0
}

#######################################
# Check prerequisites
# Returns:
#   0 if all prerequisites met, 1 otherwise
#######################################
check_prerequisites() {
    print_color "${BLUE}" "==> Checking prerequisites..."

    # Check if backlog CLI is installed
    if ! command -v backlog &> /dev/null; then
        print_color "${RED}" "ERROR: backlog CLI not found"
        print_color "${RED}" "Please install backlog.md: pnpm install -g @backlog-md/cli"
        return 1
    fi

    # Check if backlog directory exists
    if [[ ! -d "${PROJECT_ROOT}/${BACKLOG_DIR}" ]]; then
        print_color "${RED}" "ERROR: Backlog directory not found: ${BACKLOG_DIR}"
        return 1
    fi

    # Ensure archive directory exists
    mkdir -p "${PROJECT_ROOT}/${ARCHIVE_DIR}"

    print_color "${GREEN}" "✓ Prerequisites check passed"
    return 0
}

#######################################
# Get task metadata from task file
# Arguments:
#   $1 - task ID
# Outputs:
#   Task updated date in YYYY-MM-DD format (or empty string if not found)
# Returns:
#   1 if task file not found, 0 otherwise
#######################################
get_task_updated_date() {
    local task_id="$1"
    local task_file

    # Try to find the task file (could be in tasks/ or directly in backlog/)
    if [[ -d "${PROJECT_ROOT}/${BACKLOG_DIR}/tasks" ]]; then
        # Look in tasks directory first
        # Find files matching "${task_id} - *.md" and filter for exact match
        task_file=$(find "${PROJECT_ROOT}/${BACKLOG_DIR}/tasks" -type f -name "${task_id} - *.md" | \
            awk -F/ -v id="$task_id" '{
                fname = $NF;
                if (fname ~ ("^" id " - .+\\.md$")) print $0;
            }' | head -1)
    fi

    # Fallback to backlog root if not found
    if [[ -z "$task_file" || ! -f "$task_file" ]]; then
        task_file="${PROJECT_ROOT}/${BACKLOG_DIR}/${task_id}.md"
    fi

    if [[ ! -f "$task_file" ]]; then
        return 1
    fi

    # Extract updated date from YAML frontmatter (try both updated: and updated_date:)
    local updated
    updated=$(grep -E "^(updated|updated_date):" "$task_file" | sed 's/^[^:]*:[[:space:]]*//' | head -1)

    # Extract just the date portion (YYYY-MM-DD) if it's a full timestamp
    if [[ "$updated" =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        echo "${BASH_REMATCH[1]}"
    fi
}

#######################################
# Get list of task IDs based on filtering mode
# Outputs:
#   Task IDs, one per line
# Returns:
#   0 if successful, 1 otherwise
#######################################
get_tasks_to_archive() {
    local output
    local task_ids=()

    if [[ "$ARCHIVE_ALL" == true ]]; then
        # Archive ALL tasks
        print_color "${BLUE}" "==> Querying ALL tasks..." >&2
        output=$(cd "${PROJECT_ROOT}" && backlog task list --plain 2>&1) || {
            print_color "${RED}" "ERROR: Failed to query tasks" >&2
            return 1
        }
    else
        # Archive Done tasks only
        print_color "${BLUE}" "==> Querying Done tasks..." >&2
        output=$(cd "${PROJECT_ROOT}" && backlog task list -s Done --plain 2>&1) || {
            print_color "${RED}" "ERROR: Failed to query Done tasks" >&2
            return 1
        }
    fi

    # Parse task IDs from output
    # Format: "  [HIGH] task-67 - Title" or "  task-013 - Title"
    while IFS= read -r line; do
        # Skip empty lines and section headers
        [[ -z "$line" || "$line" =~ ^[A-Z][a-z]+: ]] && continue

        # Extract task ID using regex
        if [[ "$line" =~ [[:space:]]*(task-[0-9]+(\.[0-9]+)?) ]]; then
            local task_id="${BASH_REMATCH[1]}"

            # Apply date filter if specified
            if [[ -n "$DONE_BY_DATE" ]]; then
                local task_date
                task_date=$(get_task_updated_date "$task_id")

                if [[ -z "$task_date" ]]; then
                    print_color "${YELLOW}" "WARNING: Task file for '${task_id}' not found. Skipping task." >&2
                    continue
                fi

                # Compare dates
                if [[ "$task_date" > "$DONE_BY_DATE" ]]; then
                    # Task updated after cutoff date, skip
                    continue
                fi
            fi

            task_ids+=("$task_id")
        fi
    done <<< "$output"

    # Output task IDs (only if array is not empty)
    if [[ ${#task_ids[@]} -gt 0 ]]; then
        printf '%s\n' "${task_ids[@]}"
    fi
}

#######################################
# Archive a single task
# Arguments:
#   $1 - task ID (e.g., "task-67")
# Returns:
#   0 if successful, 1 otherwise
#######################################
archive_task() {
    local task_id="$1"
    # Extract numeric ID for backlog CLI (task-67 -> 67, task-67.01 -> 67.01)
    local numeric_id="${task_id#task-}"

    if [[ "$DRY_RUN" == true ]]; then
        print_color "${YELLOW}" "  [DRY RUN] Would archive: ${task_id}"
        return 0
    fi

    # Archive the task using numeric ID
    local output
    if output=$(cd "${PROJECT_ROOT}" && backlog task archive "${numeric_id}" 2>&1); then
        if [[ "$output" =~ [Aa]rchived ]]; then
            print_color "${GREEN}" "  ✓ Archived: ${task_id}"
            ((TOTAL_ARCHIVED++))
            return 0
        fi
    fi

    print_color "${RED}" "  ✗ Failed to archive: ${task_id}"
    FAILED_TASKS+=("${task_id}")
    return 1
}

#######################################
# Main function
#######################################
main() {
    local task_ids=()

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --all|-a)
                ARCHIVE_ALL=true
                shift
                ;;
            --done-by)
                if [[ -z "${2:-}" ]]; then
                    print_color "${RED}" "ERROR: --done-by requires a date argument (YYYY-MM-DD)"
                    echo ""
                    show_help
                    exit 1
                fi
                DONE_BY_DATE="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                print_color "${RED}" "ERROR: Unknown option: $1"
                echo ""
                show_help
                exit 1
                ;;
        esac
    done

    # Validate mutual exclusivity
    if [[ "$ARCHIVE_ALL" == true && -n "$DONE_BY_DATE" ]]; then
        print_color "${RED}" "ERROR: --all and --done-by are mutually exclusive"
        echo ""
        show_help
        exit 1
    fi

    # Validate date if specified
    if [[ -n "$DONE_BY_DATE" ]]; then
        if ! validate_date "$DONE_BY_DATE"; then
            exit 1
        fi
    fi

    # Check prerequisites
    if ! check_prerequisites; then
        exit 1
    fi

    # Get tasks to archive
    mapfile -t task_ids < <(get_tasks_to_archive)

    if [[ ${#task_ids[@]} -eq 0 ]]; then
        if [[ "$ARCHIVE_ALL" == true ]]; then
            print_color "${YELLOW}" "No tasks to archive."
        elif [[ -n "$DONE_BY_DATE" ]]; then
            print_color "${YELLOW}" "No Done tasks updated on or before ${DONE_BY_DATE} to archive."
        else
            print_color "${YELLOW}" "No Done tasks to archive."
        fi
        exit 2
    fi

    # Display filtering mode
    if [[ "$ARCHIVE_ALL" == true ]]; then
        print_color "${GREEN}" "Found ${#task_ids[@]} task(s) (ALL statuses)"
    elif [[ -n "$DONE_BY_DATE" ]]; then
        print_color "${GREEN}" "Found ${#task_ids[@]} Done task(s) updated on or before ${DONE_BY_DATE}"
    else
        print_color "${GREEN}" "Found ${#task_ids[@]} Done task(s)"
    fi

    if [[ "$DRY_RUN" == true ]]; then
        print_color "${YELLOW}" "==> DRY RUN MODE - No changes will be made"
    fi

    # Archive tasks
    print_color "${BLUE}" "==> Archiving tasks..."
    for task_id in "${task_ids[@]}"; do
        archive_task "$task_id" || true  # Continue even if one fails
    done

    # Report results
    echo ""
    if [[ "$DRY_RUN" == true ]]; then
        print_color "${YELLOW}" "==> DRY RUN completed"
        print_color "${YELLOW}" "Would archive ${#task_ids[@]} task(s)"
        exit 0
    fi

    if [[ ${#FAILED_TASKS[@]} -gt 0 ]]; then
        print_color "${RED}" "==> Completed with errors"
        print_color "${RED}" "Successfully archived: ${TOTAL_ARCHIVED}"
        print_color "${RED}" "Failed to archive: ${#FAILED_TASKS[@]} (${FAILED_TASKS[*]})"
        exit 3
    else
        print_color "${GREEN}" "==> Successfully archived ${TOTAL_ARCHIVED} task(s)"
        exit 0
    fi
}

# Run main function
main "$@"
