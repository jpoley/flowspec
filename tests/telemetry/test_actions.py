"""Tests for the action registry module."""

from __future__ import annotations

from flowspec_cli.telemetry.actions import (
    ActionRegistry,
    get_registry,
)


def test_registry_initialization() -> None:
    """Test that registry is initialized with 55 actions."""
    registry = ActionRegistry()
    assert registry.count() == 55


def test_get_action() -> None:
    """Test getting an action by verb."""
    registry = ActionRegistry()

    validate_action = registry.get("validate")
    assert validate_action is not None
    assert validate_action.verb == "validate"
    assert validate_action.domain == "human|agent"
    assert validate_action.category == "decide"
    assert "decision.made" in validate_action.events_emitted


def test_list_by_category() -> None:
    """Test listing actions by category."""
    registry = ActionRegistry()

    scm_actions = registry.list_by_category("scm")
    assert len(scm_actions) > 0

    scm_verbs = {action.verb for action in scm_actions}
    assert "create_worktree" in scm_verbs
    assert "remove_worktree" in scm_verbs
    assert "create_pr" in scm_verbs
    assert "merge_pr" in scm_verbs


def test_list_by_domain() -> None:
    """Test listing actions by domain."""
    registry = ActionRegistry()

    agent_actions = registry.list_by_domain("agent")
    assert len(agent_actions) > 0

    agent_verbs = {action.verb for action in agent_actions}
    assert "list" in agent_verbs
    assert "inspect" in agent_verbs
    assert "plan" in agent_verbs


def test_action_definitions() -> None:
    """Test that key actions have proper definitions."""
    registry = ActionRegistry()

    # Test validate action
    validate = registry.get("validate")
    assert validate is not None
    assert validate.intent == "check invariants"
    assert validate.idempotent is True
    assert "action.succeeded" in validate.events_emitted
    assert "decision.made" in validate.events_emitted

    # Test create_worktree action
    create_worktree = registry.get("create_worktree")
    assert create_worktree is not None
    assert create_worktree.domain == "code"
    assert create_worktree.category == "scm"
    assert create_worktree.idempotent is False
    assert "git.worktree_created" in create_worktree.events_emitted

    # Test approve action
    approve = registry.get("approve")
    assert approve is not None
    assert approve.domain == "human|agent"
    assert approve.category == "control"
    assert approve.side_effects == "records approval"


def test_allowed_followups() -> None:
    """Test that actions have proper allowed followups."""
    registry = ActionRegistry()

    plan_action = registry.get("plan")
    assert plan_action is not None
    assert "apply" in plan_action.allowed_followups
    assert "approve" in plan_action.allowed_followups
    assert "delegate" in plan_action.allowed_followups


def test_list_all() -> None:
    """Test listing all actions."""
    registry = ActionRegistry()

    all_actions = registry.list_all()
    assert len(all_actions) == 55

    # Verify we have actions from different categories
    categories = {action.category for action in all_actions}
    assert "read" in categories
    assert "decide" in categories
    assert "scm" in categories
    assert "security" in categories
    assert "control" in categories


def test_global_registry() -> None:
    """Test global registry instance."""
    registry = get_registry()
    assert isinstance(registry, ActionRegistry)
    assert registry.count() == 55


def test_container_actions() -> None:
    """Test container-related actions."""
    registry = ActionRegistry()

    container_actions = registry.list_by_category("container")
    assert len(container_actions) == 4

    container_verbs = {action.verb for action in container_actions}
    assert "spawn_container" in container_verbs
    assert "attach_container" in container_verbs
    assert "destroy_container" in container_verbs
    assert "inject_secrets" in container_verbs


def test_security_actions() -> None:
    """Test security-related actions."""
    registry = ActionRegistry()

    security_actions = registry.list_by_category("security")
    assert len(security_actions) > 0

    security_verbs = {action.verb for action in security_actions}
    assert "sast" in security_verbs
    assert "sca" in security_verbs
    assert "sign" in security_verbs
    assert "sbom" in security_verbs


def test_quality_actions() -> None:
    """Test quality-related actions."""
    registry = ActionRegistry()

    quality_actions = registry.list_by_category("quality")
    assert len(quality_actions) > 0

    quality_verbs = {action.verb for action in quality_actions}
    assert "lint" in quality_verbs
    assert "format" in quality_verbs
    assert "test" in quality_verbs
    assert "run_checks" in quality_verbs


def test_idempotent_actions() -> None:
    """Test that certain actions are marked as idempotent."""
    registry = ActionRegistry()

    # Idempotent actions
    validate = registry.get("validate")
    assert validate is not None
    assert validate.idempotent is True

    lint = registry.get("lint")
    assert lint is not None
    assert lint.idempotent is True

    # Non-idempotent actions
    create_worktree = registry.get("create_worktree")
    assert create_worktree is not None
    assert create_worktree.idempotent is False

    apply = registry.get("apply")
    assert apply is not None
    assert apply.idempotent is False
