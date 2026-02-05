# Test Runner Sub-Agent

Run automated tests, linting, and type checks. Return structured results.

## Input

- `project_type`: python | node | auto-detect
- `test_paths`: Optional specific paths to test
- `skip_types`: Optional, skip type checking

## Task

1. **Detect project type** (if auto-detect)
   - `pyproject.toml` → Python
   - `package.json` → Node.js

2. **Run test suite**
   - Python: `uv run pytest tests/ -v --tb=short`
   - Node: `npm test`

3. **Run linting**
   - Python: `uv run ruff check . --output-format=concise`
   - Node: `npm run lint`

4. **Run type checks** (unless skipped)
   - Python: `uv run mypy src/` (if configured)
   - Node: `npm run typecheck` (if configured)

5. **Capture skipped tests**
   - Document any skipped tests with reasons
   - Categorize: benchmark, integration, platform-specific, flaky

## Output Format

Return JSON:

```json
{
  "status": "pass" | "fail",
  "tests": {
    "passed": 45,
    "failed": 0,
    "skipped": 3,
    "skipped_details": [
      {"name": "test_benchmark_large", "reason": "benchmark", "file": "tests/perf/test_bench.py"}
    ]
  },
  "lint": {
    "status": "pass" | "fail",
    "errors": 0,
    "warnings": 2
  },
  "types": {
    "status": "pass" | "fail" | "skipped",
    "errors": 0
  },
  "summary": "All tests pass, 2 lint warnings, types OK"
}
```

## Critical: Collect ALL Failures

**Do NOT stop at first failure.** Run everything, collect everything:

- Run ALL tests (not `-x` / `--exitfirst`)
- Collect ALL lint errors
- Collect ALL type errors
- Return complete picture

User fixes everything in one pass, not one at a time.
