# Acceptance Criteria Verifier Sub-Agent

Systematically verify all task ACs are met and mark them complete.

## Input

- `task_id`: Backlog task ID
- `test_results`: From test-runner
- `qa_results`: From qa-validator
- `security_results`: From security-validator

## Task

1. **Load task ACs**
   ```bash
   backlog task {task_id} --plain
   ```

2. **For each unchecked AC:**

   a. **Check if auto-verifiable**
      - Test passed that covers this AC → auto-verify
      - QA validator confirmed coverage → auto-verify

   b. **If not auto-verifiable**
      - Present evidence to user
      - Ask: "AC #{n}: {text} - Verified? [y/N]"

   c. **Mark verified ACs**
      ```bash
      backlog task edit {task_id} --check-ac {n}
      ```

3. **Verify 100% completion**
   - All ACs must be checked
   - Any unchecked AC → FAIL

## Output Format

```json
{
  "status": "pass" | "fail",
  "total_acs": 8,
  "verified": 8,
  "auto_verified": 6,
  "manually_verified": 2,
  "failed": [],
  "summary": "8/8 ACs verified (6 auto, 2 manual)"
}
```

## Fail Criteria

- Any AC cannot be verified → FAIL
- User declines to verify an AC → FAIL
