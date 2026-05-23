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
            f"-> {r.fix_cmd}" if r.fix_cmd and r.status != CheckStatus.PASS else ""
        )
        table.add_row(_STATUS_ICON[r.status], r.name, r.message, fix_text)

    console.print(table)


def _print_summary(fails: int, warns: int) -> None:
    if fails == 0 and warns == 0:
        console.print("[bold green]All checks passed.[/bold green]")
    else:
        parts = []
        if fails:
            parts.append(f"[red]{fails} failure(s)[/red]")
        if warns:
            parts.append(f"[yellow]{warns} warning(s)[/yellow]")
        console.print(f"[bold]Summary:[/bold] {', '.join(parts)}")


def _attempt_fixes(results: list[CheckResult], project_path: Path) -> None:
    fixable = [r for r in results if r.status != CheckStatus.PASS and r.fix_cmd]
    if not fixable:
        fails = sum(1 for r in results if r.status == CheckStatus.FAIL)
        warns = sum(1 for r in results if r.status == CheckStatus.WARN)
        if fails == 0 and warns == 0:
            console.print("\n[green]Nothing to auto-fix -- all checks passed.[/green]")
        else:
            parts = []
            if fails:
                parts.append(f"[red]{fails} failure(s)[/red]")
            if warns:
                parts.append(f"[yellow]{warns} warning(s)[/yellow]")
            console.print(
                "\n[yellow]Nothing to auto-fix.[/yellow] "
                f"Remaining issues require manual action: {', '.join(parts)}"
            )
        return

    console.print("\n[bold cyan]Attempting fixes...[/bold cyan]\n")
    for r in fixable:
        console.print(f"  Fixing: [bold]{r.name}[/bold]")
        if r.name == "constitution.md":
            _fix_constitution(project_path)
        elif r.name == "Agent naming convention" and r.fix_cmd:
            try:
                proc = subprocess.run(
                    ["flowspec", "upgrade-repo"], check=False, cwd=project_path
                )
                if proc.returncode == 0:
                    console.print("    [green]✓[/green] upgrade-repo succeeded")
                else:
                    console.print(
                        f"    [red]✗[/red] upgrade-repo exited {proc.returncode}"
                    )
            except FileNotFoundError:
                console.print("    [red]✗[/red] flowspec not found in PATH")
        else:
            console.print(f"    [yellow]->[/yellow] Run manually: {r.fix_cmd}")


def _fix_constitution(project_path: Path) -> None:
    has_marker = (project_path / "flowspec_workflow.yml").exists() or (
        project_path / ".flowspec"
    ).is_dir()
    if not has_marker:
        console.print(
            "    [yellow]->[/yellow] Not a flowspec project directory, skipping"
        )
        return
    memory_dir = project_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    constitution_path = memory_dir / "constitution.md"
    if constitution_path.is_file():
        console.print(
            "    [yellow]->[/yellow] constitution.md already exists, skipping"
        )
        return
    if constitution_path.is_dir():
        console.print(
            "    [red]✗[/red] Cannot create constitution.md because that path is a "
            "directory. Remove or rename "
            f"{constitution_path} and run the fix again."
        )
        return
    minimal = (
        "# Project Constitution\n\n"
        "**Version**: 1.0.0\n"
        "**Ratified**: (set date)\n\n"
        "<!-- NEEDS_VALIDATION: Update with your project details -->\n\n"
        "## Purpose\n\nDescribe the purpose of this project.\n"
    )
    try:
        constitution_path.write_text(minimal, encoding="utf-8")
        console.print(
            f"    [green]✓[/green] Created minimal constitution at {constitution_path}"
        )
    except OSError as exc:
        console.print(f"    [red]✗[/red] Failed to create constitution: {exc}")


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

    console.print("\n[bold]flowspec doctor[/bold] -- environment health check\n")
    _print_results(results)

    fails = sum(1 for r in results if r.status == CheckStatus.FAIL)
    warns = sum(1 for r in results if r.status == CheckStatus.WARN)
    console.print()
    _print_summary(fails, warns)

    if fix:
        _attempt_fixes(results, project_path)
        # Re-evaluate after fixes; exit code reflects post-fix state
        results = run_all_checks(
            project_path, current_version=__version__, latest_version=latest
        )
        post_fails = sum(1 for r in results if r.status == CheckStatus.FAIL)
        post_warns = sum(1 for r in results if r.status == CheckStatus.WARN)
        if post_fails != fails or post_warns != warns:
            console.print("\n[bold]Post-fix status:[/bold]")
            _print_results(results)
            console.print()
            _print_summary(post_fails, post_warns)
        fails = post_fails
    elif fails or warns:
        console.print(
            "\n[dim]Run [bold]flowspec doctor --fix[/bold] to attempt auto-fix.[/dim]"
        )

    if fails:
        raise typer.Exit(1)
