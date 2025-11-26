# Satellite Mode Subsystems Design

**Related Tasks:**
- task-018 - Design Provider Registry
- task-019 - Design Secret Management
- task-020 - Design Sync Engine
- task-022 - Design Data Model Extensions

**Status:** Phase 2: Design

---

## Task-018: Provider Registry Design

### Overview

The Provider Registry implements a factory pattern for managing remote provider instances with auto-detection capabilities.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ProviderRegistry                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ _providers: Dict[ProviderType, Type[RemoteProvider]] │    │
│  │ _instances: Dict[str, RemoteProvider]                │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  register(type) ──► decorator for provider classes          │
│  get(type, config) ──► lazy-loaded singleton instance       │
│  detect(task_id) ──► auto-detect provider from ID pattern   │
│  list_available() ──► all registered providers              │
└─────────────────────────────────────────────────────────────┘
```

### AC#1: Provider Registration Mechanism

```python
from typing import Type, Dict, Optional
from threading import Lock

class ProviderRegistry:
    """
    Thread-safe registry for remote providers.

    Implements singleton pattern per provider+config combination.
    """

    _providers: Dict[ProviderType, Type[RemoteProvider]] = {}
    _instances: Dict[str, RemoteProvider] = {}
    _lock = Lock()

    @classmethod
    def register(cls, provider_type: ProviderType):
        """
        Decorator to register a provider class.

        Usage:
            @ProviderRegistry.register(ProviderType.GITHUB)
            class GitHubProvider(RemoteProvider):
                ...
        """
        def decorator(provider_class: Type[RemoteProvider]):
            if not issubclass(provider_class, RemoteProvider):
                raise TypeError(f"{provider_class} must subclass RemoteProvider")
            cls._providers[provider_type] = provider_class
            return provider_class
        return decorator

    @classmethod
    def get(cls, provider_type: ProviderType, config: Dict = None) -> RemoteProvider:
        """
        Get or create provider instance.

        Instances are cached by provider type + config hash.
        Thread-safe via locking.
        """
        config = config or {}
        key = f"{provider_type.value}:{hash(frozenset(config.items()))}"

        with cls._lock:
            if key not in cls._instances:
                provider_class = cls._providers.get(provider_type)
                if not provider_class:
                    raise ProviderNotFoundError(provider_type)
                cls._instances[key] = provider_class(config)
            return cls._instances[key]

    @classmethod
    def unregister(cls, provider_type: ProviderType) -> None:
        """Remove a provider registration (useful for testing)."""
        cls._providers.pop(provider_type, None)
        # Also remove cached instances
        to_remove = [k for k in cls._instances if k.startswith(provider_type.value)]
        for k in to_remove:
            del cls._instances[k]
```

### AC#2: Auto-Detection from ID Pattern

```python
import re
from typing import Optional

# Provider ID patterns
PROVIDER_PATTERNS = {
    ProviderType.GITHUB: r'^(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)#(?P<number>\d+)$',
    ProviderType.JIRA: r'^(?P<project>[A-Z][A-Z0-9]*)-(?P<number>\d+)$',
    ProviderType.NOTION: r'^(?P<id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',
}

@classmethod
def detect_provider(cls, task_id: str) -> Optional[ProviderType]:
    """
    Auto-detect provider from task ID format.

    Examples:
        "owner/repo#123" -> ProviderType.GITHUB
        "PROJ-123" -> ProviderType.JIRA
        "abc12345-..." -> ProviderType.NOTION

    Returns:
        ProviderType if matched, None otherwise
    """
    for provider_type, pattern in PROVIDER_PATTERNS.items():
        if re.match(pattern, task_id):
            return provider_type
    return None

@classmethod
def parse_task_id(cls, task_id: str) -> Optional[Dict[str, str]]:
    """
    Parse task ID into components.

    Returns:
        Dict with named groups from pattern, or None
    """
    for provider_type, pattern in PROVIDER_PATTERNS.items():
        match = re.match(pattern, task_id)
        if match:
            return {
                "provider": provider_type,
                **match.groupdict()
            }
    return None
```

### AC#3: Lazy Initialization

```python
class LazyProvider:
    """
    Proxy that defers provider initialization until first use.

    Useful for startup performance when not all providers are needed.
    """

    def __init__(self, provider_type: ProviderType, config: Dict):
        self._provider_type = provider_type
        self._config = config
        self._instance: Optional[RemoteProvider] = None

    def _get_instance(self) -> RemoteProvider:
        if self._instance is None:
            self._instance = ProviderRegistry.get(
                self._provider_type,
                self._config
            )
        return self._instance

    def __getattr__(self, name: str):
        return getattr(self._get_instance(), name)
```

### AC#4: Extension Point for Custom Providers

```python
# Example: Adding a custom Linear provider

@ProviderRegistry.register(ProviderType.LINEAR)  # Add to enum first
class LinearProvider(RemoteProvider):
    """Custom provider for Linear issue tracker."""

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.LINEAR

    @property
    def display_name(self) -> str:
        return "Linear"

    @property
    def id_pattern(self) -> str:
        return r'^[A-Z]+-\d+$'  # e.g., ENG-123

    # ... implement all abstract methods
```

---

## Task-019: Secret Management Design

### Overview

Secure credential storage using system keychain with environment variable fallback.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SecretManager                             │
│                                                              │
│  get_token(provider) ──► try keychain, then env, then prompt│
│  store_token(provider, token) ──► save to keychain          │
│  delete_token(provider) ──► remove from keychain            │
│  validate_token(provider, token) ──► test with API          │
└─────────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌───────────┐    ┌───────────┐    ┌───────────┐
   │  macOS    │    │  Linux    │    │ Windows   │
   │ Keychain  │    │ SecretSvc │    │ CredMgr   │
   └───────────┘    └───────────┘    └───────────┘
```

### AC#1: Multi-Platform Keychain Support

```python
import keyring
from keyring.errors import KeyringError
import platform

class SecretManager:
    """
    Secure credential management with platform-native storage.

    Storage backends by platform:
    - macOS: Keychain Services
    - Linux: Secret Service (GNOME Keyring / KWallet)
    - Windows: Credential Manager
    """

    SERVICE_NAME = "backlog-satellite"

    # Token key naming convention
    TOKEN_KEYS = {
        ProviderType.GITHUB: "github-token",
        ProviderType.JIRA: "jira-token",
        ProviderType.NOTION: "notion-token",
    }

    def __init__(self):
        self._validate_keyring()

    def _validate_keyring(self) -> None:
        """Ensure keyring backend is available."""
        backend = keyring.get_keyring()
        if isinstance(backend, keyring.backends.fail.Keyring):
            raise SecretStorageUnavailableError(
                "No secure storage backend available. "
                "Install a keyring backend or use environment variables."
            )

    def get_token(self, provider: ProviderType) -> Optional[str]:
        """
        Retrieve token with fallback chain:
        1. System keychain
        2. Environment variable
        3. CLI tool integration (gh, jira)
        """
        # Try keychain first
        token = self._get_from_keychain(provider)
        if token:
            return token

        # Try environment variable
        token = self._get_from_env(provider)
        if token:
            return token

        # Try CLI tool integration
        token = self._get_from_cli(provider)
        if token:
            return token

        return None

    def _get_from_keychain(self, provider: ProviderType) -> Optional[str]:
        """Get token from system keychain."""
        try:
            key = self.TOKEN_KEYS[provider]
            return keyring.get_password(self.SERVICE_NAME, key)
        except KeyringError:
            return None

    def store_token(
        self,
        provider: ProviderType,
        token: str,
        validate: bool = True
    ) -> None:
        """
        Store token in system keychain.

        Args:
            provider: Target provider
            token: API token
            validate: If True, verify token works before storing
        """
        if validate and not self._validate_token(provider, token):
            raise InvalidTokenError(provider)

        key = self.TOKEN_KEYS[provider]
        keyring.set_password(self.SERVICE_NAME, key, token)

    def delete_token(self, provider: ProviderType) -> None:
        """Remove token from keychain."""
        key = self.TOKEN_KEYS[provider]
        try:
            keyring.delete_password(self.SERVICE_NAME, key)
        except KeyringError:
            pass  # Token didn't exist
```

### AC#2: Environment Variable Fallback

```python
# Environment variable naming convention
ENV_VAR_NAMES = {
    ProviderType.GITHUB: ["GITHUB_TOKEN", "GH_TOKEN"],
    ProviderType.JIRA: ["JIRA_TOKEN", "JIRA_API_TOKEN"],
    ProviderType.NOTION: ["NOTION_TOKEN", "NOTION_API_KEY"],
}

def _get_from_env(self, provider: ProviderType) -> Optional[str]:
    """Get token from environment variables."""
    import os
    for var_name in ENV_VAR_NAMES.get(provider, []):
        token = os.environ.get(var_name)
        if token:
            return token
    return None
```

### AC#3: CLI Auth Integration

```python
import subprocess
import shutil

def _get_from_cli(self, provider: ProviderType) -> Optional[str]:
    """
    Attempt to get token from CLI tools.

    Supports:
    - GitHub: gh auth token
    - Jira: jira config get token (if jira-cli installed)
    """
    if provider == ProviderType.GITHUB:
        return self._get_gh_token()
    elif provider == ProviderType.JIRA:
        return self._get_jira_token()
    return None

def _get_gh_token(self) -> Optional[str]:
    """Get token from GitHub CLI."""
    if not shutil.which("gh"):
        return None
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None
```

### AC#4: Interactive Prompt for Missing Tokens

```python
import getpass
from rich.prompt import Prompt

def prompt_for_token(
    self,
    provider: ProviderType,
    store: bool = True
) -> str:
    """
    Interactively prompt user for token.

    Args:
        provider: Target provider
        store: If True, store token after validation

    Returns:
        Valid API token
    """
    instructions = {
        ProviderType.GITHUB: (
            "Create a GitHub token at: https://github.com/settings/tokens\n"
            "Required scopes: repo, read:user"
        ),
        ProviderType.JIRA: (
            "Create a Jira API token at: https://id.atlassian.com/manage-profile/security/api-tokens\n"
            "Use your email as username"
        ),
        ProviderType.NOTION: (
            "Create a Notion integration at: https://www.notion.so/my-integrations\n"
            "Copy the Internal Integration Token"
        ),
    }

    print(f"\n{instructions.get(provider, '')}\n")

    while True:
        token = getpass.getpass(f"Enter {provider.value} API token: ")

        if self._validate_token(provider, token):
            if store:
                self.store_token(provider, token, validate=False)
                print(f"✓ Token stored securely in system keychain")
            return token
        else:
            print("✗ Invalid token. Please try again.")
```

### AC#5: Config File Security

```yaml
# ~/.config/backlog/satellite.yml
# NEVER stores actual tokens - only references

providers:
  github:
    enabled: true
    # Token retrieved from: keychain > $GITHUB_TOKEN > gh auth token
    # No token_value field - intentionally omitted

  jira:
    enabled: true
    base_url: "https://company.atlassian.net"
    email: "user@company.com"
    # Token in keychain only

  notion:
    enabled: false
    # Not configured
```

---

## Task-020: Sync Engine Design

### Overview

Bidirectional sync algorithm with conflict detection and incremental updates.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      SyncEngine                              │
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ DiffEngine  │───►│ Reconciler  │───►│ Executor    │     │
│  │             │    │             │    │             │     │
│  │ Compare     │    │ Conflict    │    │ Apply       │     │
│  │ local/remote│    │ resolution  │    │ changes     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                              │
│  State: SyncState (last sync timestamps, ETags)             │
└─────────────────────────────────────────────────────────────┘
```

### AC#1: Sync Algorithm (Create/Update/Delete)

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple

class ChangeType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    NONE = "none"

@dataclass
class SyncPlan:
    """Plan of changes to apply."""
    local_changes: List["Change"]    # Changes to apply locally
    remote_changes: List["Change"]   # Changes to push to remote
    conflicts: List["Conflict"]      # Conflicts requiring resolution

@dataclass
class Change:
    """A single change to apply."""
    task_id: str
    change_type: ChangeType
    source: str  # "local" or "remote"
    fields: Dict[str, Any]

class SyncEngine:
    """
    Bidirectional sync engine.

    Algorithm:
    1. Fetch remote tasks modified since last sync
    2. Load local tasks modified since last sync
    3. Compute diff between local and remote states
    4. Identify conflicts (same task modified both sides)
    5. Apply conflict resolution strategy
    6. Execute changes (local first, then remote)
    7. Update sync state
    """

    def sync(
        self,
        provider: RemoteProvider,
        direction: SyncDirection = SyncDirection.BIDIRECTIONAL,
        conflict_strategy: ConflictResolver = None,
    ) -> SyncResult:
        """
        Execute sync operation.

        Args:
            provider: Remote provider to sync with
            direction: PULL, PUSH, or BIDIRECTIONAL
            conflict_strategy: How to resolve conflicts

        Returns:
            SyncResult with details of all operations
        """
        state = self._load_sync_state(provider)

        # Phase 1: Gather data
        remote_tasks = self._fetch_remote_changes(provider, state)
        local_tasks = self._get_local_changes(state)

        # Phase 2: Compute diff
        plan = self._compute_sync_plan(
            local_tasks,
            remote_tasks,
            direction
        )

        # Phase 3: Resolve conflicts
        if plan.conflicts and conflict_strategy:
            plan = self._resolve_conflicts(plan, conflict_strategy)

        # Phase 4: Execute
        result = self._execute_plan(plan, provider)

        # Phase 5: Update state
        self._save_sync_state(provider, result)

        return result

    def _compute_sync_plan(
        self,
        local: Dict[str, LocalTask],
        remote: Dict[str, RemoteTask],
        direction: SyncDirection,
    ) -> SyncPlan:
        """Compute changes needed for sync."""
        local_changes = []
        remote_changes = []
        conflicts = []

        all_ids = set(local.keys()) | set(remote.keys())

        for task_id in all_ids:
            l_task = local.get(task_id)
            r_task = remote.get(task_id)

            if l_task and not r_task:
                # Only exists locally
                if direction in (SyncDirection.PUSH, SyncDirection.BIDIRECTIONAL):
                    remote_changes.append(Change(
                        task_id=task_id,
                        change_type=ChangeType.CREATE,
                        source="local",
                        fields=l_task.to_dict()
                    ))

            elif r_task and not l_task:
                # Only exists remotely
                if direction in (SyncDirection.PULL, SyncDirection.BIDIRECTIONAL):
                    local_changes.append(Change(
                        task_id=task_id,
                        change_type=ChangeType.CREATE,
                        source="remote",
                        fields=r_task.to_local_task()
                    ))

            else:
                # Exists in both - check for changes
                diff = self._diff_tasks(l_task, r_task)

                if diff.local_newer and diff.remote_newer:
                    # Conflict: both modified
                    conflicts.append(Conflict(
                        task_id=task_id,
                        local_task=l_task,
                        remote_task=r_task,
                        conflicting_fields=diff.changed_fields
                    ))
                elif diff.local_newer:
                    if direction in (SyncDirection.PUSH, SyncDirection.BIDIRECTIONAL):
                        remote_changes.append(Change(
                            task_id=task_id,
                            change_type=ChangeType.UPDATE,
                            source="local",
                            fields=diff.local_changes
                        ))
                elif diff.remote_newer:
                    if direction in (SyncDirection.PULL, SyncDirection.BIDIRECTIONAL):
                        local_changes.append(Change(
                            task_id=task_id,
                            change_type=ChangeType.UPDATE,
                            source="remote",
                            fields=diff.remote_changes
                        ))

        return SyncPlan(local_changes, remote_changes, conflicts)
```

### AC#2: Incremental Sync Using Timestamps

```python
@dataclass
class SyncState:
    """Persisted state for incremental sync."""
    provider: ProviderType
    last_sync: datetime
    task_etags: Dict[str, str]  # task_id -> etag for conflict detection
    cursor: Optional[str]  # Pagination cursor for large syncs

class SyncStateStore:
    """Persist sync state to disk."""

    STATE_FILE = ".backlog/sync-state.json"

    def load(self, provider: ProviderType) -> SyncState:
        """Load sync state for provider."""
        path = Path(self.STATE_FILE)
        if not path.exists():
            return SyncState(
                provider=provider,
                last_sync=datetime.min,
                task_etags={},
                cursor=None
            )

        data = json.loads(path.read_text())
        provider_state = data.get(provider.value, {})
        return SyncState(
            provider=provider,
            last_sync=datetime.fromisoformat(provider_state.get("last_sync", "1970-01-01")),
            task_etags=provider_state.get("etags", {}),
            cursor=provider_state.get("cursor")
        )

    def save(self, state: SyncState) -> None:
        """Save sync state."""
        path = Path(self.STATE_FILE)
        data = json.loads(path.read_text()) if path.exists() else {}

        data[state.provider.value] = {
            "last_sync": state.last_sync.isoformat(),
            "etags": state.task_etags,
            "cursor": state.cursor
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))
```

### AC#3: Conflict Detection Logic

```python
@dataclass
class TaskDiff:
    """Result of comparing local and remote task."""
    local_newer: bool
    remote_newer: bool
    changed_fields: List[str]
    local_changes: Dict[str, Any]
    remote_changes: Dict[str, Any]

def _diff_tasks(self, local: LocalTask, remote: RemoteTask) -> TaskDiff:
    """
    Compare local and remote versions of a task.

    Uses ETags when available, falls back to timestamp comparison.
    """
    # Get tracked fields
    sync_fields = ["title", "description", "status", "assignee", "labels"]

    changed_fields = []
    local_changes = {}
    remote_changes = {}

    for field in sync_fields:
        l_value = getattr(local, field, None)
        r_value = getattr(remote, field, None)

        if l_value != r_value:
            changed_fields.append(field)
            local_changes[field] = l_value
            remote_changes[field] = r_value

    # Determine which is newer
    local_updated = local.updated_at
    remote_updated = remote.updated_at

    # Check ETag if available (preferred method)
    etag_match = (
        local.upstream_etag and
        remote.etag and
        local.upstream_etag == remote.etag
    )

    if etag_match:
        # Remote unchanged since last sync - local wins
        return TaskDiff(
            local_newer=bool(changed_fields),
            remote_newer=False,
            changed_fields=changed_fields,
            local_changes=local_changes,
            remote_changes=remote_changes
        )

    # Fall back to timestamp comparison
    return TaskDiff(
        local_newer=local_updated > local.last_sync_at,
        remote_newer=remote_updated > local.last_sync_at,
        changed_fields=changed_fields,
        local_changes=local_changes,
        remote_changes=remote_changes
    )
```

### AC#4: State Machine

```
                                    ┌──────────┐
                                    │  IDLE    │
                                    └────┬─────┘
                                         │ sync()
                                         ▼
                              ┌──────────────────┐
                              │ FETCHING_REMOTE  │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ COMPUTING_DIFF   │
                              └────────┬─────────┘
                                       │
                          ┌────────────┴────────────┐
                          │ conflicts?              │
                          ▼                         ▼
                ┌──────────────────┐      ┌──────────────────┐
                │ RESOLVING_CONFL  │      │ EXECUTING        │
                └────────┬─────────┘      └────────┬─────────┘
                         │                         │
                         └────────────┬────────────┘
                                      ▼
                              ┌──────────────────┐
                              │ UPDATING_STATE   │
                              └────────┬─────────┘
                                       │
                                       ▼
                                ┌──────────┐
                                │ COMPLETE │
                                └──────────┘
```

```python
class SyncPhase(Enum):
    IDLE = "idle"
    FETCHING_REMOTE = "fetching_remote"
    COMPUTING_DIFF = "computing_diff"
    RESOLVING_CONFLICTS = "resolving_conflicts"
    EXECUTING = "executing"
    UPDATING_STATE = "updating_state"
    COMPLETE = "complete"
    ERROR = "error"

class SyncStateMachine:
    """Track sync operation progress."""

    def __init__(self, on_phase_change: Callable = None):
        self.phase = SyncPhase.IDLE
        self.progress = 0.0
        self.on_phase_change = on_phase_change

    def transition(self, new_phase: SyncPhase, progress: float = None):
        self.phase = new_phase
        if progress is not None:
            self.progress = progress
        if self.on_phase_change:
            self.on_phase_change(self.phase, self.progress)
```

### AC#5: Performance Targets

```python
# Performance requirements
PERFORMANCE_TARGETS = {
    "fetch_100_tasks": 5.0,      # 5 seconds max
    "diff_100_tasks": 0.5,       # 500ms max
    "execute_100_changes": 10.0, # 10 seconds max (rate limited)
    "total_100_tasks": 10.0,     # 10 seconds end-to-end
}

# Optimization strategies
class SyncOptimizer:
    """Optimizations for large sync operations."""

    @staticmethod
    def batch_remote_fetches(task_ids: List[str], batch_size: int = 50):
        """Batch API calls to reduce round trips."""
        for i in range(0, len(task_ids), batch_size):
            yield task_ids[i:i + batch_size]

    @staticmethod
    def parallel_provider_sync(providers: List[RemoteProvider]):
        """Sync multiple providers concurrently."""
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(sync_provider, p): p
                for p in providers
            }
            for future in concurrent.futures.as_completed(futures):
                yield future.result()
```

---

## Task-022: Data Model Extensions

### Overview

Extend Backlog.md task schema with upstream sync, compliance, and spec fields.

### AC#1: Backward-Compatible Schema

```yaml
# Current schema (v1) - still valid
---
id: task-42
title: Example task
status: To Do
assignee: "@user"
labels: [backend]
---

# Extended schema (v2) - optional new fields
---
id: task-42
title: Example task
status: To Do
assignee: "@user"
labels: [backend]

# === NEW: Upstream sync fields ===
upstream:
  provider: github          # github | jira | notion
  id: "owner/repo#123"      # Provider-specific ID
  url: "https://..."        # Web URL to remote task
  synced_at: "2024-01-15T10:30:00Z"
  etag: "abc123"            # For conflict detection

# === NEW: Compliance fields ===
compliance:
  spec_version: "1.2.3"     # Version of spec this implements
  spec_ref: "spec.md#feature-x"  # Reference to spec
  pr_url: "https://..."     # PR that implements this
  audit_trail:              # For regulated environments
    - timestamp: "2024-01-15T10:30:00Z"
      action: "created"
      actor: "@user"
    - timestamp: "2024-01-16T14:00:00Z"
      action: "synced"
      source: "github"

# === NEW: Schema version ===
schema_version: 2
---
```

### AC#2: Migration Strategy

```python
from packaging import version

class TaskMigrator:
    """Migrate tasks between schema versions."""

    CURRENT_VERSION = "2"

    def migrate(self, task_path: Path) -> bool:
        """
        Migrate task to current schema version.

        Returns True if migration was performed.
        """
        content = task_path.read_text()
        frontmatter, body = self._parse_frontmatter(content)

        current = frontmatter.get("schema_version", "1")

        if version.parse(current) >= version.parse(self.CURRENT_VERSION):
            return False  # Already current

        # Apply migrations in sequence
        if version.parse(current) < version.parse("2"):
            frontmatter = self._migrate_v1_to_v2(frontmatter)

        # Write back
        self._write_task(task_path, frontmatter, body)
        return True

    def _migrate_v1_to_v2(self, frontmatter: Dict) -> Dict:
        """
        Migrate from v1 to v2.

        Changes:
        - Add schema_version field
        - Initialize empty upstream/compliance blocks
        """
        frontmatter["schema_version"] = "2"

        # Don't add upstream/compliance unless needed
        # They're optional in v2

        return frontmatter

    def migrate_all(self, tasks_dir: Path) -> Dict[str, int]:
        """Migrate all tasks in directory."""
        results = {"migrated": 0, "skipped": 0, "errors": 0}

        for task_file in tasks_dir.glob("task-*.md"):
            try:
                if self.migrate(task_file):
                    results["migrated"] += 1
                else:
                    results["skipped"] += 1
            except Exception as e:
                results["errors"] += 1
                print(f"Error migrating {task_file}: {e}")

        return results
```

### AC#3: Validation Rules

```python
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class UpstreamConfig(BaseModel):
    """Validation for upstream sync fields."""
    provider: str
    id: str
    url: str
    synced_at: Optional[datetime]
    etag: Optional[str]

    @validator("provider")
    def valid_provider(cls, v):
        valid = ["github", "jira", "notion"]
        if v not in valid:
            raise ValueError(f"provider must be one of {valid}")
        return v

    @validator("url")
    def valid_url(cls, v):
        if not v.startswith("https://"):
            raise ValueError("url must be HTTPS")
        return v

class ComplianceConfig(BaseModel):
    """Validation for compliance fields."""
    spec_version: Optional[str]
    spec_ref: Optional[str]
    pr_url: Optional[str]
    audit_trail: Optional[List[dict]]

class TaskSchema(BaseModel):
    """Full task schema validation."""
    id: str
    title: str
    status: str
    assignee: Optional[str]
    labels: Optional[List[str]]
    upstream: Optional[UpstreamConfig]
    compliance: Optional[ComplianceConfig]
    schema_version: str = "1"

    @validator("id")
    def valid_id(cls, v):
        if not v.startswith("task-"):
            raise ValueError("id must start with 'task-'")
        return v

    @validator("status")
    def valid_status(cls, v):
        valid = ["To Do", "In Progress", "Done", "Blocked"]
        if v not in valid:
            raise ValueError(f"status must be one of {valid}")
        return v
```

### AC#4: Schema Version 2 Definition

```python
SCHEMA_V2 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Backlog.md Task Schema v2",
    "type": "object",
    "required": ["id", "title", "status"],
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^task-\\d+$"
        },
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
        },
        "status": {
            "type": "string",
            "enum": ["To Do", "In Progress", "Done", "Blocked"]
        },
        "assignee": {
            "type": "string",
            "pattern": "^@[\\w-]+$"
        },
        "labels": {
            "type": "array",
            "items": {"type": "string"}
        },
        "upstream": {
            "type": "object",
            "properties": {
                "provider": {"type": "string", "enum": ["github", "jira", "notion"]},
                "id": {"type": "string"},
                "url": {"type": "string", "format": "uri"},
                "synced_at": {"type": "string", "format": "date-time"},
                "etag": {"type": "string"}
            },
            "required": ["provider", "id", "url"]
        },
        "compliance": {
            "type": "object",
            "properties": {
                "spec_version": {"type": "string"},
                "spec_ref": {"type": "string"},
                "pr_url": {"type": "string", "format": "uri"},
                "audit_trail": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "timestamp": {"type": "string", "format": "date-time"},
                            "action": {"type": "string"},
                            "actor": {"type": "string"}
                        }
                    }
                }
            }
        },
        "schema_version": {
            "type": "string",
            "default": "1"
        }
    }
}
```

---

## Summary

| Task | Component | Key Design Decision |
|------|-----------|---------------------|
| task-018 | Provider Registry | Decorator-based registration with lazy initialization |
| task-019 | Secret Management | Keychain-first with env/CLI fallbacks |
| task-020 | Sync Engine | ETag-based conflict detection with pluggable resolution |
| task-022 | Data Model | Backward-compatible v2 schema with optional blocks |

---

*Created for tasks 018, 019, 020, 022 - Satellite Mode Design Phase*
