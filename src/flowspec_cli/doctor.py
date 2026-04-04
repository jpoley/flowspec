"""Health check and diagnostics for flowspec setup.

This module provides the `flowspec doctor` command to verify that the environment
is properly configured for flowspec development.

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
    >>> failures = [r for r in results if r.status == CheckStatus.FAIL]
    >>> if not failures:
    ...     print("All checks passed!")
"""

import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

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
            status=CheckStatus.FAIL,
            message="Could not determine flowspec version",
        )

    # Check against PyPI for latest version
    try:
        import httpx
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
    except Exception:
        pass

    return CheckResult(
        name="flowspec CLI",
        status=CheckStatus.PASS,
        message=f"v{current} (up to date)",
    )


def check_python_version() -> CheckResult:
    """Check Python version compatibility (requires 3.11+).

    Returns:
        CheckResult indicating Python version status
    """
    version_info = sys.version_info
    major, minor = version_info[:2]
    micro = version_info[2] if len(version_info) > 2 else 0
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


def check_tool_installed(tool_name: str) -> CheckResult:
    """Check if a CLI tool is installed and accessible.

    Args:
        tool_name: Name of the tool to check (e.g., "backlog", "beads")

    Returns:
        CheckResult indicating tool installation status
    """
    tool_path = shutil.which(tool_name)
    if tool_path is None:
        return CheckResult(
            name=f"{tool_name} CLI",
            status=CheckStatus.FAIL,
            message=f"{tool_name} not found in PATH",
            fix_command=f"Install {tool_name} following the installation guide",
        )

    # Try to get version if possible
    try:
        result = subprocess.run(
            [tool_name, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        version_output = result.stdout.strip() or result.stderr.strip()
        # Extract just the version number if present
        version = version_output.split()[-1] if version_output else "installed"
    except Exception:
        version = "installed"

    return CheckResult(
        name=f"{tool_name} CLI",
        status=CheckStatus.PASS,
        message=version,
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
        with open(config_path) as f:
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

    Only checks .github/agents/ for flow.*.agent.md vs flow-*.agent.md patterns.
    Note: .claude/agents/ intentionally uses hyphens and is not checked.

    Returns:
        CheckResult indicating agent file naming status
    """
    project_root = Path.cwd()
    github_agents_dir = project_root / ".github" / "agents"

    old_convention_files = []

    if github_agents_dir.exists():
        for agent_file in github_agents_dir.glob("*.agent.md"):
            # Check if file uses old flow- prefix instead of new flow. prefix
            # Old: flow-specify.agent.md
            # New: flow.specify.agent.md
            if agent_file.name.startswith("flow-"):
                old_convention_files.append(
                    str(agent_file.relative_to(project_root))
                )

    if old_convention_files:
        return CheckResult(
            name="Agent file naming",
            status=CheckStatus.WARN,
            message=f"{len(old_convention_files)} files using old flow- prefix",
            fix_command="Run: flowspec upgrade-repo",
            details={"files": old_convention_files},
        )

    # Check if there are any agent files at all in .github/agents/
    has_agents = (
        github_agents_dir.exists()
        and any(f.suffix == ".md" for f in github_agents_dir.glob("*.agent.md"))
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
        message="Using flow. prefix convention",
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
        content = constitution_path.read_text()
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
    checks = [
        check_flowspec_version(),
        check_python_version(),
        check_tool_installed("backlog"),
        check_tool_installed("beads"),
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
        fix: If True, attempt to auto-fix fixable issues
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

        # Show suggestion to run with --fix if there are fixable issues
        if not fix:
            fixable = sum(1 for r in results if r.fix_command is not None)
            if fixable > 0:
                console.print()
                console.print(
                    f"[dim]Hint: Run 'flowspec doctor --fix' to attempt "
                    f"automatic fixes ({fixable} fixable)[/dim]"
                )

    console.print()

    # Auto-fix handling (not implemented yet - would require complex logic)
    if fix:
        console.print(
            "[yellow]Note: Auto-fix is not yet implemented. "
            "Please run the suggested fix commands manually.[/yellow]"
        )
        console.print()

    return results
