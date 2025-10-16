#!/usr/bin/env bash
#
# run-local-ci.sh - Simulate CI/CD pipeline locally (Inner Loop)
#
# This script runs the same checks that will run in GitHub Actions CI,
# allowing you to catch issues before pushing to remote.
#
# Usage: ./scripts/bash/run-local-ci.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track overall status
OVERALL_STATUS=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Local CI Simulation (Inner Loop)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to print step header
print_step() {
    echo -e "${BLUE}>>> $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
    OVERALL_STATUS=1
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Step 1: Check Python version
print_step "Step 1: Checking Python version"
if python --version | grep -q "Python 3.1[1-9]"; then
    print_success "Python version is 3.11+"
else
    print_error "Python version must be 3.11 or higher"
    python --version
fi
echo ""

# Step 2: Check dependencies
print_step "Step 2: Checking dependencies"
if command -v uv &> /dev/null; then
    print_success "uv is installed"
else
    print_error "uv is not installed. Install from: https://docs.astral.sh/uv/"
fi
echo ""

# Step 3: Sync dependencies
print_step "Step 3: Syncing dependencies"
if uv sync; then
    print_success "Dependencies synced successfully"
else
    print_error "Failed to sync dependencies"
fi
echo ""

# Step 4: Code formatting check
print_step "Step 4: Checking code formatting (ruff format)"
if ruff format --check .; then
    print_success "Code formatting is correct"
else
    print_warning "Code formatting issues found. Run: ruff format ."
    OVERALL_STATUS=1
fi
echo ""

# Step 5: Linting
print_step "Step 5: Running linter (ruff check)"
if ruff check .; then
    print_success "Linting passed"
else
    print_error "Linting failed. Run: ruff check . --fix"
fi
echo ""

# Step 6: Type checking (if mypy is configured)
print_step "Step 6: Type checking"
if command -v mypy &> /dev/null; then
    if mypy src/; then
        print_success "Type checking passed"
    else
        print_error "Type checking failed"
    fi
else
    print_warning "mypy not installed, skipping type checking"
fi
echo ""

# Step 7: Run tests
print_step "Step 7: Running tests (pytest)"
if command -v pytest &> /dev/null; then
    if pytest tests/ -v; then
        print_success "All tests passed"
    else
        print_error "Tests failed"
    fi
else
    print_error "pytest not installed"
fi
echo ""

# Step 8: Check test coverage
print_step "Step 8: Checking test coverage"
if command -v pytest &> /dev/null; then
    if pytest tests/ --cov=src/specify_cli --cov-report=term-missing --cov-fail-under=0; then
        print_success "Coverage report generated"
    else
        print_warning "Coverage check had issues"
    fi
else
    print_warning "Skipping coverage (pytest not installed)"
fi
echo ""

# Step 9: Build package
print_step "Step 9: Building package"
if uv build; then
    print_success "Package built successfully"
else
    print_error "Package build failed"
fi
echo ""

# Step 10: Install and test CLI
print_step "Step 10: Testing CLI installation"
if uv tool install . --force; then
    print_success "CLI installed successfully"

    if specify --help &> /dev/null; then
        print_success "CLI is functional"
    else
        print_error "CLI installation succeeded but command failed"
    fi
else
    print_error "CLI installation failed"
fi
echo ""

# Final summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Summary${NC}"
echo -e "${BLUE}========================================${NC}"

if [ $OVERALL_STATUS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo -e "${GREEN}  Your code is ready to push.${NC}"
else
    echo -e "${RED}✗ Some checks failed.${NC}"
    echo -e "${RED}  Please fix the issues before pushing.${NC}"
fi
echo ""

exit $OVERALL_STATUS
