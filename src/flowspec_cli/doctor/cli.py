"""CLI entry point for flowspec doctor."""

from __future__ import annotations

import subprocess
from pathlib import Path

import httpx
import typer
from rich.console import Console
from rich.table import Table

from flowspec_cli.doctor.checks import (
    CheckResult,
    CheckStatus,
    run_all_checks,
)

console = Console()

_STATUS_ICON = {
    CheckStatus.PASS: "[green]✅[/green]",
    CheckStatus.WARN: "[yellow]⚠️ [/yellow]",
    CheckStatus.FAIL: "[red]❌[/red]",
}


def _print_results(results: list[CheckResult]) -> None:
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("icon", no_wrap=True)
    table.add_column("check", style="bold", no_wrap=True)
    table.add_column("message")
    table.add_column("fix", style="dim")

    for r in results:
        fix_text = (
            f"→ {r.fix_cmd}" if r.fix_cmd and r.status != CheckStatus.PASS else ""
        )
        table.add_row(_STATUS_ICON[r.status], r.name, r.message, fix_text)

    console.print(table)


def _attempt_fixes(results: list[CheckResult], project_path: Path) -> None:
    fixable = [r for r in results if r.status != CheckStatus.PASS and r.fix_cmd]
    if not fixable:
        console.print("\n[green]Nothing to fix — all checks passed.[/green]")
        return

    console.print("\n[bold cyan]Attempting fixes…[/bold cyan]\n")
    for r in fixable:
        console.print(f"  Fixing: [bold]{r.name}[/bold]")
        if r.name == "constitution.md":
            _fix_constitution(project_path)
        elif r.name == "Agent naming convention" and r.fix_cmd:
            try:
                proc = subprocess.run(["flowspec", "upgrade-repo"], check=False)
                if proc.returncode == 0:
                    console.print("    [green]✓[/green] upgrade-repo succeeded")
                else:
                    console.print(
                        f"    [red]✗[/red] upgrade-repo exited {proc.returncode}"
                    )
            except FileNotFoundError:
                console.print("    [red]✗[/red] flowspec not found in PATH")
        else:
            console.print(f"    [yellow]→[/yellow] Run manually: {r.fix_cmd}")


def _fix_constitution(project_path: Path) -> None:
    memory_dir = project_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    constitution_path = memory_dir / "constitution.md"
    if constitution_path.exists():
        console.print("    [yellow]→[/yellow] constitution.md already exists, skipping")
        return
    minimal = (
        "# Project Constitution\n\n"
        "**Version**: 1.0.0\n"
        "**Ratified**: (set date)\n\n"
        "<!-- NEEDS_VALIDATION: Update with your project details -->\n\n"
        "## Purpose\n\nDescribe the purpose of this project.\n"
    )
    constitution_path.write_text(minimal, encoding="utf-8")
    console.print(
        f"    [green]✓[/green] Created minimal constitution at {constitution_path}"
    )


def run_doctor(project_path: Path, fix: bool = False) -> None:
    """Run all health checks and print results."""
    from flowspec_cli import (
        REPO_NAME,
        REPO_OWNER,
        __version__,
        get_github_latest_release,
    )

    latest: str | None = None
    try:
        latest = get_github_latest_release(REPO_OWNER, REPO_NAME)
    except (httpx.HTTPError, httpx.TimeoutException, OSError):
        pass

    results = run_all_checks(
        project_path, current_version=__version__, latest_version=latest
    )

    console.print("\n[bold]flowspec doctor[/bold] — environment health check\n")
    _print_results(results)

    fails = sum(1 for r in results if r.status == CheckStatus.FAIL)
    warns = sum(1 for r in results if r.status == CheckStatus.WARN)
    console.print()
    if fails == 0 and warns == 0:
        console.print("[bold green]All checks passed.[/bold green]")
    else:
        parts = []
        if fails:
            parts.append(f"[red]{fails} failure(s)[/red]")
        if warns:
            parts.append(f"[yellow]{warns} warning(s)[/yellow]")
        console.print(f"[bold]Summary:[/bold] {', '.join(parts)}")

    if fix:
        _attempt_fixes(results, project_path)
    elif fails or warns:
        console.print(
            "\n[dim]Run [bold]flowspec doctor --fix[/bold] to attempt auto-fix.[/dim]"
        )

    if fails:
        raise typer.Exit(1)
