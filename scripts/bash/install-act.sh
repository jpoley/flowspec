#!/usr/bin/env bash
#
# install-act.sh - Install act (GitHub Actions local runner)
#
# This script installs 'act' which allows running GitHub Actions workflows locally
# for testing before pushing to remote.
#
# Usage: ./scripts/bash/install-act.sh [--auto]
#
# Options:
#   --auto    Automatically install without prompting (uses Homebrew on macOS, downloads binary on Linux)
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

# Parse arguments
AUTO_INSTALL=false
if [[ "$1" == "--auto" ]]; then
    AUTO_INSTALL=true
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  act Installation Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "act allows you to run GitHub Actions workflows locally for testing."
echo "Repository: https://github.com/nektos/act"
echo ""

# Check if act is already installed
if command -v act &> /dev/null; then
    ACT_VERSION=$(act --version 2>&1 | head -n 1 || echo "unknown")
    echo -e "${GREEN}✓ act is already installed${NC}"
    echo "  Version: $ACT_VERSION"
    echo ""
    echo "To update act, use your package manager or re-run this script."
    exit 0
fi

echo -e "${YELLOW}act is not installed${NC}"
echo ""

# Installation instructions based on OS
case $OS in
    macos)
        echo -e "${BLUE}Installation options for macOS:${NC}"
        echo ""
        echo "1. Homebrew (recommended):"
        echo "   brew install act"
        echo ""
        echo "2. Manual download:"
        echo "   Visit: https://github.com/nektos/act/releases"
        echo ""

        if [ "$AUTO_INSTALL" = true ]; then
            echo -e "${YELLOW}Auto-installing with Homebrew...${NC}"
            if command -v brew &> /dev/null; then
                brew install act
                echo -e "${GREEN}✓ act installed successfully${NC}"
            else
                echo -e "${RED}✗ Homebrew not found${NC}"
                echo "Install Homebrew from: https://brew.sh"
                exit 1
            fi
        else
            echo -n "Would you like to install using Homebrew? (y/n): "
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                if command -v brew &> /dev/null; then
                    brew install act
                    echo -e "${GREEN}✓ act installed successfully${NC}"
                else
                    echo -e "${RED}✗ Homebrew not found${NC}"
                    echo "Install Homebrew from: https://brew.sh"
                    exit 1
                fi
            else
                echo "Please install act manually from: https://github.com/nektos/act/releases"
                exit 0
            fi
        fi
        ;;

    linux)
        echo -e "${BLUE}Installation options for Linux:${NC}"
        echo ""
        echo "1. Download binary (recommended):"
        echo "   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
        echo ""
        echo "2. Package managers:"
        echo "   Arch: yay -S act"
        echo "   Homebrew: brew install act"
        echo ""
        echo "3. Manual download:"
        echo "   Visit: https://github.com/nektos/act/releases"
        echo ""

        if [ "$AUTO_INSTALL" = true ]; then
            echo -e "${YELLOW}Auto-installing via installer script...${NC}"
            curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
            echo -e "${GREEN}✓ act installed successfully${NC}"
        else
            echo -n "Would you like to install using the installer script? (requires sudo) (y/n): "
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
                echo -e "${GREEN}✓ act installed successfully${NC}"
            else
                echo "Please install act manually from: https://github.com/nektos/act/releases"
                exit 0
            fi
        fi
        ;;

    windows)
        echo -e "${BLUE}Installation options for Windows:${NC}"
        echo ""
        echo "1. Chocolatey:"
        echo "   choco install act-cli"
        echo ""
        echo "2. Scoop:"
        echo "   scoop install act"
        echo ""
        echo "3. Manual download:"
        echo "   Visit: https://github.com/nektos/act/releases"
        echo ""
        echo -e "${YELLOW}Please use one of the above methods to install act on Windows.${NC}"
        echo "For WSL (recommended), use the Linux installation method."
        exit 0
        ;;

    *)
        echo -e "${RED}Unsupported operating system${NC}"
        echo "Please install act manually from: https://github.com/nektos/act/releases"
        exit 1
        ;;
esac

# Verify installation
echo ""
echo -e "${BLUE}Verifying installation...${NC}"
if command -v act &> /dev/null; then
    ACT_VERSION=$(act --version 2>&1 | head -n 1)
    echo -e "${GREEN}✓ act is installed and working${NC}"
    echo "  Version: $ACT_VERSION"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Install Docker (required by act): https://docs.docker.com/get-docker/"
    echo "2. Test act with: act -l"
    echo "3. Run a workflow: act -j <job-name>"
    echo ""
    echo "For more information, see: https://github.com/nektos/act"
else
    echo -e "${RED}✗ Installation verification failed${NC}"
    echo "Please check the error messages above and try again."
    exit 1
fi

echo -e "${GREEN}Installation complete!${NC}"
