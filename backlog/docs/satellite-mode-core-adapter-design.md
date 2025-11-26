# Satellite Mode Core Adapter Interface Design

**Related Task:** task-017 - Design Core Adapter Interface
**Status:** Phase 2: Design
**Dependencies:** task-016 (Security Architecture Review)

---

## 1. User Story Requirements Mapping

### US-1: Pull Remote Task by ID
- Fetch single task from provider
- Map remote fields to local schema
- Create local task file

### US-2: Sync Assigned Tasks
- List tasks assigned to user
- Bidirectional sync (local ↔ remote)
- Conflict detection and resolution

### US-3: Create PR with Spec Injection
- Create pull request on remote
- Inject task spec into PR body
- Link PR to task

### US-4: Compliance Mode
- Audit trail for all operations
- Provenance tracking
- SLSA/NIST alignment

---

## 2. RemoteProvider Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Iterator


class ProviderType(Enum):
    """Supported remote provider types."""
    GITHUB = "github"
    JIRA = "jira"
    NOTION = "notion"


class RemoteProvider(ABC):
    """
    Abstract base class for remote task providers.

    All providers must implement this interface to integrate
    with the Satellite Mode sync engine.
    """

    # ===================
    # Provider Metadata
    # ===================

    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        """Return the provider type identifier."""
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable provider name."""
        ...

    @property
    @abstractmethod
    def id_pattern(self) -> str:
        """Regex pattern to match task IDs for this provider.

        Examples:
            GitHub: r'^[\\w-]+/[\\w-]+#\\d+$'  # owner/repo#123
            Jira: r'^[A-Z]+-\\d+$'             # PROJ-123
            Notion: r'^[a-f0-9-]{36}$'         # UUID
        """
        ...

    # ===================
    # Authentication
    # ===================

    @abstractmethod
    def authenticate(self, token: str) -> bool:
        """
        Validate authentication token.

        Args:
            token: API token or credential

        Returns:
            True if authentication succeeds

        Raises:
            AuthenticationError: If token is invalid
        """
        ...

    @abstractmethod
    def get_current_user(self) -> "RemoteUser":
        """Get the authenticated user's information."""
        ...

    # ===================
    # US-1: Pull Task
    # ===================

    @abstractmethod
    def get_task(self, task_id: str) -> "RemoteTask":
        """
        Fetch a single task by ID.

        Args:
            task_id: Provider-specific task identifier

        Returns:
            RemoteTask with all available fields

        Raises:
            TaskNotFoundError: If task doesn't exist
            PermissionError: If user lacks access
        """
        ...

    # ===================
    # US-2: Sync Tasks
    # ===================

    @abstractmethod
    def list_tasks(
        self,
        assignee: Optional[str] = None,
        status: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        updated_since: Optional[datetime] = None,
        limit: int = 100,
    ) -> Iterator["RemoteTask"]:
        """
        List tasks matching filters.

        Args:
            assignee: Filter by assignee (None = current user)
            status: Filter by status values
            labels: Filter by labels
            updated_since: Only tasks updated after this time
            limit: Maximum tasks to return

        Yields:
            RemoteTask objects matching criteria
        """
        ...

    @abstractmethod
    def update_task(
        self,
        task_id: str,
        updates: "TaskUpdate",
    ) -> "RemoteTask":
        """
        Update a remote task.

        Args:
            task_id: Provider-specific task identifier
            updates: Fields to update

        Returns:
            Updated RemoteTask

        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If updates are invalid
            ConflictError: If remote was modified
        """
        ...

    @abstractmethod
    def create_task(self, task: "TaskCreate") -> "RemoteTask":
        """
        Create a new task on remote.

        Args:
            task: Task data to create

        Returns:
            Created RemoteTask with assigned ID
        """
        ...

    # ===================
    # US-3: PR Creation
    # ===================

    @abstractmethod
    def create_pull_request(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
        draft: bool = False,
    ) -> "RemotePullRequest":
        """
        Create a pull request (GitHub only, others raise NotImplementedError).

        Args:
            title: PR title
            body: PR body (spec injected here)
            head_branch: Source branch
            base_branch: Target branch
            draft: Create as draft PR

        Returns:
            Created RemotePullRequest
        """
        ...

    @abstractmethod
    def link_pr_to_task(
        self,
        task_id: str,
        pr_url: str,
    ) -> None:
        """Link a PR to a task (add reference/comment)."""
        ...

    # ===================
    # US-4: Compliance
    # ===================

    @abstractmethod
    def get_task_history(
        self,
        task_id: str,
        since: Optional[datetime] = None,
    ) -> List["TaskHistoryEntry"]:
        """
        Get audit history for a task.

        Args:
            task_id: Provider-specific task identifier
            since: Only changes after this time

        Returns:
            List of history entries
        """
        ...

    # ===================
    # Utility Methods
    # ===================

    @abstractmethod
    def test_connection(self) -> "ConnectionStatus":
        """Test provider connectivity and return status."""
        ...

    @abstractmethod
    def get_rate_limit_status(self) -> "RateLimitStatus":
        """Get current rate limit status."""
        ...
```

---

## 3. RemoteTask Entity

```python
@dataclass
class RemoteTask:
    """
    Domain entity representing a task from a remote provider.

    This is the canonical representation used across all providers.
    Provider-specific fields are stored in `extra_fields`.
    """

    # === Identity ===
    id: str                          # Provider-specific ID (e.g., "PROJ-123")
    provider: ProviderType           # Source provider
    url: str                         # Web URL to task

    # === Core Fields ===
    title: str                       # Task title/summary
    description: Optional[str]       # Task description (markdown)
    status: str                      # Status name (provider-specific)

    # === Assignment ===
    assignee: Optional["RemoteUser"] # Assigned user
    reporter: Optional["RemoteUser"] # Creator/reporter

    # === Classification ===
    labels: List[str]                # Labels/tags
    priority: Optional[str]          # Priority level
    task_type: Optional[str]         # Issue type (bug, feature, etc.)

    # === Hierarchy ===
    parent_id: Optional[str]         # Parent task/epic ID
    subtask_ids: List[str]           # Child task IDs

    # === Timestamps ===
    created_at: datetime             # Creation timestamp
    updated_at: datetime             # Last update timestamp
    due_date: Optional[datetime]     # Due date if set

    # === Sync Metadata ===
    etag: Optional[str]              # For conflict detection
    version: Optional[int]           # Version number

    # === Provider-Specific ===
    extra_fields: Dict[str, Any]     # Custom fields (story_points, sprint, etc.)
    raw_response: Optional[Dict]     # Original API response (for debugging)

    def to_local_task(self) -> Dict[str, Any]:
        """Convert to Backlog.md task format."""
        return {
            "id": f"remote-{self.provider.value}-{self.id}",
            "title": self.title,
            "description": self.description,
            "status": self._map_status_to_local(),
            "assignee": self.assignee.username if self.assignee else None,
            "labels": self.labels,
            "upstream": {
                "provider": self.provider.value,
                "id": self.id,
                "url": self.url,
                "synced_at": datetime.utcnow().isoformat(),
                "etag": self.etag,
            },
        }

    def _map_status_to_local(self) -> str:
        """Map provider status to Backlog.md status."""
        STATUS_MAP = {
            # GitHub
            "open": "To Do",
            "closed": "Done",
            # Jira (common)
            "to do": "To Do",
            "in progress": "In Progress",
            "done": "Done",
            # Notion
            "not started": "To Do",
            "in progress": "In Progress",
            "complete": "Done",
        }
        return STATUS_MAP.get(self.status.lower(), self.status)


@dataclass
class RemoteUser:
    """User reference from remote provider."""
    id: str                          # Provider-specific user ID
    username: str                    # Username/handle
    display_name: Optional[str]      # Full name
    email: Optional[str]             # Email (if available)
    avatar_url: Optional[str]        # Profile picture URL


@dataclass
class TaskUpdate:
    """Fields that can be updated on a remote task."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assignee: Optional[str] = None   # Username or ID
    labels: Optional[List[str]] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    extra_fields: Optional[Dict[str, Any]] = None


@dataclass
class TaskCreate:
    """Fields required to create a new remote task."""
    title: str
    description: Optional[str] = None
    assignee: Optional[str] = None
    labels: List[str] = None
    priority: Optional[str] = None
    parent_id: Optional[str] = None  # For subtasks
    task_type: str = "task"          # issue, bug, story, etc.
    extra_fields: Dict[str, Any] = None
```

---

## 4. SyncResult Entity

```python
class SyncOperation(Enum):
    """Type of sync operation performed."""
    CREATED = "created"       # New task created
    UPDATED = "updated"       # Existing task updated
    DELETED = "deleted"       # Task deleted
    SKIPPED = "skipped"       # No changes needed
    CONFLICT = "conflict"     # Conflict detected
    FAILED = "failed"         # Operation failed


class SyncDirection(Enum):
    """Direction of sync operation."""
    PULL = "pull"             # Remote → Local
    PUSH = "push"             # Local → Remote
    BIDIRECTIONAL = "both"    # Both directions


@dataclass
class SyncResult:
    """
    Result of a sync operation.

    Captures what happened, what changed, and any issues encountered.
    Used for audit logging and user feedback.
    """

    # === Identity ===
    operation_id: str                # Unique operation ID (UUID)
    timestamp: datetime              # When sync occurred
    direction: SyncDirection         # Pull, push, or both

    # === Scope ===
    provider: ProviderType           # Which provider
    task_ids: List[str]              # Tasks involved

    # === Results ===
    operations: List["TaskSyncOp"]   # Individual task operations

    # === Summary ===
    @property
    def created_count(self) -> int:
        return sum(1 for op in self.operations if op.operation == SyncOperation.CREATED)

    @property
    def updated_count(self) -> int:
        return sum(1 for op in self.operations if op.operation == SyncOperation.UPDATED)

    @property
    def conflict_count(self) -> int:
        return sum(1 for op in self.operations if op.operation == SyncOperation.CONFLICT)

    @property
    def failed_count(self) -> int:
        return sum(1 for op in self.operations if op.operation == SyncOperation.FAILED)

    @property
    def success(self) -> bool:
        return self.failed_count == 0 and self.conflict_count == 0

    # === Audit ===
    def to_audit_log(self) -> Dict[str, Any]:
        """Generate audit log entry for compliance."""
        return {
            "operation_id": self.operation_id,
            "timestamp": self.timestamp.isoformat(),
            "provider": self.provider.value,
            "direction": self.direction.value,
            "summary": {
                "total": len(self.operations),
                "created": self.created_count,
                "updated": self.updated_count,
                "conflicts": self.conflict_count,
                "failed": self.failed_count,
            },
            "tasks": [op.to_dict() for op in self.operations],
        }


@dataclass
class TaskSyncOp:
    """Result of syncing a single task."""
    task_id: str                     # Local or remote task ID
    remote_id: Optional[str]         # Remote task ID
    operation: SyncOperation         # What happened
    changes: List[str]               # Fields that changed
    error: Optional[str]             # Error message if failed
    conflict_data: Optional["ConflictData"] = None  # If conflict

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "remote_id": self.remote_id,
            "operation": self.operation.value,
            "changes": self.changes,
            "error": self.error,
        }


@dataclass
class ConflictData:
    """Details about a sync conflict."""
    field: str                       # Which field conflicts
    local_value: Any                 # Local value
    remote_value: Any                # Remote value
    local_updated: datetime          # When local was updated
    remote_updated: datetime         # When remote was updated
    resolution: Optional[str] = None # How it was resolved
```

---

## 5. Error Handling Patterns

```python
class SatelliteError(Exception):
    """Base exception for all Satellite Mode errors."""

    def __init__(self, message: str, code: str, details: Dict = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "code": self.code,
            "message": str(self),
            "details": self.details,
        }


# === Authentication Errors ===

class AuthenticationError(SatelliteError):
    """Token is invalid or expired."""
    def __init__(self, provider: str, reason: str):
        super().__init__(
            f"Authentication failed for {provider}: {reason}",
            code="AUTH_FAILED",
            details={"provider": provider, "reason": reason}
        )


class TokenExpiredError(AuthenticationError):
    """Token has expired and needs refresh."""
    def __init__(self, provider: str):
        super().__init__(provider, "Token expired")
        self.code = "TOKEN_EXPIRED"


# === Resource Errors ===

class TaskNotFoundError(SatelliteError):
    """Task does not exist on remote."""
    def __init__(self, task_id: str, provider: str):
        super().__init__(
            f"Task {task_id} not found on {provider}",
            code="TASK_NOT_FOUND",
            details={"task_id": task_id, "provider": provider}
        )


class PermissionDeniedError(SatelliteError):
    """User lacks permission for operation."""
    def __init__(self, operation: str, resource: str):
        super().__init__(
            f"Permission denied: cannot {operation} {resource}",
            code="PERMISSION_DENIED",
            details={"operation": operation, "resource": resource}
        )


# === Sync Errors ===

class ConflictError(SatelliteError):
    """Conflict between local and remote versions."""
    def __init__(self, task_id: str, conflict: ConflictData):
        super().__init__(
            f"Conflict detected for task {task_id}",
            code="CONFLICT",
            details={"task_id": task_id, "conflict": conflict.__dict__}
        )
        self.conflict = conflict


class SyncError(SatelliteError):
    """General sync operation failure."""
    def __init__(self, message: str, failed_tasks: List[str]):
        super().__init__(
            message,
            code="SYNC_FAILED",
            details={"failed_tasks": failed_tasks}
        )


# === Provider Errors ===

class RateLimitError(SatelliteError):
    """Rate limit exceeded."""
    def __init__(self, provider: str, retry_after: int):
        super().__init__(
            f"Rate limit exceeded for {provider}. Retry after {retry_after}s",
            code="RATE_LIMITED",
            details={"provider": provider, "retry_after": retry_after}
        )
        self.retry_after = retry_after


class ProviderUnavailableError(SatelliteError):
    """Provider API is unavailable."""
    def __init__(self, provider: str, status_code: int = None):
        super().__init__(
            f"Provider {provider} is unavailable",
            code="PROVIDER_UNAVAILABLE",
            details={"provider": provider, "status_code": status_code}
        )


# === Validation Errors ===

class ValidationError(SatelliteError):
    """Input validation failed."""
    def __init__(self, field: str, reason: str):
        super().__init__(
            f"Validation failed for {field}: {reason}",
            code="VALIDATION_ERROR",
            details={"field": field, "reason": reason}
        )


# === Error Handler ===

def handle_provider_error(func):
    """Decorator to convert provider exceptions to SatelliteErrors."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError(provider="unknown", reason="Invalid credentials")
            elif e.response.status_code == 403:
                raise PermissionDeniedError(operation="access", resource="resource")
            elif e.response.status_code == 404:
                raise TaskNotFoundError(task_id="unknown", provider="unknown")
            elif e.response.status_code == 429:
                retry = int(e.response.headers.get("Retry-After", 60))
                raise RateLimitError(provider="unknown", retry_after=retry)
            else:
                raise ProviderUnavailableError(provider="unknown", status_code=e.response.status_code)
    return wrapper
```

---

## 6. Extension Points

### 6.1 Custom Provider Registration

```python
from typing import Type

class ProviderRegistry:
    """Registry for remote providers."""

    _providers: Dict[ProviderType, Type[RemoteProvider]] = {}
    _instances: Dict[str, RemoteProvider] = {}

    @classmethod
    def register(cls, provider_type: ProviderType):
        """Decorator to register a provider class."""
        def decorator(provider_class: Type[RemoteProvider]):
            cls._providers[provider_type] = provider_class
            return provider_class
        return decorator

    @classmethod
    def get(cls, provider_type: ProviderType, config: Dict) -> RemoteProvider:
        """Get or create provider instance."""
        key = f"{provider_type.value}:{hash(frozenset(config.items()))}"
        if key not in cls._instances:
            provider_class = cls._providers.get(provider_type)
            if not provider_class:
                raise ValueError(f"Unknown provider: {provider_type}")
            cls._instances[key] = provider_class(config)
        return cls._instances[key]

    @classmethod
    def detect_provider(cls, task_id: str) -> Optional[ProviderType]:
        """Auto-detect provider from task ID format."""
        import re
        for ptype, pclass in cls._providers.items():
            pattern = pclass.id_pattern.fget(None)  # Get from class
            if re.match(pattern, task_id):
                return ptype
        return None


# Usage example:
@ProviderRegistry.register(ProviderType.GITHUB)
class GitHubProvider(RemoteProvider):
    ...
```

### 6.2 Field Mapper Extension

```python
class FieldMapper(ABC):
    """Abstract field mapper for custom field transformations."""

    @abstractmethod
    def to_remote(self, local_field: str, value: Any) -> Tuple[str, Any]:
        """Map local field to remote field name and value."""
        ...

    @abstractmethod
    def to_local(self, remote_field: str, value: Any) -> Tuple[str, Any]:
        """Map remote field to local field name and value."""
        ...


class JiraFieldMapper(FieldMapper):
    """Jira-specific field mapping."""

    def __init__(self, custom_field_map: Dict[str, str]):
        # Map local names to Jira customfield_NNNNN
        self.custom_map = custom_field_map

    def to_remote(self, local_field: str, value: Any) -> Tuple[str, Any]:
        if local_field in self.custom_map:
            return self.custom_map[local_field], value
        return local_field, value
```

### 6.3 Conflict Resolver Extension

```python
class ConflictResolver(ABC):
    """Strategy for resolving sync conflicts."""

    @abstractmethod
    def resolve(self, conflict: ConflictData) -> Any:
        """Resolve conflict and return winning value."""
        ...


class LocalWinsResolver(ConflictResolver):
    def resolve(self, conflict: ConflictData) -> Any:
        return conflict.local_value


class RemoteWinsResolver(ConflictResolver):
    def resolve(self, conflict: ConflictData) -> Any:
        return conflict.remote_value


class TimestampResolver(ConflictResolver):
    def resolve(self, conflict: ConflictData) -> Any:
        if conflict.local_updated > conflict.remote_updated:
            return conflict.local_value
        return conflict.remote_value
```

### 6.4 Audit Logger Extension

```python
class AuditLogger(ABC):
    """Interface for audit logging."""

    @abstractmethod
    def log_sync(self, result: SyncResult) -> None:
        """Log a sync operation."""
        ...

    @abstractmethod
    def log_auth(self, provider: str, user: str, success: bool) -> None:
        """Log authentication attempt."""
        ...


class FileAuditLogger(AuditLogger):
    """Append-only file-based audit logger."""

    def __init__(self, path: Path):
        self.path = path

    def log_sync(self, result: SyncResult) -> None:
        with open(self.path, "a") as f:
            json.dump(result.to_audit_log(), f)
            f.write("\n")
```

---

## 7. Interface Summary

| Component | Purpose | Extension Point |
|-----------|---------|-----------------|
| `RemoteProvider` | Provider abstraction | Subclass for new providers |
| `RemoteTask` | Task representation | Add fields to `extra_fields` |
| `SyncResult` | Operation outcome | Custom logging via `to_audit_log()` |
| `FieldMapper` | Field transformation | Subclass for custom mappings |
| `ConflictResolver` | Conflict handling | Subclass for custom strategies |
| `AuditLogger` | Compliance logging | Subclass for custom backends |

---

*Created for task-017 - Design Core Adapter Interface*
