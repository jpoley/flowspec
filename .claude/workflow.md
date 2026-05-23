# Workflow — Planning, Execution, Definition of Done

Applies to every task in this repo.

---

## Before Writing Any Code

1. Read the task: `backlog task <id> --plain`
2. Understand all acceptance criteria before touching files.
3. Write an implementation plan — what files change, what the approach is, why.
4. Save the plan to `.claude/plans/task-<id>-<slug>.md`.
5. Share the plan. Wait for explicit approval before coding.

---

## While Working

- Mark task In Progress: `backlog task edit <id> -s "In Progress" -a @myself`
- Work through ACs one at a time. Check each as completed:  
  `backlog task edit <id> --check-ac 1`
- After every meaningful change: run lint + tests.
  ```bash
  ruff check . --fix && ruff format .
  pytest tests/ -x -q
  ```
- Log non-trivial decisions:  
  `backlog task edit <id> --append-notes "Decision: X because Y"`

---

## Definition of Done

A task is done **only** when ALL of the following pass:

| Gate | Command |
|------|---------|
| Format | `uv run ruff format --check .` → 0 errors |
| Lint | `uv run ruff check .` → 0 errors |
| Tests | `uv run pytest tests/ -x -q` → 0 failures |
| ACs | All checkboxes checked in backlog task |
| Notes | Implementation notes written in task |
| Status | `backlog task edit <id> -s Done` |
| PR | Created, closes the GitHub issue |

---

## Branch Naming

```
{hostname}/task-{id}/{slug}
```

Example: `galway/task-606/flowspec-doctor`

```bash
HOSTNAME=$(hostname -s | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')
git checkout -b "${HOSTNAME}/task-606/flowspec-doctor"
```

---

## Commit Format

All commits require DCO sign-off:

```bash
git commit -s -m "feat: description"
```

Prefixes: `feat:` `fix:` `docs:` `refactor:` `test:` `chore:`

---

## PR Rules

- Title: ≤ 70 characters, conventional prefix
- Body: summary bullets + test plan
- Never merge directly to `main` — humans merge
- Never create a PR if lint or tests fail
- Close + reopen rather than updating (Copilot won't re-review updates)
