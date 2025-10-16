# Task 012A: Stack Selection During Init - Feasibility Analysis

## Executive Summary

**Feasibility**: ✅ **FEASIBLE** with **MEDIUM-HIGH COMPLEXITY**

**Effort Estimate**: **3-5 days** (1 developer)

**Recommendation**: Implementable but requires careful design decisions and testing. Consider phased approach.

---

## Problem Statement

Allow users to select a **technology stack** (e.g., React+Go Backend, React+Python Backend, Full-Stack TypeScript, Mobile+Go, etc.) when running `specify init`, and then remove files/configurations related to unselected stacks to avoid clutter and confusion.

---

## Current State Analysis

### What Exists Today

1. **Technology Stack Definitions** (`.stacks/` directory)
   - 9 comprehensive stack definitions with documentation
   - Each stack includes:
     - `README.md` - Full stack documentation (~10-25KB)
     - `workflows/ci-cd.yml` - GitHub Actions CI/CD pipeline
     - `examples/` - Dockerfiles, k8s manifests, configs
   - Stack sizes: 8KB - 40KB each
   - **Total**: ~200KB for all stacks

2. **Stack Categories**:
   - **Web Applications**:
     - `full-stack-react-typescript`
     - `react-frontend-go-backend`
     - `react-frontend-python-backend`
   - **Mobile Applications**:
     - `mobile-frontend-go-backend`
     - `mobile-frontend-python-backend`
   - **Data & ML**:
     - `data-ml-pipeline-python`
   - **Developer Tools**:
     - `vscode-extension-typescript`
     - `chrome-extension-typescript`
   - **Desktop**:
     - `tray-app-cross-platform`

3. **Stack Selection Guide**
   - `.stacks/STACK-SELECTION-GUIDE.md` - Comprehensive decision trees
   - `.stacks/STACK-ORGANIZATION.md` - Organization principles
   - Helps architects choose appropriate stack during `/jpspec:plan`

### What's Missing

1. **Stacks are NOT in release packages**
   - Current release packages only include:
     - `.specify/memory/` (constitution)
     - `.specify/scripts/` (bash or powershell)
     - `.specify/templates/` (spec-template, plan-template, etc.)
     - Agent-specific commands
   - Stacks are only in the source repository

2. **No stack selection during init**
   - Users currently select:
     - AI assistant (claude, copilot, etc.)
     - Script type (sh or ps)
   - No stack selection exists

3. **Stack files are static**
   - Cannot be selectively included/excluded
   - Would need to package ALL stacks and remove unwanted ones

---

## Proposed Solution Design

### Approach 1: Include All Stacks, Remove Unwanted (Recommended)

**Workflow:**
1. User runs `specify init my-project`
2. Selects AI assistant (existing behavior)
3. Selects script type (existing behavior)
4. **NEW**: Selects technology stack (new interactive selection)
5. Download template from GitHub (includes ALL stacks)
6. Extract template to project directory
7. **NEW**: Remove unselected stack directories
8. **NEW**: Copy selected stack's `workflows/ci-cd.yml` to `.github/workflows/`
9. Continue with existing git init, etc.

**Pros:**
- Simpler release package creation (one package per agent+script combo)
- No combinatorial explosion of release assets
- Can add stack selection without changing GitHub Actions workflows

**Cons:**
- Download larger templates (~200KB extra)
- Need to implement removal logic
- Slightly slower download

### Approach 2: Create Stack-Specific Release Packages

**Workflow:**
1. Create separate release packages for each combination:
   - `spec-kit-template-{agent}-{script}-{stack}-{version}.zip`
   - Example: `spec-kit-template-claude-sh-react-go-v0.3.0.zip`
2. User selects stack during init
3. Download only the selected stack package

**Pros:**
- Smaller downloads (only selected stack)
- Cleaner approach

**Cons:**
- **Combinatorial explosion**: 13 agents × 2 scripts × 9 stacks = **234 release assets** per version
- Much more complex release workflow
- GitHub has limits on release assets
- Harder to maintain
- NOT RECOMMENDED

---

## Implementation Plan

### Phase 1: Preparation (Day 1)

#### 1.1 Update Release Package Script
**File**: `.github/workflows/scripts/create-release-packages.sh`

**Changes**:
```bash
# Add stacks to each package
if [[ -d .stacks ]]; then
  mkdir -p "$SPEC_DIR/stacks"
  cp -r .stacks/* "$SPEC_DIR/stacks/"
  echo "Copied .stacks -> .specify/stacks"
fi
```

**Effort**: 1-2 hours

#### 1.2 Add Stack Configuration
**File**: `src/specify_cli/__init__.py`

**Changes**:
```python
STACK_CONFIG = {
    "react-go": {
        "name": "React Frontend + Go Backend",
        "folder": "react-frontend-go-backend",
        "description": "High-performance web apps",
        "project_types": ["web", "api"],
    },
    "react-python": {
        "name": "React Frontend + Python Backend",
        "folder": "react-frontend-python-backend",
        "description": "Data-driven web apps with ML",
        "project_types": ["web", "ml"],
    },
    "full-stack-ts": {
        "name": "Full Stack TypeScript",
        "folder": "full-stack-react-typescript",
        "description": "Rapid development, single language",
        "project_types": ["web", "saas"],
    },
    "mobile-go": {
        "name": "Mobile + Go Backend",
        "folder": "mobile-frontend-go-backend",
        "description": "Native mobile with performant backend",
        "project_types": ["mobile"],
    },
    "mobile-python": {
        "name": "Mobile + Python Backend",
        "folder": "mobile-frontend-python-backend",
        "description": "Mobile with ML features",
        "project_types": ["mobile", "ml"],
    },
    "data-ml": {
        "name": "Data/ML Pipeline (Python)",
        "folder": "data-ml-pipeline-python",
        "description": "ETL, ML training, analytics",
        "project_types": ["data", "ml"],
    },
    "vscode-ext": {
        "name": "VS Code Extension",
        "folder": "vscode-extension-typescript",
        "description": "Developer productivity tools",
        "project_types": ["tooling"],
    },
    "chrome-ext": {
        "name": "Chrome Extension",
        "folder": "chrome-extension-typescript",
        "description": "Browser extensions",
        "project_types": ["tooling"],
    },
    "tray-app": {
        "name": "System Tray App",
        "folder": "tray-app-cross-platform",
        "description": "Desktop background utilities",
        "project_types": ["desktop"],
    },
    "skip": {
        "name": "Skip (choose stack later)",
        "folder": None,
        "description": "Install all stacks, choose during /jpspec:plan",
        "project_types": [],
    },
}
```

**Effort**: 2 hours

### Phase 2: Add Interactive Stack Selection (Day 2)

#### 2.1 Create Stack Selection Function
**File**: `src/specify_cli/__init__.py`

**Changes**:
```python
def select_stack(default_key: str = "skip") -> str:
    """Interactive stack selection using arrow keys."""
    stack_choices = {
        key: f"{config['name']} - {config['description']}"
        for key, config in STACK_CONFIG.items()
    }

    selected_stack = select_with_arrows(
        stack_choices,
        "Choose your technology stack (or skip to choose later):",
        default_key
    )

    return selected_stack
```

**Effort**: 2-3 hours

#### 2.2 Integrate into init Command
**File**: `src/specify_cli/__init__.py` - `init()` function

**Changes**:
```python
@app.command()
def init(..., stack: str = typer.Option(None, "--stack", help="Technology stack to use")):
    # ... existing code ...

    # After script selection, before download
    if stack:
        if stack not in STACK_CONFIG:
            console.print(f"[red]Error:[/red] Invalid stack '{stack}'...")
            raise typer.Exit(1)
        selected_stack = stack
    else:
        if sys.stdin.isatty():
            selected_stack = select_stack()
        else:
            selected_stack = "skip"

    console.print(f"[cyan]Selected stack:[/cyan] {selected_stack}")

    # ... continue with download ...
```

**Effort**: 3-4 hours

### Phase 3: Implement Stack Filtering (Day 3)

#### 3.1 Create Stack Cleanup Function
**File**: `src/specify_cli/__init__.py`

**New function**:
```python
def cleanup_unselected_stacks(project_path: Path, selected_stack: str, tracker: StepTracker | None = None) -> None:
    """Remove stack directories that weren't selected."""
    stacks_dir = project_path / ".specify" / "stacks"

    if not stacks_dir.exists():
        if tracker:
            tracker.skip("stack-cleanup", "no stacks directory")
        return

    if selected_stack == "skip":
        # User wants to keep all stacks
        if tracker:
            tracker.complete("stack-cleanup", "keeping all stacks")
        return

    stack_folder = STACK_CONFIG[selected_stack]["folder"]

    # Remove all stack folders except the selected one and documentation
    removed_count = 0
    kept_files = {"README.md", "STACK-SELECTION-GUIDE.md", "STACK-ORGANIZATION.md"}

    for item in stacks_dir.iterdir():
        if item.name in kept_files:
            continue  # Keep documentation

        if item.is_dir() and item.name != stack_folder:
            shutil.rmtree(item)
            removed_count += 1

    if tracker:
        tracker.complete("stack-cleanup", f"removed {removed_count} unused stacks")
```

**Effort**: 4 hours

#### 3.2 Copy Stack Workflow to .github/workflows/
**New function**:
```python
def setup_stack_workflow(project_path: Path, selected_stack: str, tracker: StepTracker | None = None) -> None:
    """Copy the selected stack's CI/CD workflow to .github/workflows/."""
    if selected_stack == "skip":
        if tracker:
            tracker.skip("stack-workflow", "no stack selected")
        return

    stack_folder = STACK_CONFIG[selected_stack]["folder"]
    source_workflow = project_path / ".specify" / "stacks" / stack_folder / "workflows" / "ci-cd.yml"

    if not source_workflow.exists():
        if tracker:
            tracker.error("stack-workflow", f"workflow not found: {source_workflow}")
        return

    # Create .github/workflows directory
    workflows_dir = project_path / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    # Copy workflow with stack-specific name
    dest_workflow = workflows_dir / f"{stack_folder}-ci-cd.yml"
    shutil.copy2(source_workflow, dest_workflow)

    if tracker:
        tracker.complete("stack-workflow", f"installed {stack_folder} CI/CD")
```

**Effort**: 3 hours

#### 3.3 Integrate Cleanup into init()
**File**: `src/specify_cli/__init__.py` - `init()` function

**Changes**:
```python
with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
    # ... existing download and extract ...

    # NEW: Add to tracker
    tracker.add("stack-cleanup", "Remove unused stacks")
    tracker.add("stack-workflow", "Install stack CI/CD workflow")

    # NEW: Cleanup stacks
    cleanup_unselected_stacks(project_path, selected_stack, tracker=tracker)

    # NEW: Setup stack workflow
    setup_stack_workflow(project_path, selected_stack, tracker=tracker)

    # ... existing chmod, git init, etc. ...
```

**Effort**: 2 hours

### Phase 4: Update Release Workflow & Testing (Days 4-5)

#### 4.1 Test Release Package Creation
**Actions**:
1. Test `create-release-packages.sh` locally with stacks included
2. Verify package sizes (should increase by ~200KB)
3. Test extraction

**Effort**: 4 hours

#### 4.2 Create Integration Tests
**File**: `tests/test_stack_selection.py`

**Test Cases**:
```python
def test_stack_selection_removes_others():
    """Test that selecting one stack removes others."""
    # Test setup
    # Run init with stack selection
    # Verify only selected stack remains
    # Verify documentation files remain
    pass

def test_skip_stack_keeps_all():
    """Test that skipping keeps all stacks."""
    # Test setup
    # Run init with stack=skip
    # Verify all stacks remain
    pass

def test_stack_workflow_copied():
    """Test that stack workflow is copied to .github/workflows."""
    # Test setup
    # Run init with stack selection
    # Verify workflow file exists in .github/workflows
    pass
```

**Effort**: 6 hours

#### 4.3 Update Documentation
**Files to Update**:
- `README.md` - Add stack selection examples
- `CLAUDE.md` - Document new `--stack` flag
- `.github/workflows/release.yml` - Ensure stacks are included

**Effort**: 3 hours

### Phase 5: Optional Enhancements (Future)

#### 5.1 Stack Detection from Project Type
- Analyze user's requirements to suggest stack
- Use AI to recommend based on keywords

#### 5.2 Stack Migration Support
- Allow changing stack after init
- Preserve custom code during migration

---

## Detailed Effort Breakdown

| Phase | Task | Effort | Complexity |
|-------|------|--------|-----------|
| 1.1 | Update release package script | 1-2 hours | Low |
| 1.2 | Add stack configuration | 2 hours | Low |
| 2.1 | Create stack selection function | 2-3 hours | Medium |
| 2.2 | Integrate into init command | 3-4 hours | Medium |
| 3.1 | Create stack cleanup function | 4 hours | Medium-High |
| 3.2 | Copy stack workflow function | 3 hours | Medium |
| 3.3 | Integrate cleanup into init | 2 hours | Low |
| 4.1 | Test release package creation | 4 hours | Medium |
| 4.2 | Create integration tests | 6 hours | High |
| 4.3 | Update documentation | 3 hours | Low |
| **TOTAL** | | **30-34 hours** | **3-5 days** |

---

## Risks & Mitigation

### Risk 1: Release Package Size Increase
**Impact**: Download time increases by ~200KB (20-30% increase from current ~800KB)
**Likelihood**: Certain
**Mitigation**:
- Acceptable tradeoff for better UX
- Consider compression improvements
- Document in changelog

### Risk 2: Stack Documentation Gets Outdated
**Impact**: Users get incorrect guidance
**Likelihood**: Medium
**Mitigation**:
- Add CI checks to validate stack documentation
- Link to `.languages/` for detailed standards
- Regular review process

### Risk 3: User Confusion with "skip" Option
**Impact**: Users might not understand when to skip
**Likelihood**: Medium
**Mitigation**:
- Clear description in selection prompt
- Add help text explaining `/jpspec:plan` workflow
- Default to "skip" with good explanation

### Risk 4: Stack Selection vs. Agent Selection Confusion
**Impact**: Users might confuse technology stack with AI agent
**Likelihood**: Low-Medium
**Mitigation**:
- Clear labeling and separation in UI
- Use different terminology ("AI assistant" vs "technology stack")
- Show distinct selection prompts

---

## Alternative Approaches Considered

### Alternative 1: Download Stack Separately
**Description**: Download stack files separately via `specify add-stack <name>`
**Pros**: Smaller initial download, more modular
**Cons**: Extra command, more complex workflow, worse UX
**Verdict**: Rejected - worse UX

### Alternative 2: No Removal, Just Guidance
**Description**: Include all stacks, provide documentation to guide selection
**Pros**: Simpler implementation, no removal logic needed
**Cons**: Cluttered project, confusing for users
**Verdict**: Rejected - poor UX for majority use case

### Alternative 3: Template Variants per Stack
**Description**: Create release packages for each agent+script+stack combination
**Pros**: Smallest possible downloads
**Cons**: 234 release assets per version, unmaintainable
**Verdict**: Rejected - too complex

---

## Testing Strategy

### Unit Tests
- `test_stack_config_valid()` - Validate STACK_CONFIG structure
- `test_cleanup_removes_correct_stacks()` - Test removal logic
- `test_skip_preserves_all()` - Test skip behavior
- `test_workflow_copy()` - Test workflow copying

### Integration Tests
- `test_full_init_with_stack()` - Full init with stack selection
- `test_init_stack_flag()` - Test --stack CLI flag
- `test_init_stack_interactive()` - Test interactive selection

### Manual Tests
- Test with each AI agent
- Test with each script type
- Test each stack selection
- Test "skip" option
- Test --stack flag

---

## Success Criteria

✅ **Functional Requirements**:
1. User can select stack during init (interactive or via `--stack` flag)
2. Only selected stack remains in `.specify/stacks/`
3. Stack documentation (README.md, etc.) always remains
4. Selected stack's CI/CD workflow copied to `.github/workflows/`
5. "skip" option keeps all stacks
6. Backward compatible (existing init still works)

✅ **Non-Functional Requirements**:
1. Download time increase <30%
2. Selection UX is clear and intuitive
3. No breaking changes to existing workflows
4. Documentation updated
5. Test coverage >80%

---

## Recommendations

### Priority: MEDIUM-HIGH
This feature adds significant value for users who want opinionated CI/CD and project structure from the start, but is not critical for core functionality.

### Approach: PHASED IMPLEMENTATION
1. **Phase 1-3**: Core functionality (Days 1-3)
2. **Phase 4**: Testing and documentation (Days 4-5)
3. **Phase 5**: Future enhancements (as needed)

### Key Decision Points
1. **Default Behavior**: Default to "skip" to maintain backward compatibility
2. **Documentation**: Keep all stack documentation files even when stack is not selected
3. **Workflow Naming**: Use `{stack-name}-ci-cd.yml` for clarity
4. **Release Packages**: Include all stacks (Approach 1)

---

## Conclusion

**Task 12A is FEASIBLE and RECOMMENDED for implementation.**

**Estimated Effort**: 3-5 days (1 developer)
**Complexity**: Medium-High
**Value**: High (better UX, opinionated CI/CD from start)
**Risk**: Low-Medium (manageable with proper testing)

The implementation is straightforward with existing patterns in the codebase. The main complexity is in ensuring proper cleanup logic and testing all combinations. The recommended approach (include all stacks, remove unwanted) balances implementation complexity with user experience.

**Next Steps**:
1. Review and approve this analysis
2. Create GitHub issue with implementation plan
3. Implement Phase 1-3 (core functionality)
4. Test thoroughly with different combinations
5. Deploy and monitor user feedback
