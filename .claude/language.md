# Language — Python

## Version
Python 3.11+ (enforced by `pyproject.toml`)

## Formatter
`ruff format` — line length 88, configured in `pyproject.toml`

```bash
uv run ruff format .          # format in place
uv run ruff format --check .  # CI check (no changes)
```

## Linter
`ruff check` — replaces flake8, isort, pyflakes

```bash
uv run ruff check .           # lint
uv run ruff check . --fix     # auto-fix safe issues
```

## Type Hints
- Required on all public API functions and class methods
- Not enforced with a type checker (no pyright/mypy in CI)
- Use `from __future__ import annotations` when needed for forward refs

## Test Framework
**pytest** — run with:
```bash
uv run pytest tests/ -x -q         # fail-fast, quiet
uv run pytest tests/ -x -q -k foo  # filter by name
```

Current stats: ~3473 tests, ~37s runtime

### Test Patterns
- File: `tests/test_<module>.py`
- Classes: `class TestFeatureName:` — group related tests
- Methods: `def test_<behaviour>(self) -> None:` — explicit return type
- Pattern: Arrange → Act → Assert
- Fixtures: `tmp_path` for file isolation, `monkeypatch` for subprocess/env mocking
- Never use relative paths — always `Path(__file__).resolve().parent.parent` for project root

### Coverage Target
>80% on core functionality (not enforced in CI, but expected)

### What NOT to mock
- Real YAML parsing — use `tmp_path` fixtures with actual files
- Real file I/O — prefer real files over StringIO

## Naming Conventions
- Never shadow Python builtins: no `type`, `list`, `dict`, `input`, `filter`, `map`, `hash`
- `id` acceptable in public APIs where required
- Never shadow imported modules: if `import html` exists, don't do `html = generate_html()`

## File I/O
Always specify encoding:
```python
path.read_text(encoding="utf-8")
path.write_text(content, encoding="utf-8")
with open(path, encoding="utf-8") as f: ...
```

## Imports
All imports at module level (top of file). Never inline inside functions.

## Comments
Default: none. Add only when the WHY is non-obvious — a hidden constraint, subtle invariant, or known workaround.
