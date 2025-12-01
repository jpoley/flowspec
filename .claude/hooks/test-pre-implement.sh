#!/usr/bin/env bash
# Test suite for pre-implement.sh quality gates

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test workspace
TEST_DIR="$(mktemp -d)"
trap 'rm -rf "$TEST_DIR"' EXIT

# Script under test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRE_IMPLEMENT_SCRIPT="$SCRIPT_DIR/pre-implement.sh"

echo "========================================"
echo "Testing pre-implement.sh quality gates"
echo "========================================"
echo "Test workspace: $TEST_DIR"
echo ""

# Helper function to run a test
run_test() {
    local test_name="$1"
    local expected_exit="$2"
    shift 2
    local test_fn="$@"

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "Test $TESTS_RUN: $test_name ... "

    # Create clean test environment
    rm -rf "$TEST_DIR"/*
    mkdir -p "$TEST_DIR/docs/prd"
    mkdir -p "$TEST_DIR/docs/adr"
    cd "$TEST_DIR"

    # Run test function
    set +e
    $test_fn
    local exit_code=$?
    set -e

    # Check exit code
    if [[ $exit_code -eq $expected_exit ]]; then
        echo -e "${GREEN}PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC} (expected exit $expected_exit, got $exit_code)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Test functions
test_all_gates_pass() {
    # Create valid spec, plan, tasks
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

## Description
This is a complete specification.

## User Story
As a user, I want to do something.

## Acceptance Criteria
- AC1: The feature works
- AC2: Tests pass

## Testing Requirements
We will use pytest for testing.

## Git Commit Requirements
All commits must use DCO sign-off: git commit -s
EOF

    cat > docs/adr/plan.md <<'EOF'
# Implementation Plan

This plan references the acceptance criteria from the spec.
EOF

    cat > tasks.md <<'EOF'
# Tasks

- [ ] Task 1: Implement feature
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_missing_spec() {
    # Create only plan and tasks, no spec
    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_missing_plan() {
    # Create only spec and tasks, no plan
    cat > docs/prd/spec.md <<'EOF'
# Spec
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_missing_tasks() {
    # Create only spec and plan, no tasks
    cat > docs/prd/spec.md <<'EOF'
# Spec
EOF

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_needs_clarification_marker() {
    # Spec with NEEDS CLARIFICATION marker
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

## Description
NEEDS CLARIFICATION: What should this feature do?

## Acceptance Criteria
- AC1: Something

## Testing
Use pytest.

## Git
Use git commit -s
EOF

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_tbd_marker() {
    # Spec with [TBD] marker
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

## Description
This feature will [TBD] do something.

## Acceptance Criteria
- AC1: Something

## Testing
Use pytest.

## Git
Use git commit -s
EOF

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_todo_marker() {
    # Spec with [TODO] marker
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

## Description
[TODO] Add description here.

## Acceptance Criteria
- AC1: Something

## Testing
Use pytest.

## Git
Use git commit -s
EOF

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_empty_spec() {
    # Empty spec file
    touch docs/prd/spec.md

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_missing_dco() {
    # Spec without DCO mention
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

## Description
This is a specification.

## Acceptance Criteria
- AC1: Something

## Testing
Use pytest.
EOF

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_missing_testing() {
    # Spec without testing mention
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

## Description
This is a specification.

## Acceptance Criteria
- AC1: Something

## Git
Use git commit -s
EOF

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_missing_acceptance_criteria() {
    # Spec without acceptance criteria
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

## Description
This is a specification.

## Testing
Use pytest.

## Git
Use git commit -s
EOF

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_skip_quality_gates_flag() {
    # No files at all, but skip flag should bypass
    bash "$PRE_IMPLEMENT_SCRIPT" --skip-quality-gates
}

test_multiple_failures() {
    # Multiple issues: missing files and markers
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

NEEDS CLARIFICATION: Everything

[TBD] Add details
EOF

    # Missing plan.md and tasks.md
    bash "$PRE_IMPLEMENT_SCRIPT"
}

test_mixed_markers() {
    # Some resolved, some not
    cat > docs/prd/spec.md <<'EOF'
# Feature Specification

## Description
This part is fine.

## Details
NEEDS CLARIFICATION: This part needs work.

But this part is also fine.

## Acceptance Criteria
- AC1: Something

## Testing
Use pytest.

## Git
Use git commit -s
EOF

    cat > docs/adr/plan.md <<'EOF'
# Plan
EOF

    cat > tasks.md <<'EOF'
# Tasks
EOF

    bash "$PRE_IMPLEMENT_SCRIPT"
}

# Run all tests
echo "Running tests..."
echo ""

# Test 1: All gates pass (exit 0)
run_test "All gates pass" 0 test_all_gates_pass

# Test 2-4: Missing required files (exit 1)
run_test "Missing spec.md" 1 test_missing_spec
run_test "Missing plan.md" 1 test_missing_plan
run_test "Missing tasks.md" 1 test_missing_tasks

# Test 5-7: Unresolved markers (exit 1)
run_test "NEEDS CLARIFICATION marker" 1 test_needs_clarification_marker
run_test "[TBD] marker" 1 test_tbd_marker
run_test "[TODO] marker" 1 test_todo_marker

# Test 8: Empty spec (exit 1)
run_test "Empty spec.md" 1 test_empty_spec

# Test 9-11: Constitutional violations (exit 1)
run_test "Missing DCO mention" 1 test_missing_dco
run_test "Missing testing mention" 1 test_missing_testing
run_test "Missing acceptance criteria" 1 test_missing_acceptance_criteria

# Test 12: Skip flag (exit 0)
run_test "--skip-quality-gates flag" 0 test_skip_quality_gates_flag

# Test 13-14: Complex scenarios
run_test "Multiple failures" 1 test_multiple_failures
run_test "Mixed markers" 1 test_mixed_markers

# Summary
echo ""
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Tests run:    $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed.${NC}"
    exit 1
fi
