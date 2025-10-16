# Task 012B: Multi-Agent Installation - Feasibility Analysis

## Executive Summary

**Feasibility**: ✅ **HIGHLY FEASIBLE** with **LOW-MEDIUM COMPLEXITY**

**Effort Estimate**: **1-3 days** (1 developer)

**Recommendation**: RECOMMENDED for implementation. Simpler than Task 12A and provides clear value for teams using multiple AI agents.

---

## Problem Statement

Allow users to install spec-kit support for **multiple AI coding agents** (not just one) when running `specify init`. This enables teams or individuals who use multiple AI assistants (e.g., Claude Code for backend, GitHub Copilot for frontend) to have spec-kit commands available in all of them.

---

## Current State Analysis

### What Exists Today

1. **Single Agent Installation**
   - `specify init` downloads and installs ONE agent's template
   - User selects agent via:
     - Interactive selection (arrow keys)
     - `--ai <agent>` flag
   - Template extracted to agent-specific directory:
     - `.claude/commands/` (Claude Code)
     - `.github/prompts/` (GitHub Copilot)
     - `.gemini/commands/` (Gemini)
     - `.cursor/commands/` (Cursor)
     - `.windsurf/workflows/` (Windsurf)
     - `.qwen/commands/` (Qwen)
     - `.opencode/command/` (opencode)
     - `.codex/prompts/` (Codex)
     - `.kilocode/workflows/` (Kilo Code)
     - `.augment/commands/` (Auggie)
     - `.roo/commands/` (Roo Code)
     - `.codebuddy/commands/` (CodeBuddy)
     - `.amazonq/prompts/` (Amazon Q Developer)

2. **Agent Directory Independence**
   - Each agent uses a different directory
   - **NO CONFLICTS** between agent directories
   - Multiple agent directories can coexist in the same project
   - Each agent reads only its own directory

3. **Supported Agents**: 13 total
   - **CLI-based** (requires_cli: true): claude, gemini, qwen, opencode, codex, auggie, codebuddy, q
   - **IDE-based** (requires_cli: false): copilot, cursor-agent, windsurf, kilocode, roo

4. **Current Limitations**
   - User can only pick ONE agent
   - Installing for multiple agents requires:
     - Run `specify init` multiple times? (doesn't work - would overwrite shared files)
     - Manual copying of agent directories
     - No official support for multi-agent setup

### What Users Want

**Use Case 1: Team with Mixed Preferences**
- Frontend devs use GitHub Copilot
- Backend devs use Claude Code
- Everyone wants access to spec-kit commands

**Use Case 2: Individual Using Multiple Agents**
- Uses Claude Code for architecture and planning
- Uses Cursor for quick edits
- Uses GitHub Copilot in VS Code

**Use Case 3: Marketplace/Plugin Installation (Claude Code)**
- Install spec-kit via Claude Code marketplace
- Already have other agents configured
- Want to add spec-kit to multiple agents at once

---

## Proposed Solution Design

### Approach 1: Multi-Select During Init (Recommended for CLI)

**Workflow:**
1. User runs `specify init my-project`
2. **NEW**: Select one or more AI assistants (multi-select with checkboxes)
   - Use space to toggle selection
   - Use arrow keys to navigate
   - Press Enter to confirm
3. Select script type (existing)
4. Download and extract templates for ALL selected agents
5. Continue with git init, etc.

**UI Example:**
```
Choose your AI assistant(s) (space to select, enter to confirm):

 [✓] Claude Code
 [ ] GitHub Copilot
 [✓] Cursor
 [ ] Gemini CLI
 [ ] Qwen Code
 [ ] opencode
 [ ] Windsurf
 [ ] Kilo Code
 [ ] Auggie CLI
 [ ] CodeBuddy
 [ ] Roo Code
 [ ] Codex CLI
 [ ] Amazon Q Developer CLI
```

**Pros:**
- Best UX for new projects
- All agents configured from the start
- Simple, clear interface

**Cons:**
- Need to implement multi-select UI
- More complex validation logic

### Approach 2: Comma-Separated CLI Flag

**Workflow:**
```bash
specify init my-project --ai claude,copilot,cursor
```

**Pros:**
- Simple for CLI users
- Easy for scripts/automation
- No UI changes needed

**Cons:**
- Less discoverable
- Harder to validate input
- Not as user-friendly

### Approach 3: Hybrid (Recommended)

**Support both**:
- Interactive multi-select (when TTY available)
- Comma-separated flag (for automation/non-interactive)

**Examples:**
```bash
# Interactive multi-select
specify init my-project

# CLI flag
specify init my-project --ai claude,copilot,cursor

# Single agent (backward compatible)
specify init my-project --ai claude
```

### Approach 4: Add Agents Later with New Command

**New command**: `specify add-agent <agent-name>`

**Example:**
```bash
specify init my-project --ai claude
cd my-project
specify add-agent copilot
specify add-agent cursor
```

**Pros:**
- Modular, flexible
- Can add agents incrementally
- Simpler initial implementation

**Cons:**
- Extra command to learn
- More steps for users
- Doesn't solve init use case

---

## Implementation Plan (Approach 3: Hybrid)

### Phase 1: Core Multi-Agent Support (Day 1)

#### 1.1 Update Agent Selection Logic
**File**: `src/specify_cli/__init__.py`

**Changes**:
```python
def parse_agent_list(agent_string: str) -> list[str]:
    """Parse comma-separated agent list and validate."""
    agents = [a.strip() for a in agent_string.replace(',', ' ').split()]
    agents = [a for a in agents if a]  # Remove empty strings

    # Validate all agents exist
    for agent in agents:
        if agent not in AGENT_CONFIG:
            raise ValueError(f"Unknown agent: {agent}")

    return agents

def select_agents_multi(default_agents: list[str] = None) -> list[str]:
    """Interactive multi-select for AI assistants."""
    if default_agents is None:
        default_agents = ["copilot"]  # Default selection

    selected_agents = []

    # Create options with checkboxes
    agent_keys = list(AGENT_CONFIG.keys())
    selected_indices = [i for i, k in enumerate(agent_keys) if k in default_agents]

    def create_selection_panel():
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=5)
        table.add_column(style="white", justify="left")

        for i, agent_key in enumerate(agent_keys):
            config = AGENT_CONFIG[agent_key]
            checkbox = "[✓]" if i in selected_indices else "[ ]"
            name = config["name"]

            if i == current_index:
                table.add_row(
                    f"▶ {checkbox}",
                    f"[cyan]{name}[/cyan]"
                )
            else:
                table.add_row(
                    f"  {checkbox}",
                    f"{name}"
                )

        table.add_row("", "")
        table.add_row("", "[dim]Space: toggle, ↑/↓: navigate, Enter: confirm[/dim]")

        return Panel(
            table,
            title="[bold]Select AI Assistant(s)[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )

    current_index = 0

    console.print()

    with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
        while True:
            try:
                key = get_key()
                if key == 'up':
                    current_index = (current_index - 1) % len(agent_keys)
                elif key == 'down':
                    current_index = (current_index + 1) % len(agent_keys)
                elif key == ' ':  # Space to toggle
                    if current_index in selected_indices:
                        selected_indices.remove(current_index)
                    else:
                        selected_indices.append(current_index)
                elif key == 'enter':
                    if not selected_indices:
                        console.print("\n[yellow]Please select at least one agent[/yellow]")
                        continue
                    selected_agents = [agent_keys[i] for i in sorted(selected_indices)]
                    break
                elif key == 'escape':
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

                live.update(create_selection_panel(), refresh=True)

            except KeyboardInterrupt:
                console.print("\n[yellow]Selection cancelled[/yellow]")
                raise typer.Exit(1)

    return selected_agents
```

**Effort**: 6-8 hours

#### 1.2 Update init() Command Signature
**File**: `src/specify_cli/__init__.py`

**Changes**:
```python
@app.command()
def init(
    project_name: str = typer.Argument(None, help="..."),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant(s) to use (comma-separated for multiple, e.g., 'claude,copilot,cursor')"),
    # ... other parameters ...
):
    """Initialize a new Specify project from the latest template.

    Examples:
        # Interactive selection (single or multiple agents)
        specify init my-project

        # Single agent
        specify init my-project --ai claude

        # Multiple agents
        specify init my-project --ai claude,copilot,cursor

        # Multiple agents with spaces
        specify init my-project --ai "claude, copilot, cursor"
    """
    # ... existing code ...

    # NEW: Parse and validate agents
    if ai_assistant:
        try:
            selected_agents = parse_agent_list(ai_assistant)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            console.print(f"[yellow]Valid agents:[/yellow] {', '.join(AGENT_CONFIG.keys())}")
            raise typer.Exit(1)
    else:
        if sys.stdin.isatty():
            selected_agents = select_agents_multi()
        else:
            # Non-interactive: default to copilot
            selected_agents = ["copilot"]

    console.print(f"[cyan]Selected AI assistant(s):[/cyan] {', '.join(selected_agents)}")

    # ... continue with rest of init ...
```

**Effort**: 3-4 hours

### Phase 2: Multi-Agent Download & Installation (Day 2)

#### 2.1 Download Multiple Templates
**File**: `src/specify_cli/__init__.py`

**Changes**:
```python
def download_and_extract_multiple_agents(
    project_path: Path,
    agents: list[str],
    script_type: str,
    is_current_dir: bool = False,
    *,
    verbose: bool = True,
    tracker: StepTracker | None = None,
    client: httpx.Client = None,
    debug: bool = False,
    github_token: str = None
) -> Path:
    """Download and extract templates for multiple agents."""

    # Download and extract first agent (full template)
    first_agent = agents[0]
    if tracker:
        tracker.add(f"agent-{first_agent}", f"Install {AGENT_CONFIG[first_agent]['name']}")
        tracker.start(f"agent-{first_agent}")

    download_and_extract_template(
        project_path,
        first_agent,
        script_type,
        is_current_dir,
        verbose=verbose,
        tracker=None,  # Use custom tracking
        client=client,
        debug=debug,
        github_token=github_token
    )

    if tracker:
        tracker.complete(f"agent-{first_agent}")

    # For remaining agents, only extract agent-specific directories
    for agent in agents[1:]:
        if tracker:
            tracker.add(f"agent-{agent}", f"Install {AGENT_CONFIG[agent]['name']}")
            tracker.start(f"agent-{agent}")

        try:
            # Download template
            zip_path, meta = download_template_from_github(
                agent,
                Path.cwd(),
                script_type=script_type,
                verbose=False,
                show_progress=False,
                client=client,
                debug=debug,
                github_token=github_token
            )

            # Extract only agent-specific directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                agent_folder = AGENT_CONFIG[agent]["folder"]

                # Find agent directory in zip
                agent_files = [f for f in zip_ref.namelist() if agent_folder in f]

                # Extract agent directory
                for file_path in agent_files:
                    # Extract to project directory
                    zip_ref.extract(file_path, project_path)

            # Cleanup zip
            if zip_path.exists():
                zip_path.unlink()

            if tracker:
                tracker.complete(f"agent-{agent}")

        except Exception as e:
            if tracker:
                tracker.error(f"agent-{agent}", str(e))
            console.print(f"[yellow]Warning:[/yellow] Failed to install {agent}: {e}")

    return project_path
```

**Effort**: 6-8 hours

#### 2.2 Update Agent Tool Checks
**File**: `src/specify_cli/__init__.py`

**Changes**:
```python
# In init() function, after agent selection

if not ignore_agent_tools:
    missing_tools = []

    for agent in selected_agents:
        agent_config = AGENT_CONFIG.get(agent)
        if agent_config and agent_config["requires_cli"]:
            if not check_tool(agent):
                missing_tools.append({
                    "agent": agent,
                    "name": agent_config["name"],
                    "url": agent_config["install_url"]
                })

    if missing_tools:
        error_lines = ["[red]Missing required tools:[/red]\n"]
        for tool in missing_tools:
            error_lines.append(f"  • [cyan]{tool['agent']}[/cyan] ({tool['name']})")
            error_lines.append(f"    Install from: {tool['url']}\n")

        error_lines.append("\n[dim]Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check[/dim]")

        error_panel = Panel(
            "\n".join(error_lines),
            title="[red]Agent Detection Error[/red]",
            border_style="red",
            padding=(1, 2)
        )
        console.print()
        console.print(error_panel)
        raise typer.Exit(1)
```

**Effort**: 2-3 hours

### Phase 3: Testing & Documentation (Day 3)

#### 3.1 Create Tests
**File**: `tests/test_multi_agent.py`

**Test Cases**:
```python
def test_parse_agent_list_single():
    """Test parsing single agent."""
    result = parse_agent_list("claude")
    assert result == ["claude"]

def test_parse_agent_list_multiple():
    """Test parsing multiple comma-separated agents."""
    result = parse_agent_list("claude,copilot,cursor")
    assert result == ["claude", "copilot", "cursor"]

def test_parse_agent_list_with_spaces():
    """Test parsing with spaces."""
    result = parse_agent_list("claude, copilot, cursor")
    assert result == ["claude", "copilot", "cursor"]

def test_parse_agent_list_invalid():
    """Test invalid agent raises error."""
    with pytest.raises(ValueError):
        parse_agent_list("claude,invalid-agent")

def test_multi_agent_init():
    """Test init with multiple agents."""
    # Test that multiple agent directories are created
    # Test that shared files are not duplicated
    # Test that each agent has its commands
    pass

def test_multi_agent_no_conflicts():
    """Test that multiple agents don't conflict."""
    # Verify each agent directory is independent
    # Verify no file overwrites
    pass
```

**Effort**: 5-6 hours

#### 3.2 Update Documentation
**Files to Update**:
- `README.md` - Add multi-agent examples
- `CLAUDE.md` - Document `--ai` flag with comma-separated values
- Add FAQ section about multi-agent usage

**Examples to Add:**
```markdown
### Multiple AI Assistants

Install spec-kit for multiple AI assistants at once:

```bash
# Interactive multi-select
specify init my-project

# Via CLI flag (comma-separated)
specify init my-project --ai claude,copilot,cursor

# Or with spaces
specify init my-project --ai "claude, copilot, cursor"
```

This is useful for:
- Teams using different AI assistants
- Individuals who switch between tools
- Projects that want maximum compatibility
```

**Effort**: 3-4 hours

---

## Detailed Effort Breakdown

| Phase | Task | Effort | Complexity |
|-------|------|--------|-----------|
| 1.1 | Create multi-select UI | 6-8 hours | Medium-High |
| 1.2 | Update init command signature | 3-4 hours | Low-Medium |
| 2.1 | Multi-agent download logic | 6-8 hours | Medium |
| 2.2 | Update tool checks for multiple agents | 2-3 hours | Low |
| 3.1 | Create tests | 5-6 hours | Medium |
| 3.2 | Update documentation | 3-4 hours | Low |
| **TOTAL** | | **25-33 hours** | **1-3 days** |

---

## Risks & Mitigation

### Risk 1: Agent Directory Conflicts
**Impact**: Files overwrite each other
**Likelihood**: Very Low (agents use different directories)
**Mitigation**:
- Agents already use separate directories
- Test with all agent combinations
- Document which directories each agent uses

### Risk 2: Download Time Increases
**Impact**: Multiple template downloads take longer
**Likelihood**: Certain
**Mitigation**:
- Download in parallel where possible
- Only download agent-specific portions for 2nd+ agents
- Show progress for each agent
- Acceptable tradeoff for better UX

### Risk 3: Tool Check Failures for Multiple Agents
**Impact**: User must install multiple CLI tools
**Likelihood**: Medium
**Mitigation**:
- Clear error messages listing all missing tools
- Provide install links for each
- `--ignore-agent-tools` flag still works
- Separate IDE-based (no CLI) from CLI-based agents

### Risk 4: Confusion About Which Agent to Use
**Impact**: Users don't know which agent to use for which command
**Likelihood**: Low
**Mitigation**:
- All agents get the same commands
- Commands work identically in all agents
- Document in README

---

## Alternative Approaches Considered

### Alternative 1: Agent-Specific Command Variants
**Description**: Different commands for different agents (e.g., `/speckit.claude.specify`, `/speckit.copilot.specify`)
**Pros**: Clear which agent is being used
**Cons**: Confusing, verbose, defeats the purpose
**Verdict**: Rejected - poor UX

### Alternative 2: Primary + Secondary Agents
**Description**: User picks one primary agent, optionally add secondary agents
**Pros**: Simpler selection flow
**Cons**: Artificial distinction, confusing
**Verdict**: Rejected - unnecessary complexity

### Alternative 3: Install All Agents by Default
**Description**: Always install all 13 agents
**Pros**: Maximum compatibility, no selection needed
**Cons**: Clutters project, downloads/checks for tools user doesn't have
**Verdict**: Rejected - poor default behavior

### Alternative 4: Post-Init Agent Addition (specify add-agent)
**Description**: New command to add agents after init
**Pros**: Modular, incremental
**Cons**: Extra command, doesn't solve init use case
**Verdict**: **Consider as Future Enhancement**

---

## Integration with Claude Code Marketplace

### Marketplace Installation Flow

**Scenario**: User installs spec-kit via Claude Code marketplace/plugin system

**Current Challenge**:
- Marketplace install might only set up `.claude/` directory
- User might want spec-kit in other agents too

**Proposed Solution**:
```bash
# After marketplace install, user runs:
cd their-project
specify add-agent copilot
specify add-agent cursor
```

**Alternative**: Marketplace metadata could specify post-install command:
```json
{
  "name": "spec-kit",
  "postInstall": "specify add-agent claude --here"
}
```

**Recommendation**: Support `specify add-agent` as Phase 2 enhancement

---

## Testing Strategy

### Unit Tests
- `test_parse_agent_list()` - Various input formats
- `test_multi_select_ui()` - UI interaction simulation
- `test_validate_agents()` - Invalid agent handling

### Integration Tests
- `test_init_multiple_agents()` - Full init with 2+ agents
- `test_agent_directories_created()` - Verify all directories exist
- `test_no_file_conflicts()` - Ensure no overwrites

### Manual Tests
- Test all agent combinations (at least sampling)
- Test with/without CLI tools installed
- Test interactive vs. CLI flag
- Test backward compatibility (single agent)

---

## Success Criteria

✅ **Functional Requirements**:
1. Users can select multiple agents (interactive or via `--ai` flag)
2. All selected agent directories are created with proper commands
3. Shared files (`.specify/`) are created only once (not duplicated)
4. Tool checks validate all selected CLI-based agents
5. Backward compatible (single agent selection still works)
6. Each agent can independently access spec-kit commands

✅ **Non-Functional Requirements**:
1. Multi-select UI is intuitive and clear
2. Download time for N agents < N × single-agent time (optimization)
3. Clear error messages for missing tools
4. Documentation shows multi-agent examples
5. Test coverage >80%

---

## Recommendations

### Priority: HIGH
This feature is straightforward to implement and provides significant value for:
- Teams with mixed agent preferences
- Individuals who use multiple AI assistants
- Future marketplace/plugin installations

### Approach: HYBRID (Approach 3)
Support both:
1. **Interactive multi-select** (best UX for new users)
2. **CLI flag** `--ai agent1,agent2,agent3` (best for automation)

### Phased Implementation
**Phase 1**: Core multi-agent support (Days 1-2)
**Phase 2**: Testing and documentation (Day 3)
**Phase 3**: Future enhancements:
- `specify add-agent <name>` command
- `specify remove-agent <name>` command
- `specify list-agents` command
- Marketplace integration

---

## Dependency on Task 12A

**Independent**: Task 12B can be implemented independently of Task 12A.

**Combined Implementation**:
If implementing both tasks:
1. Task 12B is simpler - implement first
2. Task 12A can build on multi-agent selection patterns
3. Combined: User selects agent(s) + stack in one flow

**UI Example (Combined)**:
```
1. Select AI assistant(s): claude, copilot, cursor
2. Select script type: sh
3. Select technology stack: react-frontend-go-backend
```

---

## Conclusion

**Task 12B is HIGHLY FEASIBLE and RECOMMENDED for implementation.**

**Estimated Effort**: 1-3 days (1 developer)
**Complexity**: Low-Medium
**Value**: High (supports common use case, minimal complexity)
**Risk**: Low (agents already independent, well-tested)

The implementation is straightforward since:
1. Agent directories are already independent (no conflicts)
2. Multi-select UI pattern exists in codebase
3. Template download/extraction logic is reusable
4. Backward compatible by default

**Key Benefits**:
- ✅ Solves real user problem (teams with mixed agents)
- ✅ Simple implementation (lower risk than 12A)
- ✅ High value-to-effort ratio
- ✅ Enables future marketplace features
- ✅ No breaking changes

**Next Steps**:
1. Review and approve this analysis
2. Decide on phasing: standalone or combined with 12A
3. Create GitHub issue with implementation plan
4. Implement Phase 1-2 (core + tests)
5. Deploy and monitor user feedback
6. Consider Phase 3 enhancements (`add-agent` command)

---

## Appendix: Agent Directory Reference

| Agent | Directory | Format | CLI Required |
|-------|-----------|--------|--------------|
| Claude Code | `.claude/commands/` | `.md` | ✅ |
| GitHub Copilot | `.github/prompts/` | `.prompt.md` | ❌ (IDE) |
| Gemini | `.gemini/commands/` | `.toml` | ✅ |
| Cursor | `.cursor/commands/` | `.md` | ❌ (IDE) |
| Windsurf | `.windsurf/workflows/` | `.md` | ❌ (IDE) |
| Qwen | `.qwen/commands/` | `.toml` | ✅ |
| opencode | `.opencode/command/` | `.md` | ✅ |
| Codex | `.codex/prompts/` | `.md` | ✅ |
| Kilo Code | `.kilocode/workflows/` | `.md` | ❌ (IDE) |
| Auggie | `.augment/commands/` | `.md` | ✅ |
| Roo Code | `.roo/commands/` | `.md` | ❌ (IDE) |
| CodeBuddy | `.codebuddy/commands/` | `.md` | ✅ |
| Amazon Q | `.amazonq/prompts/` | `.md` | ✅ |

**Key Observations**:
- All agents use different directory paths → No conflicts possible
- Different file formats (`.md`, `.toml`, `.prompt.md`) → No confusion
- Mixed CLI requirements → Validation logic already exists
