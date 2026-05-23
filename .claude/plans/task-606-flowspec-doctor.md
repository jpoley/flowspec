# Plan: `flowspec doctor` — Setup Health Check and Diagnostics

**Task:** TASK-606  
**Branch:** `galway/task-606/flowspec-doctor`  
**Issue:** [#1221](https://github.com/jpoley/flowspec/issues/1221)

---

## Goal

Add `flowspec doctor` CLI command that checks the environment and surfaces setup problems before they cause confusing failures.

```
flowspec doctor          # run all checks
flowspec doctor --fix    # attempt auto-fix where possible
```

Example output:
```
✅ Python 3.12.2
✅ flowspec v0.4.008 (up to date)
✅ backlog.md v1.21.0
✅ beads v0.29.0
✅ flowspec_workflow.yml present and valid
⚠️  Agent files using old hyphen naming — run: flowspec upgrade-repo
❌ Constitution not found — run: /flow:init
```

---

## Files to Create

```
src/flowspec_cli/doctor/
├── __init__.py      — exports run_doctor()
├── checks.py        — CheckResult dataclass + 8 check functions
└── cli.py           — Typer command + run_doctor()
tests/test_doctor.py — ~15 unit tests (pass/fail/warn per check)
```

## Files to Modify

```
src/flowspec_cli/__init__.py  — add thin @app.command("doctor") wrapper (~10 lines)
```

---

## The 8 Checks

| # | Check | Pass | Warn | Fail |
|---|-------|------|------|------|
| 1 | Python version | ≥ 3.11 | — | < 3.11 |
| 2 | flowspec version | current = latest GitHub release | behind latest | cannot fetch |
| 3 | backlog.md | `backlog --version` succeeds | — | not found |
| 4 | beads | `bd --version` succeeds | — | not found |
| 5 | `flowspec_workflow.yml` | exists + valid YAML | — | missing / parse error |
| 6 | Agent naming convention | no `flow-*.agent.md` in `.github/agents/` | old files found | — |
| 7 | Constitution | `memory/constitution.md` exists | missing | — |
| 8 | `.flowspec/` directory | exists | missing | — |

---

## `checks.py` Design

```python
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class CheckStatus(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"

@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    message: str
    fix_cmd: str | None = None  # shown in --fix or as hint

def check_python_version() -> CheckResult: ...
def check_flowspec_version(current: str) -> CheckResult: ...
def check_backlog_installed() -> CheckResult: ...
def check_beads_installed() -> CheckResult: ...
def check_workflow_config(project_path: Path) -> CheckResult: ...
def check_agent_naming(project_path: Path) -> CheckResult: ...
def check_constitution(project_path: Path) -> CheckResult: ...
def check_flowspec_dir(project_path: Path) -> CheckResult: ...

def run_all_checks(project_path: Path, current_version: str) -> list[CheckResult]: ...
```

## `cli.py` Design

```python
def run_doctor(project_path: Path, fix: bool = False) -> None:
    results = run_all_checks(project_path, current_version=__version__)
    # print rich table with ✅/⚠️/❌
    # if fix=True: attempt fixes for warn/fail items
```

## `--fix` Behavior

| Check | Fix Action |
|-------|-----------|
| Agent naming (warn) | `subprocess.run(["flowspec", "upgrade-repo"])` |
| Constitution (warn) | Write minimal constitution template to `memory/constitution.md` |
| Others | Print the fix command, do not auto-run |

## `__init__.py` Addition

Near line 9179 (after `app.add_typer(telemetry_app, ...)`):

```python
@app.command(name="doctor")
def doctor_cmd(
    fix: bool = typer.Option(False, "--fix", help="Attempt auto-fix where possible"),
):
    """Check flowspec setup health and diagnose configuration issues."""
    from flowspec_cli.doctor.cli import run_doctor
    run_doctor(project_path=Path.cwd(), fix=fix)
```

---

## Tests (`tests/test_doctor.py`)

```python
class TestCheckPythonVersion:
    def test_pass_current_version(self): ...      # sys.version_info >= (3, 11)
    def test_fail_old_version(self, monkeypatch): ... # mock sys.version_info = (3, 10)

class TestCheckBacklogInstalled:
    def test_pass_when_installed(self, monkeypatch): ...  # mock subprocess returning version
    def test_fail_when_not_found(self, monkeypatch): ... # mock FileNotFoundError

class TestCheckBeadsInstalled:
    def test_pass_when_installed(self, monkeypatch): ...
    def test_fail_when_not_found(self, monkeypatch): ...

class TestCheckWorkflowConfig:
    def test_pass_valid_yml(self, tmp_path): ...
    def test_fail_missing(self, tmp_path): ...
    def test_fail_invalid_yaml(self, tmp_path): ...

class TestCheckAgentNaming:
    def test_pass_no_hyphenated_files(self, tmp_path): ...
    def test_warn_hyphenated_files_present(self, tmp_path): ...
    def test_pass_no_agents_dir(self, tmp_path): ...   # no .github/agents/ = no issue

class TestCheckConstitution:
    def test_pass_constitution_exists(self, tmp_path): ...
    def test_warn_constitution_missing(self, tmp_path): ...

class TestCheckFlowspecDir:
    def test_pass_dir_exists(self, tmp_path): ...
    def test_warn_dir_missing(self, tmp_path): ...

class TestRunAllChecks:
    def test_returns_eight_checks(self, tmp_path, monkeypatch): ...
```

---

## Definition of Done

- [ ] `uv run ruff check .` passes
- [ ] `uv run ruff format --check .` passes
- [ ] `uv run pytest tests/ -x -q` passes (including new doctor tests)
- [ ] `flowspec doctor` runs and prints formatted output
- [ ] `flowspec doctor --fix` runs without error
- [ ] All 5 ACs in TASK-606 checked
- [ ] PR created, closes #1221
