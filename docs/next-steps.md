# Next Steps: Flowspec Flexible Orchestration

## Critical Self-Assessment of Previous Failure

**What I got completely wrong:**

1. ❌ **Misunderstood the objective** - Created hardcoded "Research/Build/Run" meta-workflows instead of USER-CUSTOMIZABLE orchestration
2. ❌ **Followed flawed analysis** - analysis-flowspec.md suggests consolidation, but that defeats the purpose (same as spec-kit)
3. ❌ **Removed functionality** - Didn't include /flow:submit-n-review-pr which is CRITICAL
4. ❌ **Ignored rigor rules** - No logging, ADRs, or constitution enforcement
5. ❌ **Wrong integration** - Used bash scripts instead of MCP
6. ❌ **Security vulnerabilities** - bash eval(), curl pipes
7. ❌ **Skipped validation** - Didn't run CI/CD checks before PR

**The fundamental mistake:** I tried to REPLACE the 8 commands with 3 hardcoded ones. That's the OPPOSITE of what "flexible orchestration" means.

## What the Requirements Actually Say

### Core Mission (from flowspec-loop.md)

**Vibe OR Spec mode - MUST always:**
- Log key events, decisions, actions
- Make spec + workflow system flexible (user changes it)
- This is for Inner Loop but be aware of Inner & Outer Loop

### Inner Loop vs Outer Loop

**Inner Loop (THIS IS FLOWSPEC):**
- `/flow:specify` → Spec (PM Planner)
- `/flow:plan` → Arch Docs (Architect, Platform Eng)
- `/flow:implement` → Working solution (Frontend/Backend Engineers)
- `/flow:validate` → Merged (QA, Security Engineers)

**Outer Loop (NOT flowspec - falcondev handles):**
- Promote → deployed
- Observe → Running
- Operate → Running
- Feedback → into inner loop

### REQUIRED (Always Present - Never Optional)

**1. LOGGING:**
- Log decisions to `.logs/decisions/*.jsonl`
- Log events to `.logs/events/*.jsonl`
- Outputs of steps produce artifacts

**2. BACKLOG SYSTEM:**
- Keep backlog.md/beads up to date and accurate throughout process

**3. MEMORY SYSTEM:**
- Task memory system
- Track and save task state
- Keep agent aware of losing focus (across sessions, across time)

**4. CRITICAL AD HOC COMMANDS:**
These are disconnected from workflows but critical:
- `/flow:submit-n-watch-pr` - Get feedback from other agents (Copilot, etc.), iterate til good
- `/flow:timed-task` - Given rules, time, branch → produce outcome
- `/flow:refactor` - Full complete refactor loop

### FLEXIBLE (User Can Edit via falcondev/workflow-editor)

Must be easy to customize, can't over-scrutinize at CI/CD time:
- Agents
- Prompts
- Flowspec workflows
- Constitution
- Skills
- Custom workflow sequences

### From objective.md

- **"let users completely customize their flow steps"** - Users define sequences
- **"with the workflow editor in falcondev"** - Must be editable via UI/YAML
- **"simply be the glue that loosely binds the steps"** - Orchestration layer
- **"vibing"** - Autonomous execution with full logging, no interaction
- **"spec-ing"** - Stop for guidance at configurable checkpoints

### From feedback.md

- Different from spec-kit = flexible orchestration + rigor rules + multi-tool support
- NOT hardcoded simplification

## What Actually Needs to Happen

### Core Principle
**Keep ALL existing workflows working independently. Add flexible orchestration layer on TOP.**

### Inner Loop Workflows (Core Flowspec)

**Primary workflows (always available):**
1. `/flow:specify` - Requirements specification → Spec (PM Planner)
2. `/flow:plan` - Technical design → Arch Docs (Architect, Platform Eng)
3. `/flow:implement` - Code generation → Working solution (Frontend/Backend Engineers)
4. `/flow:validate` - QA/security checks → Merged (QA, Security Engineers)

**Supporting workflows:**
5. `/flow:assess` - Complexity scoring (optional, informational)
6. `/flow:research` - Deep research (optional, for complex features)
7. `/flow:operate` - Deployment and operational readiness

**Critical ad hoc commands (disconnected but essential):**
8. `/flow:submit-n-watch-pr` - PR submission, monitor CI/CD, iterate with agent feedback til good
9. `/flow:timed-task` - Given rules, time, branch → produce outcome
10. `/flow:refactor` - Full complete refactor loop

**ALL of these must:**
- Continue working independently
- Be usable in custom workflow sequences
- Integrate with backlog.md/beads
- Use memory system
- Log decisions and events
- Follow constitution

### What Gets Added: User-Customizable Orchestration

Users define their own workflow sequences in `flowspec_workflow.yml`:

```yaml
# Example: User wants lightweight design for simple features
custom_workflows:
  quick_design:
    name: "Quick Design"
    mode: "vibing"  # autonomous, no stops
    steps:
      - workflow: assess
      - workflow: specify
      - workflow: plan
        condition: "complexity >= 5"  # skip if too simple
    rigor:
      log_decisions: true
      log_events: true
      create_adrs: true
      follow_constitution: true

  # Example: User wants full research with checkpoints
  full_research:
    name: "Full Research"
    mode: "spec-ing"  # stop for approvals
    steps:
      - workflow: assess
      - workflow: specify
        checkpoint: "Review PRD before continuing?"
      - workflow: research
      - workflow: plan
        checkpoint: "Review architecture before implementing?"
    rigor:
      log_decisions: true
      log_events: true
      create_adrs: true
      follow_constitution: true

  # Example: User wants build + ship in one go
  build_and_ship:
    name: "Build and Ship"
    mode: "vibing"
    steps:
      - workflow: implement
      - workflow: validate
      - workflow: submit-n-review-pr
    rigor:
      log_decisions: true
      log_events: true
      create_adrs: true
      follow_constitution: true
```

### Key Capabilities

**User Control:**
- Define any sequence of the 8 workflows
- Name their custom workflows
- Set conditions for skipping steps (based on complexity, context, etc.)
- Choose vibing (autonomous) or spec-ing (approval checkpoints)
- Edit via YAML or falcondev workflow editor UI

**Rigor Enforcement (NO EXCEPTIONS):**
Every workflow (existing and custom) MUST:
- Log decisions to `.logs/decisions/*.jsonl`
- Log events to `.logs/events/*.jsonl`
- Create ADRs for architectural decisions
- Follow constitution from `.specify/memory/constitution.md`
- Stay in branch
- Stay on task

**MCP Integration (NOT bash):**
All backlog operations use MCP tools:
```python
from flowspec_cli.backlog.shim import task_view, task_edit

# View task state
task_data = task_view(task_id, plain=True)
current_state = parse_state_from_output(task_data)

# Update task state
task_edit(task_id=task_id, status="Validated", workspace_root=workspace_root)
```

NO bash scripts like:
```bash
# WRONG - security vulnerability
backlog task "$TASK_ID" --plain
```

**Security:**
- Remove ALL eval() usage
- Remove ALL curl | bash patterns
- Sanitize all inputs
- Use subprocess with proper escaping

**CI/CD:**
- Run all checks locally BEFORE PR
- Use `/flow:submit-n-review-pr` to monitor checks
- Fix ALL failing checks before requesting review
- validate-agent-sync MUST pass
- auto-fix-drift MUST pass
- Semgrep MUST pass (no HIGH+ findings)

### Implementation Steps

**Step 1: Add orchestration engine**
- Create `src/flowspec_cli/workflow/orchestrator.py`
- Reads custom workflow definitions from `flowspec_workflow.yml`
- Executes workflows in sequence
- Handles conditional logic
- Supports checkpoints for spec-ing mode
- Enforces rigor rules on every step

**Step 2: Extend schema**
- Update `schemas/flowspec_workflow.schema.json`
- Add `custom_workflows` section
- Support conditions, checkpoints, modes

**Step 3: MCP migration**
- Replace ALL bash backlog calls with MCP tools
- In ALL 8 existing workflows
- In orchestrator
- Add proper error handling

**Step 4: Rigor enforcement**
- Add decision logging to ALL workflows
- Add event emission to ALL workflows
- Add ADR creation hooks
- Add constitution validation

**Step 5: Security fixes**
- Remove ALL eval()
- Remove ALL curl | bash
- Sanitize inputs everywhere

**Step 6: Validation**
- Run ALL CI/CD checks locally
- Use `/flow:submit-n-review-pr` for PR
- Fix ALL failing checks
- Only then request review

## Success Criteria

**REQUIRED Systems (Always Present):**
✅ Logging system intact - decisions/events to `.logs/`
✅ Backlog system intact - backlog.md/beads up to date
✅ Memory system intact - task memory across sessions
✅ Critical ad hoc commands intact - submit-n-watch-pr, timed-task, refactor

**Inner Loop Workflows:**
✅ All 10 workflows work independently (unchanged)
✅ Primary: specify, plan, implement, validate
✅ Supporting: assess, research, operate
✅ Critical ad hoc: submit-n-watch-pr, timed-task, refactor

**Flexible Orchestration:**
✅ Users can define custom sequences in YAML
✅ Supports vibing (autonomous) and spec-ing (checkpoints) modes
✅ Editable via falcondev workflow editor
✅ Agents, prompts, workflows, constitution, skills all customizable

**Rigor Enforcement:**
✅ Rigor rules enforced everywhere (no exceptions)
✅ All workflows log decisions and events
✅ All workflows integrate with backlog/beads
✅ All workflows use memory system
✅ All workflows follow constitution

**Security & Integration:**
✅ MCP used for all backlog integration (no bash)
✅ Zero security vulnerabilities (no eval, no curl pipes)
✅ All CI/CD checks pass
✅ Works across Claude Code, Copilot, Cursor, Gemini

## What Makes This Different from spec-kit

- **spec-kit**: Fixed workflow, not customizable
- **flowspec**: Users define their own workflow sequences via YAML
- **spec-kit**: No rigor enforcement
- **flowspec**: Mandatory logging, ADRs, constitution
- **spec-kit**: Single tool
- **flowspec**: Works across multiple AI tools

## What NOT to Do (Lessons Learned)

❌ **DON'T** replace workflows with hardcoded sequences
❌ **DON'T** remove any existing workflows (especially critical ad hoc ones)
❌ **DON'T** skip rigor enforcement (logging, ADRs, constitution)
❌ **DON'T** use bash for backlog integration (use MCP)
❌ **DON'T** introduce security vulnerabilities (eval, curl pipes)
❌ **DON'T** skip CI/CD validation before PR
❌ **DON'T** assume workflows are flexible if they're hardcoded
❌ **DON'T** forget memory system, backlog system, or logging system
❌ **DON'T** over-scrutinize user-editable prompts/agents/skills at CI/CD time

## Ready to Execute

This approach covers:
- ✅ Core mission (flexible workflows + always log in vibe/spec modes)
- ✅ Inner vs Outer Loop distinction
- ✅ REQUIRED systems (logging, backlog, memory, critical commands)
- ✅ FLEXIBLE components (agents, prompts, workflows, constitution, skills)
- ✅ All 10 workflows intact
- ✅ User-customizable orchestration
- ✅ Vibing and spec-ing modes
- ✅ MCP integration
- ✅ Security fixes
- ✅ CI/CD compliance

Awaiting your approval to proceed with implementation.
