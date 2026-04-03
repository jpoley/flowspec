"""Event schema v1.1.0 for flowspec JSONL event system.

This module defines the complete event schema with all namespaces:
- lifecycle, activity, coordination, hook, git, task, container, decision,
  system, action, security

Based on: build-docs/jsonl-event-system.md
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

# Type aliases for clarity
EventType = str
AgentId = str
SessionId = str
TaskId = str
EventSource = Literal["mcp", "hook", "cli", "system"]


@dataclass
class ToolObject:
    """Tool execution details."""

    tool_name: str
    tool_input: dict[str, Any] | None = None
    tool_result: str | None = None
    duration_ms: int | None = None


@dataclass
class HookObject:
    """Hook-specific payload."""

    hook_type: str
    raw_payload: dict[str, Any] | None = None


@dataclass
class GitObject:
    """Git operation details."""

    operation: str
    sha: str | None = None
    branch_name: str | None = None
    from_branch: str | None = None
    gpg_key_id: str | None = None
    gpg_fingerprint: str | None = None
    signer_agent_id: str | None = None
    message: str | None = None
    files_changed: int | None = None
    insertions: int | None = None
    deletions: int | None = None


@dataclass
class TaskObject:
    """Task operation details."""

    task_id: str
    title: str | None = None
    from_state: str | None = None
    to_state: str | None = None
    assigned_to: str | None = None
    labels: list[str] = field(default_factory=list)
    ac_index: int | None = None
    ac_text: str | None = None


@dataclass
class ResourceLimits:
    """Container resource limits."""

    memory_mb: int | None = None
    cpu_cores: int | None = None


@dataclass
class ContainerObject:
    """Container details."""

    container_id: str
    image: str | None = None
    exit_code: int | None = None
    secrets_injected: list[str] = field(default_factory=list)
    network_mode: str | None = None
    resource_limits: ResourceLimits | None = None


@dataclass
class ReversibilityInfo:
    """Decision reversibility details."""

    type: Literal["one-way-door", "two-way-door"]
    lock_in_factors: list[str] = field(default_factory=list)
    reversal_cost: str | None = None
    reversal_window: str | None = None


@dataclass
class Alternative:
    """Alternative option considered."""

    option: str
    rejected_reason: str


@dataclass
class Link:
    """External reference link."""

    url: str
    title: str
    type: str


@dataclass
class SupportingMaterial:
    """Supporting documentation."""

    links: list[Link] = field(default_factory=list)
    internal_refs: list[str] = field(default_factory=list)


@dataclass
class DecisionObject:
    """Decision details."""

    decision_id: str
    category: str
    reversibility: ReversibilityInfo | None = None
    alternatives_considered: list[Alternative] = field(default_factory=list)
    supporting_material: SupportingMaterial | None = None


@dataclass
class ActionErrorObject:
    """Action error details."""

    code: str
    message: str
    issues: list[Any] = field(default_factory=list)


@dataclass
class ActionObject:
    """Action invocation details."""

    verb: str
    domain: str | None = None
    category: str | None = None
    input: dict[str, Any] | None = None
    output: dict[str, Any] | None = None
    duration_ms: int | None = None
    error: ActionErrorObject | None = None


@dataclass
class ArtifactRef:
    """Security artifact reference."""

    type: str
    ref: str


@dataclass
class SignatureInfo:
    """Signature details."""

    algorithm: str
    key_id: str
    signature_ref: str


@dataclass
class AttestationInfo:
    """Attestation details."""

    type: str
    predicate: str


@dataclass
class VulnerabilityInfo:
    """Vulnerability details."""

    id: str
    severity: str
    package: str


@dataclass
class SecurityObject:
    """Security operation details."""

    artifact: ArtifactRef | None = None
    signature: SignatureInfo | None = None
    attestation: AttestationInfo | None = None
    vulnerability: VulnerabilityInfo | None = None


@dataclass
class ContextObject:
    """Cross-reference context for unified tracking."""

    task_id: str | None = None
    branch_name: str | None = None
    worktree_path: str | None = None
    container_id: str | None = None
    pr_number: int | None = None
    decision_id: str | None = None


@dataclass
class CorrelationObject:
    """Distributed tracing context."""

    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    root_agent_id: str | None = None


@dataclass
class FlowspecEvent:
    """Unified event structure for flowspec JSONL event system.

    Schema version: 1.1.0

    Attributes:
        version: Schema version (semver)
        event_type: Namespaced event type (e.g., "lifecycle.started")
        timestamp: ISO 8601 timestamp with timezone
        agent_id: Unique agent identifier
        event_id: UUID for this event
        session_id: Session grouping identifier
        source: Event origin (mcp, hook, cli, system)
        status: Legacy status for backward compatibility
        message: Human-readable description
        progress: Completion percentage (0.0-1.0)
        tool: Tool execution details
        hook: Hook-specific payload
        git: Git operation details
        task: Task operation details
        container: Container details
        decision: Decision details
        action: Action invocation details
        security: Security operation details
        context: Cross-reference context
        correlation: Distributed tracing context
        metadata: Arbitrary extensible data
    """

    version: str
    event_type: EventType
    timestamp: str
    agent_id: AgentId
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: SessionId | None = None
    source: EventSource | None = None
    status: str | None = None
    message: str | None = None
    progress: float | None = None
    tool: ToolObject | None = None
    hook: HookObject | None = None
    git: GitObject | None = None
    task: TaskObject | None = None
    container: ContainerObject | None = None
    decision: DecisionObject | None = None
    action: ActionObject | None = None
    security: SecurityObject | None = None
    context: ContextObject | None = None
    correlation: CorrelationObject | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary for JSON serialization.

        Returns:
            Dictionary representation with None values omitted
        """
        data: dict[str, Any] = {
            "version": self.version,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "agent_id": self.agent_id,
            "event_id": self.event_id,
        }

        # Add optional fields if present
        if self.session_id:
            data["session_id"] = self.session_id
        if self.source:
            data["source"] = self.source
        if self.status:
            data["status"] = self.status
        if self.message:
            data["message"] = self.message
        if self.progress is not None:
            data["progress"] = self.progress

        # Add object fields if present
        if self.tool:
            data["tool"] = self._obj_to_dict(self.tool)
        if self.hook:
            data["hook"] = self._obj_to_dict(self.hook)
        if self.git:
            data["git"] = self._obj_to_dict(self.git)
        if self.task:
            data["task"] = self._obj_to_dict(self.task)
        if self.container:
            data["container"] = self._obj_to_dict(self.container)
        if self.decision:
            data["decision"] = self._obj_to_dict(self.decision)
        if self.action:
            data["action"] = self._obj_to_dict(self.action)
        if self.security:
            data["security"] = self._obj_to_dict(self.security)
        if self.context:
            data["context"] = self._obj_to_dict(self.context)
        if self.correlation:
            data["correlation"] = self._obj_to_dict(self.correlation)
        if self.metadata:
            data["metadata"] = self.metadata

        return data

    def _obj_to_dict(self, obj: Any) -> dict[str, Any]:
        """Convert dataclass to dict, omitting None values."""
        if not hasattr(obj, "__dict__"):
            return obj

        result = {}
        for key, value in obj.__dict__.items():
            if value is None:
                continue
            if hasattr(value, "__dict__"):
                result[key] = self._obj_to_dict(value)
            elif isinstance(value, list):
                result[key] = [
                    self._obj_to_dict(item) if hasattr(item, "__dict__") else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

    @classmethod
    def create(
        cls,
        event_type: EventType,
        agent_id: AgentId,
        source: EventSource | None = None,
        message: str | None = None,
        session_id: SessionId | None = None,
        status: str | None = None,
        progress: float | None = None,
        tool: ToolObject | None = None,
        hook: HookObject | None = None,
        git: GitObject | None = None,
        task: TaskObject | None = None,
        container: ContainerObject | None = None,
        decision: DecisionObject | None = None,
        action: ActionObject | None = None,
        security: SecurityObject | None = None,
        context: ContextObject | None = None,
        correlation: CorrelationObject | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> FlowspecEvent:
        """Create a new flowspec event.

        Args:
            event_type: Namespaced event type
            agent_id: Unique agent identifier
            source: Event origin
            message: Human-readable description
            session_id: Session grouping identifier
            status: Legacy status for backward compatibility
            progress: Completion percentage
            tool: Tool execution details
            hook: Hook-specific payload
            git: Git operation details
            task: Task operation details
            container: Container details
            decision: Decision details
            action: Action invocation details
            security: Security operation details
            context: Cross-reference context
            correlation: Distributed tracing context
            metadata: Arbitrary extensible data

        Returns:
            A new FlowspecEvent instance
        """
        return cls(
            version="1.1.0",
            event_type=event_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            agent_id=agent_id,
            source=source,
            message=message,
            session_id=session_id,
            status=status,
            progress=progress,
            tool=tool,
            hook=hook,
            git=git,
            task=task,
            container=container,
            decision=decision,
            action=action,
            security=security,
            context=context,
            correlation=correlation,
            metadata=metadata or {},
        )


__all__ = [
    "EventType",
    "AgentId",
    "SessionId",
    "TaskId",
    "EventSource",
    "ToolObject",
    "HookObject",
    "GitObject",
    "TaskObject",
    "ResourceLimits",
    "ContainerObject",
    "ReversibilityInfo",
    "Alternative",
    "Link",
    "SupportingMaterial",
    "DecisionObject",
    "ActionErrorObject",
    "ActionObject",
    "ArtifactRef",
    "SignatureInfo",
    "AttestationInfo",
    "VulnerabilityInfo",
    "SecurityObject",
    "ContextObject",
    "CorrelationObject",
    "FlowspecEvent",
]
