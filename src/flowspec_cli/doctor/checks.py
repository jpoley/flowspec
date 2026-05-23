"""Health check functions for flowspec doctor command."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml


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
        message=f"Python {version_str} — requires ≥ 3.11",
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
    if current == latest:
        return CheckResult(
            name="flowspec version",
            status=CheckStatus.PASS,
            message=f"flowspec v{current} (up to date)",
        )
    return CheckResult(
        name="flowspec version",
        status=CheckStatus.WARN,
        message=f"flowspec v{current} — v{latest} available",
        fix_cmd="flowspec upgrade",
    )


def check_backlog_installed() -> CheckResult:
    """Check that the backlog CLI is installed."""
    try:
        result = subprocess.run(
            ["backlog", "--version"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return CheckResult(
                name="backlog.md",
                status=CheckStatus.PASS,
                message=f"backlog.md v{version}",
            )
    except FileNotFoundError:
        pass
    return CheckResult(
        name="backlog.md",
        status=CheckStatus.FAIL,
        message="backlog not found",
        fix_cmd="npm install -g backlog.md",
    )


def check_beads_installed() -> CheckResult:
    """Check that the beads CLI is installed."""
    try:
        result = subprocess.run(
            ["bd", "--version"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            version = output
            if output.startswith("bd version "):
                parts = output.split()
                if len(parts) >= 3:
                    version = parts[2]
            return CheckResult(
                name="beads",
                status=CheckStatus.PASS,
                message=f"beads v{version}",
            )
    except FileNotFoundError:
        pass
    return CheckResult(
        name="beads",
        status=CheckStatus.FAIL,
        message="beads (bd) not found",
        fix_cmd="npm install -g @jpoley/beads",
    )


def check_workflow_config(project_path: Path) -> CheckResult:
    """Check that flowspec_workflow.yml exists and is valid YAML."""
    config_path = project_path / "flowspec_workflow.yml"
    if not config_path.exists():
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.FAIL,
            message="flowspec_workflow.yml not found",
            fix_cmd="flowspec init --here",
        )
    try:
        content = config_path.read_text(encoding="utf-8")
        yaml.safe_load(content)
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.PASS,
            message="flowspec_workflow.yml present and valid",
        )
    except yaml.YAMLError as exc:
        return CheckResult(
            name="flowspec_workflow.yml",
            status=CheckStatus.FAIL,
            message=f"flowspec_workflow.yml parse error: {exc}",
            fix_cmd="flowspec init --here",
        )


def check_agent_naming(project_path: Path) -> CheckResult:
    """Warn if old hyphen-naming agent files exist in .github/agents/."""
    agents_dir = project_path / ".github" / "agents"
    if not agents_dir.exists():
        return CheckResult(
            name="Agent naming convention",
            status=CheckStatus.PASS,
            message="No .github/agents/ directory (nothing to check)",
        )
    old_files = [
        f.name
        for f in agents_dir.iterdir()
        if f.name.startswith("flow-") and f.suffix == ".md"
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
    if constitution_path.exists():
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
    if flowspec_dir.exists():
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
