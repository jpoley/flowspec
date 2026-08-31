"""Pinned versions of the external tools flowspec depends on.

Kept in a dedicated module so both the CLI and ``flowspec doctor`` can import
them without a circular import through ``flowspec_cli/__init__.py``.
"""

from __future__ import annotations

import re
from typing import Optional

# Matches a dotted numeric version with an optional leading "v" and an optional
# SemVer prerelease/build suffix, e.g. "v1.34.0", "1.50.1", "1.50.2-beta.1".
_VERSION_RE = re.compile(r"^v?(\d+(?:\.\d+)*)(?:[-+].*)?$")


def parse_version(value: str) -> Optional[tuple[int, ...]]:
    """Parse a dotted numeric version into a comparable tuple.

    A leading "v" and any SemVer prerelease/build suffix are ignored, so
    "v1.50.2-beta.1" parses as (1, 50, 2). Prerelease precedence is deliberately
    not modelled: flowspec only needs release-line comparisons.

    Args:
        value: Version string to parse.

    Returns:
        Tuple of ints, or None if the value is not a recognisable version.
        Never raises.
    """
    if not value:
        return None
    match = _VERSION_RE.match(value.strip())
    if match is None:
        return None
    try:
        return tuple(int(part) for part in match.group(1).split("."))
    except ValueError:  # pragma: no cover - regex already guarantees digits
        return None


def compare_versions(version1: str, version2: str) -> Optional[int]:
    """Compare two versions, padding to equal length so 1.2.3 == 1.2.3.0.

    Args:
        version1: First version.
        version2: Second version.

    Returns:
        -1, 0 or 1 as version1 is less than, equal to or greater than version2,
        or None if either value could not be parsed. Never raises.
    """
    v1 = parse_version(version1)
    v2 = parse_version(version2)
    if v1 is None or v2 is None:
        return None
    width = max(len(v1), len(v2))
    v1 += (0,) * (width - len(v1))
    v2 += (0,) * (width - len(v2))
    if v1 < v2:
        return -1
    if v1 > v2:
        return 1
    return 0


# Recommended backlog-md version installed by `flowspec backlog install`.
# Bump when upstream ships features flowspec relies on.
BACKLOG_RECOMMENDED_VERSION = "1.50.1"

# Minimum backlog-md version flowspec supports.
# 1.34.0 is the first release with native Definition of Done support
# (`--dod`, `--check-dod`, `--no-dod-defaults`), which flowspec's DoD workflow uses.
BACKLOG_MIN_VERSION = "1.34.0"
