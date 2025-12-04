# Constitution Validation Guide

## Overview

Constitutions created by JP Spec Kit include **NEEDS_VALIDATION** markers to indicate sections that require manual review and validation. These markers ensure that auto-generated or templated content is reviewed and customized for your specific project needs.

## What are NEEDS_VALIDATION Markers?

NEEDS_VALIDATION markers are HTML comments embedded in constitution files that indicate content requiring human validation:

```markdown
<!-- NEEDS_VALIDATION: Description of what needs to be validated -->
```

### Example

```markdown
## Technology Stack
<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->
[LANGUAGES_AND_FRAMEWORKS]

### Linting & Formatting
<!-- NEEDS_VALIDATION: Detected linting tools -->
[LINTING_TOOLS]
```

## Why Use NEEDS_VALIDATION Markers?

1. **Prevent blind acceptance** - Auto-generated content might not match your exact needs
2. **Explicit review process** - Clear indication of what needs human judgment
3. **Quality assurance** - Ensures constitution accurately reflects your project
4. **Traceability** - Easy to track which sections have been reviewed

## Validation Workflow

### Step 1: Generate Constitution

When you create a constitution, it may include NEEDS_VALIDATION markers:

```bash
# During project initialization
specify init my-project --constitution medium

# Or add to existing project
specify init --here
```

### Step 2: Check Validation Status

Run the validation command to see which sections need review:

```bash
specify constitution validate
```

**Example output:**

```
Constitution Validation Status
========================================

⚠ 3 section(s) need validation:

✗ Technology Stack
  Line 74: Populate with detected languages/frameworks

✗ Linting & Formatting
  Line 78: Detected linting tools

✗ Version and dates
  Line 95: Version and dates

Next steps:
1. Review each section marked with NEEDS_VALIDATION
2. Update the content to match your project needs
3. Remove the <!-- NEEDS_VALIDATION: ... --> comment
4. Run this command again to verify

Edit file: /home/user/project/memory/constitution.md
```

### Step 3: Review and Update Sections

For each marked section:

1. **Read the marker description** - Understand what needs validation
2. **Update the content** - Replace placeholders or verify accuracy
3. **Remove the marker** - Delete the entire `<!-- NEEDS_VALIDATION: ... -->` line

**Before validation:**

```markdown
## Technology Stack
<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->
[LANGUAGES_AND_FRAMEWORKS]

### Linting & Formatting
<!-- NEEDS_VALIDATION: Detected linting tools -->
[LINTING_TOOLS]
```

**After validation:**

```markdown
## Technology Stack
- **Python 3.11+**: FastAPI, SQLAlchemy, Pydantic
- **TypeScript 5**: React, Next.js 15
- **Go 1.22+**: CLI tools, microservices

### Linting & Formatting
- **Python**: ruff (linting + formatting)
- **TypeScript**: eslint + prettier
- **Go**: gofmt + golangci-lint
```

### Step 4: Verify Validation

Run the validation command again to confirm all markers are resolved:

```bash
specify constitution validate
```

**Success output:**

```
Constitution Validation Status
========================================

✓ Constitution fully validated!

All sections have been reviewed. No NEEDS_VALIDATION markers found.
```

## Common Validation Scenarios

### Scenario 1: Technology Stack

**Marker:** `<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->`

**What to validate:**
- List all primary languages used in the project
- Include major frameworks and libraries
- Specify version requirements where critical
- Document linting and formatting tools

### Scenario 2: Project Name

**Marker:** `<!-- NEEDS_VALIDATION: Project name -->`

**What to validate:**
- Replace `[PROJECT_NAME]` placeholder with actual project name
- Ensure project name is consistent throughout constitution

### Scenario 3: Version and Dates

**Marker:** `<!-- NEEDS_VALIDATION: Version and dates -->`

**What to validate:**
- Set initial version (typically `1.0.0`)
- Record ratification date (when constitution is first adopted)
- Update last amended date when making changes

### Scenario 4: Quality Standards

**Marker:** `<!-- NEEDS_VALIDATION: Adjust quality principles to team practices -->`

**What to validate:**
- Confirm test coverage requirements match team capabilities
- Verify code review process aligns with team size
- Adjust documentation standards based on project complexity

### Scenario 5: Branch Strategy

**Marker:** `<!-- NEEDS_VALIDATION: Branch strategy matches team workflow -->`

**What to validate:**
- Confirm branch naming convention matches team practices
- Verify protected branch settings
- Adjust PR requirements for team size

## JSON Output for Automation

For CI/CD or scripting, use JSON output:

```bash
specify constitution validate --json
```

**Example output:**

```json
{
  "path": "/home/user/project/memory/constitution.md",
  "validated": false,
  "unvalidated_count": 3,
  "markers": [
    {
      "line": 74,
      "section": "Technology Stack",
      "description": "Populate with detected languages/frameworks",
      "context": "<!-- NEEDS_VALIDATION: Populate with detected languages/frameworks -->"
    },
    {
      "line": 78,
      "section": "Linting & Formatting",
      "description": "Detected linting tools",
      "context": "<!-- NEEDS_VALIDATION: Detected linting tools -->"
    },
    {
      "line": 95,
      "section": "Governance",
      "description": "Version and dates",
      "context": "<!-- NEEDS_VALIDATION: Version and dates -->"
    }
  ]
}
```

## Exit Codes

The `specify constitution validate` command uses standard exit codes:

| Exit Code | Meaning | Use Case |
|-----------|---------|----------|
| `0` | All validated | Constitution is ready to use |
| `1` | Unvalidated sections | Review and update required |
| `2` | Error | File not found or read error |

### CI/CD Integration Example

```bash
# In your CI pipeline
specify constitution validate
if [ $? -eq 1 ]; then
  echo "❌ Constitution has unvalidated sections"
  exit 1
fi
echo "✅ Constitution validated"
```

## Custom Constitution Path

If your constitution is not in the default location:

```bash
specify constitution validate --path path/to/custom/constitution.md
```

## Troubleshooting

### "Constitution file not found"

**Problem:** The constitution file doesn't exist at the expected location.

**Solution:**
```bash
# Create a constitution
specify init --here

# Or specify custom path
specify constitution validate --path custom/location/constitution.md
```

### Markers Not Detected

**Problem:** You've added content but the marker still shows.

**Solution:** Ensure you've removed the **entire** marker line, including the `<!--` and `-->` delimiters:

```markdown
<!-- NEEDS_VALIDATION: Description -->  ← Delete this entire line
```

### Unable to Remove All Markers

**Problem:** Some sections genuinely can't be validated yet (e.g., future requirements).

**Solution:** Two options:
1. **Best practice:** Add placeholder content and remove the marker
2. **Temporary:** Leave markers in place, but document why in constitution notes

## Integration with /jpspec Commands

**Important:** Some `/jpspec` workflow commands may warn you if the constitution has unvalidated sections:

```
⚠ Constitution has unvalidated sections. Run 'specify constitution validate' to review.
```

This is a **warning**, not a blocker, but it's recommended to validate your constitution before starting implementation workflows.

## Best Practices

### Do:
- ✅ Review markers before starting implementation
- ✅ Update content to match your actual project
- ✅ Remove markers once validated
- ✅ Run validation command to verify completion
- ✅ Commit validated constitution to version control

### Don't:
- ❌ Remove markers without reviewing content
- ❌ Leave placeholder text (e.g., `[PROJECT_NAME]`) in place
- ❌ Skip validation because "it's just a template"
- ❌ Ignore warnings from `/jpspec` commands

## Related Documentation

- [Constitution Distribution PRD](../prd/constitution-distribution-prd.md) - Full feature specification
- [Tiered Constitution Templates](../../templates/constitutions/) - Template source files
- [JP Spec Kit CLI Reference](../reference/cli-commands.md) - All CLI commands

## Quick Reference

```bash
# Check validation status
specify constitution validate

# Check with custom path
specify constitution validate --path custom/constitution.md

# Get JSON output
specify constitution validate --json

# View help
specify constitution validate --help
```

---

**Next Steps:**
1. Run `specify constitution validate` to check your constitution
2. Review and update sections with NEEDS_VALIDATION markers
3. Remove markers after validation
4. Verify with `specify constitution validate` again
