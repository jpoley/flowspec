#!/usr/bin/env bash
#
# pre-commit-hook.sh - Pre-commit validation hook (Inner Loop)
#
# This script runs fast validation checks before allowing a commit.
# Install it as a git hook with: ln -s ../../scripts/bash/pre-commit-hook.sh .git/hooks/pre-commit
#
# Or use the install script: ./scripts/bash/install-pre-commit-hook.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Running pre-commit checks...${NC}"
echo ""

# Check if we're in the root of the repository
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: Must be run from repository root${NC}"
    exit 1
fi

# Track status
STATUS=0

# 1. Format check (fast)
echo -e "${BLUE}1. Checking code formatting...${NC}"
if ruff format --check . > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Formatting is correct${NC}"
else
    echo -e "${YELLOW}⚠ Formatting issues detected. Auto-fixing...${NC}"
    ruff format .
    echo -e "${GREEN}✓ Code formatted${NC}"
fi
echo ""

# 2. Linting (fast)
echo -e "${BLUE}2. Running linter...${NC}"
if ruff check . --fix > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Linting passed${NC}"
else
    echo -e "${RED}✗ Linting failed${NC}"
    echo "Run: ruff check . --fix"
    STATUS=1
fi
echo ""

# 3. Quick test run (only fast tests if marked)
echo -e "${BLUE}3. Running quick tests...${NC}"
if command -v pytest &> /dev/null; then
    # Run tests marked as 'quick' or all tests if no markers
    if pytest tests/ -m quick --tb=short > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Quick tests passed${NC}"
    elif pytest tests/ -x --tb=short > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Tests passed${NC}"
    else
        echo -e "${RED}✗ Tests failed${NC}"
        echo "Run: pytest tests/ -v"
        STATUS=1
    fi
else
    echo -e "${YELLOW}⚠ pytest not installed, skipping tests${NC}"
fi
echo ""

# Summary
if [ $STATUS -eq 0 ]; then
    echo -e "${GREEN}✓ Pre-commit checks passed${NC}"
    echo ""
else
    echo -e "${RED}✗ Pre-commit checks failed${NC}"
    echo -e "${RED}  Please fix the issues before committing${NC}"
    echo ""
    exit 1
fi
