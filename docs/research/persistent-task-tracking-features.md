# Persistent Task Tracking for AI Agents — Feature Analysis

> Features and patterns observed in a mature, open-source AI-agent task coordination system. Documented as standalone capabilities for potential adoption in flowspec's multi-agent orchestration layer.

---

## 1. Structured Task Artifacts (Not Just Todos)

Every task is a three-part artifact rather than a simple checkbox:

| Field | Purpose | Analogy |
|-------|---------|---------|
| **Name** | One-line summary | Issue title |
| **Description** | Full context: requirements, approach, acceptance criteria | Issue body |
| **Result** | What was actually done, decisions made, outcomes | PR description |

**Why it matters:** The `result` field is the key differentiator. When an agent completes work, it records *how* and *why* — not just that it's done. This creates an audit trail and enables handoffs between agents or to humans without context loss.

---

## 2. Three-Tier Hierarchy with Dependency Graphs

Tasks organize into three tiers:

```
Epic (5+ tasks)
  └── Task (3–7 subtasks)
        └── Subtask (atomic step)
```

Combined with a **blocking dependency system**:

- `blockedBy[]` / `blocks[]` — bidirectional enforcement
- **Cycle detection** prevents circular dependencies at write time
- **Ready state calculation** — automatically identifies tasks with zero unresolved blockers

**Why it matters:** Agents can autonomously pick the next unblocked task without human triage. The cycle detection is a subtle but critical safety feature — without it, agents could deadlock themselves.

---

## 3. Merge-Aware Issue Closure

Integration with issue trackers uses an intelligent closure rule:

```
Issue closes ONLY when:
  1. Task is marked completed  AND
  2. Associated commit SHA exists on the default branch (i.e., merged)
```

This prevents the classic problem of issues closing when a branch is pushed but before the PR is reviewed and merged. Closure is deferred via a post-push hook.

**Why it matters:** In multi-agent workflows where agents produce PRs, premature issue closure creates false confidence. This pattern ensures issues track *delivered* work, not *attempted* work.

---

## 4. Commit-Linked Completion Verification

Leaf tasks require explicit linkage to a commit SHA when completing:

```
complete <task> --commit <sha>     # Link to specific commit
complete <task> --no-commit        # Explicitly opt out
```

Parent tasks close automatically only when all descendant tasks have verified commits.

**Why it matters:** This creates a verifiable chain: task → commit → merged branch. For a skills marketplace, this enables automated verification that a skill actually produced working code, not just claimed to.

---

## 5. JSONL Storage — Git-Native by Design

Tasks are stored as JSON Lines (one task per line) rather than individual files or a database:

- **Atomic writes** via temp-file + rename (no corruption on crash)
- **Minimal diffs** — changing one task changes one line in version control
- **Merge-conflict-friendly** — independent lines rarely conflict
- **Auto-migration** from legacy formats

**Why it matters:** Task state becomes part of the git history. PRs can include task changes alongside code changes. Reviewers see what was planned, what changed, and what was delivered — all in the same diff.

---

## 6. Archive with Compaction

Completed tasks graduate to an archive system:

| Setting | Default | Purpose |
|---------|---------|---------|
| `age_days` | 90 | Archive tasks older than N days |
| `keep_recent` | 50 | Always keep N most recent completed tasks |
| `auto` | false | Auto-archive on every write |

Archived tasks are **compacted** — transient fields (blockedBy, blocks, children, priorities) are stripped, preserving only the permanent record: id, name, description, result, and integration metadata.

**Why it matters:** Active task lists stay focused. Historical context is preserved for auditing. The compaction step is thoughtful — it removes the fields that only matter during active work.

---

## 7. MCP Server with Minimal Tool Surface

The entire API surface is just **3 MCP tools**:

| Tool | Purpose |
|------|---------|
| `create_task` | Create with name, description, parent, priority, blockers |
| `update_task` | Modify any field, complete, delete |
| `list_tasks` | Filter by status, query, blocking state, archive |

All responses follow a consistent JSON envelope:
```json
{
  "success": true,
  "taskId": "abc123",
  "data": { ... },
  "error": null
}
```

**Why it matters:** A 3-tool surface is trivially adoptable by any AI agent. Contrast with systems that expose 15+ tools — agents waste context window tokens on tool descriptions. The design proves you can model complex workflows with minimal API surface by composing filters and updates.

---

## 8. Bidirectional External Sync with Conflict Strategy

Syncs with GitHub Issues and Shortcut Stories using a clear conflict model:

- **Local is authoritative** for task content (name, description)
- **Remote is authoritative** for workflow state
- **Timestamp-based resolution** (last-write-wins) for conflicts
- **Never reopens closed remote issues** — prevents accidental state regression
- **Staleness threshold** — skips re-sync if under configured `max_age`

Subtask rendering differs per integration:
- **GitHub**: Subtasks render as markdown checkboxes in the parent issue body
- **Shortcut**: Subtasks create separate linked stories

**Why it matters:** The "never reopen" rule is a safety feature born from real-world pain. The staleness check prevents API rate-limit exhaustion in high-frequency agent loops.

---

## 9. Planning-to-Implementation Pipeline

A planning tool converts markdown documents into structured task hierarchies:

```
Markdown Plan → Parse Structure → Create Epic + Tasks + Subtasks
```

This bridges the gap between a human writing a plan in natural language and an agent needing structured, trackable work items.

**Why it matters:** For flowspec's SDD workflow, this enables:
1. `/flow:specify` or `/flow:plan` produces a structured plan
2. The plan is parsed into trackable tasks with dependencies
3. Agents claim and execute tasks across `/flow:implement` phases
4. Results flow back through the completion verification chain

---

## 10. Graceful Degradation & Self-Diagnosis

Two operational features stand out:

**Graceful degradation:**
- If a GitHub token is missing, sync is silently skipped — local operations continue
- If a remote is unreachable, local state is still usable
- No hard failures from missing optional configuration

**Self-diagnosis (`doctor` command):**
- Checks storage accessibility
- Validates integration credentials
- Reports configuration state
- Identifies orphaned tasks or broken relationships

**Why it matters:** Agents running autonomously can't fix auth issues or network problems. Graceful degradation means they keep working locally rather than failing entirely. The doctor command gives humans a fast way to diagnose integration issues.

---

## 11. Multi-Agent, Multi-Machine Coordination

The system explicitly supports distributed workflows:

- Multiple agents/machines can sync to the same GitHub issues
- Timestamp-based conflict resolution handles concurrent edits
- Post-push hooks ensure closure happens from the correct machine
- No central server required — coordination happens through git and issue tracker

**Why it matters:** Flowspec's multi-agent orchestration will have multiple agents working on different tasks simultaneously. This pattern shows how to coordinate without a central orchestrator — using git and issue trackers as the shared state layer.

---

## Feature Adoption Candidates for Flowspec

### High Priority

| Feature | Rationale |
|---------|-----------|
| **Structured task artifacts** (name/description/result) | Agents need to document what they did, not just that they finished |
| **Commit-linked verification** | Proves an agent produced real, merged code |
| **Minimal MCP tool surface** (3 tools) | Easy for any agent to integrate; low context-window cost |
| **Merge-aware closure** | Prevents false completion signals in PR-based workflows |

### Medium Priority

| Feature | Rationale |
|---------|-----------|
| **JSONL git-native storage** | Task state in version control alongside code |
| **Blocking dependencies with cycle detection** | Enables automated task sequencing across agent phases |
| **Graceful degradation** | Agents shouldn't hard-fail on auth/network issues mid-workflow |
| **Archive with compaction** | Keeps active task lists focused across long SDD cycles |

### Worth Monitoring

| Feature | Rationale |
|---------|-----------|
| **Plan-to-task pipeline** | Could feed `/flow:plan` → `/flow:implement` task handoffs |
| **Bidirectional external sync** | Useful for GitHub Projects or Linear integration in `/flow:submit-n-watch-pr` |
| **Multi-machine coordination** | Relevant for distributed agent pools and parallel agent execution |

---

*Analysis date: 2026-02-06*
