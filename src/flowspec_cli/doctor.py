"""Health check and diagnostics for flowspec setup.

This module provides diagnostic helpers, including `run_doctor()`, to verify that
the environment is properly configured for flowspec development.

Checks performed:
- flowspec CLI version (currently installed)
- Python version compatibility (requires 3.11+)
- Required tools installed (backlog.md, beads)
- Workflow configuration present and valid
- Agent files using correct naming convention (dot notation)
- Constitution file present (if configured)

Example:
    >>> from flowspec_cli.doctor import run_doctor, CheckStatus
    >>> results = run_doctor(fix=False)
    >>> failures = [r for r in results if r.status != CheckStatus.PASS]
    >>> if not failures:
    ...     print("All checks passed!")
"""

import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

import httpx
import yaml
from rich.console import Console
from rich.table import Table

from flowspec_cli.workflow.validator import validate_workflow

console = Console()


class CheckStatus(Enum):
    """Status of a health check."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class CheckResult:
    """Result of a single health check.

    Attributes:
        name: Display name of the check
        status: Pass/warn/fail status
        message: Human-readable message about the check result
        fix_command: Optional command to fix the issue (for auto-fixable issues)
        details: Additional context or details
    """

    name: str
    status: CheckStatus
    message: str
    fix_command: str | None = None
    details: dict[str, Any] | None = None


def get_flowspec_version() -> str:
    """Get the currently installed flowspec version.

    Returns:
        Version string (e.g., "0.4.004") or "unknown"
    """
    try:
        # Import version from package metadata
        from importlib.metadata import version

        return version("flowspec-cli")
    except Exception:
        return "unknown"


def check_flowspec_version() -> CheckResult:
    """Check flowspec CLI version.

    Returns:
        CheckResult indicating version status
    """
    current = get_flowspec_version()
    if current == "unknown":
        return CheckResult(
            name="flowspec CLI",
            status=CheckStatus.WARN,
            message="Could not determine flowspec version (source checkout?)",
        )

    # Check against PyPI for latest version
    try:
        resp = httpx.get("https://pypi.org/pypi/flowspec-cli/json", timeout=5)
        if resp.status_code == 200:
            latest = resp.json()["info"]["version"]
            if latest != current:
                return CheckResult(
                    name="flowspec CLI",
                    status=CheckStatus.WARN,
                    message=f"v{current} installed, v{latest} available",
                    fix_command="pip install --upgrade flowspec-cli",
                )
            return CheckResult(
                name="flowspec CLI",
                status=CheckStatus.PASS,
                message=f"v{current} (up to date)",
            )
    except Exception:
        pass

    # Could not verify against PyPI — report installed version without "up to date" claim
    return CheckResult(
        name="flowspec CLI",
        status=CheckStatus.PASS,
        message=f"v{current}",
    )


def check_python_version() -> CheckResult:
    """Check Python version compatibility (requires 3.11+).

    Returns:
        CheckResult indicating Python version status
    """
    version_info = sys.version_info
    major, minor, micro = version_info[:3]
    version_str = f"{major}.{minor}.{micro}"

    if major < 3 or (major == 3 and minor < 11):
        return CheckResult(
            name="Python version",
            status=CheckStatus.FAIL,
            message=f"Python {version_str} (requires 3.11+)",
        )

    return CheckResult(
        name="Python version",
        status=CheckStatus.PASS,
        message=f"Python {version_str}",
    )


def check_tool_installed(
    binary_name: str,
    display_name: str | None = None,
    version_getter: Callable[[], str | None] | None = None,
) -> CheckResult:
    """Check if a CLI tool is installed and accessible.

    Args:
        binary_name: Executable name to look for in PATH (e.g., "backlog", "bd")
        display_name: Human-friendly name shown in output (defaults to binary_name)
        version_getter: Optional callable returning the installed version; used
            in preference to a generic ``--version`` probe so parsing matches
            the rest of the CLI.

    Returns:
        CheckResult indicating tool installation status
    """
    label = display_name or binary_name

    if shutil.which(binary_name) is None:
        return CheckResult(
            name=f"{label} CLI",
            status=CheckStatus.FAIL,
            message=f"{binary_name} not found in PATH",
            fix_command=f"Install {label} following the installation guide",
        )

    version: str | None = None

    if version_getter is not None:
        try:
            version = version_getter()
        except Exception:
            version = None

    if version is None:
        # Fallback: probe ``<tool> --version`` and take the last whitespace-
        # separated token as the version.
        try:
            result = subprocess.run(
                [binary_name, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            version_output = result.stdout.strip() or result.stderr.strip()
            if version_output:
                version = version_output.split()[-1]
        except Exception:
            version = None

    return CheckResult(
        name=f"{label} CLI",
        status=CheckStatus.PASS,
        message=version or "installed",
    )


def check_workflow_config() -> CheckResult:
    """Check if workflow configuration exists and is valid.

    Returns:
        CheckResult indicating workflow configuration status
    """
    project_root = Path.cwd()

    # Check for workflow config file
    config_paths = [
        project_root / "flowspec_workflow.yml",
        project_root / ".flowspec" / "workflow.yml",
    ]

    config_path = None
    for path in config_paths:
        if path.exists():
            config_path = path
            break

    if config_path is None:
        return CheckResult(
            name="Workflow config",
            status=CheckStatus.WARN,
            message="No workflow configuration found",
            fix_command="Run: /flow:init",
        )

    # Try to load and validate the config
    try:
        with open(config_path, encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        # Validate using the workflow validator
        validation_result = validate_workflow(config_data)

        if not validation_result.is_valid:
            error_count = len(validation_result.errors)
            warning_count = len(validation_result.warnings)
            details = {
                "errors": [str(e) for e in validation_result.errors],
                "warnings": [str(w) for w in validation_result.warnings],
            }
            return CheckResult(
                name="Workflow config",
                status=CheckStatus.FAIL,
                message=f"Invalid ({error_count} errors, {warning_count} warnings)",
                fix_command="Run: flowspec workflow validate --verbose",
                details=details,
            )

        # Valid config
        warning_count = len(validation_result.warnings)
        if warning_count > 0:
            return CheckResult(
                name="Workflow config",
                status=CheckStatus.WARN,
                message=f"Valid ({warning_count} warnings)",
                details={"warnings": [str(w) for w in validation_result.warnings]},
            )

        return CheckResult(
            name="Workflow config",
            status=CheckStatus.PASS,
            message="Valid",
        )

    except yaml.YAMLError as e:
        return CheckResult(
            name="Workflow config",
            status=CheckStatus.FAIL,
            message=f"Invalid YAML: {e}",
        )
    except Exception as e:
        return CheckResult(
            name="Workflow config",
            status=CheckStatus.FAIL,
            message=f"Error reading config: {e}",
        )


def check_agent_files() -> CheckResult:
    """Check if agent files use correct naming convention.

    Only checks .github/agents/ for flow.*.agent.md pattern.
    Note: .claude/agents/ intentionally uses hyphens and is not checked.

    Returns:
        CheckResult indicating agent file naming status
    """
    project_root = Path.cwd()
    github_agents_dir = project_root / ".github" / "agents"

    non_compliant_files = []

    if github_agents_dir.exists():
        for agent_file in github_agents_dir.glob("*.md"):
            name = agent_file.name
            # Skip README and underscore-prefixed files
            if name.startswith("_") or name == "README.md":
                continue
            # Expected pattern: flow.<phase>.agent.md (4 dot-separated parts)
            parts = name.split(".")
            is_compliant = (
                len(parts) == 4
                and parts[0] == "flow"
                and parts[1] != ""
                and parts[2] == "agent"
                and parts[3] == "md"
            )
            if not is_compliant:
                non_compliant_files.append(str(agent_file.relative_to(project_root)))

    if non_compliant_files:
        return CheckResult(
            name="Agent file naming",
            status=CheckStatus.WARN,
            message=f"{len(non_compliant_files)} files not matching flow.*.agent.md",
            fix_command="Run: flowspec upgrade-repo",
            details={"files": non_compliant_files},
        )

    # Check if there are any agent files at all in .github/agents/
    has_agents = github_agents_dir.exists() and any(
        f.suffix == ".md"
        for f in github_agents_dir.glob("*.md")
        if not f.name.startswith("_") and f.name != "README.md"
    )

    if not has_agents:
        return CheckResult(
            name="Agent file naming",
            status=CheckStatus.WARN,
            message="No agent files found in .github/agents/",
        )

    return CheckResult(
        name="Agent file naming",
        status=CheckStatus.PASS,
        message="Using flow.*.agent.md convention",
    )


def check_constitution() -> CheckResult:
    """Check if constitution file exists.

    Returns:
        CheckResult indicating constitution file status
    """
    project_root = Path.cwd()
    constitution_path = project_root / "memory" / "constitution.md"

    if not constitution_path.exists():
        return CheckResult(
            name="Constitution",
            status=CheckStatus.WARN,
            message="Constitution not found",
            fix_command="Run: /flow:init",
        )

    # Check if it's just the template (contains placeholders)
    try:
        content = constitution_path.read_text(encoding="utf-8")
        if "[PROJECT_NAME]" in content or "[PRINCIPLE_1_NAME]" in content:
            return CheckResult(
                name="Constitution",
                status=CheckStatus.WARN,
                message="Contains placeholders (not configured)",
                fix_command="Run: /flow:init",
            )
    except Exception:
        pass

    return CheckResult(
        name="Constitution",
        status=CheckStatus.PASS,
        message="Present",
    )


def run_all_checks() -> list[CheckResult]:
    """Run all health checks.

    Returns:
        List of CheckResult objects for all checks performed
    """
    # Lazy import to avoid a circular import at module load time: the top-level
    # package imports ``doctor`` while ``doctor`` needs the version helpers that
    # live in the package's ``__init__``.
    from flowspec_cli import (
        check_backlog_installed_version,
        check_beads_installed_version,
    )

    checks = [
        check_flowspec_version(),
        check_python_version(),
        check_tool_installed(
            "backlog",
            display_name="backlog",
            version_getter=check_backlog_installed_version,
        ),
        check_tool_installed(
            "bd",
            display_name="beads",
            version_getter=check_beads_installed_version,
        ),
        check_workflow_config(),
        check_agent_files(),
        check_constitution(),
    ]
    return checks


def display_results(results: list[CheckResult], verbose: bool = False) -> None:
    """Display check results in a formatted table.

    Args:
        results: List of CheckResult objects to display
        verbose: If True, show additional details
    """
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Status", width=3)
    table.add_column("Check", style="bold")
    table.add_column("Details")

    for result in results:
        # Choose symbol and color based on status
        if result.status == CheckStatus.PASS:
            symbol = "[green]✅[/green]"
        elif result.status == CheckStatus.WARN:
            symbol = "[yellow]⚠️[/yellow]"
        else:
            symbol = "[red]❌[/red]"

        table.add_row(symbol, result.name, result.message)

        # Show fix commands for issues
        if result.fix_command and result.status != CheckStatus.PASS:
            table.add_row(
                "",
                "",
                f"[dim cyan]→ Fix: {result.fix_command}[/dim cyan]",
            )

        # Show details in verbose mode
        if verbose and result.details:
            for key, value in result.details.items():
                if isinstance(value, list):
                    for item in value[:3]:  # Show first 3 items
                        table.add_row(
                            "",
                            "",
                            f"[dim]  {key}: {item}[/dim]",
                        )
                    if len(value) > 3:
                        table.add_row(
                            "",
                            "",
                            f"[dim]  ... and {len(value) - 3} more[/dim]",
                        )
                else:
                    table.add_row(
                        "",
                        "",
                        f"[dim]  {key}: {value}[/dim]",
                    )

    console.print()
    console.print(table)
    console.print()


def run_doctor(fix: bool = False, verbose: bool = False) -> list[CheckResult]:
    """Run health checks and optionally attempt fixes.

    Args:
        fix: Reserved for future use (auto-fix not yet implemented)
        verbose: If True, show additional details

    Returns:
        List of CheckResult objects. Filter for failures:
        ``issues = [r for r in results if r.status == CheckStatus.FAIL]``
    """
    console.print()
    console.print("[bold]flowspec doctor[/bold]")
    console.print()

    results = run_all_checks()

    # Display results
    display_results(results, verbose=verbose)

    # Count issues
    errors = sum(1 for r in results if r.status == CheckStatus.FAIL)
    warnings = sum(1 for r in results if r.status == CheckStatus.WARN)

    # Summary
    if errors == 0 and warnings == 0:
        console.print("[green]✓ All checks passed![/green]")
    else:
        summary_parts = []
        if errors > 0:
            summary_parts.append(f"[red]{errors} error(s)[/red]")
        if warnings > 0:
            summary_parts.append(f"[yellow]{warnings} warning(s)[/yellow]")
        console.print(" ".join(summary_parts))

    console.print()

    if fix:
        # Auto-fix is intentionally not implemented yet; the per-check
        # ``fix_command`` hints rendered above are the manual remediation path.
        console.print(
            "[yellow]Note: Auto-fix is not yet implemented. "
            "Please run the suggested fix commands manually.[/yellow]"
        )
        console.print()

    return results
