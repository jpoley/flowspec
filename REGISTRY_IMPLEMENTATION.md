# Provider Registry Implementation

## Overview

This document describes the implementation of the Provider Registry for JP Spec Kit's Satellite Mode. The registry implements a factory pattern with auto-detection, lazy initialization, and thread-safe singleton behavior.

## Files Created/Modified

### Created Files
- `src/specify_cli/satellite/registry.py` - Main implementation

### Modified Files
- `src/specify_cli/satellite/__init__.py` - Export registry components

## Acceptance Criteria Verification

### AC#1: ProviderRegistry class with registration ✓

**Implementation:**
- `ProviderRegistry` class with `@register` decorator
- Class-level storage: `_providers` dict and `_instances` dict
- Thread-safe locking mechanism (`_lock`)

**Key Methods:**
```python
@classmethod
def register(cls, provider_type: ProviderType):
    """Decorator to register a provider class."""
    # Validates provider is RemoteProvider subclass
    # Stores in _providers dict
```

**Usage Example:**
```python
@ProviderRegistry.register(ProviderType.GITHUB)
class GitHubProvider(RemoteProvider):
    # ... implementation
```

### AC#2: Auto-detection using regex patterns ✓

**Implementation:**
- `PROVIDER_PATTERNS` dict with regex patterns for each provider type
- `detect_provider()` method matches task ID against patterns
- `parse_task_id()` method extracts named groups from matched pattern

**Patterns Implemented:**
- GitHub: `r'^(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)#(?P<number>\d+)$'`
  - Example: `owner/repo#123`
- Jira: `r'^(?P<project>[A-Z][A-Z0-9]*)-(?P<number>\d+)$'`
  - Example: `PROJ-123`
- Notion: `r'^(?P<id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$'`
  - Example: `abc12345-1234-1234-1234-123456789abc`

**Usage Example:**
```python
provider_type = ProviderRegistry.detect_provider("owner/repo#123")
# Returns: ProviderType.GITHUB

parsed = ProviderRegistry.parse_task_id("PROJ-456")
# Returns: {'provider': ProviderType.JIRA, 'project': 'PROJ', 'number': '456'}
```

### AC#3: Lazy initialization ✓

**Implementation:**
- `LazyProvider` class acts as a proxy
- Provider instance created only on first attribute access
- Subsequent accesses reuse the same instance

**Key Features:**
- `__init__` stores config without creating provider
- `_get_instance()` creates provider on demand
- `__getattr__` delegates to actual provider instance

**Usage Example:**
```python
lazy = LazyProvider(ProviderType.GITHUB, {"token": "..."})
# Provider not created yet

task = lazy.get_task("owner/repo#123")
# Provider created on first method call
```

### AC#4: Thread-safe singleton pattern ✓

**Implementation:**
- `threading.Lock` for concurrent access protection
- Instances cached by provider type + config hash
- Same config returns same instance (singleton per config)
- Different configs create separate instances

**Thread Safety Features:**
```python
with cls._lock:
    if key not in cls._instances:
        cls._instances[key] = provider_class(config)
    return cls._instances[key]
```

**Cache Key Strategy:**
```python
config_hash = hash(frozenset(config.items()))
key = f"{provider_type.value}:{config_hash}"
```

### AC#5: Extension API documented ✓

**Documentation Provided:**
- Comprehensive docstrings for all public methods
- Usage examples in docstrings
- Type hints for all parameters and return values
- Clear error messages (raises TypeError if not RemoteProvider subclass)

**Extension Points:**

1. **Register Custom Provider:**
```python
@ProviderRegistry.register(ProviderType.LINEAR)
class LinearProvider(RemoteProvider):
    # Implement abstract methods
    pass
```

2. **Add Custom Pattern:**
```python
# First add to ProviderType enum
class ProviderType(Enum):
    LINEAR = "linear"

# Then add pattern to registry
PROVIDER_PATTERNS[ProviderType.LINEAR] = r'^[A-Z]+-\d+$'
```

3. **Utility Methods:**
- `list_available()` - Get all registered providers
- `unregister()` - Remove provider (useful for testing)
- `clear_instances()` - Clear cached instances

## API Reference

### ProviderRegistry

#### Class Methods

**register(provider_type: ProviderType)**
- Decorator to register a provider class
- Validates provider is RemoteProvider subclass
- Raises TypeError if not

**get(provider_type: ProviderType, config: Optional[Dict] = None) -> RemoteProvider**
- Get or create provider instance
- Thread-safe singleton per provider+config
- Raises ProviderNotFoundError if not registered

**detect_provider(task_id: str) -> Optional[ProviderType]**
- Auto-detect provider from task ID format
- Returns ProviderType or None

**parse_task_id(task_id: str) -> Optional[Dict[str, str]]**
- Parse task ID into components
- Returns dict with 'provider' key and named groups

**list_available() -> Dict[ProviderType, Type[RemoteProvider]]**
- Get all registered providers
- Returns copy of _providers dict

**unregister(provider_type: ProviderType) -> None**
- Remove provider registration
- Clears cached instances for that type

**clear_instances() -> None**
- Clear all cached instances
- Preserves registrations

### LazyProvider

**__init__(provider_type: ProviderType, config: Optional[Dict] = None)**
- Create lazy provider proxy
- Does not initialize provider

**_get_instance() -> RemoteProvider**
- Internal method to get/create provider
- Called automatically on attribute access

**__getattr__(name: str)**
- Proxy attribute access to provider
- Triggers initialization on first call

**__repr__() -> str**
- Show initialization status

## Design Decisions

### 1. Class-Level State
- Used class variables instead of module globals
- Allows testing with multiple independent registries if needed
- Cleaner API with registry.ProviderRegistry.method()

### 2. Config Hashing
- Used `frozenset(config.items())` for hashable config
- Enables singleton per unique configuration
- Different configs create different instances

### 3. Error Handling
- Raises TypeError for invalid provider classes
- Raises ProviderNotFoundError for unknown providers
- Clear error messages with context

### 4. Pattern Matching
- Used regex with named groups
- Enables both detection and parsing with same patterns
- Easy to extend with new providers

### 5. Thread Safety
- Single lock for all registry operations
- Lock held for minimal time (only during dict operations)
- No deadlock risk (no nested locks)

## Integration with Existing Code

### Dependencies
- `src/specify_cli/satellite/enums.py` - ProviderType enum
- `src/specify_cli/satellite/errors.py` - ProviderNotFoundError
- `src/specify_cli/satellite/provider.py` - RemoteProvider ABC

### Exports
Added to `src/specify_cli/satellite/__init__.py`:
- ProviderRegistry
- LazyProvider
- PROVIDER_PATTERNS

## Testing Considerations

### Manual Tests Performed
1. ✓ Syntax validation (py_compile)
2. ✓ AST parsing (valid Python)
3. ✓ Import structure verification

### Suggested Integration Tests
1. **Registration Tests**
   - Register mock provider
   - Verify in list_available()
   - Test TypeError on non-RemoteProvider

2. **Auto-Detection Tests**
   - Test GitHub, Jira, Notion patterns
   - Test invalid formats return None
   - Test parse_task_id extracts fields

3. **Singleton Tests**
   - Same config returns same instance
   - Different config returns different instance
   - Test across threads

4. **Lazy Loading Tests**
   - Verify provider not created on LazyProvider init
   - Verify created on first attribute access
   - Verify reused on subsequent access

5. **Thread Safety Tests**
   - Multiple threads requesting same provider
   - Verify only one instance created
   - Verify all threads get same instance

## Future Enhancements

1. **Pattern Validation**
   - Validate patterns compile correctly on registration
   - Detect pattern conflicts (overlapping patterns)

2. **Provider Discovery**
   - Auto-discover providers via entry points
   - Plugin architecture for third-party providers

3. **Instance Lifecycle**
   - TTL for cached instances
   - Automatic cleanup of stale instances
   - Connection pooling

4. **Metrics**
   - Track provider usage
   - Monitor instance count
   - Log registration events

5. **Configuration**
   - Support environment-based configs
   - Config validation on registration
   - Default configs per provider

## Related Tasks

- **task-023**: RemoteProvider ABC (dependency - completed)
- **task-025**: Secret Management (uses registry for provider instances)
- **task-026**: Sync Engine (uses registry for provider auto-detection)

## Compliance Notes

This implementation:
- Follows design doc exactly (task-018 section in satellite-mode-subsystems-design.md)
- Maintains thread safety for multi-threaded CLI usage
- Provides extension points for custom providers
- Includes comprehensive documentation
- Uses type hints throughout
- Follows Python best practices

## Status

**Implementation Status**: Complete ✓

All acceptance criteria met:
- [x] #1 ProviderRegistry class with registration
- [x] #2 Auto-detection using regex patterns
- [x] #3 Lazy initialization
- [x] #4 Thread-safe singleton pattern
- [x] #5 Extension API documented
