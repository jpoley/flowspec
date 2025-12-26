"""Satellite Mode - Remote provider integration for Backlog.md."""

__all__ = [
    # Enums
    "ProviderType",
    "SyncOperation",
    "SyncDirection",
    "ResolutionResult",
    # Entities
    "RemoteUser",
    "RemoteTask",
    "TaskUpdate",
    "TaskCreate",
    "RemotePullRequest",
    "TaskHistoryEntry",
    "ConnectionStatus",
    "RateLimitStatus",
    "TaskSyncOp",
    "ConflictData",
    "SyncResult",
    # Provider
    "RemoteProvider",
    # Registry
    "ProviderRegistry",
    "LazyProvider",
    "PROVIDER_PATTERNS",
    # Secrets
    "SecretManager",
    "TokenRedactionFilter",
    "ENV_VAR_NAMES",
    "TOKEN_PATTERNS",
    # Audit
    "AuditLogger",
    "AuditEvent",
    "AuditEventType",
    "AuditSeverity",
    "AuditQuery",
    "SLSAAttestation",
    "JSONFormatter",
    "MarkdownFormatter",
    # Errors
    "SatelliteError",
    "AuthenticationError",
    "TokenExpiredError",
    "SecretStorageUnavailableError",
    "InvalidTokenError",
    "TaskNotFoundError",
    "PermissionDeniedError",
    "ConflictError",
    "SyncError",
    "SyncCancelledError",
    "RateLimitError",
    "ProviderUnavailableError",
    "ProviderNotFoundError",
    "ValidationError",
    # Migration
    "TaskMigrator",
    "MigrationError",
    "migrate_tasks_cli",
    "cleanup_backups",
]

# Enums
# Audit
from .audit import (
    AuditEvent,
    AuditEventType,
    AuditLogger,
    AuditQuery,
    AuditSeverity,
    JSONFormatter,
    MarkdownFormatter,
    SLSAAttestation,
)

# Entities
from .entities import (
    ConflictData,
    ConnectionStatus,
    RateLimitStatus,
    RemotePullRequest,
    RemoteTask,
    RemoteUser,
    SyncResult,
    TaskCreate,
    TaskHistoryEntry,
    TaskSyncOp,
    TaskUpdate,
)
from .enums import (
    ProviderType,
    ResolutionResult,
    SyncDirection,
    SyncOperation,
)

# Errors
from .errors import (
    AuthenticationError,
    ConflictError,
    InvalidTokenError,
    PermissionDeniedError,
    ProviderNotFoundError,
    ProviderUnavailableError,
    RateLimitError,
    SatelliteError,
    SecretStorageUnavailableError,
    SyncCancelledError,
    SyncError,
    TaskNotFoundError,
    TokenExpiredError,
    ValidationError,
)

# Migration
from .migration import MigrationError, TaskMigrator, cleanup_backups, migrate_tasks_cli

# Provider ABC
from .provider import RemoteProvider

# Registry
from .registry import PROVIDER_PATTERNS, LazyProvider, ProviderRegistry

# Secrets
from .secrets import ENV_VAR_NAMES, TOKEN_PATTERNS, SecretManager, TokenRedactionFilter
