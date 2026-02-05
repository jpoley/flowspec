#!/bin/bash
#
# PostToolUse hook: Auto-lint Python files
#
# Runs 'ruff check --fix' on Python files after Edit/Write operations
# Returns JSON decision with linting results
#
# IMPORTANT: No strict mode - uses fail-open principle

# Fail-open helper
allow_and_exit() {
    local reason="${1:-ok}"
    echo "{\"decision\":\"allow\",\"reason\":\"$reason\"}"
    exit 0
}

# Read JSON input from stdin (fail-open if cat fails)
input=$(cat 2>/dev/null) || allow_and_exit "failed to read stdin"

# Extract tool name and file path using jq if available, otherwise use Python
if command -v jq &> /dev/null; then
    tool_name=$(echo "$input" | jq -r '.tool_name // ""' 2>/dev/null) || tool_name=""
    file_path=$(echo "$input" | jq -r '.tool_input.file_path // ""' 2>/dev/null) || file_path=""
elif command -v python3 &> /dev/null; then
    # Fallback to Python for JSON parsing
    tool_name=$(echo "$input" | python3 -c "import json, sys; data = json.load(sys.stdin); print(data.get('tool_name', ''))" 2>/dev/null) || tool_name=""
    file_path=$(echo "$input" | python3 -c "import json, sys; data = json.load(sys.stdin); print(data.get('tool_input', {}).get('file_path', ''))" 2>/dev/null) || file_path=""
else
    allow_and_exit "no JSON parser available"
fi

# Only process Write and Edit tools
if [[ "$tool_name" != "Write" && "$tool_name" != "Edit" ]]; then
    allow_and_exit "not a Write/Edit tool"
fi

# Check if file is a Python file
if [[ ! "$file_path" =~ \.py$ ]]; then
    allow_and_exit "not a Python file"
fi

# Check if file exists
if [[ ! -f "$file_path" ]]; then
    allow_and_exit "file does not exist"
fi

# Check if ruff is available
if ! command -v ruff &> /dev/null; then
    allow_and_exit "ruff not installed"
fi

# Run ruff check with auto-fix (capture output, fail-open on any error)
output=$(ruff check --fix "$file_path" 2>&1) || true

if echo "$output" | grep -q "fixed" 2>/dev/null; then
    echo "{\"decision\":\"allow\",\"reason\":\"auto-fixed linting issues\"}"
elif echo "$output" | grep -qE "error|Error" 2>/dev/null; then
    # Linting found issues but couldn't fix - still allow, just report
    echo "{\"decision\":\"allow\",\"reason\":\"linting issues found (may need manual fix)\"}"
else
    allow_and_exit "no linting issues"
fi

exit 0
