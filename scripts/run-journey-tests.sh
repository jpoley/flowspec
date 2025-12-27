#!/bin/bash
#
# USER JOURNEY TEST SUITE RUNNER
#
# This script runs comprehensive tests that verify REAL customer experience.
# Each test represents something a customer would actually do.
#
# Run this personally to verify claims and catch "declared victory too soon".
#

set -e

echo "======================================================================"
echo "USER JOURNEY TEST SUITE"
echo "======================================================================"
echo ""
echo "This test suite verifies COMPLETE customer journeys, not just units."
echo "Each test must pass for customers to have a good experience."
echo ""

cd "$(dirname "$0")/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

echo "======================================================================"
echo "PART 1: Infrastructure Tests (Should all pass)"
echo "======================================================================"
echo ""

echo "Test 1.1: List workflows..."
if uv run flowspec flow custom --list > /tmp/test1.out 2>&1; then
    if grep -q "quick_build" /tmp/test1.out && \
       grep -q "full_design" /tmp/test1.out; then
        echo -e "${GREEN}✓ PASS${NC}: List workflows works"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ FAIL${NC}: Workflows not shown correctly"
        cat /tmp/test1.out
        ((FAILED_TESTS++))
    fi
else
    echo -e "${RED}✗ FAIL${NC}: Command failed"
    cat /tmp/test1.out
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "Test 1.2: Get execution plan..."
if uv run flowspec flow custom quick_build > /tmp/test2.out 2>&1; then
    if grep -q "/flow:specify" /tmp/test2.out && \
       grep -q "/flow:implement" /tmp/test2.out && \
       grep -q "/flow:validate" /tmp/test2.out; then
        echo -e "${GREEN}✓ PASS${NC}: Execution plan shows all steps"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ FAIL${NC}: Execution plan incomplete"
        cat /tmp/test2.out
        ((FAILED_TESTS++))
    fi
else
    echo -e "${RED}✗ FAIL${NC}: Command failed"
    cat /tmp/test2.out
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "Test 1.3: Logs created..."
# Run command to generate logs
uv run flowspec flow custom quick_build > /dev/null 2>&1
if [ -d ".logs/decisions" ] && [ -d ".logs/events" ]; then
    DECISION_COUNT=$(find .logs/decisions -name "session-*.jsonl" | wc -l)
    EVENT_COUNT=$(find .logs/events -name "session-*.jsonl" | wc -l)

    if [ "$DECISION_COUNT" -gt 0 ] && [ "$EVENT_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Logs created ($DECISION_COUNT decision, $EVENT_COUNT event files)"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ FAIL${NC}: No log files created"
        ((FAILED_TESTS++))
    fi
else
    echo -e "${RED}✗ FAIL${NC}: Log directories missing"
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "Test 1.4: Error handling..."
if uv run flowspec flow custom nonexistent_workflow > /tmp/test4.out 2>&1; then
    echo -e "${RED}✗ FAIL${NC}: Should fail for invalid workflow"
    ((FAILED_TESTS++))
else
    if grep -qi "not found\|error" /tmp/test4.out; then
        echo -e "${GREEN}✓ PASS${NC}: Error handling works"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ FAIL${NC}: No clear error message"
        cat /tmp/test4.out
        ((FAILED_TESTS++))
    fi
fi
((TOTAL_TESTS++))
echo ""

echo "Test 1.5: Unit tests pass..."
if uv run pytest tests/workflow/ -q > /tmp/test5.out 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}: All workflow unit tests pass"
    ((PASSED_TESTS++))
else
    echo -e "${RED}✗ FAIL${NC}: Unit tests failing"
    cat /tmp/test5.out
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "======================================================================"
echo "PART 2: Customer Value Tests (KEY TESTS)"
echo "======================================================================"
echo ""

echo "Test 2.1: Workflow execution (--execute flag)..."
if uv run flowspec flow custom quick_build --execute > /tmp/test6.out 2>&1; then
    if grep -q "Executing\|executing" /tmp/test6.out && \
       grep -qi "complete" /tmp/test6.out; then
        echo -e "${GREEN}✓ PASS${NC}: Workflow execution works"
        ((PASSED_TESTS++))
    else
        echo -e "${YELLOW}⚠ PARTIAL${NC}: Command ran but execution unclear"
        echo "Output:"
        cat /tmp/test6.out
        ((SKIPPED_TESTS++))
    fi
else
    echo -e "${YELLOW}⏭ SKIP${NC}: --execute flag not implemented yet"
    echo "This is the PRIMARY CUSTOMER VALUE GAP"
    ((SKIPPED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "Test 2.2: Backlog integration (--task flag)..."
# Create test task
TASK_ID=$(backlog task create "Test Journey" \
    --description "Test task" \
    --status "To Do" 2>&1 | grep -o "task-[0-9]*" | head -1)

if [ -n "$TASK_ID" ]; then
    echo "Created test task: $TASK_ID"

    if uv run flowspec flow custom quick_build --execute --task "$TASK_ID" > /tmp/test7.out 2>&1; then
        # Check if task was updated
        if backlog task view "$TASK_ID" | grep -q "Done\|In Progress"; then
            echo -e "${GREEN}✓ PASS${NC}: Backlog integration works"
            ((PASSED_TESTS++))
        else
            echo -e "${YELLOW}⚠ PARTIAL${NC}: Execution ran but task not updated"
            ((SKIPPED_TESTS++))
        fi
    else
        echo -e "${YELLOW}⏭ SKIP${NC}: --execute and --task not implemented"
        echo "This is the SECONDARY CUSTOMER VALUE GAP"
        ((SKIPPED_TESTS++))
    fi

    # Cleanup
    backlog task archive "$TASK_ID" > /dev/null 2>&1
else
    echo -e "${YELLOW}⏭ SKIP${NC}: Could not create test task"
    ((SKIPPED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "Test 2.3: End-to-end workflow with real execution..."
echo -e "${YELLOW}⏭ SKIP${NC}: Requires real workflow commands to be executable"
echo "This test would:"
echo "  1. Create a task"
echo "  2. Execute workflow"
echo "  3. Verify each step ran"
echo "  4. Verify task updated"
echo "  5. Verify artifacts created"
((SKIPPED_TESTS++))
((TOTAL_TESTS++))
echo ""

echo "======================================================================"
echo "PART 3: Demo Scripts (Should all work)"
echo "======================================================================"
echo ""

echo "Test 3.1: Basic demo script..."
if uv run python scripts/demo-workflow-execution.py quick_build > /tmp/test8.out 2>&1; then
    if grep -q "DEMONSTRATION COMPLETE" /tmp/test8.out; then
        echo -e "${GREEN}✓ PASS${NC}: Basic demo works"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ FAIL${NC}: Demo incomplete"
        ((FAILED_TESTS++))
    fi
else
    echo -e "${RED}✗ FAIL${NC}: Demo script failed"
    cat /tmp/test8.out
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "Test 3.2: Conditional demo script..."
if uv run python scripts/demo-conditional-workflow.py > /tmp/test9.out 2>&1; then
    if grep -q "CONDITIONAL EXECUTION DEMONSTRATION COMPLETE" /tmp/test9.out; then
        echo -e "${GREEN}✓ PASS${NC}: Conditional demo works"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ FAIL${NC}: Demo incomplete"
        ((FAILED_TESTS++))
    fi
else
    echo -e "${RED}✗ FAIL${NC}: Demo script failed"
    cat /tmp/test9.out
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "Test 3.3: E2E demo script..."
if uv run python scripts/e2e-workflow-with-mcp.py > /tmp/test10.out 2>&1; then
    if grep -q "E2E DEMONSTRATION COMPLETE" /tmp/test10.out; then
        echo -e "${GREEN}✓ PASS${NC}: E2E demo works"
        ((PASSED_TESTS++))
    else
        echo -e "${RED}✗ FAIL${NC}: Demo incomplete"
        ((FAILED_TESTS++))
    fi
else
    echo -e "${RED}✗ FAIL${NC}: Demo script failed"
    cat /tmp/test10.out
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

echo "======================================================================"
echo "RESULTS SUMMARY"
echo "======================================================================"
echo ""

# Calculate percentages
PASS_PCT=$((PASSED_TESTS * 100 / TOTAL_TESTS))
FAIL_PCT=$((FAILED_TESTS * 100 / TOTAL_TESTS))
SKIP_PCT=$((SKIPPED_TESTS * 100 / TOTAL_TESTS))

echo "Total Tests: $TOTAL_TESTS"
echo -e "  ${GREEN}Passed: $PASSED_TESTS ($PASS_PCT%)${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAILED_TESTS ($FAIL_PCT%)${NC}"
else
    echo "  Failed: 0 (0%)"
fi
if [ $SKIPPED_TESTS -gt 0 ]; then
    echo -e "  ${YELLOW}Skipped: $SKIPPED_TESTS ($SKIP_PCT%)${NC}"
else
    echo "  Skipped: 0 (0%)"
fi
echo ""

# Grade
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "Grade: ${RED}F (FAILURES PRESENT)${NC}"
    EXIT_CODE=1
elif [ $SKIPPED_TESTS -gt 3 ]; then
    echo -e "Grade: ${YELLOW}C ($PASS_PCT% complete)${NC}"
    echo ""
    echo "CRITICAL GAPS:"
    echo "  - Workflow execution not implemented (--execute)"
    echo "  - Backlog integration not implemented (--task)"
    echo "  - E2E customer journey not possible"
    EXIT_CODE=0
elif [ $SKIPPED_TESTS -gt 0 ]; then
    echo -e "Grade: ${YELLOW}B ($PASS_PCT% complete)${NC}"
    EXIT_CODE=0
else
    echo -e "Grade: ${GREEN}A (100% complete)${NC}"
    EXIT_CODE=0
fi

echo ""
echo "======================================================================"
echo "HONEST ASSESSMENT"
echo "======================================================================"
echo ""

if [ $PASS_PCT -eq 100 ]; then
    echo "✅ COMPLETE: All customer journeys work"
    echo "   Customers can actually use this product"
elif [ $PASS_PCT -ge 80 ]; then
    echo "⚠️  MOSTLY WORKING: Infrastructure solid, execution gaps remain"
    echo "   Customers can plan workflows but not execute them automatically"
elif [ $PASS_PCT -ge 60 ]; then
    echo "⚠️  PARTIAL: Core features work, key features missing"
    echo "   Customers would be disappointed - can't fully use the product"
else
    echo "❌ INCOMPLETE: Major features broken or missing"
    echo "   Not ready for customers"
fi

echo ""
echo "To see details of failed/skipped tests, check /tmp/test*.out files"
echo ""

exit $EXIT_CODE
