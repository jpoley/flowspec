# Code Standards

## Python

- **Linter/Formatter**: Ruff (replaces Black, Flake8, isort)
- **Line length**: 88 characters
- **Type hints**: Required for public APIs
- **File paths**: Use `pathlib`

## File I/O (Critical)

- **Always use `encoding="utf-8"`** for all file operations:
  ```python
  # Reading
  with open(file_path, encoding="utf-8") as f:
      content = f.read()

  # Writing with pathlib
  path.write_text(content, encoding="utf-8")
  path.read_text(encoding="utf-8")
  ```
- **Always clean up temp files** with try-finally:
  ```python
  with tempfile.NamedTemporaryFile(delete=False) as f:
      temp_path = f.name
  try:
      # use temp file
  finally:
      Path(temp_path).unlink(missing_ok=True)
  ```

## Naming (Avoid Shadowing)

Never use Python built-in names as parameters or variables:
- **Bad**: `id`, `type`, `list`, `dict`, `input`, `filter`, `map`, `hash`
- **Good**: `finding_id`, `item_type`, `items`, `data`, `user_input`

## Defensive Programming

- **Clamp external inputs** to expected ranges:
  ```python
  confidence = float(data.get("confidence", 0.5))
  confidence = max(0.0, min(1.0, confidence))  # Clamp to [0.0, 1.0]
  ```
- **Explicit type conversions** for clarity:
  ```python
  # Good: explicit
  validate_path(str(finding.location.file))

  # Bad: implicit conversion
  validate_path(finding.location.file)  # Relies on __str__
  ```

## YAGNI (You Aren't Gonna Need It)

- Don't add config fields you don't use
- Remove dead code, don't comment it out
- If a feature isn't implemented, don't scaffold it

## Testing

- **Framework**: pytest
- **Coverage**: >80% on core functionality
- **Pattern**: Arrange-Act-Assert (AAA)
- **No shadowing** in test helpers either

## Commits

Follow conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

## Pre-PR Checklist

Before creating a PR, verify:
- [ ] `encoding="utf-8"` on all file operations
- [ ] No Python built-in names shadowed
- [ ] All temp files cleaned up properly
- [ ] External inputs validated/clamped
- [ ] No unused config fields or dead code
- [ ] Explicit type conversions where needed
