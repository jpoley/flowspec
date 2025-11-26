# Satellite Mode Conflict Resolution Strategies

**Related Task:** task-021 - Design Conflict Resolution Strategies
**Status:** Phase 2: Design
**Dependencies:** task-020 (Sync Engine)

---

## Overview

When a task is modified both locally and remotely since the last sync, a conflict occurs. This document defines the strategy pattern for resolving such conflicts.

```
Last Sync: t0
         │
    ┌────┴────┐
    │         │
    ▼         ▼
Local Edit  Remote Edit
  (t1)        (t2)
    │         │
    └────┬────┘
         │
         ▼
    CONFLICT!
         │
         ▼
  Resolution Strategy
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  Winner    Merged
```

---

## Strategy Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional
from enum import Enum

class ResolutionResult(Enum):
    """Outcome of conflict resolution."""
    LOCAL_WINS = "local_wins"
    REMOTE_WINS = "remote_wins"
    MERGED = "merged"
    SKIP = "skip"
    USER_CANCELLED = "user_cancelled"

@dataclass
class ConflictContext:
    """Full context for a sync conflict."""
    task_id: str
    field: str                      # Which field conflicts
    local_value: Any               # Current local value
    remote_value: Any              # Current remote value
    base_value: Optional[Any]      # Value at last sync (if known)
    local_updated: datetime        # When local was modified
    remote_updated: datetime       # When remote was modified
    local_task: "LocalTask"        # Full local task
    remote_task: "RemoteTask"      # Full remote task

@dataclass
class Resolution:
    """Result of resolving a conflict."""
    result: ResolutionResult
    resolved_value: Any
    reason: str                    # Human-readable explanation

class ConflictResolver(ABC):
    """
    Abstract base class for conflict resolution strategies.

    Implement this interface to create custom resolution strategies.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Strategy name for config/logging."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description."""
        ...

    @abstractmethod
    def resolve(self, context: ConflictContext) -> Resolution:
        """
        Resolve a single field conflict.

        Args:
            context: Full conflict information

        Returns:
            Resolution with chosen value and reason
        """
        ...

    def resolve_task(
        self,
        local: "LocalTask",
        remote: "RemoteTask",
        conflicts: List[str]
    ) -> Dict[str, Resolution]:
        """
        Resolve all conflicts for a task.

        Default implementation calls resolve() for each field.
        Override for strategies that need holistic view.
        """
        resolutions = {}
        for field in conflicts:
            context = ConflictContext(
                task_id=local.id,
                field=field,
                local_value=getattr(local, field),
                remote_value=getattr(remote, field),
                base_value=getattr(local, f"_base_{field}", None),
                local_updated=local.updated_at,
                remote_updated=remote.updated_at,
                local_task=local,
                remote_task=remote
            )
            resolutions[field] = self.resolve(context)
        return resolutions
```

---

## AC#1: LocalWinsStrategy

```python
class LocalWinsStrategy(ConflictResolver):
    """
    Always prefer local changes over remote.

    Use case: Local-first workflow where local edits are authoritative.
    Risk: May lose remote changes made by teammates.
    """

    @property
    def name(self) -> str:
        return "local-wins"

    @property
    def description(self) -> str:
        return "Always keep local changes, overwrite remote"

    def resolve(self, context: ConflictContext) -> Resolution:
        return Resolution(
            result=ResolutionResult.LOCAL_WINS,
            resolved_value=context.local_value,
            reason=f"Local wins: keeping local value for {context.field}"
        )
```

---

## AC#2: RemoteWinsStrategy

```python
class RemoteWinsStrategy(ConflictResolver):
    """
    Always prefer remote changes over local.

    Use case: Remote tracker is source of truth (e.g., Jira for PMs).
    Risk: May lose local work that wasn't pushed.
    """

    @property
    def name(self) -> str:
        return "remote-wins"

    @property
    def description(self) -> str:
        return "Always keep remote changes, overwrite local"

    def resolve(self, context: ConflictContext) -> Resolution:
        return Resolution(
            result=ResolutionResult.REMOTE_WINS,
            resolved_value=context.remote_value,
            reason=f"Remote wins: keeping remote value for {context.field}"
        )
```

---

## AC#3: PromptStrategy

```python
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table

class PromptStrategy(ConflictResolver):
    """
    Interactively prompt user to resolve each conflict.

    Use case: Important syncs where user wants control.
    """

    def __init__(self, console: Console = None):
        self.console = console or Console()

    @property
    def name(self) -> str:
        return "prompt"

    @property
    def description(self) -> str:
        return "Ask user to resolve each conflict"

    def resolve(self, context: ConflictContext) -> Resolution:
        self._display_conflict(context)

        choices = {
            "l": ("Keep local", context.local_value, ResolutionResult.LOCAL_WINS),
            "r": ("Keep remote", context.remote_value, ResolutionResult.REMOTE_WINS),
            "s": ("Skip this field", None, ResolutionResult.SKIP),
            "q": ("Cancel sync", None, ResolutionResult.USER_CANCELLED),
        }

        choice = Prompt.ask(
            "Choose",
            choices=list(choices.keys()),
            default="l"
        )

        desc, value, result = choices[choice]

        if result == ResolutionResult.USER_CANCELLED:
            raise SyncCancelledError("User cancelled conflict resolution")

        return Resolution(
            result=result,
            resolved_value=value,
            reason=f"User chose: {desc}"
        )

    def _display_conflict(self, context: ConflictContext):
        """Display conflict details to user."""
        table = Table(title=f"Conflict: {context.task_id} / {context.field}")
        table.add_column("Source", style="cyan")
        table.add_column("Value", style="white")
        table.add_column("Modified", style="dim")

        table.add_row(
            "Local",
            str(context.local_value),
            context.local_updated.strftime("%Y-%m-%d %H:%M")
        )
        table.add_row(
            "Remote",
            str(context.remote_value),
            context.remote_updated.strftime("%Y-%m-%d %H:%M")
        )

        self.console.print(table)
        self.console.print("\n[l] Keep local  [r] Keep remote  [s] Skip  [q] Cancel\n")


class BatchPromptStrategy(PromptStrategy):
    """
    Show all conflicts, let user resolve in batch.

    More efficient for multiple conflicts.
    """

    def resolve_task(
        self,
        local: "LocalTask",
        remote: "RemoteTask",
        conflicts: List[str]
    ) -> Dict[str, Resolution]:
        """Show all conflicts at once."""
        self._display_all_conflicts(local, remote, conflicts)

        # Offer batch options
        batch_choice = Prompt.ask(
            "Resolve all conflicts",
            choices=["all-local", "all-remote", "one-by-one", "cancel"],
            default="one-by-one"
        )

        if batch_choice == "all-local":
            return {f: Resolution(
                result=ResolutionResult.LOCAL_WINS,
                resolved_value=getattr(local, f),
                reason="Batch: all local"
            ) for f in conflicts}

        elif batch_choice == "all-remote":
            return {f: Resolution(
                result=ResolutionResult.REMOTE_WINS,
                resolved_value=getattr(remote, f),
                reason="Batch: all remote"
            ) for f in conflicts}

        elif batch_choice == "cancel":
            raise SyncCancelledError("User cancelled")

        else:
            # Fall back to one-by-one
            return super().resolve_task(local, remote, conflicts)
```

---

## AC#4: SmartMergeStrategy

```python
from difflib import SequenceMatcher
import re

class SmartMergeStrategy(ConflictResolver):
    """
    Intelligently merge changes when possible.

    Strategies by field type:
    - Text: Three-way merge if base available, else newest wins
    - Lists: Union of both lists
    - Scalar: Newest timestamp wins
    """

    @property
    def name(self) -> str:
        return "smart-merge"

    @property
    def description(self) -> str:
        return "Automatically merge when possible, prompt for true conflicts"

    def __init__(self, fallback: ConflictResolver = None):
        self.fallback = fallback or PromptStrategy()

    def resolve(self, context: ConflictContext) -> Resolution:
        # Determine field type and apply appropriate strategy
        if self._is_text_field(context.field):
            return self._merge_text(context)
        elif self._is_list_field(context.field):
            return self._merge_list(context)
        else:
            return self._merge_scalar(context)

    def _is_text_field(self, field: str) -> bool:
        return field in ("description", "notes", "implementation_notes")

    def _is_list_field(self, field: str) -> bool:
        return field in ("labels", "acceptance_criteria", "subtask_ids")

    def _merge_text(self, context: ConflictContext) -> Resolution:
        """
        Three-way merge for text fields.

        If base is available, perform proper three-way merge.
        Otherwise, append both versions with markers.
        """
        if context.base_value:
            # Three-way merge
            merged = self._three_way_merge(
                context.base_value,
                context.local_value,
                context.remote_value
            )
            if merged is not None:
                return Resolution(
                    result=ResolutionResult.MERGED,
                    resolved_value=merged,
                    reason="Three-way merge successful"
                )

        # Fallback: append with conflict markers
        if context.local_value and context.remote_value:
            merged = (
                f"<<<<<<< LOCAL\n"
                f"{context.local_value}\n"
                f"=======\n"
                f"{context.remote_value}\n"
                f">>>>>>> REMOTE"
            )
            return Resolution(
                result=ResolutionResult.MERGED,
                resolved_value=merged,
                reason="Merged with conflict markers (manual review needed)"
            )

        # One is empty - take the non-empty one
        return Resolution(
            result=ResolutionResult.MERGED,
            resolved_value=context.local_value or context.remote_value,
            reason="Kept non-empty value"
        )

    def _merge_list(self, context: ConflictContext) -> Resolution:
        """
        Merge lists by taking union.

        Preserves order: local items first, then new remote items.
        """
        local_list = context.local_value or []
        remote_list = context.remote_value or []

        # Union preserving local order
        merged = list(local_list)
        for item in remote_list:
            if item not in merged:
                merged.append(item)

        return Resolution(
            result=ResolutionResult.MERGED,
            resolved_value=merged,
            reason=f"Merged lists: {len(local_list)} local + {len(remote_list)} remote = {len(merged)} total"
        )

    def _merge_scalar(self, context: ConflictContext) -> Resolution:
        """
        For scalar values, newest timestamp wins.
        """
        if context.local_updated > context.remote_updated:
            return Resolution(
                result=ResolutionResult.LOCAL_WINS,
                resolved_value=context.local_value,
                reason=f"Local is newer ({context.local_updated} > {context.remote_updated})"
            )
        else:
            return Resolution(
                result=ResolutionResult.REMOTE_WINS,
                resolved_value=context.remote_value,
                reason=f"Remote is newer ({context.remote_updated} > {context.local_updated})"
            )

    def _three_way_merge(
        self,
        base: str,
        local: str,
        remote: str
    ) -> Optional[str]:
        """
        Attempt three-way merge of text.

        Returns merged text if successful, None if conflicts.
        """
        # Simple line-based merge
        base_lines = base.splitlines()
        local_lines = local.splitlines()
        remote_lines = remote.splitlines()

        # Use difflib for matching
        local_diff = list(SequenceMatcher(None, base_lines, local_lines).get_opcodes())
        remote_diff = list(SequenceMatcher(None, base_lines, remote_lines).get_opcodes())

        # Check for overlapping changes
        local_changed = set()
        remote_changed = set()

        for tag, i1, i2, j1, j2 in local_diff:
            if tag != 'equal':
                local_changed.update(range(i1, i2))

        for tag, i1, i2, j1, j2 in remote_diff:
            if tag != 'equal':
                remote_changed.update(range(i1, i2))

        # If same lines changed in both, we have a true conflict
        if local_changed & remote_changed:
            return None

        # Apply non-conflicting changes
        # (simplified - real implementation would be more sophisticated)
        result_lines = base_lines.copy()

        # Apply local changes first
        for tag, i1, i2, j1, j2 in reversed(local_diff):
            if tag == 'replace':
                result_lines[i1:i2] = local_lines[j1:j2]
            elif tag == 'delete':
                del result_lines[i1:i2]
            elif tag == 'insert':
                result_lines[i1:i1] = local_lines[j1:j2]

        return '\n'.join(result_lines)
```

---

## AC#5: Configuration Options

```yaml
# ~/.config/backlog/satellite.yml

sync:
  # Default conflict resolution strategy
  # Options: local-wins, remote-wins, prompt, smart-merge
  conflict_strategy: smart-merge

  # Per-provider override
  providers:
    github:
      conflict_strategy: prompt      # Always ask for GitHub
    jira:
      conflict_strategy: remote-wins # Jira is source of truth
    notion:
      conflict_strategy: local-wins  # Local edits preferred

  # Per-field strategy overrides
  field_strategies:
    status: remote-wins              # Status from remote tracker
    labels: smart-merge              # Merge labels from both
    description: prompt              # Ask for description conflicts

  # Smart merge settings
  smart_merge:
    # Auto-merge lists without prompting
    auto_merge_lists: true
    # Use conflict markers for text (vs prompting)
    text_conflict_markers: true
    # Max lines for auto-merge (prompt if larger)
    max_auto_merge_lines: 50

  # Prompt settings
  prompt:
    # Show diff in prompt
    show_diff: true
    # Enable batch mode for multiple conflicts
    batch_mode: true
    # Timeout for prompt (seconds, 0 = no timeout)
    timeout: 0
```

### Configuration Loading

```python
from pathlib import Path
import yaml

@dataclass
class SyncConfig:
    """Sync configuration loaded from config file."""
    default_strategy: str = "smart-merge"
    provider_strategies: Dict[str, str] = None
    field_strategies: Dict[str, str] = None
    smart_merge: Dict[str, Any] = None
    prompt: Dict[str, Any] = None

    @classmethod
    def load(cls, config_path: Path = None) -> "SyncConfig":
        """Load config from file with defaults."""
        config_path = config_path or Path.home() / ".config/backlog/satellite.yml"

        if not config_path.exists():
            return cls()

        data = yaml.safe_load(config_path.read_text())
        sync_config = data.get("sync", {})

        return cls(
            default_strategy=sync_config.get("conflict_strategy", "smart-merge"),
            provider_strategies={
                k: v.get("conflict_strategy")
                for k, v in sync_config.get("providers", {}).items()
                if v.get("conflict_strategy")
            },
            field_strategies=sync_config.get("field_strategies", {}),
            smart_merge=sync_config.get("smart_merge", {}),
            prompt=sync_config.get("prompt", {})
        )

    def get_resolver(
        self,
        provider: ProviderType = None,
        field: str = None
    ) -> ConflictResolver:
        """Get appropriate resolver based on config."""
        # Field-specific takes precedence
        if field and field in self.field_strategies:
            strategy_name = self.field_strategies[field]
        # Provider-specific next
        elif provider and provider.value in self.provider_strategies:
            strategy_name = self.provider_strategies[provider.value]
        # Default
        else:
            strategy_name = self.default_strategy

        return self._create_resolver(strategy_name)

    def _create_resolver(self, name: str) -> ConflictResolver:
        """Factory for resolver instances."""
        resolvers = {
            "local-wins": LocalWinsStrategy,
            "remote-wins": RemoteWinsStrategy,
            "prompt": lambda: PromptStrategy(),
            "smart-merge": lambda: SmartMergeStrategy(
                fallback=PromptStrategy()
            ),
        }
        factory = resolvers.get(name)
        if not factory:
            raise ValueError(f"Unknown strategy: {name}")
        return factory() if callable(factory) else factory
```

---

## Strategy Selection Flowchart

```
                              ┌─────────────────┐
                              │ Conflict Found  │
                              └────────┬────────┘
                                       │
                          ┌────────────▼────────────┐
                          │ Field-specific config?  │
                          └────────────┬────────────┘
                                 yes/  │ \no
                                 ┌─────┴─────┐
                                 ▼           ▼
                          Use field      ┌────────────────────┐
                          strategy       │ Provider config?   │
                                         └──────────┬─────────┘
                                              yes/  │ \no
                                              ┌─────┴─────┐
                                              ▼           ▼
                                        Use provider  Use default
                                        strategy      strategy
```

---

## Summary

| Strategy | Best For | Risks |
|----------|----------|-------|
| `local-wins` | Local-first workflows | Loses remote changes |
| `remote-wins` | Remote tracker is SoT | Loses local work |
| `prompt` | Important syncs | Slow, requires user |
| `smart-merge` | Most cases | May need manual review |

---

*Created for task-021 - Design Conflict Resolution Strategies*
