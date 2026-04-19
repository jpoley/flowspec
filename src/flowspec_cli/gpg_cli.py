"""CLI commands for GPG signing management.

This module provides user-facing commands for:
- Setting up agent GPG keys
- Viewing GPG key status
- Rotating keys
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .signing import (
    configure_git_signing,
    delete_agent_key,
    generate_agent_key,
    get_key_fingerprint,
    get_key_info,
    is_git_signing_enabled,
    key_exists,
    GPGConfigurationError,
    GPGError,
    GPGKeyGenerationError,
)

gpg_app = typer.Typer(
    name="gpg",
    help="Manage agent GPG commit signing",
    add_completion=False,
)

console = Console()


@gpg_app.command("setup")
def setup_command(
    project_root: Optional[str] = typer.Option(
        None,
        "--project-root",
        "-p",
        help="Project directory to configure (default: current directory)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force key regeneration if key already exists",
    ),
) -> None:
    """Set up agent GPG commit signing.

    This command:
    1. Generates a new GPG key for the Flowspec agent (if needed)
    2. Configures git to sign commits with the agent key
    3. Displays the key fingerprint

    The key fingerprint is stored in the system keyring and can be
    included in telemetry output.

    Examples:
        flowspec gpg setup
        flowspec gpg setup --project-root /path/to/repo
        flowspec gpg setup --force  # Regenerate key
    """
    root = Path(project_root) if project_root else Path.cwd()

    try:
        # Read key state exactly once. ``key_exists()`` itself calls
        # ``get_key_fingerprint()`` internally, so using both here would still
        # incur two keyring reads and reintroduce the inconsistency this
        # caching was meant to prevent. Branch on the fingerprint alone.
        existing_fingerprint = get_key_fingerprint()

        if existing_fingerprint and not force:
            console.print("[yellow]Agent GPG key already exists.[/yellow]")
            console.print("[dim]Use --force to regenerate the key.[/dim]")
            fingerprint = existing_fingerprint
        else:
            if existing_fingerprint and force:
                console.print("[yellow]Regenerating agent GPG key...[/yellow]")
                delete_agent_key()

            # Generate new key
            console.print("[cyan]Generating agent GPG key...[/cyan]")
            fingerprint = generate_agent_key()
            console.print("[green]✓[/green] GPG key generated")

        # Configure git
        console.print("[cyan]Configuring git for commit signing...[/cyan]")
        configure_git_signing(project_root=root)
        console.print("[green]✓[/green] Git configured for signing")

        # Display summary
        console.print()
        panel_content = f"""[bold]Agent GPG Setup Complete[/bold]

[cyan]Fingerprint:[/cyan] {fingerprint}

All commits in this repository will now be signed by the agent.

[dim]View status:[/dim] flowspec gpg status
[dim]Include in telemetry:[/dim] fingerprint is automatically included when signing is active
"""
        console.print(
            Panel(
                panel_content,
                title="✓ GPG Signing Enabled",
                border_style="green",
                padding=(1, 2),
            )
        )

    except GPGKeyGenerationError as e:
        console.print(f"[red]✗ Key generation failed:[/red] {e}")
        raise typer.Exit(1)
    except GPGConfigurationError as e:
        console.print(f"[red]✗ Git configuration failed:[/red] {e}")
        raise typer.Exit(1)
    except GPGError as e:
        console.print(f"[red]✗ GPG error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Unexpected error:[/red] {e}")
        raise typer.Exit(1)


@gpg_app.command("status")
def status_command(
    project_root: Optional[str] = typer.Option(
        None,
        "--project-root",
        "-p",
        help="Project directory to check (default: current directory)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed key information",
    ),
) -> None:
    """Show agent GPG signing status.

    Displays:
    - Whether an agent GPG key exists
    - Key fingerprint and details
    - Git signing configuration status

    Examples:
        flowspec gpg status
        flowspec gpg status --verbose
        flowspec gpg status --project-root /path/to/repo
    """
    root = Path(project_root) if project_root else Path.cwd()

    # Build status table
    table = Table(title="Agent GPG Signing Status", show_header=False, box=None)
    table.add_column("Setting", style="cyan")
    table.add_column("Value")

    # Check if key exists
    if not key_exists():
        table.add_row("Status", "[red]Not configured[/red]")
        console.print(table)
        console.print()
        console.print(
            "[dim]Run 'flowspec gpg setup' to enable agent commit signing.[/dim]"
        )
        return

    # Get key information
    fingerprint = get_key_fingerprint()
    key_info = get_key_info()

    table.add_row("Status", "[green]Configured[/green]")
    table.add_row("Fingerprint", fingerprint or "[dim]unknown[/dim]")

    if verbose and key_info:
        if uid := key_info.get("uid"):
            table.add_row("Identity", uid)
        if created := key_info.get("created"):
            # Convert Unix timestamp to readable date
            try:
                dt = datetime.fromtimestamp(int(created), tz=timezone.utc)
                table.add_row("Created", dt.strftime("%Y-%m-%d %H:%M:%S"))
            except (ValueError, OSError):
                table.add_row("Created", created)

    # Check git configuration
    git_enabled = is_git_signing_enabled(project_root=root)
    if git_enabled:
        table.add_row("Git Signing", "[green]Enabled[/green]")
    else:
        table.add_row("Git Signing", "[yellow]Not enabled in this repo[/yellow]")

    console.print(table)

    # Show next steps if git not configured
    if not git_enabled:
        console.print()
        console.print(
            "[yellow]Git commit signing is not enabled in this repository.[/yellow]"
        )
        console.print(
            "[dim]Run 'flowspec gpg setup' to configure this repository.[/dim]"
        )


@gpg_app.command("rotate")
def rotate_command(
    project_root: Optional[str] = typer.Option(
        None,
        "--project-root",
        "-p",
        help="Project directory to reconfigure (default: current directory)",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompt",
    ),
) -> None:
    """Rotate the agent GPG key.

    This command:
    1. Deletes the existing agent GPG key
    2. Generates a new key
    3. Updates git configuration

    Key rotation is useful for security best practices or if a key is compromised.

    Examples:
        flowspec gpg rotate
        flowspec gpg rotate --yes  # Skip confirmation
    """
    root = Path(project_root) if project_root else Path.cwd()

    if not key_exists():
        console.print("[yellow]No agent GPG key found. Nothing to rotate.[/yellow]")
        console.print("[dim]Run 'flowspec gpg setup' to create a new key.[/dim]")
        return

    # Get old fingerprint for display
    old_fingerprint = get_key_fingerprint()

    if not yes:
        console.print(
            "[yellow]⚠ This will delete the current agent GPG key and generate a new one.[/yellow]"
        )
        console.print(f"[dim]Current fingerprint: {old_fingerprint}[/dim]")
        console.print()
        confirm = typer.confirm("Do you want to continue?", default=False)
        if not confirm:
            console.print("[dim]Cancelled.[/dim]")
            raise typer.Exit(0)

    try:
        # Delete old key
        console.print("[cyan]Deleting old key...[/cyan]")
        delete_agent_key()
        console.print("[green]✓[/green] Old key deleted")

        # Generate new key
        console.print("[cyan]Generating new key...[/cyan]")
        new_fingerprint = generate_agent_key()
        console.print("[green]✓[/green] New key generated")

        # Reconfigure git
        console.print("[cyan]Updating git configuration...[/cyan]")
        configure_git_signing(project_root=root)
        console.print("[green]✓[/green] Git configuration updated")

        # Display summary
        console.print()
        panel_content = f"""[bold]Key Rotation Complete[/bold]

[dim]Old fingerprint:[/dim]
{old_fingerprint}

[cyan]New fingerprint:[/cyan]
{new_fingerprint}

[dim]All future commits will be signed with the new key.[/dim]
"""
        console.print(
            Panel(
                panel_content,
                title="✓ Key Rotated",
                border_style="green",
                padding=(1, 2),
            )
        )

    except GPGError as e:
        console.print(f"[red]✗ Key rotation failed:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Unexpected error:[/red] {e}")
        raise typer.Exit(1)


__all__ = ["gpg_app"]
