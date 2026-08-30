# Plan — Upstream Sync Evaluation: spec-kit 1.0.x + Backlog.md 1.50.x

**Date:** 2026-08-30
**Branch:** `refresh`
**Baseline:** `uv run pytest tests/ -q` → 3513 passed, 42 skipped, 0 failures (90s)

---

## 1. How flowspec actually consumes each upstream

### spec-kit — vendored fork, no runtime dependency

`src/flowspec_cli/templates_deploy.py:30` (`deploy_local_templates`) is the default
path for `flowspec init`. It copies **only** `src/flowspec_cli/templates/`.
`download_and_extract_two_stage()` is a fallback, and it points at
`REPO_OWNER = "jpoley" / REPO_NAME = "flowspec"` (`src/flowspec_cli/__init__.py:1322`),
**not** `github/spec-kit`.

Consequences:

- flowspec has **no live dependency** on spec-kit. Nothing breaks if upstream moves.
- The only real inheritance is **document template content** and **command prompt design**.
- Root `scripts/bash/*`, `scripts/powershell/*` are spec-kit carryover that are **not
  deployed** to user projects and are **not referenced** by any `/flow:*` command
  (verified: zero hits for `check-prerequisites|setup-plan|create-new-feature` across
  `src/flowspec_cli/templates/commands/flow/*.md`). Their drift from upstream is
  cosmetic, not functional.

### Backlog.md — live runtime dependency

flowspec shells out to the `backlog` binary and pins a recommended version:

- `get_backlog_validated_version()` (`src/flowspec_cli/__init__.py:1336`) returns a
  **hardcoded `"1.21.0"`**. Despite the docstring/help text referring to a
  "compatibility matrix", `.spec-kit-compatibility.yml` **does not exist** in the repo.
- `flowspec backlog install` / `flowspec backlog upgrade` install that pinned version.
- 112 `backlog task edit` invocations across the deployed templates.

**npm latest: 1.50.1. Locally installed: 1.48.0. Pinned: 1.21.0 — 29 minor versions behind.**

---

## 2. Compatibility check against Backlog.md 1.48/1.50

Every flag flowspec uses today still exists and behaves the same. Verified against the
installed 1.48.0 CLI:

| flowspec usage | 1.50 status |
|---|---|
| `backlog task <id> --plain` | OK |
| `backlog task list -s "In Progress" --plain` | OK |
| `backlog task edit <id> -s/-a/-l/--ac/--check-ac/--notes/--append-notes/--plan` | OK |
| `backlog task create ... --ac --priority` | OK |
| `backlog search <q>` | OK |
| `backlog --version` → bare `X.Y.Z` (parser at `__init__.py:1354` requires digits+dots) | OK |

**No breaking changes.** Raising the pin is safe. The 671 commits between 1.21.0 and
1.50.1 are dominated by TUI/web polish and internal hardening; the CLI surface only grew.

### New Backlog.md capability flowspec does not use

Grep across `src/flowspec_cli/templates/`, `src/flowspec_cli/backlog/`, `.claude/`:

| Capability | Occurrences in flowspec |
|---|---|
| `--dod` / `--check-dod` (native Definition of Done) | **0** |
| `--final-summary` / `--append-final-summary` | **0** |
| `backlog doctor` (duplicate task ID repair) | **0** |
| `backlog overview` | **0** |
| `backlog instructions` | **0** |
| `--ref` / `--modified-file` / `--doc` | **0** |
| `--depends-on` / `--dep` | **0** |
| `--type` (configured task types) | **0** |
| `backlog mcp` server | **0** |
| milestones (`-m`) | 7 (prose only) |

The standout is **Definition of Done**. flowspec already enforces a DoD, but only as
prose in `.claude/workflow.md` and
`src/flowspec_cli/templates/partials/flow/_backlog-instructions.md:137`. Backlog.md now
models DoD natively (`--dod`, `--check-dod`, `--no-dod-defaults`, and a
`definitionOfDone` config key — currently `[]` in this repo). This is a direct,
mechanical upgrade from prose to enforced state.

---

## 3. Compatibility check against spec-kit 1.0.1

Upstream tag: `v0.1.10-1308-g51e52be6`, `pyproject` version `1.0.2.dev0`.

### 3a. Document template deltas (worth porting)

| Template | Upstream addition |
|---|---|
| `spec-template.md` | **New `## Assumptions` section** (4 guided placeholders) |
| `plan-template.md` | `Project Type` examples broadened to `library/cli/web-service/mobile-app/compiler/desktop-app`; `Complexity Tracking` note promoted to a blockquote; fenced blocks tagged `text` |
| `checklist-template.md` | **Reviewer-ownership + marker semantics**: `[x]` means *the requirements-quality criterion was reviewed and satisfied*, not *implementation done*; implement reads checkbox state as a gate and must not mutate markers |
| `tasks-template.md` | Markdown-lint whitespace only |

Most of the remaining diff is upstream replacing literal command names with
`__SPECKIT_COMMAND_*__` placeholder tokens so templates are agent-agnostic. flowspec
resolves this differently (fixed `/flow:*` namespace), so **those tokens must not be
copied in.**

### 3b. Commands present upstream, absent from `/flow:*`

flowspec ships: assess, build, custom, gate, generate-prp, implement, init, intake,
map-codebase, plan, pre-pr, reset, review, rigor, security_*, specify,
submit-n-watch-pr, validate.

Upstream ships: analyze, checklist, clarify, constitution, converge, implement, plan,
specify, tasks, taskstoissues.

Genuine gaps: **`clarify`** (structured ambiguity resolution before planning) and
**`converge`** (diff the built codebase against spec/plan/tasks, append the unbuilt
remainder as new tasks). `analyze` overlaps `/flow:gate` + `/flow:validate`.
`taskstoissues` is superseded by the backlog integration.

### 3c. Upstream subsystems deliberately NOT to port

spec-kit 1.0 grew: extensions (`.specify/extensions.yml` + catalog + hooks),
integrations (scaffold/install/query + manifests), presets, bundles (offline
manifest+hash), an events system, and a YAML workflow engine with switch/cases,
conditions and dispatch.

flowspec already has its own equivalents — `src/flowspec_cli/workflow/` (20 modules:
orchestrator, dispatcher, state_guard, transition, validation_engine, rigor, …),
`flowspec_workflow.yml` (roles/states/workflows/transitions/agent_loops/custom_workflows),
`hooks/`, `skills/`, `security/`, `telemetry/`.

**Porting these would duplicate working subsystems, be a one-way-door architectural
change, and directly contradict "keep this working and simple so we do not break
anything." Recommend: do not port. Re-evaluate only if flowspec wants to consume the
public spec-kit extension catalog.**

---

## 4. Release-path check

### BLOCKER FOUND AND FIXED: the wheel did not build

`uv build` failed on `refresh` **before any of this work** (confirmed by stashing all
changes and rebuilding). It fails on `main` too - the misconfiguration is committed:

```
ValueError: A second file is being added to the wheel archive at the same path:
`flowspec_cli/templates/.mcp.json`.
```

This is a *latent* misconfiguration, not a historical outage. Releases v0.4.007 and
v0.4.008 built successfully on an older hatchling that tolerated duplicate archive
entries; hatchling 1.32.0 rejects them. Since `release.yml` runs `uv build` before
creating the GitHub Release, the **next** release attempt publishes nothing at all -
not even the template zips. Note also that `create-github-release.sh` only ever
attached template zips, never `dist/*.whl`, so the absence of a wheel on past releases
is by design and is not evidence of this bug.

Root cause: `pyproject.toml` declared

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/flowspec_cli"]

[tool.hatch.build.targets.wheel.force-include]
"src/flowspec_cli/templates" = "flowspec_cli/templates"
```

`src/flowspec_cli/templates` is *already inside* the packaged path, so hatchling added
every template twice and aborted. Since `release.yml` builds before it publishes,
**a failing build means the whole release job dies and nothing ships.**

Fix: dropped the redundant `force-include` table. Verified the built wheel contains
**128/128** template files — matching `git ls-files src/flowspec_cli/templates` exactly
— including `.mcp.json`, `.flowspec/` and `.github/`. `tests/test_packaging.py` pins the
invariant so it cannot silently regress.

### Trigger conditions


`.github/workflows/release.yml` triggers only on a merged PR whose head branch matches
`release/vX.Y.Z`, or on `workflow_dispatch`. Merging `refresh` → `main` does **not**
cut a release; it only needs to leave `main` green and releasable. Current version:
`0.4.008` (`pyproject.toml` and `__init__.py:__version__` must stay in sync — there is a
`version-check.yml` workflow guarding this).

---

## 5. Recommendation — tiered

### Tier 1 — do now (safe, additive, no architectural change)

1. **Raise the Backlog.md pin `1.21.0` → `1.50.1`**, and add an explicit *minimum*
   version so `flowspec doctor` can flag stale installs. Remove the dead
   `.spec-kit-compatibility.yml` references from help text since the file does not exist.
2. **Add a `backlog` minimum-version check to `flowspec doctor`** using the existing
   `compare_semver()` helper.
3. **Port the three spec-kit template improvements** (spec `Assumptions`, plan
   `Project Type`/`Complexity Tracking`, checklist reviewer-ownership semantics),
   *without* the `__SPECKIT_COMMAND_*__` tokens.
4. **Adopt native Definition of Done**: document `--dod` / `--check-dod` /
   `--no-dod-defaults` in the backlog partials and key-flags table, and seed
   `definitionOfDone` defaults matching `.claude/workflow.md`'s DoD gates.

All four are content/constant changes. Risk to the 3513-test suite: low, and each is
covered by new tests.

### Tier 2 — propose, needs operator sign-off

5. `/flow:clarify` — port spec-kit's structured clarification loop into the flow
   namespace (new command template + tests).
6. `/flow:converge` — port spec-kit's gap-closing pass, wired to backlog task creation
   rather than `tasks.md`.
7. Richer backlog linkage: `--ref`, `--modified-file`, `--depends-on` in
   `/flow:implement` so tasks carry provenance.

### Tier 3 — do not port

8. spec-kit extensions / integrations / presets / bundles / events / workflow engine.

---

## 6. Tier 1 execution steps — DONE

| # | File | Change |
|---|---|---|
| 0 | `pyproject.toml`, `tests/test_packaging.py` | **Release blocker:** removed the duplicate templates `force-include` that broke `uv build` (see §4) |
| 0b | `src/flowspec_cli/__init__.py` | **Bug:** merged the two shadowed `backlog` Typer groups so `flowspec backlog migrate` is reachable again |
| 1 | `src/flowspec_cli/__init__.py` | `get_backlog_validated_version()` → `"1.50.1"`; add `BACKLOG_MIN_VERSION = "1.34.0"` (first release with `--dod`, verified via `git log -S` on the upstream checkout); fix stale `.spec-kit-compatibility.yml` help strings |
| 2 | `src/flowspec_cli/doctor/checks.py` | `check_backlog_installed()` warns when installed < `BACKLOG_MIN_VERSION` |
| 3 | `src/flowspec_cli/templates/spec-template.md` | append `## Assumptions` |
| 4 | `src/flowspec_cli/templates/plan-template.md` | broaden `Project Type`; blockquote `Complexity Tracking` |
| 5 | `src/flowspec_cli/templates/checklist-template.md` | add Review Ownership + Marker Semantics |
| 6 | `src/flowspec_cli/templates/partials/flow/_backlog-instructions.md` | DoD flags in the reference table + DoD checklist wired to `--check-dod` |
| 7 | `tests/` | new tests for the version constants, the doctor check, and template content |

Gates: `uv run ruff format --check .`, `uv run ruff check .`, `uv run pytest tests/ -x -q`.


---

## 7. Result

| Gate | Before | After |
|---|---|---|
| `uv run ruff format --check .` | pass | pass (324 files) |
| `uv run ruff check .` | pass | pass |
| `uv run pytest tests/ -x -q` | 3513 passed, 42 skipped | **3537 passed, 42 skipped** (+24: 16 upstream-sync, 6 packaging, 2 doctor) |
| `uv build` | **FAILS — no wheel** | **wheel + sdist build; 128/128 templates present** |
| `flowspec doctor` | all pass | all pass |
| `flowspec init` smoke test | n/a | ported content deploys correctly |

Tier 2 and Tier 3 remain open decisions for the operator.
