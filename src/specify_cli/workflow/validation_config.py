"""Workflow transition validation configuration.

This module provides interactive configuration for workflow transition validation modes.
Used by 'specify init' to configure validation gates for each workflow transition.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from specify_cli.workflow.transition import (
    WORKFLOW_TRANSITIONS,
    ValidationMode,
    format_validation_mode,
)

console = Console()


def prompt_validation_mode(
    transition_name: str, transition_description: str
) -> tuple[ValidationMode, str | None]:
    """Prompt user to select validation mode for a transition.

    Args:
        transition_name: Name of the transition (e.g., "assess", "specify").
        transition_description: Human-readable description of the transition.

    Returns:
        Tuple of (ValidationMode, optional keyword string).

    Example:
        >>> mode, keyword = prompt_validation_mode("specify", "Create PRD")
        >>> # User selects KEYWORD and enters "PRD_APPROVED"
        >>> mode == ValidationMode.KEYWORD
        True
        >>> keyword
        'PRD_APPROVED'
    """
    console.print(f"\n[cyan]{transition_name}:[/cyan] {transition_description}")
    console.print("[dim]How should this transition be validated?[/dim]")
    console.print("  [1] NONE (default) - Proceed automatically")
    console.print("  [2] KEYWORD - Require typed keyword to proceed")
    console.print("  [3] PULL_REQUEST - Require merged PR to proceed")

    choice = Prompt.ask(
        "Select validation mode",
        choices=["1", "2", "3", ""],
        default="1",
        show_default=False,
    )

    if choice == "2":
        console.print(
            "[dim]Enter the keyword users must type to approve this transition:[/dim]"
        )
        keyword = Prompt.ask(
            "Keyword",
            default=f"{transition_name.upper()}_APPROVED",
        )
        return (ValidationMode.KEYWORD, keyword)
    elif choice == "3":
        return (ValidationMode.PULL_REQUEST, None)
    else:
        # Default or explicit choice "1"
        return (ValidationMode.NONE, None)


def prompt_all_transitions(
    batch_mode: str | None = None, batch_keyword: str | None = None
) -> dict[str, tuple[ValidationMode, str | None]]:
    """Prompt for validation modes for all workflow transitions.

    Args:
        batch_mode: Optional batch mode (none, keyword, pull-request) to skip prompts.
        batch_keyword: Optional keyword to use for all KEYWORD validations in batch mode.

    Returns:
        Dictionary mapping transition names to (ValidationMode, keyword) tuples.

    Example:
        >>> configs = prompt_all_transitions()
        >>> # User interactively selects modes for each transition
        >>> configs["specify"]
        (ValidationMode.KEYWORD, 'PRD_APPROVED')
    """
    if batch_mode:
        # Batch mode: apply same validation to all transitions
        if batch_mode == "keyword":
            default_keyword = batch_keyword or "APPROVED"
            return {
                t.name: (ValidationMode.KEYWORD, default_keyword)
                for t in WORKFLOW_TRANSITIONS
            }
        elif batch_mode == "pull-request":
            return {
                t.name: (ValidationMode.PULL_REQUEST, None)
                for t in WORKFLOW_TRANSITIONS
            }
        else:  # none
            return {t.name: (ValidationMode.NONE, None) for t in WORKFLOW_TRANSITIONS}

    # Interactive mode
    console.print(
        Panel(
            "[cyan]Workflow Transition Validation Configuration[/cyan]\n\n"
            "Configure validation gates for each workflow transition.\n"
            "Press Enter to accept default (NONE).",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    configs: dict[str, tuple[ValidationMode, str | None]] = {}
    for transition in WORKFLOW_TRANSITIONS:
        mode, keyword = prompt_validation_mode(
            transition.name,
            transition.description or f"Transition to {transition.to_state}",
        )
        configs[transition.name] = (mode, keyword)

    return configs


def generate_workflow_yaml(
    configs: dict[str, tuple[ValidationMode, str | None]], output_path: Path
) -> None:
    """Generate jpspec_workflow.yml with configured validation modes.

    Args:
        configs: Dictionary mapping transition names to (ValidationMode, keyword) tuples.
        output_path: Path where jpspec_workflow.yml should be written.

    Example:
        >>> configs = {
        ...     "specify": (ValidationMode.KEYWORD, "PRD_APPROVED"),
        ...     "plan": (ValidationMode.NONE, None),
        ... }
        >>> generate_workflow_yaml(configs, Path("./jpspec_workflow.yml"))
    """
    # Build workflow data structure
    workflow_data: dict[str, Any] = {
        "version": "1.0",
        "workflow": {"name": "jpspec", "description": "JP Spec Kit Workflow"},
        "transitions": [],
    }

    for transition in WORKFLOW_TRANSITIONS:
        mode, keyword = configs.get(transition.name, (ValidationMode.NONE, None))

        # Update transition with configured validation
        transition.validation = mode
        transition.validation_keyword = keyword

        # Convert to dict for YAML
        workflow_data["transitions"].append(transition.to_dict())

    # Write YAML file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(
            workflow_data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )

    console.print(
        f"\n[green]Workflow configuration saved to:[/green] {output_path.relative_to(Path.cwd()) if output_path.is_relative_to(Path.cwd()) else output_path}"
    )


def display_validation_summary(
    configs: dict[str, tuple[ValidationMode, str | None]],
) -> None:
    """Display summary of configured validation modes.

    Args:
        configs: Dictionary mapping transition names to (ValidationMode, keyword) tuples.

    Example:
        >>> configs = {
        ...     "specify": (ValidationMode.KEYWORD, "PRD_APPROVED"),
        ...     "plan": (ValidationMode.NONE, None),
        ... }
        >>> display_validation_summary(configs)
    """
    lines = ["[cyan]Validation Mode Summary:[/cyan]", ""]

    for transition in WORKFLOW_TRANSITIONS:
        mode, keyword = configs.get(transition.name, (ValidationMode.NONE, None))
        mode_str = format_validation_mode(mode, keyword)

        # Format display
        if mode == ValidationMode.KEYWORD:
            display = f"[yellow]{mode_str}[/yellow]"
        elif mode == ValidationMode.PULL_REQUEST:
            display = f"[magenta]{mode_str}[/magenta]"
        else:
            display = f"[dim]{mode_str}[/dim]"

        lines.append(f"  {transition.name:<15} → {display}")

    console.print(
        Panel(
            "\n".join(lines),
            title="[cyan]Configured Validation Modes[/cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )


def configure_validation_modes(
    project_path: Path,
    batch_mode: str | None = None,
    batch_keyword: str | None = None,
    no_prompts: bool = False,
) -> None:
    """Configure validation modes for workflow transitions.

    Main entry point for validation configuration, called by 'specify init'.

    Args:
        project_path: Path to the project directory.
        batch_mode: Optional batch mode (none, keyword, pull-request).
        batch_keyword: Optional keyword for batch KEYWORD mode.
        no_prompts: If True, use NONE for all transitions (skip prompts).

    Example:
        >>> configure_validation_modes(Path("./my-project"))
        # Interactive prompts for each transition
        >>> configure_validation_modes(
        ...     Path("./my-project"),
        ...     batch_mode="keyword",
        ...     batch_keyword="APPROVED"
        ... )
        # All transitions use KEYWORD["APPROVED"]
    """
    if no_prompts:
        # Skip all prompts, use NONE
        configs = {t.name: (ValidationMode.NONE, None) for t in WORKFLOW_TRANSITIONS}
    elif batch_mode:
        # Batch mode
        configs = prompt_all_transitions(
            batch_mode=batch_mode, batch_keyword=batch_keyword
        )
    else:
        # Interactive mode
        configs = prompt_all_transitions()

    # Generate workflow YAML
    workflow_path = project_path / "jpspec_workflow.yml"
    generate_workflow_yaml(configs, workflow_path)

    # Display summary
    if not no_prompts:
        display_validation_summary(configs)


# CLI command for reconfiguration
def reconfigure_validation_modes(
    batch_mode: str | None = None,
    batch_keyword: str | None = None,
) -> None:
    """Reconfigure validation modes for existing project.

    Used by 'specify config validation' command.

    Args:
        batch_mode: Optional batch mode (none, keyword, pull-request).
        batch_keyword: Optional keyword for batch KEYWORD mode.

    Example:
        >>> reconfigure_validation_modes()
        # Interactive prompts
        >>> reconfigure_validation_modes(batch_mode="none")
        # Set all to NONE
    """
    project_path = Path.cwd()
    workflow_path = project_path / "jpspec_workflow.yml"

    if not workflow_path.exists():
        console.print(
            f"[yellow]Warning:[/yellow] {workflow_path} not found. Creating new configuration."
        )

    configure_validation_modes(
        project_path, batch_mode=batch_mode, batch_keyword=batch_keyword
    )

    console.print("[green]Validation configuration updated successfully![/green]")
