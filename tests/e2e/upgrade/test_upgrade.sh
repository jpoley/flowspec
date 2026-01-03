#!/bin/bash
# End-to-end test for flowspec upgrade-tools functionality
# Run this from the flowspec root directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "=== Building test container ==="
cd "$PROJECT_ROOT"
docker build -f tests/e2e/upgrade/Dockerfile -t flowspec-upgrade-test .

echo ""
echo "=== Running upgrade test ==="
docker run --rm flowspec-upgrade-test

echo ""
echo "=== Test completed successfully ==="
