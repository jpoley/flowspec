#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Determine next semantic version tag by bumping the patch (Z) of the latest existing tag.
#
# Supports version bumping via commit message label:
#   [version_bump:X.Y] - Sets major.minor to X.Y, patch continues incrementing
#   Example: [version_bump:0.2] with latest tag v0.0.313 → v0.2.314
#
# Outputs two GitHub Actions variables:
#   latest_tag=<vX.Y.Z>  # current latest tag (or v0.0.0 if none)
#   new_version=<vX.Y.Z> # next version with patch auto-incremented
#
# Usage: get-next-version.sh

# Ensure we have tags locally (in CI, checkout@v4 with fetch-depth: 0 already fetches tags)
git fetch --tags --quiet || true

# Find the latest semver tag (prefer v-prefixed)
find_latest_tag() {
  local latest
  latest=$(git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=v:refname | tail -n1 || true)
  if [[ -z "$latest" ]]; then
    # Fallback: allow non-v tags and normalize by adding v for internal use
    latest=$(git tag -l '[0-9]*.[0-9]*.[0-9]*' --sort=v:refname | tail -n1 || true)
    if [[ -n "$latest" ]]; then
      echo "v$latest"
      return 0
    fi
    echo "v0.0.0"
  else
    echo "$latest"
  fi
}

# Check commits since last tag for version bump directive
# Returns "X.Y" if found, empty string if not
find_version_bump_directive() {
  local latest_tag="$1"
  local bump_version=""

  # Get commits since last tag (or all commits if no tag)
  local commit_range=""
  if [[ "$latest_tag" == "v0.0.0" ]]; then
    commit_range="HEAD"
  else
    commit_range="${latest_tag}..HEAD"
  fi

  # Search commit messages for [version_bump:X.Y] pattern
  # Use the LAST occurrence if multiple exist (most recent wins)
  bump_version=$(git log --format="%s %b" "$commit_range" 2>/dev/null | \
    grep -oE '\[version_bump:[0-9]+\.[0-9]+\]' | \
    tail -n1 | \
    sed 's/\[version_bump:\([0-9]*\.[0-9]*\)\]/\1/' || true)

  echo "$bump_version"
}

LATEST_TAG=$(find_latest_tag)
echo "latest_tag=$LATEST_TAG" >> "$GITHUB_OUTPUT"

# Parse X.Y.Z from latest tag (strip leading v if present)
BASE=${LATEST_TAG#v}
IFS='.' read -r MAJOR MINOR PATCH <<< "$BASE"

# Validate numeric parts; default to 0.0.0 if parsing fails
if ! [[ $MAJOR =~ ^[0-9]+$ && $MINOR =~ ^[0-9]+$ && $PATCH =~ ^[0-9]+$ ]]; then
  MAJOR=0; MINOR=0; PATCH=0
fi

# Check for version bump directive in commits
VERSION_BUMP=$(find_version_bump_directive "$LATEST_TAG")

if [[ -n "$VERSION_BUMP" ]]; then
  # Parse X.Y from bump directive
  IFS='.' read -r NEW_MAJOR NEW_MINOR <<< "$VERSION_BUMP"

  # Validate
  if [[ $NEW_MAJOR =~ ^[0-9]+$ && $NEW_MINOR =~ ^[0-9]+$ ]]; then
    echo "Found version bump directive: [version_bump:${NEW_MAJOR}.${NEW_MINOR}]"
    MAJOR=$NEW_MAJOR
    MINOR=$NEW_MINOR
    # Patch continues incrementing from current value
  else
    echo "Warning: Invalid version bump format '$VERSION_BUMP', ignoring"
  fi
fi

# Increment patch (Z)
PATCH=$((PATCH + 1))

NEW_VERSION="v${MAJOR}.${MINOR}.${PATCH}"
echo "new_version=$NEW_VERSION" >> "$GITHUB_OUTPUT"

echo "Latest tag: $LATEST_TAG"
if [[ -n "$VERSION_BUMP" ]]; then
  echo "Version bump: [version_bump:$VERSION_BUMP]"
fi
echo "Next version: $NEW_VERSION (auto-bumped patch)"
