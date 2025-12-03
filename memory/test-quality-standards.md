# Test Quality Standards

This document captures defensive coding patterns for test files and code examples, learned from fixing fragile tests and broken code examples in task-087, task-191a, task-191b, and task-191c.

## CRITICAL: Code Examples Must Be Complete and Runnable

**Every code example in documentation, agent definitions, and templates MUST be complete enough to run.** This means:

1. **ALL imports must be present** - no implicit imports
2. **No undefined references** - explain any dependencies with comments
3. **Use proper validators** - not weak regex patterns

### Why This Matters

Code examples are frequently copy-pasted by users and AI assistants. Incomplete examples:
- Fail immediately when run
- Waste time debugging missing imports
- Set a poor standard for the codebase
- Indicate the code was never actually tested

### Required Import Patterns

```python
# WRONG - Missing imports that would cause immediate failure
router = APIRouter(prefix="/users", tags=["users"])

class UserCreate(BaseModel):
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")  # Weak regex!

class UserResponse(BaseModel):
    created_at: datetime  # Where does datetime come from?

async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):  # AsyncSession? get_db?
    existing = await db.scalar(select(User).where(...))  # select? User?
```

```python
# CORRECT - Complete imports and documented dependencies
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field  # Use EmailStr for email validation!
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db  # Your database dependency
from app.models import User  # Your SQLAlchemy User model

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    email: EmailStr  # Robust email validation, not weak regex
    name: str = Field(..., min_length=1, max_length=100)


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Exception Handler Example

```python
# WRONG - Missing imports and undefined app
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):  # Request? JSONResponse?
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```

```python
# CORRECT - Complete imports and defined app
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()  # Your FastAPI application instance


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "user_id": exc.user_id},
    )
```

### Test Example Imports

```python
# WRONG - Missing imports in test examples
@pytest.mark.asyncio
async def test_user_flow(client: AsyncClient):  # AsyncClient from where?
    response = await client.post("/users/", json={...})
```

```python
# CORRECT - Complete test imports
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_flow(client: AsyncClient) -> None:
    """Test complete user creation and retrieval flow."""
    response = await client.post(
        "/users/",
        json={"email": "test@example.com", "name": "Test User"},
    )
    assert response.status_code == 201
```

### Checklist for Code Examples

- [ ] All imports are explicitly listed
- [ ] All type hints use imported types
- [ ] Undefined dependencies have explanatory comments
- [ ] Uses `EmailStr` not regex for email validation
- [ ] Test methods have `-> None` return type
- [ ] Test methods have docstrings
- [ ] The example could be copy-pasted and run (with appropriate model definitions)

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

## Except Clauses Must Have Explanatory Comments

Empty `except` blocks or those that just `pass` must explain why:

```python
# WRONG - Silent suppression without explanation
try:
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
except (OSError, IOError, PermissionError):
    pass  # Why are we suppressing? Unclear!
return None
```

```python
# CORRECT - Comment explains the intent
try:
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
except (OSError, IOError, PermissionError):
    # Suppress file read errors; function returns None if file can't be read
    pass
return None
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
- [ ] Empty except clauses have explanatory comments

## Checklist for Code Examples in Documentation

- [ ] All imports are explicitly listed at top
- [ ] No undefined type hints (datetime, AsyncSession, etc.)
- [ ] Dependencies explained with comments (get_db, User model)
- [ ] Uses proper validators (EmailStr, not regex for email)
- [ ] Could be copy-pasted and would run

## NEVER CLAIM CODE WORKS WITHOUT TESTING

The root cause of these issues is claiming code is complete without actually running it. This is unacceptable.

### Verification Requirements

1. **For test files**: Actually run `pytest` and verify tests pass
2. **For code examples**: Verify imports exist and types are correct
3. **For lint**: Actually run `ruff check` and `ruff format`
4. **For the full suite**: Run the complete test suite before claiming "done"

### What "Testing Passed" Means

- NOT: "I think it would pass"
- NOT: "It looks correct"
- NOT: "The structure is right"
- YES: "I ran `pytest` and saw all tests pass"
- YES: "I ran `ruff check` and there were no errors"

### Common Lies to Avoid

- "All 28 tests pass" (without running them)
- "Lint passes" (without running ruff)
- "This would work" (without verifying imports exist)

If you say tests pass, you MUST have run them. Period.
