# Complete Testing Runbook - Copy/Paste Edition

**Purpose**: Every test and demo you can run, with exact commands and expected results.

**Time required**: ~2 minutes total

---

## Quick Test (30 seconds)

```bash
# From flowspec project root:
cd /home/jpoley/prj/jp/flowspec

# 1. Run workflow tests
uv run pytest tests/workflow/ -q

# 2. Test CLI
uv run flowspec flow custom --list

# 3. Run one demo
uv run python scripts/demo-workflow-execution.py quick_build
```

**Expected**: All pass, no errors

---

## Complete Test Suite

### 1. Unit Tests

**Run workflow tests** (10 seconds):
```bash
uv run pytest tests/workflow/ -v
```

**Expected output**:
```
tests/workflow/test_dispatcher.py::test_dispatcher_initialization PASSED
tests/workflow/test_dispatcher.py::test_dispatch_specify PASSED
...
============================== 64 passed ==============================
```

**Run MCP client tests** (1 second):
```bash
uv run pytest tests/backlog/test_mcp_client.py -v
```

**Expected output**:
```
tests/backlog/test_mcp_client.py::test_client_initialization PASSED
tests/backlog/test_mcp_client.py::test_task_view PASSED
...
============================== 10 passed ==============================
```

**Run full test suite** (40 seconds):
```bash
uv run pytest tests/ -q
```

**Expected output**:
```
........................................................................ [100%]
================ 3498 passed, 17 skipped in 41.07s =================
```

---

### 2. CLI Tests

**List available workflows**:
```bash
uv run flowspec flow custom --list
```

**Expected output**:
```
Available custom workflows (3):

  quick_build
    Name: Quick Build
    Mode: vibing
    Steps: 3
    Description: Lightweight workflow for simple features...

  full_design
    Name: Full Design Workflow
    Mode: spec-ing
    Steps: 4
    Description: Complete design workflow with conditional research

  ship_it
    Name: Build and Ship
    Mode: vibing
    Steps: 3
    Description: Implementation to validation with PR submission
```

**Get execution plan - quick_build**:
```bash
uv run flowspec flow custom quick_build
```

**Expected output**:
```
Executing custom workflow: quick_build

✓ Custom workflow 'quick_build' execution plan prepared
  Steps to execute: 3
  Steps to skip: 0

Workflow execution steps:
  [1] /flow:specify
      Workflow: specify
  [2] /flow:implement
      Workflow: implement
  [3] /flow:validate
      Workflow: validate

Decision log: .logs/decisions/session-YYYYMMDD-HHMMSS.jsonl
Event log: .logs/events/session-YYYYMMDD-HHMMSS.jsonl

NOTE: In Claude Code, use the Skill tool to execute each command above.
```

**Get execution plan - full_design**:
```bash
uv run flowspec flow custom full_design
```

**Expected output**:
```
Executing custom workflow: full_design
Variable 'complexity' not found in context

✓ Custom workflow 'full_design' execution plan prepared
  Steps to execute: 4
  Steps to skip: 0

Workflow execution steps:
  [1] /flow:assess
      Workflow: assess
  [2] /flow:specify
      Workflow: specify
  [3] /flow:research
      Workflow: research
  [4] /flow:plan
      Workflow: plan
```

**Get execution plan - ship_it**:
```bash
uv run flowspec flow custom ship_it
```

**Expected output**:
```
Executing custom workflow: ship_it

✓ Custom workflow 'ship_it' execution plan prepared
  Steps to execute: 3
  Steps to skip: 0

Workflow execution steps:
  [1] /flow:implement
      Workflow: implement
  [2] /flow:validate
      Workflow: validate
  [3] /flow:submit-n-watch-pr
      Workflow: submit-n-watch-pr
```

---

### 3. Demo Scripts

**Demo 1: Basic workflow execution**:
```bash
uv run python scripts/demo-workflow-execution.py quick_build
```

**Expected output**:
```
======================================================================
WORKFLOW AUTO-EXECUTOR DEMONSTRATION
======================================================================

🚀 Auto-executing workflow: quick_build
   Workspace: /home/jpoley/prj/jp/flowspec
   Session: YYYYMMDD-HHMMSS

📋 Preparing execution plan...
✓ Plan prepared
  Steps to execute: 3
  Steps to skip: 0

🔄 Executing workflow steps...
----------------------------------------------------------------------

[1] ▶️  /flow:specify
    Workflow: specify
    ✓ Ready for execution
    [Agent would invoke: Skill(skill='flow:specify')]

[2] ▶️  /flow:implement
    Workflow: implement
    ✓ Ready for execution
    [Agent would invoke: Skill(skill='flow:implement')]

[3] ▶️  /flow:validate
    Workflow: validate
    ✓ Ready for execution
    [Agent would invoke: Skill(skill='flow:validate')]

----------------------------------------------------------------------

✅ Workflow execution complete: quick_build
   ✓ Executed: 3
   ⏭  Skipped: 0

📁 Logs:
   Decision log: .logs/decisions/session-YYYYMMDD-HHMMSS.jsonl
   Event log: .logs/events/session-YYYYMMDD-HHMMSS.jsonl

📝 MCP Backlog Integration:
   [Agent context would update task via MCP]
   Example:
     mcp__backlog__task_edit(
       id='task-123',
       status='In Progress',
       notesAppend=['Executing workflow: quick_build']
     )

======================================================================
✅ DEMONSTRATION COMPLETE
======================================================================
```

**Demo 2: Conditional workflow execution**:
```bash
uv run python scripts/demo-conditional-workflow.py
```

**Expected output**:
```
======================================================================
TEST 1: Low Complexity (complexity=5)
======================================================================
...
🔄 Step-by-step execution:
----------------------------------------------------------------------

[1] ▶️  EXECUTE: assess
    Command: /flow:assess

[2] ▶️  EXECUTE: specify
    Command: /flow:specify

[3] ⏭️  SKIPPED: research
    Reason: Condition not met: complexity >= 7

[4] ▶️  EXECUTE: plan
    Command: /flow:plan

----------------------------------------------------------------------

📊 Conditional Logic:
   Complexity threshold: >= 7
   Current complexity: 5

   ⏭  Research step SKIPPED (complexity < 7)


======================================================================
TEST 2: High Complexity (complexity=8)
======================================================================
...
[3] ▶️  EXECUTE: research
    Command: /flow:research

----------------------------------------------------------------------

📊 Conditional Logic:
   Complexity threshold: >= 7
   Current complexity: 8

   ✓ Research step INCLUDED (complexity >= 7)

======================================================================
✅ CONDITIONAL EXECUTION DEMONSTRATION COMPLETE
======================================================================
```

**Demo 3: Different workflows**:
```bash
# Test full_design
uv run python scripts/demo-workflow-execution.py full_design

# Test ship_it
uv run python scripts/demo-workflow-execution.py ship_it
```

---

### 4. Verify Logs Created

**Check decision logs**:
```bash
ls -lh .logs/decisions/*.jsonl | tail -5
```

**Expected**: Recent .jsonl files with timestamps

**Check event logs**:
```bash
ls -lh .logs/events/*.jsonl | tail -5
```

**Expected**: Recent .jsonl files with timestamps

**View latest decision log**:
```bash
cat .logs/decisions/session-*.jsonl | tail -10 | jq .
```

**Expected**: JSON objects with decision, context, reasoning, outcome fields

**View latest event log**:
```bash
cat .logs/events/session-*.jsonl | tail -10 | jq .
```

**Expected**: JSON objects with event_type, timestamp, workflow, details fields

---

## Complete Runbook (All Tests)

**Copy/paste this entire block**:

```bash
#!/bin/bash
# Complete test runbook for custom workflow orchestration

echo "========================================"
echo "CUSTOM WORKFLOW ORCHESTRATION TEST SUITE"
echo "========================================"
echo ""

cd /home/jpoley/prj/jp/flowspec

echo "1. Running workflow unit tests..."
uv run pytest tests/workflow/ -q
echo ""

echo "2. Running MCP client tests..."
uv run pytest tests/backlog/test_mcp_client.py -q
echo ""

echo "3. Testing CLI - List workflows..."
uv run flowspec flow custom --list
echo ""

echo "4. Testing CLI - quick_build execution plan..."
uv run flowspec flow custom quick_build
echo ""

echo "5. Testing CLI - full_design execution plan..."
uv run flowspec flow custom full_design
echo ""

echo "6. Demo: Basic workflow execution..."
uv run python scripts/demo-workflow-execution.py quick_build
echo ""

echo "7. Demo: Conditional workflow execution..."
uv run python scripts/demo-conditional-workflow.py
echo ""

echo "8. Checking logs were created..."
ls -lh .logs/decisions/*.jsonl | tail -3
ls -lh .logs/events/*.jsonl | tail -3
echo ""

echo "========================================"
echo "✅ ALL TESTS COMPLETE"
echo "========================================"
```

**Save and run**:
```bash
# Save to file
cat > /tmp/test-workflows.sh << 'EOF'
[paste the block above]
EOF

# Make executable
chmod +x /tmp/test-workflows.sh

# Run all tests
/tmp/test-workflows.sh
```

---

## Expected Results Summary

| Test | Expected Result | Time |
|------|----------------|------|
| Workflow tests | 64 passed | 10s |
| MCP client tests | 10 passed | 1s |
| Full test suite | 3498 passed, 17 skipped | 40s |
| CLI list | Shows 3 workflows | <1s |
| CLI quick_build | Shows 3 steps | <1s |
| CLI full_design | Shows 4 steps | <1s |
| CLI ship_it | Shows 3 steps | <1s |
| Demo basic | Shows execution | <1s |
| Demo conditional | Shows skip logic | <1s |
| Logs created | Recent .jsonl files | <1s |

**Total time**: ~60 seconds

---

## Troubleshooting

### Test Failures

**If workflow tests fail**:
```bash
# Run with verbose output
uv run pytest tests/workflow/ -xvs

# Check specific test
uv run pytest tests/workflow/test_orchestrator.py::test_condition_evaluation -xvs
```

**If CLI fails**:
```bash
# Reinstall CLI
uv tool install . --force

# Verify installation
which flowspec
flowspec --version
```

**If demos fail**:
```bash
# Check Python path
uv run python -c "import sys; print('\n'.join(sys.path))"

# Run with verbose imports
uv run python -v scripts/demo-workflow-execution.py quick_build 2>&1 | grep flowspec
```

### Missing Files

**If scripts not found**:
```bash
# Check scripts exist
ls -l scripts/demo-*.py

# Make executable
chmod +x scripts/demo-*.py
```

**If workflows not found**:
```bash
# Check workflow config exists
cat flowspec_workflow.yml | grep -A 5 custom_workflows
```

---

## What This Tests

### ✅ What's Tested
- Orchestrator loads workflows correctly
- Dispatcher maps workflows to commands
- Conditional logic evaluates correctly
- CLI displays execution plans
- Decision/event logging works
- All 3 custom workflows (quick_build, full_design, ship_it)
- Skip logic for conditions
- Demo scripts execute without errors

### ❌ What's NOT Tested
- Actual Skill tool invocations (agent-only)
- Real MCP backlog operations (agent-only)
- End-to-end workflow execution with real /flow commands
- Backlog task updates via MCP

---

## For Your Review

Run these commands and let me know:

1. **Do all tests pass?**
   ```bash
   uv run pytest tests/workflow/ -q
   ```

2. **Does CLI work correctly?**
   ```bash
   uv run flowspec flow custom --list
   uv run flowspec flow custom quick_build
   ```

3. **Do demos run without errors?**
   ```bash
   uv run python scripts/demo-workflow-execution.py quick_build
   uv run python scripts/demo-conditional-workflow.py
   ```

4. **Are logs being created?**
   ```bash
   ls -lh .logs/decisions/*.jsonl | tail -3
   ls -lh .logs/events/*.jsonl | tail -3
   ```

**If any fail, paste the error and I'll fix it.**
