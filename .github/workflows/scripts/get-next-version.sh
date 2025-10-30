#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Get version from pyproject.toml and output GitHub Actions variables
# Usage: get-next-version.sh

# Get the latest tag, or use v0.0.0 if no tags exist
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
echo "latest_tag=$LATEST_TAG" >> $GITHUB_OUTPUT

# Read version from pyproject.toml
if [ -f "pyproject.toml" ]; then
  VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
  NEW_VERSION="v$VERSION"
  echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT
  echo "Version from pyproject.toml: $NEW_VERSION"
else
  echo "Error: pyproject.toml not found"
  exit 1
fi
