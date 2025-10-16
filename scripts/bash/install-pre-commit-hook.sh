#!/usr/bin/env bash
#
# install-pre-commit-hook.sh - Install pre-commit hook
#
# This script installs the pre-commit hook into .git/hooks/
#
# Usage: ./scripts/bash/install-pre-commit-hook.sh
#

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Installing pre-commit hook...${NC}"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not a git repository${NC}"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create symlink to pre-commit hook
HOOK_PATH=".git/hooks/pre-commit"
SCRIPT_PATH="../../scripts/bash/pre-commit-hook.sh"

if [ -f "$HOOK_PATH" ]; then
    echo -e "${BLUE}Existing pre-commit hook found. Backing up...${NC}"
    mv "$HOOK_PATH" "${HOOK_PATH}.backup.$(date +%Y%m%d%H%M%S)"
fi

cd .git/hooks
ln -s "$SCRIPT_PATH" pre-commit
cd ../..

echo -e "${GREEN}✓ Pre-commit hook installed successfully${NC}"
echo ""
echo "The hook will run automatically before each commit."
echo "To bypass the hook (not recommended), use: git commit --no-verify"
echo ""
