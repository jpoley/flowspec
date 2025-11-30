---
id: task-176
title: Implement Acceptance Criteria Test Requirement Gate
status: To Do
assignee: []
created_date: '2025-11-30 21:32'
labels:
  - workflow-artifacts
  - critical
dependencies: []
priority: high
---

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Summary
Implement a requirement that all acceptance criteria from the PRD must have corresponding runnable tests before transitioning from "In Implementation" to "Validated".

## AC-to-Test Mapping

### Test Marking Convention
```python
# Python (pytest)
import pytest

@pytest.mark.ac("AC1: User can register with email")
def test_user_registration():
    """AC1: User can register with email"""
    pass

@pytest.mark.ac("AC2: Password minimum 8 characters")  
def test_password_validation():
    pass
```

```typescript
// TypeScript (jest/vitest)
describe("User Authentication", () => {
  // @ac AC1: User can register with email
  it("should allow registration with valid email", () => {
    // ...
  });
});
```

```go
// Go
func TestUserRegistration(t *testing.T) {
    // AC1: User can register with email
    t.Run("AC1_user_registration", func(t *testing.T) {
        // ...
    })
}
```

### AC Coverage Manifest
Generated artifact: `./tests/ac-coverage.json`

```json
{
  "feature": "user-authentication",
  "prd_path": "./docs/prd/user-authentication.md",
  "generated_at": "2025-11-30T20:30:00Z",
  "acceptance_criteria": [
    {
      "id": "AC1",
      "description": "User can register with email",
      "user_story": "US1",
      "tests": [
        "tests/test_auth.py::test_user_registration"
      ],
      "status": "covered"
    },
    {
      "id": "AC2",
      "description": "Password minimum 8 characters",
      "user_story": "US1", 
      "tests": [
        "tests/test_auth.py::test_password_validation"
      ],
      "status": "covered"
    },
    {
      "id": "AC3",
      "description": "Email verification required",
      "user_story": "US2",
      "tests": [],
      "status": "uncovered"
    }
  ],
  "summary": {
    "total_acs": 3,
    "covered": 2,
    "uncovered": 1,
    "coverage_percent": 66.7
  }
}
```

### Transition Definition
```yaml
implementing_to_validated:
  from: "Planned"
  to: "In Implementation"
  via: "implement"
  input_artifacts:
    - type: adr
      path: ./docs/adr/ADR-*.md
      required: true
  output_artifacts:
    - type: source_code
      path: ./src/
      required: true
    - type: tests
      path: ./tests/
      required: true
    - type: ac_coverage
      path: ./tests/ac-coverage.json
      required: true
      constraints:
        coverage_percent: 100  # All ACs must have tests
  validation: NONE  # Default
```

## Acceptance Criteria
- [ ] AC1: Create pytest marker @pytest.mark.ac("description") for Python
- [ ] AC2: Document test marking conventions for TypeScript and Go
- [ ] AC3: Implement AC scanner that parses PRD and extracts acceptance criteria
- [ ] AC4: Implement test scanner that finds AC markers in test files
- [ ] AC5: Generate ./tests/ac-coverage.json manifest
- [ ] AC6: Block transition if coverage_percent < 100%
- [ ] AC7: Report uncovered ACs with specific guidance
- [ ] AC8: Add `specify ac-coverage` CLI command for manual check
- [ ] AC9: Support --allow-partial-coverage flag for exceptional cases

## Dependencies
- task-172 (Workflow Transition Validation Schema)
- task-173 (PRD Requirement Gate) - PRD contains ACs to validate against
<!-- SECTION:NOTES:END -->
