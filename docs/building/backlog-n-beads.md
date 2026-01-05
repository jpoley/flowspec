# Backlog + Beads Integration Design

> **Status**: Design Proposal
> **Date**: 2026-01-05
> **Author**: Analysis session

## Executive Summary

This document analyzes whether and how to integrate Backlog.md (human-facing task management) with Beads (AI-native issue tracker), evaluates complexity vs. value, and proposes a phased implementation approach.

**Key Findings**:
- The systems are **complementary, not competing**, when used as a vertical stack
- Integration adds value for **complex, multi-session agent work**
- Recommended approach: **Convention-first, automate incrementally**
- Decision/event logging should remain in `.logs/`, with rollup summarization

---

## Table of Contents

1. [System Comparison](#system-comparison)
2. [The Vertical Integration Model](#the-vertical-integration-model)
3. [Complexity vs Value Analysis](#complexity-vs-value-analysis)
4. [Deterministic Sync Design](#deterministic-sync-design)
5. [Linking Schema](#linking-schema)
6. [Decision & Event Integration](#decision--event-integration)
7. [Competition vs Complementary Analysis](#competition-vs-complementary-analysis)
8. [Phased Implementation Approach](#phased-implementation-approach)
9. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
10. [Decision Matrix](#decision-matrix)

---

## System Comparison

### Backlog.md

**Purpose**: Human-facing task management with acceptance criteria tracking.

| Aspect | Details |
|--------|---------|
| **Storage** | Markdown files with YAML frontmatter (`backlog/tasks/task-*.md`) |
| **Interface** | CLI, Web UI (Kanban board), MCP server for AI assistants |
| **Strengths** | Human-readable, acceptance criteria, milestones, visual boards |
| **Weaknesses** | Basic dependencies, no agent session tracking, no blocking relationships |

**Key Fields**: `id`, `title`, `status`, `priority`, `labels`, `assignee`, `dependencies`, `acceptance_criteria`, `implementation_notes`

**Status Flow**: `To Do → Assessed → Specified → Planned → In Progress → In Implementation → Validated → Done`

### Beads

**Purpose**: AI-native issue tracker with dependency graphs and agent forensics.

| Aspect | Details |
|--------|---------|
| **Storage** | SQLite (local) + JSONL (git-tracked) in `.beads/` |
| **Interface** | CLI (`bd` command), no web UI |
| **Strengths** | Dependencies, blocking, agent sessions, molecules (templates), smart git merge |
| **Weaknesses** | CLI-only, no MCP server, no visual boards |

**Key Fields**: `id`, `title`, `description`, `status`, `priority` (0-4), `type`, `assignee`, `labels`, `external_ref`, `parent_id`, `session`

**Status Flow**: `open → in_progress → blocked/deferred → closed`

### Side-by-Side Capability Matrix

| Capability | Backlog.md | Beads |
|------------|-----------|-------|
| Human-readable board | ✅ Strong | ❌ CLI only |
| MCP server for AI | ✅ Yes | ❌ No |
| Acceptance criteria | ✅ First-class | ❌ Text only |
| Dependency graphs | ⚠️ Basic | ✅ First-class |
| Blocking relationships | ❌ No | ✅ First-class |
| Agent session tracking | ❌ No | ✅ Built-in |
| Workflow templates | ❌ No | ✅ Molecules |
| Cross-repo references | ❌ No | ✅ External refs |
| Milestone tracking | ✅ Yes | ❌ No |
| Web UI | ✅ Yes | ❌ No |
| Git conflict resolution | ⚠️ Manual | ✅ Smart merge |

---

## The Vertical Integration Model

When properly integrated, Backlog and Beads form a **vertical stack**, not competing systems:

```
┌─────────────────────────────────────────────────────┐
│                    HUMAN LAYER                       │
│  Backlog.md: WHAT needs to be done                  │
│  - Task definitions and intent                       │
│  - Acceptance criteria (definition of done)          │
│  - Milestones and deadlines                          │
│  - Human-visible status for stakeholders             │
└─────────────────────┬───────────────────────────────┘
                      │ Decomposes Into
                      ▼
┌─────────────────────────────────────────────────────┐
│                    AGENT LAYER                       │
│  Beads: HOW work gets done                          │
│  - Execution subtasks and dependencies               │
│  - Blocking relationships and ordering               │
│  - Agent session tracking and forensics              │
│  - Cross-session state persistence                   │
└─────────────────────┬───────────────────────────────┘
                      │ Captures
                      ▼
┌─────────────────────────────────────────────────────┐
│                    AUDIT LAYER                       │
│  .logs/: WHY and WHEN decisions were made           │
│  - Decision logs with rationale                      │
│  - Event streams for debugging                       │
│  - Session transcripts                               │
│  - Error traces                                      │
└─────────────────────────────────────────────────────┘
```

### Information Flow

```
Human creates Backlog task
         │
         ▼
Agent decomposes into Beads issues (complex work only)
         │
         ▼
Agent executes, logging decisions to .logs/
         │
         ▼
Beads issues closed, notes rolled up to Backlog
         │
         ▼
Backlog task marked complete with summary
```

---

## Complexity vs Value Analysis

### Complexity Costs

| Cost | Description | Mitigation |
|------|-------------|------------|
| **Two systems to learn** | Users must understand both tools | Clear decision framework |
| **Sync failures** | Systems can drift out of sync | Manual sync, graceful degradation |
| **Cognitive overhead** | Deciding which system to use | Simple rules based on task complexity |
| **More failure modes** | Additional tooling in critical path | Either system works standalone |
| **Merge conflicts** | Git conflicts in both formats | Beads has smart merge; backlog is per-file |

### Value Matrix by Scenario

| Scenario | Value of Integration | Recommendation |
|----------|---------------------|----------------|
| Simple, single-session task | ❌ Low | Backlog only |
| Complex multi-session work | ✅ High | Backlog + Beads |
| Multiple agents, shared work | ✅ Very High | Backlog + Beads |
| Audit/compliance requirements | ✅ High | Full stack |
| Solo developer, quick fix | ❌ Low | Backlog only |
| Vibe mode exploration | ❌ None | .logs/ only |
| Feature with many subtasks | ✅ High | Backlog + Beads |
| Bug fix with known solution | ❌ Low | Backlog only |

### Cost-Benefit Summary

| Approach | Complexity | Value | Net Benefit |
|----------|------------|-------|-------------|
| Backlog only | Low | Medium | ✅ Good default |
| Beads only | Medium | Medium | ⚠️ Missing human interface |
| **Backlog + Beads (layered)** | Medium-High | **High** | ✅ **Best for complex work** |
| Full automation | Very High | High | ⚠️ Fragile, over-engineered |

---

## Deterministic Sync Design

For sync to be "deterministic" (predictable, reliable), we need clear ownership and triggers.

### Source of Truth by Data Type

| Data Type | Source of Truth | Syncs To |
|-----------|----------------|----------|
| Task intent/definition | **Backlog** | Read by beads for context |
| Acceptance criteria | **Backlog** | Referenced (not copied) in beads |
| High-level status | **Backlog** | Computed from beads aggregate |
| Execution subtasks | **Beads** | Summarized in backlog notes |
| Dependencies/blocking | **Beads** | Not synced (beads-only) |
| Agent decisions | **.logs/** | Summarized in rollup |
| Session tracking | **Beads** | Referenced in rollup |

### Sync Triggers

| Trigger Event | Sync Action |
|---------------|-------------|
| Backlog task → "In Progress" | Suggest creating beads scaffold |
| Beads issue closed | Append completion note to backlog |
| All beads for task closed | Suggest backlog task completion |
| Backlog task → "Done" | Archive associated beads issues |
| Decision logged for task | Include in next rollup |

### Sync Commands

```bash
# Link a beads issue to a backlog task
bd create "[task-42] Subtask" --external-ref=backlog:task-42

# Query beads for a backlog task
bd list --search="[task-42]"

# Manual rollup to backlog
backlog task edit task-42 --notes-append "Completed beads: bd-001, bd-002"

# Helper scripts (Phase 2)
backlog-beads link task-42 bd-001      # Add bidirectional reference
backlog-beads scaffold task-42          # Create beads from acceptance criteria
backlog-beads rollup task-42            # Summarize beads work → backlog notes
backlog-beads status task-42            # Show linked beads and their status
```

---

## Linking Schema

### Beads → Backlog Reference

Use the `external_ref` field:

```bash
bd create "Implement login endpoint" \
  --external-ref=backlog:task-42 \
  --type=task \
  --priority=2
```

The external_ref format: `backlog:<task-id>`

### Backlog → Beads Reference

Add a section to backlog task implementation notes:

```markdown
## Implementation Details

### Beads Tracking
This task is tracked in beads for detailed execution:
- `bd-001` - JWT token service (closed)
- `bd-002` - Login endpoint (in_progress)
- `bd-003` - Session persistence (open)

Status: 1/3 complete
```

### Title Convention

For easy filtering, prefix beads titles with the backlog task ID:

```bash
bd create "[task-42] JWT token service" --external-ref=backlog:task-42
bd create "[task-42] Login endpoint" --external-ref=backlog:task-42
```

Query all beads for a task:
```bash
bd list --search="\[task-42\]"
```

---

## Decision & Event Integration

### Current State

- **Decisions**: Logged to `.logs/decisions/YYYY-MM-DD.jsonl`
- **Events**: Logged to `.logs/events/YYYY-MM-DD.jsonl`
- **Beads**: Has `type: event` for workflow events (gates, milestones)

### Integration Options Evaluated

| Option | Description | Verdict |
|--------|-------------|---------|
| **A: Keep separate** | .logs/ for logging, beads for work | ❌ Decisions fragmented |
| **B: Mirror to beads** | Promote significant decisions to beads issues | ⚠️ Duplication, judgment required |
| **C: Beads as primary** | Log all decisions as beads issues | ❌ Beads becomes bloated |
| **D: Hybrid rollup** | .logs/ primary, summarize in beads/backlog | ✅ **Recommended** |

### Recommended Approach: Hybrid Rollup

1. **Continue using .logs/** for all decisions and events (low friction, append-only)
2. **Tag decisions with task ID** in the decision log:
   ```json
   {
     "timestamp": "2026-01-05T10:30:00Z",
     "task_id": "task-42",
     "phase": "execution",
     "decision": "Use JWT with 24h expiry",
     "rationale": "Balance security with UX",
     "actor": "claude-agent"
   }
   ```
3. **Summarize in beads notes** when work is significant:
   ```bash
   bd update bd-001 --notes-append "Decision: Using JWT with 24h expiry (see .logs/)"
   ```
4. **Include in backlog rollup** when task completes:
   ```markdown
   ## Key Decisions
   - JWT with 24h expiry for session management
   - bcrypt for password hashing (cost factor 12)
   ```

This preserves .logs/ simplicity while enabling decision correlation.

---

## Competition vs Complementary Analysis

### Where They Compete (Overlap)

| Area | Backlog | Beads | Resolution |
|------|---------|-------|------------|
| Task status | ✅ Tracks status | ✅ Tracks status | **Backlog wins** (human-visible) |
| Notes/description | ✅ Has notes | ✅ Has notes | **Beads for details**, rollup to backlog |
| Labels/tags | ✅ Supports labels | ✅ Supports labels | Use both independently |
| Timestamps | ✅ created/updated | ✅ created/updated | Both valid for their scope |

### Where They Complement (Unique Strengths)

| Backlog Unique | Beads Unique |
|----------------|--------------|
| Human-readable Kanban | Dependency graphs |
| MCP server for AI | Agent session tracking |
| Acceptance criteria checkboxes | Blocking relationships |
| Milestone tracking | Workflow templates (molecules) |
| Web UI | Cross-repo references |
| Stakeholder visibility | Smart git merge |

### The Complementary Sweet Spot

```
┌────────────────────────────────────────────────┐
│              Backlog.md Territory              │
│  - Task creation and intent                    │
│  - Acceptance criteria definition              │
│  - Status visible to stakeholders              │
│  - Milestone and deadline tracking             │
│  - Simple tasks (no decomposition needed)      │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│               Beads Territory                  │
│  - Execution subtasks for complex work         │
│  - Dependency ordering between subtasks        │
│  - Agent session correlation                   │
│  - Multi-session state persistence             │
│  - Cross-agent coordination                    │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│               .logs/ Territory                 │
│  - Decision audit trail                        │
│  - Event stream for debugging                  │
│  - Session-scoped context                      │
│  - Ephemeral, low-friction capture             │
└────────────────────────────────────────────────┘
```

---

## Phased Implementation Approach

### Phase 1: Convention + Manual Sync (Recommended Start)

**Complexity**: Low
**Implementation**: Documentation only, no code changes

**What to do**:
1. Document the linking convention (`[task-XX]` prefix, `external_ref`)
2. Document the rollup workflow (manual notes update)
3. Update `docs/guides/task-management-tiers.md` with examples
4. Train agents on conventions via CLAUDE.md

**Workflow**:
```bash
# Starting complex work
backlog task edit task-42 -s "In Progress"
bd create "[task-42] First subtask" --external-ref=backlog:task-42 --priority=2
bd create "[task-42] Second subtask" --external-ref=backlog:task-42 --priority=2
bd dep add bd-002 bd-001

# Working
bd ready
bd update bd-001 --status=in_progress
# ... work ...
bd close bd-001

# Completing
bd close bd-002
backlog task edit task-42 --notes-append "Completed: bd-001 (JWT), bd-002 (Login)"
backlog task edit task-42 -s "Done"
```

**Exit Criteria**: Use this for 2-4 weeks, assess friction points.

### Phase 2: Helper Scripts (If Phase 1 Proves Useful)

**Complexity**: Medium
**Implementation**: Shell scripts or Python utilities

**Scripts to create**:

```bash
# scripts/bash/backlog-beads.sh

backlog-beads link <task-id> <bead-id>
# Adds external_ref to bead, adds reference to backlog notes

backlog-beads scaffold <task-id>
# Reads backlog task ACs, creates beads issues for each
# Example: AC "User can login" → bd create "[task-42] User can login"

backlog-beads rollup <task-id>
# Queries all beads with external_ref, generates summary for backlog notes
# Includes: bead IDs, titles, status, completion date

backlog-beads status <task-id>
# Shows linked beads with current status
# Output: 2/5 complete, 1 blocked, 2 open
```

**Exit Criteria**: Use for 2-4 weeks, assess if hooks would reduce friction.

### Phase 3: Hook Integration (If Automation Needed)

**Complexity**: High
**Implementation**: Claude Code hooks in `.claude/hooks/`

**Hooks to consider**:

```yaml
# .claude/hooks/hooks.yaml
hooks:
  - event: task.status_changed
    conditions:
      new_status: "In Progress"
      labels_contain: "complex"
    action: scripts/suggest-beads-scaffold.sh
    type: prompt  # Suggests, doesn't auto-execute

  - event: beads.all_closed
    conditions:
      external_ref_pattern: "backlog:task-*"
    action: scripts/suggest-backlog-complete.sh
    type: prompt
```

**Exit Criteria**: Stable hooks, assess if MCP integration would help.

### Phase 4: MCP Integration (For Heavy Use)

**Complexity**: Very High
**Implementation**: Extend backlog MCP server

**New MCP tools**:
```python
# Added to backlog MCP server
backlog_beads_link(task_id: str, bead_ids: list[str])
backlog_beads_scaffold(task_id: str) -> list[str]  # Returns created bead IDs
backlog_beads_rollup(task_id: str) -> str  # Returns rollup summary
backlog_beads_status(task_id: str) -> dict  # Returns linked beads status
```

**Only implement if**:
- Teams are using the integration daily
- Manual/script approach causes significant friction
- Need programmatic access from AI agents via MCP

---

## Anti-Patterns to Avoid

### 1. Beads for Every Task
❌ **Don't**: Create beads issues for every backlog task
✅ **Do**: Only use beads for complex, multi-session work

### 2. Automated Status Sync
❌ **Don't**: Auto-sync status between systems (fragile, surprising)
✅ **Do**: Let humans/agents update each system appropriately

### 3. Duplicating Acceptance Criteria
❌ **Don't**: Copy ACs from backlog to beads issues
✅ **Do**: Reference the backlog task, keep ACs in one place

### 4. Over-Engineering Automation
❌ **Don't**: Build complex sync infrastructure before validating need
✅ **Do**: Start with conventions, add automation only when friction is proven

### 5. Forcing Beads on Simple Work
❌ **Don't**: Require beads decomposition for bug fixes or simple features
✅ **Do**: Use judgment - most work is simple enough for backlog alone

### 6. Ignoring Graceful Degradation
❌ **Don't**: Make the workflow fail if beads isn't available
✅ **Do**: Ensure either system works standalone (degraded but functional)

---

## Decision Matrix

### When to Use Which System

```
                         ┌─────────────────────────┐
                         │    Is this work         │
                         │    tracked in backlog?  │
                         └───────────┬─────────────┘
                                     │
                        ┌────────────┴────────────┐
                        │                         │
                        ▼                         ▼
                       YES                        NO
                        │                         │
                        ▼                         ▼
              ┌─────────────────┐       ┌─────────────────┐
              │  Is it complex  │       │  Create backlog │
              │  (multi-session,│       │  task first,    │
              │  dependencies)? │       │  then re-assess │
              └────────┬────────┘       └─────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
         YES                        NO
          │                         │
          ▼                         ▼
┌─────────────────────┐   ┌─────────────────────┐
│  Use Backlog +      │   │  Use Backlog only   │
│  Beads (two-tier)   │   │  Track in notes     │
│                     │   │                     │
│  - Create beads     │   │  - Work directly    │
│    with [task-XX]   │   │  - Log decisions    │
│  - Set dependencies │   │  - Update notes     │
│  - Roll up when     │   │  - Mark complete    │
│    complete         │   │                     │
└─────────────────────┘   └─────────────────────┘
```

### Quick Reference Table

| Situation | Use |
|-----------|-----|
| Quick bug fix | Backlog only |
| Single-session feature | Backlog only |
| Multi-session complex work | Backlog + Beads |
| Work with dependencies | Backlog + Beads |
| Multiple agents collaborating | Backlog + Beads |
| Vibe mode exploration | .logs/ only |
| Needs audit trail | Full stack |
| Stakeholder visibility needed | Backlog (source of truth for status) |

---

## Summary

### Key Takeaways

1. **Backlog and Beads are complementary**, not competing, when used as layers
2. **Start with conventions** (Phase 1) before building automation
3. **Beads adds value for complex work** but is overhead for simple tasks
4. **Decision logging stays in .logs/**, with rollup summarization to backlog
5. **Either system should work standalone** (graceful degradation)
6. **Automate incrementally** based on proven friction

### Recommended Next Steps

1. **Immediate**: Update `docs/guides/task-management-tiers.md` with linking conventions
2. **Short-term**: Create `scripts/bash/backlog-beads.sh` helper script
3. **Medium-term**: Evaluate hook integration based on usage patterns
4. **Long-term**: Consider MCP integration only if heavy team usage

### Success Metrics

- **Adoption**: Complex tasks consistently use two-tier approach
- **Friction**: Sync workflow takes < 2 minutes
- **Visibility**: Backlog status accurately reflects beads progress
- **Audit**: Decisions can be traced from backlog → beads → .logs/

---

*Document created as design proposal. Implementation should follow phased approach with validation at each stage.*
