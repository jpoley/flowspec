"""Action Registry and action→event mapping for flowspec.

This module provides the action registry with 55 actions across 18 categories
as defined in the action system specification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .event_writer import emit_event
from .schema import ActionObject, FlowspecEvent


ActionDomain = Literal["human", "agent", "code", "system", "human|agent"]
ActionCategory = Literal[
    "read",
    "analyze",
    "decide",
    "plan",
    "control",
    "execute",
    "integrate",
    "scm",
    "quality",
    "security",
    "mutate",
    "signal",
    "session",
    "explain",
    "recovery",
    "record",
    "comms",
    "container",
]


@dataclass
class ActionDefinition:
    """Definition of an action in the registry.

    Attributes:
        verb: Action verb (e.g., "validate", "merge")
        domain: Who can perform this action
        category: Action category
        intent: Human-readable intent
        input_contract: Expected input fields
        output_contract: Expected output fields
        side_effects: Description of side effects
        idempotent: Whether action is idempotent
        events_emitted: List of event types emitted
        typical_use_cases: List of use cases
        allowed_followups: Actions that can follow this one
    """

    verb: str
    domain: ActionDomain
    category: ActionCategory
    intent: str
    input_contract: dict[str, Any] = field(default_factory=dict)
    output_contract: dict[str, Any] = field(default_factory=dict)
    side_effects: str = "none"
    idempotent: bool = True
    events_emitted: list[str] = field(default_factory=list)
    typical_use_cases: list[str] = field(default_factory=list)
    allowed_followups: list[str] = field(default_factory=list)


class ActionRegistry:
    """Registry for all flowspec actions.

    The registry maintains definitions for 55 actions across 18 categories.
    """

    def __init__(self) -> None:
        """Initialize the action registry."""
        self._actions: dict[str, ActionDefinition] = {}
        self._initialize_actions()

    def _initialize_actions(self) -> None:
        """Initialize all action definitions."""
        # Read actions
        self.register(
            ActionDefinition(
                verb="list",
                domain="agent",
                category="read",
                intent="enumerate resources",
                events_emitted=["action.succeeded"],
                typical_use_cases=["list repos", "list tasks", "list sessions"],
                allowed_followups=["describe", "inspect", "diff"],
            )
        )

        self.register(
            ActionDefinition(
                verb="inspect",
                domain="agent",
                category="read",
                intent="deep state fetch",
                events_emitted=["action.succeeded"],
                typical_use_cases=["inspect repo metadata", "inspect backlog item"],
                allowed_followups=["diff", "validate", "plan"],
            )
        )

        self.register(
            ActionDefinition(
                verb="describe",
                domain="agent",
                category="read",
                intent="human summary",
                events_emitted=["action.succeeded"],
                typical_use_cases=["summarize a PR", "explain a plan"],
                allowed_followups=["inspect", "audit"],
            )
        )

        # Analyze actions
        self.register(
            ActionDefinition(
                verb="diff",
                domain="code",
                category="analyze",
                intent="compare states",
                events_emitted=["action.succeeded"],
                typical_use_cases=["git diff branches", "infra/state diff"],
                allowed_followups=["plan", "apply"],
            )
        )

        # Decision actions
        self.register(
            ActionDefinition(
                verb="validate",
                domain="human|agent",
                category="decide",
                intent="check invariants",
                events_emitted=["action.succeeded", "decision.made"],
                typical_use_cases=["preflight checks", "schema validation"],
                allowed_followups=["plan", "break"],
            )
        )

        self.register(
            ActionDefinition(
                verb="triage",
                domain="agent",
                category="decide",
                intent="prioritize findings",
                events_emitted=["action.succeeded", "decision.made"],
                typical_use_cases=["triage lint/SAST findings"],
            )
        )

        self.register(
            ActionDefinition(
                verb="verify",
                domain="human|agent",
                category="decide",
                intent="confirm expected outcome",
                events_emitted=["action.succeeded", "decision.made"],
                typical_use_cases=["post-merge checks", "release verification"],
            )
        )

        # Planning actions
        self.register(
            ActionDefinition(
                verb="plan",
                domain="agent",
                category="plan",
                intent="propose actions",
                events_emitted=["action.succeeded", "decision.made"],
                typical_use_cases=["generate rollout plan", "refactor plan"],
                allowed_followups=["apply", "delegate", "break", "approve"],
            )
        )

        # Control actions
        self.register(
            ActionDefinition(
                verb="approve",
                domain="human|agent",
                category="control",
                intent="explicit approval gate",
                side_effects="records approval",
                events_emitted=["action.succeeded", "decision.made"],
                typical_use_cases=["change-control signoff", "gated release"],
                allowed_followups=["apply", "break"],
            )
        )

        self.register(
            ActionDefinition(
                verb="reject",
                domain="human",
                category="control",
                intent="explicit rejection",
                side_effects="records rejection",
                events_emitted=["action.succeeded", "decision.made"],
                typical_use_cases=["reject PR", "deny release"],
                allowed_followups=["plan", "break"],
            )
        )

        self.register(
            ActionDefinition(
                verb="delegate",
                domain="agent",
                category="control",
                intent="hand off to sub-agent",
                side_effects="spawns work",
                idempotent=False,
                events_emitted=["action.succeeded", "coordination.handoff"],
                typical_use_cases=["delegate SAST review to security agent"],
            )
        )

        self.register(
            ActionDefinition(
                verb="waive",
                domain="human|agent",
                category="control",
                intent="risk-accept exception",
                side_effects="records exception",
                events_emitted=["action.succeeded", "decision.made"],
                typical_use_cases=["accept false positive"],
            )
        )

        self.register(
            ActionDefinition(
                verb="request_changes",
                domain="human",
                category="control",
                intent="request modifications",
                side_effects="records request",
                events_emitted=["action.succeeded"],
                typical_use_cases=["request PR modifications"],
            )
        )

        # Execute actions
        self.register(
            ActionDefinition(
                verb="apply",
                domain="agent",
                category="execute",
                intent="enact a plan safely",
                side_effects="mutates state",
                idempotent=False,
                events_emitted=["action.succeeded", "git.commit"],
                typical_use_cases=["run planned CI/CD steps", "apply changes"],
            )
        )

        self.register(
            ActionDefinition(
                verb="execute",
                domain="code",
                category="execute",
                intent="run one concrete step",
                side_effects="may mutate",
                idempotent=False,
                events_emitted=["action.succeeded"],
                typical_use_cases=["run lint", "run tests", "run formatter"],
            )
        )

        # Integration actions
        self.register(
            ActionDefinition(
                verb="merge",
                domain="agent",
                category="integrate",
                intent="combine work products",
                side_effects="updates artifacts",
                idempotent=False,
                events_emitted=["action.succeeded", "git.merged"],
                typical_use_cases=["merge sub-agent changes", "merge edits"],
            )
        )

        # SCM actions
        self.register(
            ActionDefinition(
                verb="create_worktree",
                domain="code",
                category="scm",
                intent="create git worktree",
                side_effects="creates worktree",
                idempotent=False,
                events_emitted=[
                    "action.succeeded",
                    "git.worktree_created",
                    "git.branch_created",
                ],
                typical_use_cases=["isolate task work"],
            )
        )

        self.register(
            ActionDefinition(
                verb="remove_worktree",
                domain="code",
                category="scm",
                intent="remove git worktree",
                side_effects="removes worktree",
                idempotent=False,
                events_emitted=["action.succeeded", "git.worktree_removed"],
                typical_use_cases=["cleanup after task"],
            )
        )

        self.register(
            ActionDefinition(
                verb="create_pr",
                domain="code",
                category="scm",
                intent="open pull request",
                side_effects="creates PR",
                idempotent=False,
                events_emitted=["action.succeeded", "git.pr_created"],
                typical_use_cases=["open PR after changes"],
            )
        )

        self.register(
            ActionDefinition(
                verb="merge_pr",
                domain="code",
                category="scm",
                intent="merge pull request",
                side_effects="merges PR",
                idempotent=False,
                events_emitted=["action.succeeded", "git.merged"],
                typical_use_cases=["finalize approved work"],
            )
        )

        self.register(
            ActionDefinition(
                verb="rebase",
                domain="code",
                category="scm",
                intent="replay commits",
                side_effects="rewrites history",
                idempotent=False,
                events_emitted=["action.succeeded", "git.commit"],
                typical_use_cases=["keep branch up to date"],
            )
        )

        self.register(
            ActionDefinition(
                verb="resolve_conflicts",
                domain="code",
                category="scm",
                intent="resolve merge conflicts",
                side_effects="mutates tree",
                idempotent=False,
                events_emitted=["action.succeeded", "git.conflict_resolved"],
                typical_use_cases=["fix conflict markers"],
            )
        )

        self.register(
            ActionDefinition(
                verb="submit_local_pr",
                domain="code",
                category="scm",
                intent="submit for local review",
                side_effects="triggers checks",
                idempotent=False,
                events_emitted=["action.succeeded", "git.local_pr_submitted"],
                typical_use_cases=["pre-push quality gate"],
            )
        )

        # Quality actions
        self.register(
            ActionDefinition(
                verb="lint",
                domain="code",
                category="quality",
                intent="style/static checks",
                events_emitted=["action.succeeded"],
                typical_use_cases=["run ESLint", "golangci-lint"],
            )
        )

        self.register(
            ActionDefinition(
                verb="format",
                domain="code",
                category="quality",
                intent="auto-format",
                side_effects="mutates files",
                events_emitted=["action.succeeded", "git.commit"],
                typical_use_cases=["gofmt", "prettier", "black"],
            )
        )

        self.register(
            ActionDefinition(
                verb="test",
                domain="code",
                category="quality",
                intent="run tests",
                side_effects="may start services",
                idempotent=False,
                events_emitted=["action.succeeded"],
                typical_use_cases=["run CI tests"],
            )
        )

        self.register(
            ActionDefinition(
                verb="run_checks",
                domain="code",
                category="quality",
                intent="run all quality gates",
                events_emitted=[
                    "action.succeeded",
                    "git.local_pr_approved",
                    "git.local_pr_rejected",
                ],
                typical_use_cases=["unified quality gate"],
            )
        )

        # Security actions
        self.register(
            ActionDefinition(
                verb="sast",
                domain="code",
                category="security",
                intent="static security test",
                events_emitted=["action.succeeded"],
                typical_use_cases=["CodeQL", "Semgrep scan"],
            )
        )

        self.register(
            ActionDefinition(
                verb="sca",
                domain="code",
                category="security",
                intent="dependency scan",
                events_emitted=["action.succeeded"],
                typical_use_cases=["dependency CVEs"],
            )
        )

        self.register(
            ActionDefinition(
                verb="sbom",
                domain="code",
                category="security",
                intent="generate SBOM",
                side_effects="writes artifact",
                events_emitted=["action.succeeded"],
                typical_use_cases=["CycloneDX generation"],
            )
        )

        self.register(
            ActionDefinition(
                verb="sign",
                domain="code",
                category="security",
                intent="sign artifact",
                side_effects="writes signature",
                events_emitted=["action.succeeded", "security.artifact_signed"],
                typical_use_cases=["sign container"],
            )
        )

        self.register(
            ActionDefinition(
                verb="sign_commit",
                domain="code",
                category="security",
                intent="GPG sign commit",
                side_effects="updates commit",
                events_emitted=["action.succeeded", "git.commit"],
                typical_use_cases=["agent commit signing"],
            )
        )

        # Mutation actions
        self.register(
            ActionDefinition(
                verb="fix",
                domain="code",
                category="mutate",
                intent="apply code changes",
                side_effects="mutates files",
                idempotent=False,
                events_emitted=["action.succeeded"],
                typical_use_cases=["apply suggested edits"],
            )
        )

        # Signal actions
        self.register(
            ActionDefinition(
                verb="trigger",
                domain="system",
                category="signal",
                intent="emit event",
                side_effects="emits event",
                events_emitted=["action.succeeded"],
                typical_use_cases=["fire webhook"],
            )
        )

        # Session actions
        self.register(
            ActionDefinition(
                verb="start",
                domain="agent",
                category="session",
                intent="begin session",
                side_effects="alloc session",
                idempotent=False,
                events_emitted=["action.succeeded", "lifecycle.started"],
                typical_use_cases=["start agent/job"],
            )
        )

        self.register(
            ActionDefinition(
                verb="break",
                domain="human|agent",
                category="session",
                intent="interrupt + demand rationale",
                side_effects="interrupts",
                events_emitted=["action.succeeded", "lifecycle.paused"],
                typical_use_cases=["halt on risk", "pause for approval"],
            )
        )

        self.register(
            ActionDefinition(
                verb="resume",
                domain="human|agent",
                category="session",
                intent="continue session",
                side_effects="continues",
                idempotent=False,
                events_emitted=["action.succeeded", "lifecycle.resumed"],
                typical_use_cases=["resume paused workflow"],
            )
        )

        self.register(
            ActionDefinition(
                verb="stop",
                domain="human|agent",
                category="session",
                intent="end session",
                side_effects="may cleanup",
                events_emitted=["action.succeeded", "lifecycle.completed"],
                typical_use_cases=["stop agent/job"],
            )
        )

        # Explain actions
        self.register(
            ActionDefinition(
                verb="why",
                domain="agent",
                category="explain",
                intent="rationale for action",
                events_emitted=["action.succeeded"],
                typical_use_cases=["explain why break happened"],
            )
        )

        # Recovery actions
        self.register(
            ActionDefinition(
                verb="retry",
                domain="agent",
                category="recovery",
                intent="rerun operation",
                side_effects="repeats execution",
                idempotent=False,
                events_emitted=["action.succeeded", "action.failed"],
                typical_use_cases=["rerun flaky step"],
            )
        )

        self.register(
            ActionDefinition(
                verb="rollback",
                domain="agent",
                category="recovery",
                intent="revert effects",
                side_effects="mutates state",
                idempotent=False,
                events_emitted=["action.succeeded"],
                typical_use_cases=["revert deploy"],
            )
        )

        # Record actions
        self.register(
            ActionDefinition(
                verb="audit",
                domain="agent",
                category="record",
                intent="evidence trail",
                side_effects="records evidence",
                events_emitted=["action.succeeded"],
                typical_use_cases=["compliance pack"],
            )
        )

        self.register(
            ActionDefinition(
                verb="publish",
                domain="agent",
                category="record",
                intent="make artifact available",
                side_effects="writes artifact",
                events_emitted=["action.succeeded"],
                typical_use_cases=["publish SBOM/SARIF"],
            )
        )

        # Communication actions
        self.register(
            ActionDefinition(
                verb="notify",
                domain="system",
                category="comms",
                intent="alert humans/systems",
                side_effects="sends message",
                events_emitted=["action.succeeded"],
                typical_use_cases=["Slack/page/email"],
            )
        )

        self.register(
            ActionDefinition(
                verb="comment",
                domain="human",
                category="comms",
                intent="provide feedback",
                side_effects="records comment",
                events_emitted=["action.succeeded"],
                typical_use_cases=["PR comment", "task comment"],
            )
        )

        self.register(
            ActionDefinition(
                verb="review",
                domain="human",
                category="comms",
                intent="formal review",
                side_effects="records review",
                events_emitted=["action.succeeded", "decision.made"],
                typical_use_cases=["code review submission"],
            )
        )

        # Container actions
        self.register(
            ActionDefinition(
                verb="spawn_container",
                domain="system",
                category="container",
                intent="create container",
                side_effects="creates container",
                idempotent=False,
                events_emitted=["action.succeeded", "container.started"],
                typical_use_cases=["create devcontainer for task"],
            )
        )

        self.register(
            ActionDefinition(
                verb="attach_container",
                domain="agent",
                category="container",
                intent="attach to container",
                side_effects="records attachment",
                events_emitted=["action.succeeded", "container.agent_attached"],
                typical_use_cases=["agent connects to container"],
            )
        )

        self.register(
            ActionDefinition(
                verb="destroy_container",
                domain="system",
                category="container",
                intent="remove container",
                side_effects="removes container",
                idempotent=False,
                events_emitted=["action.succeeded", "container.stopped"],
                typical_use_cases=["cleanup container"],
            )
        )

        self.register(
            ActionDefinition(
                verb="inject_secrets",
                domain="system",
                category="container",
                intent="inject runtime secrets",
                side_effects="injects secrets",
                events_emitted=["action.succeeded", "container.secrets_injected"],
                typical_use_cases=["runtime secret injection"],
            )
        )

    def register(self, action: ActionDefinition) -> None:
        """Register an action definition.

        Args:
            action: Action definition to register
        """
        self._actions[action.verb] = action

    def get(self, verb: str) -> ActionDefinition | None:
        """Get an action definition by verb.

        Args:
            verb: Action verb

        Returns:
            Action definition or None if not found
        """
        return self._actions.get(verb)

    def list_by_category(self, category: ActionCategory) -> list[ActionDefinition]:
        """List all actions in a category.

        Args:
            category: Action category

        Returns:
            List of action definitions
        """
        return [
            action for action in self._actions.values() if action.category == category
        ]

    def list_by_domain(self, domain: ActionDomain) -> list[ActionDefinition]:
        """List all actions in a domain.

        Args:
            domain: Action domain

        Returns:
            List of action definitions
        """
        return [action for action in self._actions.values() if action.domain == domain]

    def list_all(self) -> list[ActionDefinition]:
        """List all registered actions.

        Returns:
            List of all action definitions
        """
        return list(self._actions.values())

    def count(self) -> int:
        """Count registered actions.

        Returns:
            Number of registered actions
        """
        return len(self._actions)


# Global registry instance
_registry: ActionRegistry | None = None


def get_registry() -> ActionRegistry:
    """Get the global action registry.

    Returns:
        The global ActionRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = ActionRegistry()
    return _registry


def emit_action_invoked(
    verb: str,
    domain: ActionDomain,
    category: ActionCategory,
    agent_id: str,
    input_data: dict[str, Any] | None = None,
    message: str | None = None,
) -> bool:
    """Emit an action.invoked event.

    Args:
        verb: Action verb
        domain: Action domain
        category: Action category
        agent_id: Agent performing the action
        input_data: Input parameters for the action
        message: Human-readable message

    Returns:
        True if event was emitted successfully
    """
    action_obj = ActionObject(
        verb=verb,
        domain=domain,
        category=category,
        input=input_data,
    )

    event = FlowspecEvent.create(
        event_type="action.invoked",
        agent_id=agent_id,
        source="cli",
        message=message or f"Action invoked: {verb}",
        action=action_obj,
    )

    return emit_event(event)


def emit_action_succeeded(
    verb: str,
    agent_id: str,
    output_data: dict[str, Any] | None = None,
    duration_ms: int | None = None,
    message: str | None = None,
) -> bool:
    """Emit an action.succeeded event.

    Args:
        verb: Action verb
        agent_id: Agent who performed the action
        output_data: Output from the action
        duration_ms: Execution duration in milliseconds
        message: Human-readable message

    Returns:
        True if event was emitted successfully
    """
    action_obj = ActionObject(
        verb=verb,
        output=output_data,
        duration_ms=duration_ms,
    )

    event = FlowspecEvent.create(
        event_type="action.succeeded",
        agent_id=agent_id,
        source="cli",
        message=message or f"Action succeeded: {verb}",
        action=action_obj,
    )

    return emit_event(event)


def emit_action_failed(
    verb: str,
    agent_id: str,
    error_code: str,
    error_message: str,
    duration_ms: int | None = None,
    message: str | None = None,
) -> bool:
    """Emit an action.failed event.

    Args:
        verb: Action verb
        agent_id: Agent who performed the action
        error_code: Error code
        error_message: Error message
        duration_ms: Execution duration in milliseconds
        message: Human-readable message

    Returns:
        True if event was emitted successfully
    """
    from .schema import ActionErrorObject

    error_obj = ActionErrorObject(code=error_code, message=error_message)
    action_obj = ActionObject(
        verb=verb,
        error=error_obj,
        duration_ms=duration_ms,
    )

    event = FlowspecEvent.create(
        event_type="action.failed",
        agent_id=agent_id,
        source="cli",
        message=message or f"Action failed: {verb}",
        action=action_obj,
    )

    return emit_event(event)


__all__ = [
    "ActionDomain",
    "ActionCategory",
    "ActionDefinition",
    "ActionRegistry",
    "get_registry",
    "emit_action_invoked",
    "emit_action_succeeded",
    "emit_action_failed",
]
