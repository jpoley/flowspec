#!/usr/bin/env bash
# run-local-ci.sh - Run GitHub Actions locally using act
# Task: task-085 - Local CI Simulation Script
#
# Usage:
#   ./scripts/bash/run-local-ci.sh              # Run all jobs
#   ./scripts/bash/run-local-ci.sh --job lint   # Run specific job
#   ./scripts/bash/run-local-ci.sh --job test   # Run tests only
#   ./scripts/bash/run-local-ci.sh --list       # List available jobs

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ACT_IMAGE="${ACT_IMAGE:-catthehacker/ubuntu:act-latest}"
WORKFLOW_FILE="${WORKFLOW_FILE:-.github/workflows/ci.yml}"
SECRETS_FILE="${SECRETS_FILE:-.secrets}"

log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

check_dependencies() {
    if ! command -v act &> /dev/null; then
        log_error "act is not installed."
        log_info "Install: brew install act (macOS) or see https://github.com/nektos/act"
        exit 1
    fi
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed."
        exit 1
    fi
    if ! docker info &> /dev/null; then
        log_error "Docker daemon not running. Start Docker first."
        exit 1
    fi
}

show_help() {
    cat << 'EOF'
run-local-ci.sh - Run GitHub Actions locally using act

USAGE:
    ./scripts/bash/run-local-ci.sh [OPTIONS]

OPTIONS:
    --job <name>     Run specific job (lint, test, build, security)
    --list           List available jobs
    --dry-run        Preview without executing
    --workflow <f>   Use specific workflow file
    --verbose        Verbose output
    --help           Show help

EXAMPLES:
    ./scripts/bash/run-local-ci.sh                    # Run all jobs
    ./scripts/bash/run-local-ci.sh --job lint         # Lint only (~30s)
    ./scripts/bash/run-local-ci.sh --job test         # Tests only
EOF
}

list_jobs() {
    log_info "Available jobs in ${WORKFLOW_FILE}:"
    if [[ -f "$WORKFLOW_FILE" ]]; then
        grep -E "^\s+[a-zA-Z0-9_-]+:" "$WORKFLOW_FILE" | grep -v "^#" | sed 's/://g' | sed 's/^[[:space:]]*/  /'
    else
        log_error "Workflow not found: ${WORKFLOW_FILE}"
        exit 1
    fi
}

run_act() {
    local job_filter="" dry_run="" verbose="" secrets_arg=""
    while [[ $# -gt 0 ]]; do
        case $1 in
            --job) job_filter="-j $2"; shift 2 ;;
            --dry-run) dry_run="--dryrun"; shift ;;
            --verbose) verbose="--verbose"; shift ;;
            *) shift ;;
        esac
    done

    [[ -f "$SECRETS_FILE" ]] && secrets_arg="--secret-file $SECRETS_FILE"
    [[ ! -f "$WORKFLOW_FILE" ]] && { log_error "Workflow not found: ${WORKFLOW_FILE}"; exit 1; }

    log_info "Running local CI..."
    log_info "Workflow: ${WORKFLOW_FILE}"
    [[ -n "$job_filter" ]] && log_info "Job: ${job_filter#-j }"

    local cmd="act -W ${WORKFLOW_FILE} -P ubuntu-latest=${ACT_IMAGE}"
    [[ -n "$job_filter" ]] && cmd+=" ${job_filter}"
    [[ -n "$dry_run" ]] && cmd+=" ${dry_run}"
    [[ -n "$verbose" ]] && cmd+=" ${verbose}"
    [[ -n "$secrets_arg" ]] && cmd+=" ${secrets_arg}"

    local start=$(date +%s)
    if eval "$cmd"; then
        log_success "CI passed in $(($(date +%s) - start))s"
    else
        log_error "CI failed after $(($(date +%s) - start))s"
        exit 1
    fi
}

main() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h) show_help; exit 0 ;;
            --list) list_jobs; exit 0 ;;
            --workflow) WORKFLOW_FILE="$2"; shift 2 ;;
            *) break ;;
        esac
    done
    check_dependencies
    run_act "$@"
}

main "$@"
