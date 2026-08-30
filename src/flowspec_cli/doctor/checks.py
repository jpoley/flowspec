"""Health check functions for flowspec doctor command."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml

from flowspec_cli.versions import BACKLOG_MIN_VERSION
from flowspec_cli.workflow.config import WorkflowConfig
from flowspec_cli.workflow.exceptions import (
    WorkflowConfigError,
    WorkflowConfigValidationError,
)
from flowspec_cli.workflow.validator import WorkflowValidator

_VERSION_RE = re.compile(r"^\d+(\.\d+)*$")


class CheckStatus(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    message: str
    fix_cmd: Optional[str] = field(default=None)


def _parse_version(v: str) -> tuple[int, ...]:
    """Normalize a version string to a comparable tuple, stripping leading v and zero-padding.

    Short versions are padded to three components so "1.34" compares equal to
    "1.34.0" rather than sorting below it.

    Returns:
        Tuple of ints with at least three components, or (0, 0, 0) if unparseable.
    """
    v = v.lstrip("v").strip()
    try:
        parts = tuple(int(part) for part in v.split("."))
    except ValueError:
        return (0, 0, 0)
    if len(parts) < 3:
        parts += (0,) * (3 - len(parts))
    return parts


def check_python_version() -> CheckResult:
    """Check that Python >= 3.11 is running."""
    major, minor, micro = sys.version_info[0], sys.version_info[1], sys.version_info[2]
    version_str = f"{major}.{minor}.{micro}"
    if (major, minor) >= (3, 11):
        return CheckResult(
            name="Python version",
            status=CheckStatus.PASS,
            message=f"Python {version_str}",
        )
    return CheckResult(
        name="Python version",
        status=CheckStatus.FAIL,
        message=f"Python {version_str} -- requires >= 3.11",
        fix_cmd="Install Python 3.11+ from https://python.org",
    )


def check_flowspec_version(current: str, latest: Optional[str]) -> CheckResult:
    """Check whether the installed flowspec version is up to date."""
    if latest is None:
        return CheckResult(
            name="flowspec version",
            status=CheckStatus.WARN,
            message=f"flowspec v{current} (could not check latest)",
        )
    current_tuple = _parse_version(current)
    latest_tuple = _parse_version(latest)
    if current_tuple >= latest_tuple:
        return CheckResult(
            name="flowspec version",
            status=CheckStatus.PASS,
            message=f"flowspec v{current} (up to date)",
        )
    return CheckResult(
        name="flowspec version",
        status=CheckStatus.WARN,
        message=f"flowspec v{current} -- v{latest} available",
        fix_cmd="flowspec upgrade",
    )


def _is_version_string(s: str) -> bool:
    """Return True if s looks like a dotted-integer version string (e.g. '1.2.3')."""
    return bool(_VERSION_RE.match(s)) if s else False


def check_backlog_installed() -> CheckResult:
    """Check that the backlog CLI is installed."""
    try:
        result = subprocess.run(
            ["backlog", "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except FileNotFoundError:
        return CheckResult(
            name="backlog.md",
            status=CheckStatus.FAIL,
            message="backlog not found",
            fix_cmd="npm install -g backlog.md",
        )
    except subprocess.TimeoutExpired:
        return CheckResult(
            name="backlog.md",
            status=CheckStatus.FAIL,
            message="backlog --version timed out",
        )

    if result.returncode != 0:
        return CheckResult(
            name="backlog.md",
            status=CheckStatus.FAIL,
            message=f"backlog --version exited with code {result.returncode}",
        )

    version = result.stdout.strip()
    if _is_version_string(version):
        if _parse_version(version) < _parse_version(BACKLOG_MIN_VERSION):
            return CheckResult(
                name="backlog.md",
                status=CheckStatus.WARN,
                message=(
                    f"backlog.md v{version} is older than the minimum "
                    f"supported version ({BACKLOG_MIN_VERSION}); "
                    "Definition of Done flags are unavailable"
                ),
                fix_cmd="flowspec backlog upgrade",
            )
        return CheckResult(
            name="backlog.md",
            status=CheckStatus.PASS,
            message=f"backlog.md v{version}",
        )

    return CheckResult(
        name="backlog.md",
        status=CheckStatus.FAIL,
        message=f"backlog --version returned unrecognized output: {version!r}",
    )


def check_beads_installed() -> CheckResult:
    """Check that the beads CLI is installed."""
    try:
        result = subprocess.run(
            ["bd", "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except FileNotFoundError:
        return CheckResult(
            name="beads",
            status=CheckStatus.FAIL,
            message="beads (bd) not found",
            fix_cmd="npm install -g @jpoley/beads",
        )
    except subprocess.TimeoutExpired:
        return CheckResult(
            name="beads",
            status=CheckStatus.FAIL,
            message="beads (bd) command timed out while checking version",
            fix_cmd="Run `bd --version` manually to diagnose hangs or reinstall @jpoley/beads",
        )

    if result.returncode != 0:
        error_output = (result.stderr or result.stdout or "").strip()
        message = f"beads (bd) failed with exit code {result.returncode}"
        if error_output:
            message = f"{message}: {error_output}"
        return CheckResult(
            name="beads",
            status=CheckStatus.FAIL,
            message=message,
            fix_cmd="Run `bd --version` manually to diagnose the failure or reinstall @jpoley/beads",
        )

    output = result.stdout.strip()
    # Expected: "bd version X.Y.Z (hash)"
    version = None
    if output.startswith("bd version "):
        parts = output.split()
        if len(parts) >= 3 and _is_version_string(parts[2]):
            version = parts[2]
    if version:
        return CheckResult(
            name="beads",
            status=CheckStatus.PASS,
            message=f"beads v{version}",
        )

    unexpected_output = output or "<empty output>"
    return CheckResult(
        name="beads",
        status=CheckStatus.FAIL,
        message=f"beads (bd) returned unexpected version output: {unexpected_output}",
        fix_cmd="Run `bd --version` manually to inspect the output or reinstall @jpoley/beads",
    )


def check_workflow_config(project_path: Path) -> CheckResult:
    """Check that flowspec_workflow.yml exists, is valid YAML, and passes schema+semantic validation."""
    config_path = project_path / "flowspec_workflow.yml"
    if not config_path.exists():
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.FAIL,
            message="flowspec_workflow.yml not found",
            fix_cmd="flowspec init --here",
        )

    # Basic YAML parse
    try:
        content = config_path.read_text(encoding="utf-8")
        config_data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.FAIL,
            message=f"flowspec_workflow.yml parse error: {exc}",
            fix_cmd="flowspec init --here",
        )
    except (OSError, UnicodeDecodeError) as exc:
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.FAIL,
            message=f"flowspec_workflow.yml read error: {exc}",
            fix_cmd="flowspec init --here",
        )

    if not isinstance(config_data, dict):
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.FAIL,
            message="flowspec_workflow.yml is empty or not a YAML mapping",
            fix_cmd="flowspec init --here",
        )

    # Schema + semantic validation via existing WorkflowValidator
    try:
        WorkflowConfig.load(path=config_path, validate=True, cache=False)
    except WorkflowConfigValidationError as exc:
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.FAIL,
            message=f"flowspec_workflow.yml schema error: {exc}",
            fix_cmd="flowspec init --here",
        )
    except WorkflowConfigError as exc:
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.FAIL,
            message=f"flowspec_workflow.yml config error: {exc}",
            fix_cmd="flowspec init --here",
        )

    validator = WorkflowValidator(config_data)
    validation_result = validator.validate()
    if not validation_result.is_valid:
        error_count = len(validation_result.errors)
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.WARN,
            message=f"flowspec_workflow.yml has {error_count} semantic issue(s)",
            fix_cmd="flowspec workflow validate --verbose",
        )

    return CheckResult(
        name="flowspec_workflow.yml",
        status=CheckStatus.PASS,
        message="flowspec_workflow.yml present and valid",
    )


def check_agent_naming(project_path: Path) -> CheckResult:
    """Warn if old hyphen-naming agent files exist in .github/agents/."""
    agents_dir = project_path / ".github" / "agents"
    if not agents_dir.is_dir():
        return CheckResult(
            name="Agent naming convention",
            status=CheckStatus.PASS,
            message="No .github/agents/ directory (nothing to check)",
        )
    old_files = [
        f.name
        for f in agents_dir.iterdir()
        if f.is_file() and f.name.startswith("flow-") and f.name.endswith(".agent.md")
    ]
    if old_files:
        return CheckResult(
            name="Agent naming convention",
            status=CheckStatus.WARN,
            message=f"{len(old_files)} agent file(s) using old hyphen naming",
            fix_cmd="flowspec upgrade-repo",
        )
    return CheckResult(
        name="Agent naming convention",
        status=CheckStatus.PASS,
        message="Agent files use current naming convention",
    )


def check_constitution(project_path: Path) -> CheckResult:
    """Warn if memory/constitution.md is missing."""
    constitution_path = project_path / "memory" / "constitution.md"
    if constitution_path.is_file():
        return CheckResult(
            name="constitution.md",
            status=CheckStatus.PASS,
            message="memory/constitution.md present",
        )
    return CheckResult(
        name="constitution.md",
        status=CheckStatus.WARN,
        message="memory/constitution.md not found",
        fix_cmd="flowspec init --here",
    )


def check_flowspec_dir(project_path: Path) -> CheckResult:
    """Warn if .flowspec/ directory is missing."""
    flowspec_dir = project_path / ".flowspec"
    if flowspec_dir.is_dir():
        return CheckResult(
            name=".flowspec/ directory",
            status=CheckStatus.PASS,
            message=".flowspec/ directory present",
        )
    return CheckResult(
        name=".flowspec/ directory",
        status=CheckStatus.WARN,
        message=".flowspec/ directory not found",
        fix_cmd="flowspec init --here",
    )


def run_all_checks(
    project_path: Path, current_version: str, latest_version: Optional[str] = None
) -> list[CheckResult]:
    """Run all health checks and return results."""
    return [
        check_python_version(),
        check_flowspec_version(current_version, latest_version),
        check_backlog_installed(),
        check_beads_installed(),
        check_workflow_config(project_path),
        check_agent_naming(project_path),
        check_constitution(project_path),
        check_flowspec_dir(project_path),
    ]
