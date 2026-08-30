"""Pinned versions of the external tools flowspec depends on.

Kept in a dedicated module so both the CLI and ``flowspec doctor`` can import
them without a circular import through ``flowspec_cli/__init__.py``.
"""

from __future__ import annotations

# Recommended backlog-md version installed by `flowspec backlog install`.
# Bump when upstream ships features flowspec relies on.
BACKLOG_RECOMMENDED_VERSION = "1.50.1"

# Minimum backlog-md version flowspec supports.
# 1.34.0 is the first release with native Definition of Done support
# (`--dod`, `--check-dod`, `--no-dod-defaults`), which flowspec's DoD workflow uses.
BACKLOG_MIN_VERSION = "1.34.0"
