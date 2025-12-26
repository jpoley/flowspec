# Failure Learnings

This document tracks significant implementation failures and the lessons learned. Each failure is documented to prevent repeating the same mistakes.

---

## Failure #1: Hardcoded Meta-Workflows (December 2024)

### What I Got Completely Wrong

1. ❌ **Misunderstood the objective** - Created hardcoded "Research/Build/Run" meta-workflows instead of USER-CUSTOMIZABLE orchestration
2. ❌ **Followed flawed analysis** - analysis-flowspec.md suggests consolidation, but that defeats the purpose (same as spec-kit)
3. ❌ **Removed functionality** - Didn't include /flow:submit-n-review-pr which is CRITICAL
4. ❌ **Ignored rigor rules** - No logging, ADRs, or constitution enforcement
5. ❌ **Wrong integration** - Used bash scripts instead of MCP
6. ❌ **Security vulnerabilities** - bash eval(), curl pipes
7. ❌ **Skipped validation** - Didn't run CI/CD checks before PR

### The Fundamental Mistake

I tried to REPLACE the commands with 3 hardcoded ones. That's the OPPOSITE of what "flexible orchestration" means.

### What I Should Have Done

1. **Read flowspec-loop.md FIRST** - It defines the core mission: 4 commands ARE flowspec
2. **Understood Inner vs Outer Loop** - Flowspec = Inner Loop ONLY (Outer Loop = falcondev)
3. **Recognized "glue" means orchestration** - NOT hardcoded workflows, but flexible user-defined sequences
4. **Preserved ALL commands** - Add orchestration ON TOP, don't replace
5. **Enforced rigor rules** - Logging, ADRs, constitution from day one
6. **Used MCP** - Not bash scripts for backlog integration
7. **Fixed security** - No eval(), no curl pipes
8. **Validated before PR** - Run all CI/CD checks locally first

### Key Lessons

**Mission-Critical Documents:**
- flowspec-loop.md defines THE MISSION (4 core commands)
- Inner/Outer Loop distinction is fundamental
- "Glue that loosely binds" = orchestration layer, NOT consolidation

**Architecture Principles:**
- Never remove existing functionality
- Add layers ON TOP, don't replace
- User customization ≠ hardcoded simplification
- Flexible = user-editable, not fewer options

**Process Requirements:**
- Always use MCP for backlog (never bash)
- Always enforce rigor rules (logging, ADRs, constitution)
- Always validate with CI/CD before PR
- Always check security (no eval, no curl pipes)

---

## Failure #2: Created Bad Meta-Workflow Files (December 2024)

### What I Got Completely Wrong

1. ❌ **Created hardcoded meta-workflow files** - Added `meta-build.md`, `meta-research.md`, `meta-run.md` command files
2. ❌ **Built wrong orchestrator** - Implemented `meta_orchestrator.py` that hardcodes sequences instead of reading user-defined configs
3. ❌ **Misread the objective** - "Glue that loosely binds" means USER-CUSTOMIZABLE sequences, NOT hardcoded 3-command replacement
4. ❌ **Ignored flowspec-loop.md** - The document clearly states the 4 core commands ARE the mission
5. ❌ **Confused consolidation with orchestration** - Tried to REPLACE commands instead of adding a layer ON TOP
6. ❌ **Didn't follow flexibility model** - Users should customize via YAML, not be forced into 3 rigid workflows

### The Meta-Workflow Files Were Wrong Because

**What they did:**
- `/flow:meta-research` - Hardcoded sequence: assess → specify → research → plan
- `/flow:meta-build` - Hardcoded sequence: implement → validate
- `/flow:meta-run` - Hardcoded sequence: operate (which is outer loop!)

**Why this was wrong:**
- These are FIXED sequences that users can't customize
- They REPLACE the individual commands instead of orchestrating them
- They reduce flexibility instead of increasing it
- They're the SAME as spec-kit (hardcoded workflow), which defeats the purpose

### What I Should Have Done

**Instead of meta-workflow command files, should have:**
1. Extended `flowspec_workflow.yml` schema with `custom_workflows` section
2. Let users define their OWN sequences like:
   ```yaml
   custom_workflows:
     my_quick_flow:
       steps:
         - workflow: specify
         - workflow: implement
         - workflow: validate
   ```
3. Built an orchestrator that READS user configs, not hardcodes sequences
4. Kept ALL individual commands working independently

**The orchestrator should:**
- Read `custom_workflows` from `flowspec_workflow.yml`
- Execute user-defined sequences
- Support conditional logic (skip if complexity < 5, etc.)
- Support checkpoints for approval (vibing vs spec-ing modes)
- Enforce rigor rules on every step

### Files That Were Wrong and Must Be Deleted

From this branch (`simplify-flowspec-muckross`):
- `.claude/commands/flow/meta-build.md` - DELETE
- `.claude/commands/flow/meta-research.md` - DELETE
- `.claude/commands/flow/meta-run.md` - DELETE
- `src/flowspec_cli/workflow/meta_orchestrator.py` - DELETE (replace with correct implementation)

### Key Lessons

**Flexibility Principle:**
- Flexibility = users define sequences, NOT fewer hardcoded options
- "Glue that loosely binds" = orchestration layer, NOT command consolidation
- Adding 3 rigid workflows is the OPPOSITE of making it more flexible

**Architecture Approach:**
- Add layers ON TOP of existing functionality
- Never replace working features
- Let users compose workflows via configuration
- Build engines that read user intent, not hardcode it

**Reading Requirements:**
- ALWAYS read flowspec-loop.md FIRST - it defines the mission
- "4 core commands ARE flowspec" means they're non-negotiable
- "Flexible orchestration" ≠ "hardcoded meta-commands"

---

*Add new failures below with incrementing numbers and clear lessons learned.*
