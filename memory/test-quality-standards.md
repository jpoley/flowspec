# Test Quality Standards

This document captures defensive coding patterns for test files, learned from fixing fragile tests in task-087, task-191a, task-191b, and task-191c.

## Required Helper Functions

Every test file that reads project files MUST include these helper functions:

### 1. Project Root Detection

```python
def get_project_root() -> Path:
    """Get the project root directory reliably.

    Returns:
        Path to the project root directory.
    """
    return Path(__file__).resolve().parent.parent
```

**Why**: Using relative paths like `Path(".claude/agents/...")` breaks depending on the working directory. Tests run from different directories (IDE, CI, command line) must work consistently.

**Wrong**:
```python
AGENT_DIR = ".claude/agents"  # Fragile!
return Path(AGENT_DIR) / filename
```

**Correct**:
```python
return get_project_root() / ".claude" / "agents" / filename
```

### 2. Safe File Reading

```python
def safe_read_file(file_path: Path) -> Optional[str]:
    """Safely read a file, returning None if it doesn't exist or can't be read.

    Args:
        file_path: Path to the file to read.

    Returns:
        File contents as string, or None if the file can't be read.
    """
    try:
        if file_path.exists() and file_path.is_file():
            return file_path.read_text(encoding="utf-8")
    except (OSError, IOError, PermissionError):
        pass
    return None
```

**Why**: Functions named "safe" should not raise exceptions. Return `Optional[str]` to allow graceful handling when files don't exist or can't be read.

**Wrong** (misleading name):
```python
def _read_file_safely(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(...)  # NOT safe!
```

**Correct**: Return `None` instead of raising, let callers decide how to handle.

## Required Imports

Always import these types:

```python
from pathlib import Path
from typing import Dict, Optional

import pytest
```

## Constants at Module Level

Define expected values as module-level constants:

```python
# Constants
AGENT_NAME = "backend-engineer"
EXPECTED_COLOR = "green"
EXPECTED_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
REQUIRED_FRONTMATTER_FIELDS = ["name", "description", "tools", "color"]
REQUIRED_CONTENT_SECTIONS = [
    "## Core Technologies",
    "## Implementation Standards",
]
```

## Type Hints

All functions and methods must have complete type hints:

```python
def test_method(self, fixture: Path) -> None:  # -> None required
    ...

def helper_function(content: str) -> Dict[str, str]:  # Return type required
    ...
```

## File Encoding

Always specify encoding when reading files:

```python
# Correct
file_path.read_text(encoding="utf-8")

# Wrong (relies on system default)
file_path.read_text()
```

## Assertion Messages

Include meaningful assertion messages that help diagnose failures:

```python
# Good
assert agent_path.exists(), f"Agent file not found at {agent_path}"
assert frontmatter.get("name") == AGENT_NAME, (
    f"Agent name should be '{AGENT_NAME}', got '{frontmatter.get('name')}'"
)

# Bad (no context on failure)
assert agent_path.exists()
assert frontmatter.get("name") == AGENT_NAME
```

## Fixture Patterns

Use consistent fixture patterns for shared test data:

```python
@pytest.fixture
def agent_path(self) -> Path:
    """Get path to the agent file."""
    return get_project_root() / ".claude" / "agents" / "agent-name.md"

@pytest.fixture
def agent_content(self, agent_path: Path) -> str:
    """Return content of the agent file."""
    content = safe_read_file(agent_path)
    if content is None:
        pytest.skip(f"Agent file not found: {agent_path}")
    return content
```

## Test Organization

Group related tests into classes with clear docstrings:

```python
class TestAgentFile:
    """Test the agent file exists and is valid."""

class TestFrontmatter:
    """Test the YAML frontmatter of the agent."""

class TestTools:
    """Test the tools configuration for the agent."""

class TestContent:
    """Test the content of the agent."""
```

## Checklist for New Test Files

- [ ] `get_project_root()` helper function included
- [ ] `safe_read_file()` returns `Optional[str]`, not raises
- [ ] `Optional` imported from typing
- [ ] All paths use project root detection
- [ ] `encoding="utf-8"` on all file reads
- [ ] `-> None` on all test methods
- [ ] Constants defined at module level
- [ ] Meaningful assertion messages
- [ ] Test classes with descriptive docstrings
