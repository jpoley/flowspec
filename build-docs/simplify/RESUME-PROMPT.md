# Resume Prompt: Complete Custom Workflow Orchestration

**Copy/paste this prompt when ready to resume work:**

---

## Prompt

I'm working on the flowspec custom workflow orchestration feature. The infrastructure is ~60% complete and I need you to finish the integration.

**Branch**: `muckross-simplify-flow-take2`
**Latest Commit**: `e033e70` - docs: add comprehensive next steps and clean up outer loop artifacts
**Status**: Infrastructure complete, integration pending

### Context

Read these files FIRST (in order):
1. `build-docs/simplify/flowspec-loop.md` - THE MISSION: Inner loop architecture
2. `build-docs/simplify/dec27-next.md` - Complete next steps (2800 lines)
3. `build-docs/simplify/FAILURE-LEARNINGS.md` - What NOT to do

### What's Already Done (~60% complete)

✅ **Working Code:**
- `src/flowspec_cli/workflow/orchestrator.py` (432 lines) - REAL orchestrator implementation
- `src/flowspec_cli/workflow/rigor.py` (150 lines) - Rigor enforcement
- `schemas/flowspec_workflow.schema.json` (+110 lines) - Extended schema
- `tests/workflow/test_orchestrator.py` (122 lines) - Tests passing (3/3)
- `flowspec_workflow.yml` - Example custom workflows (quick_build, full_design, ship_it)
- `.claude/commands/flow/custom.md` - Command documentation
- `docs/guides/custom-workflows.md` - User guide

✅ **Cleanup:**
- `/flow:operate` removed (outer loop, not flowspec)
- `Deployed` state removed (outer loop)
- Tests updated for 8 states, 6 workflows (35/35 passing)

### What Needs to Be Done (~40% remaining)

Follow **`build-docs/simplify/dec27-next.md`** exactly:

**Phase 2: CLI Integration (60 min)**
- Create `src/flowspec_cli/commands/flow_custom.py`
- Register `/flow:custom` command in CLI
- Test: `flowspec flow:custom --list`

**Phase 3: Workflow Dispatch (90 min)**
- Create `src/flowspec_cli/workflow/dispatcher.py`
- Wire to actual workflow handlers (specify, plan, implement, validate, etc.)
- Integrate with orchestrator (replace lines 390-416 in orchestrator.py)

**Phase 4: MCP Migration (60 min)**
- Create `src/flowspec_cli/backlog/mcp_shim.py`
- Replace ALL bash `backlog task` calls with MCP tools
- Remove security vulnerabilities (no eval, no shell=True)

**Phase 5: E2E Testing (45 min)**
- Create `tests/e2e/test_custom_workflows.py`
- Test quick_build, full_design, ship_it workflows
- Verify rigor logging to `.logs/`

**Phase 6: Documentation & PR (30 min)**
- Update `CLAUDE.md` with custom workflow section
- Final test run
- Create PR to main

### Critical Rules (From FAILURE-LEARNINGS.md)

**NEVER:**
- ❌ Create stub/fake implementations
- ❌ Lie about completion percentage
- ❌ Use eval() or shell=True
- ❌ Skip rigor enforcement
- ❌ Claim success without testing

**ALWAYS:**
- ✅ Create REAL working code
- ✅ Be honest about status
- ✅ Use MCP for backlog (not bash)
- ✅ Enforce logging/ADRs/constitution
- ✅ Test everything

### Starting Point

```bash
# Checkout branch
git checkout muckross-simplify-flow-take2

# Verify status
git log --oneline -3
# Should show: e033e70 docs: add comprehensive next steps...

# Verify tests pass
uv run pytest tests/test_workflow_config_valid.py -v
# Should show: 35 passed

# Start with Phase 2
# Read: build-docs/simplify/dec27-next.md (lines 369-520)
# Create: src/flowspec_cli/commands/flow_custom.py
```

### Success Criteria

When complete, you should be able to:
```bash
# List custom workflows
flowspec flow:custom --list

# Execute a custom workflow
flowspec flow:custom quick_build

# Verify logs created
ls -la .logs/decisions/
ls -la .logs/events/

# All tests passing
uv run pytest tests/ -v
```

### Key Files to Reference

**Architecture:**
- `src/flowspec_cli/workflow/orchestrator.py` - Already complete
- `src/flowspec_cli/workflow/rigor.py` - Already complete

**Plan:**
- `build-docs/simplify/dec27-next.md` - YOUR ROADMAP (follow exactly)

**Requirements:**
- `build-docs/simplify/DO-NOW.md` - Full requirements
- `build-docs/simplify/MISSION.md` - Core mission

**Tests:**
- `tests/workflow/test_orchestrator.py` - Existing tests

### Estimated Time

- Total remaining: ~5 hours (285 minutes)
- Can be broken into phases (60-90 min each)

### Questions to Ask Before Starting

1. Have you read `build-docs/simplify/dec27-next.md`?
2. Do you understand the inner/outer loop distinction?
3. Are you ready to follow the plan exactly?

---

**Now execute `build-docs/simplify/dec27-next.md` starting with Phase 2 (line 369). Follow the plan exactly. Create REAL working code, not stubs. Be honest about progress.**

---

## Notes for Claude

- The orchestrator at lines 390-416 has a TODO comment marking the dispatch integration point
- All infrastructure is tested and working
- Just needs wiring to existing workflow handlers
- Example custom workflows already defined in flowspec_workflow.yml
- NO shortcuts - implement everything properly

---

**END OF RESUME PROMPT**
