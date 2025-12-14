# Action & Event System

A unified vocabulary for what humans, agents, and programs **do** (actions) and what **happened** (events).

## Overview

| Concept | Definition | Can Be Denied? | Performer |
|---------|------------|----------------|-----------|
| **Action** | A request to do something | Yes | Human, Agent, Program |
| **Event** | An observation that something happened | No (it's a fact) | Human, Agent, Program |

**Examples**:
- **Action**: "approve this PR" (request - can be denied)
- **Event**: "PR was approved" (fact - it happened)

## Action Lifecycle

Every action invocation follows this lifecycle:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ACTION LIFECYCLE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  REQUEST ──► [denied?] ──► ACCEPTED ──► EXECUTION ──► COMPLETED     │
│                 │              │             │             │         │
│                 │              ▼             ▼             ▼         │
│                 │        action.invoked  (side-effect   action.succeeded │
│                 │                         events)       action.failed    │
│                 │                                       action.aborted   │
│                 ▼                                                    │
│            (no events)                                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Guaranteed Terminal Event

For every accepted action, **exactly one** terminal event is always emitted:

| Outcome | Terminal Event | When |
|---------|----------------|------|
| **Denied** | None | Request rejected before execution |
| **Succeeded** | `action.succeeded` | Execution completed successfully |
| **Failed** | `action.failed` | Execution encountered error |
| **Aborted** | `action.aborted` | Execution interrupted by user/system |

## Domains

| Domain | Description | Examples |
|--------|-------------|----------|
| `human` | Actions performed by humans | review, comment, reject |
| `agent` | Actions performed by AI agents | plan, delegate, triage |
| `code` | Actions that modify code/artifacts | fix, format, rebase |
| `system` | Actions performed by automation | trigger, notify |
| `human\|agent` | Actions performable by either | approve, validate, verify |

## Categories

| Category | Description |
|----------|-------------|
| `read` | Enumerate or fetch resources without modification |
| `analyze` | Compare, diff, or analyze states |
| `decide` | Make decisions, check invariants, verify outcomes |
| `plan` | Propose future actions or changes |
| `control` | Explicit gates, approvals, delegation |
| `execute` | Enact plans or run concrete steps |
| `integrate` | Combine work products from multiple sources |
| `scm` | Source control management operations |
| `quality` | Code quality checks and formatting |
| `security` | Security scanning, signing, attestation |
| `mutate` | Apply code changes |
| `signal` | Emit events or trigger workflows |
| `session` | Manage agent/job sessions |
| `explain` | Provide rationale or explanation |
| `recovery` | Retry, rollback, error recovery |
| `record` | Audit trails and artifact publishing |
| `comms` | Communication with humans/systems |
| `container` | Container lifecycle management |

## Action Reference

### Read Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| list | agent | read | enumerate resources | filters?:object, cursor?:string | items:array, next_cursor?:string | none | true | action.succeeded | list repos, list tasks, list sessions |
| inspect | agent | read | deep state fetch | target:{type,id}, fields?:array | snapshot:object, etag?:string | none | true | action.succeeded | inspect repo metadata, inspect backlog item |
| describe | agent | read | human summary | target:{type,id} | summary:string, highlights:array | none | true | action.succeeded | summarize a PR, explain a plan |

### Analyze Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| diff | code | analyze | compare states | a:{ref}, b:{ref}, scope?:array | changes:array, stats:object | none | true | action.succeeded | git diff branches, infra/state diff |

### Decision Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| validate | human\|agent | decide | check invariants | subject:{ref}, ruleset:{ref} | ok:boolean, issues:array | none | true | action.succeeded, decision.made | preflight checks, schema validation |
| triage | agent | decide | prioritize findings | issues:array, policy?:ref | decisions:array<{id,severity,action}> | none | true | action.succeeded, decision.made (per issue) | triage lint/SAST findings |
| verify | human\|agent | decide | confirm expected outcome | subject:{ref}, expectations?:object | ok:boolean, findings:array | none | true | action.succeeded, decision.made | post-merge checks, release verification |

### Planning Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| plan | agent | plan | propose actions | goal:{ref}, context?:object | steps:array, risks:array, rollback_plan?:object | none | true | action.succeeded, decision.made | generate rollout plan, refactor plan |

### Control Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| approve | human\|agent | control | explicit approval gate | plan:{ref}, approver?:string, notes?:string | approved:boolean, notes?:string | records approval | true | action.succeeded, decision.made | change-control signoff, gated release |
| reject | human | control | explicit rejection | plan:{ref}, reason:string, reviewer?:string | rejected:boolean, reason:string | records rejection | true | action.succeeded, decision.made | reject PR, deny release |
| delegate | agent | control | hand off to sub-agent | task:{ref\|object}, agent:{name\|id}, constraints?:object | delegation_id:string, accepted:boolean | spawns work | false | action.succeeded, coordination.handoff | delegate SAST review to security agent |
| waive | human\|agent | control | risk-accept exception | issue_id:string, justification:string, expiry?:date | waiver_id:string | records exception | true | action.succeeded, decision.made | accept false positive |
| request_changes | human | control | request modifications | pr:{ref}, comments:array, reviewer?:string | request_id:string | records request | true | action.succeeded | request PR modifications |

### Execute Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| apply | agent | execute | enact a plan safely | plan:{ref}, mode?:"dry_run"\|"live" | results:array, errors?:array | mutates state | false | action.succeeded, (git.commit if commits) | run planned CI/CD steps, apply changes |
| execute | code | execute | run one concrete step | step:{name}, params?:object, cwd?:string | result:object, logs?:array, exit_code:int | may mutate | false | action.succeeded | run lint, run tests, run formatter |

### Integration Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| merge | agent | integrate | combine work products | inputs:array<{ref,type}>, strategy?:string | merged:{ref,type}, conflicts?:array | updates artifacts | false | action.succeeded, (git.merged if git) | merge sub-agent changes, merge edits |

### SCM Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| create_worktree | code | scm | create git worktree | task_id:string, branch_name:string, base_branch?:string | worktree_path:string | creates worktree | false | action.succeeded, git.worktree_created, git.branch_created | isolate task work |
| remove_worktree | code | scm | remove git worktree | worktree_path:string, delete_branch?:boolean | removed:boolean | removes worktree | false | action.succeeded, git.worktree_removed | cleanup after task |
| create_pr | code | scm | open pull request | base:string, head:string, title:string, body?:string | pr:{id,url,number} | creates PR | false | action.succeeded, git.pr_created | open PR after changes |
| merge_pr | code | scm | merge pull request | pr:{id\|number}, method?:string | merged:boolean, sha?:string | merges PR | false | action.succeeded, git.merged | finalize approved work |
| rebase | code | scm | replay commits | branch:string, onto:string, strategy?:string | result:{ok:boolean, conflicts?:array} | rewrites history | false | action.succeeded, git.commit (per rebased commit) | keep branch up to date |
| resolve_conflicts | code | scm | resolve merge conflicts | conflicts:array, policy?:string | result:{ok:boolean, remaining?:array} | mutates tree | false | action.succeeded, git.conflict_resolved | fix conflict markers |
| submit_local_pr | code | scm | submit for local review | branch:string, checks:array | submission_id:string, status:string | triggers checks | false | action.succeeded, git.local_pr_submitted | pre-push quality gate |

### Quality Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| lint | code | quality | style/static checks | tool:string, targets?:array, config?:string | findings:array, exit_code:int | none | true | action.succeeded | run ESLint, golangci-lint |
| format | code | quality | auto-format | tool:string, targets?:array | changed_files:array | mutates files | true | action.succeeded, (git.commit if autocommit) | gofmt, prettier, black |
| test | code | quality | run tests | suite?:string, targets?:array | report:object, exit_code:int | may start services | false | action.succeeded | run CI tests |
| run_checks | code | quality | run all quality gates | checks:array, targets?:array | results:object, all_passed:boolean | none | true | action.succeeded, git.local_pr_approved\|rejected | unified quality gate |

### Security Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| sast | code | security | static security test | tool:string, targets?:array | issues:array, exit_code:int, sarif?:ref | none | true | action.succeeded | CodeQL, Semgrep scan |
| sca | code | security | dependency scan | tool:string, manifest?:array | vulns:array, sbom?:ref | none | true | action.succeeded | dependency CVEs |
| sbom | code | security | generate SBOM | tool:string, targets?:array | sbom_ref:ref, format:string | writes artifact | true | action.succeeded | CycloneDX generation |
| sign | code | security | sign artifact | artifact:ref, key_ref:ref, algo?:string | signature_ref:ref | writes signature | true | action.succeeded, security.artifact_signed | sign container |
| sign_commit | code | security | GPG sign commit | sha:string, key_ref:ref | signed:boolean, signature:string | updates commit | true | action.succeeded, git.commit (with gpg_key_id) | agent commit signing |

### Mutation Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| fix | code | mutate | apply code changes | changes:array\|patch:ref, strategy?:string | result:{ok:boolean, files_changed:array} | mutates files | false | action.succeeded | apply suggested edits |

### Signal Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| trigger | system | signal | emit event | event:{name,payload}, target?:string | accepted:boolean, event_id?:string | emits event | true | action.succeeded, (custom event) | fire webhook |

### Session Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| start | agent | session | begin session | session_type:string, context?:object | session_id:string, state:"running" | alloc session | false | action.succeeded, lifecycle.started | start agent/job |
| break | human\|agent | session | interrupt + demand rationale | session_id:string, reason_code?:string, note?:string | state:"paused", prompt:"why" | interrupts | true | action.succeeded, lifecycle.paused | halt on risk, pause for approval |
| resume | human\|agent | session | continue session | session_id:string, changes?:object | state:"running", checkpoint?:string | continues | false | action.succeeded, lifecycle.resumed | resume paused workflow |
| stop | human\|agent | session | end session | session_id:string | state:"stopped", summary?:object | may cleanup | true | action.succeeded, lifecycle.completed | stop agent/job |

### Explain Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| why | agent | explain | rationale for action | ref:{session_id\|action_id}, focus?:string | explanation:object, evidence?:array | none | true | action.succeeded | explain why break happened |

### Recovery Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| retry | agent | recovery | rerun operation | action_id:string, backoff?:object | result:object | repeats execution | false | action.succeeded\|failed | rerun flaky step |
| rollback | agent | recovery | revert effects | action_id?:string, plan_id?:string, to_checkpoint?:string | reverted:boolean, notes?:string | mutates state | false | action.succeeded | revert deploy |

### Record Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| audit | agent | record | evidence trail | scope:{ref}, format?:string | records:array, digest?:string | records evidence | true | action.succeeded | compliance pack |
| publish | agent | record | make artifact available | artifact:{ref}, destination:string | published:boolean, uri?:string | writes artifact | true | action.succeeded | publish SBOM/SARIF |

### Communication Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| notify | system | comms | alert humans/systems | message:string, channel:string, severity?:string | delivered:boolean, receipt?:string | sends message | true | action.succeeded | Slack/page/email |
| comment | human | comms | provide feedback | target:{ref}, text:string, commenter?:string | comment_id:string | records comment | true | action.succeeded | PR comment, task comment |
| review | human | comms | formal review | target:{ref}, outcome:string, notes?:string, reviewer?:string | review_id:string | records review | true | action.succeeded, decision.made | code review submission |

### Container Actions

| verb | domain | category | intent | input_contract | output_contract | side_effects | idempotent | events_emitted | typical_use_cases |
|------|--------|----------|--------|----------------|-----------------|--------------|------------|----------------|-------------------|
| spawn_container | system | container | create container | image:string, task_id?:string, config?:object | container_id:string | creates container | false | action.succeeded, container.started | create devcontainer for task |
| attach_container | agent | container | attach to container | container_id:string, agent_id:string | attached:boolean | records attachment | true | action.succeeded, container.agent_attached | agent connects to container |
| destroy_container | system | container | remove container | container_id:string, force?:boolean | destroyed:boolean | removes container | false | action.succeeded, container.stopped | cleanup container |
| inject_secrets | system | container | inject runtime secrets | container_id:string, secrets:array<string> | injected:boolean | injects secrets | true | action.succeeded, container.secrets_injected | runtime secret injection |

## Action → Event Mapping

Every action invocation follows this pattern:

```
action.invoked → [action execution] → action.succeeded OR action.failed
                                    → [side-effect events]
```

### Complete Mapping Table

| Action | Primary Events | Side-Effect Events |
|--------|---------------|-------------------|
| list | action.succeeded | - |
| inspect | action.succeeded | - |
| describe | action.succeeded | - |
| diff | action.succeeded | - |
| validate | action.succeeded | decision.made |
| triage | action.succeeded | decision.made (per issue) |
| verify | action.succeeded | decision.made |
| plan | action.succeeded | decision.made |
| approve | action.succeeded | decision.made |
| reject | action.succeeded | decision.made |
| delegate | action.succeeded | coordination.handoff |
| waive | action.succeeded | decision.made |
| request_changes | action.succeeded | - |
| apply | action.succeeded | git.commit (if commits), task.state_changed |
| execute | action.succeeded | (depends on step) |
| merge | action.succeeded | git.merged (if git) |
| create_worktree | action.succeeded | git.worktree_created, git.branch_created |
| remove_worktree | action.succeeded | git.worktree_removed |
| create_pr | action.succeeded | git.pr_created |
| merge_pr | action.succeeded | git.merged |
| rebase | action.succeeded | git.commit (per rebased commit) |
| resolve_conflicts | action.succeeded | git.conflict_resolved |
| submit_local_pr | action.succeeded | git.local_pr_submitted |
| lint | action.succeeded | - |
| format | action.succeeded | git.commit (if autocommit) |
| test | action.succeeded | - |
| run_checks | action.succeeded | git.local_pr_approved OR git.local_pr_rejected |
| sast | action.succeeded | - |
| sca | action.succeeded | - |
| sbom | action.succeeded | - |
| sign | action.succeeded | security.artifact_signed |
| sign_commit | action.succeeded | git.commit (with gpg_key_id) |
| fix | action.succeeded | - |
| trigger | action.succeeded | (custom event) |
| start | action.succeeded | lifecycle.started |
| break | action.succeeded | lifecycle.paused |
| resume | action.succeeded | lifecycle.resumed |
| stop | action.succeeded | lifecycle.completed |
| why | action.succeeded | - |
| retry | action.succeeded OR failed | (depends on retried action) |
| rollback | action.succeeded | (reversal events) |
| audit | action.succeeded | - |
| publish | action.succeeded | - |
| notify | action.succeeded | - |
| comment | action.succeeded | - |
| review | action.succeeded | decision.made |
| spawn_container | action.succeeded | container.started |
| attach_container | action.succeeded | container.agent_attached |
| destroy_container | action.succeeded | container.stopped |
| inject_secrets | action.succeeded | container.secrets_injected |

## Allowed Followups

Actions define which actions can logically follow:

| Action | Allowed Followups |
|--------|------------------|
| list | describe, inspect, diff |
| inspect | diff, validate, plan |
| describe | inspect, audit |
| diff | plan, apply |
| validate | plan, break |
| plan | apply, delegate, break, approve |
| approve | apply, break |
| reject | plan, break |
| delegate | inspect, merge, break |
| merge | diff, validate, apply, break |
| apply | verify, rollback, break |
| execute | verify, retry, break |
| create_pr | inspect, validate, notify, merge_pr, break |
| merge_pr | verify, audit, break |
| rebase | diff, resolve_conflicts, break |
| resolve_conflicts | diff, rebase, merge_pr, break |
| submit_local_pr | run_checks, approve, break |
| lint | fix, break |
| format | diff, lint, break |
| test | break, retry, audit |
| run_checks | approve, reject, break |
| sast | triage, break, audit |
| sca | triage, break, audit |
| sbom | publish, audit, break |
| sign | verify, publish, audit, break |
| sign_commit | verify, break |
| triage | fix, waive, break |
| fix | diff, lint, test, break |
| waive | audit, notify |
| trigger | inspect, audit |
| start | break, stop, inspect |
| break | why, resume, stop, rollback |
| why | inspect, plan, resume, rollback |
| resume | break, stop, verify |
| stop | audit, report |
| verify | rollback, audit |
| retry | break, verify |
| rollback | verify, audit, break |
| audit | publish, notify |
| publish | notify, audit |
| notify | inspect, audit |
| comment | review, approve, reject |
| review | approve, reject, request_changes |
| request_changes | comment, review |
| spawn_container | attach_container, inject_secrets, break |
| attach_container | start, break |
| inject_secrets | start, break |
| destroy_container | audit |

## Integration with Git Workflow

The following actions map to [Git Workflow Objectives](git-workflow-objectives.md) features:

| Feature | Actions Used |
|---------|-------------|
| Git Worktree Support | create_worktree, remove_worktree |
| Local PR Approval | submit_local_pr, run_checks, lint, test, sast, approve |
| Agent GPG Signing | sign_commit |
| Container Experiments | spawn_container, attach_container, destroy_container |
| Devcontainer Isolation | spawn_container, inject_secrets, destroy_container |

## Integration with Decision Tracker

Actions that produce [decision events](decision-tracker.md):

| Action | Decision Category | Decision Type |
|--------|------------------|---------------|
| validate | varies | pass/fail invariant check |
| triage | security, quality | severity assignment |
| verify | varies | verification outcome |
| plan | architecture, technology | approach selection |
| approve | process, security | approval granted |
| reject | process | rejection with reason |
| waive | security | risk acceptance |
| review | varies | review outcome |

## Related Documents

- [JSONL Event System](jsonl-event-system.md) - Event schema, types, and storage format
- [Git Workflow Objectives](git-workflow-objectives.md) - Git workflow with action/event integration
- [Decision Tracker](decision-tracker.md) - Decision events and audit trails
