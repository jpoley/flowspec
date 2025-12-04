# Constitution Validation Guide

## Overview

After creating a constitution with `specify init`, several sections require manual review and customization. These are marked with `NEEDS_VALIDATION` comments.

## Finding Sections to Validate

Run the validation command:

```bash
specify constitution validate
```

This will list all sections that need your attention.

## Validation Process

### 1. Project Name

- Replace `[PROJECT_NAME]` with your actual project name
- Update in the title and throughout the document

### 2. Quality Standards

- Review and adjust based on your team's practices
- Consider your project's maturity level
- Adjust test coverage requirements if needed

### 3. Git Workflow

- Match to your team size (solo, small team, large team)
- Adjust branch protection rules
- Update PR review requirements

### 4. Technology Stack

- Will be populated by `/speckit:constitution` command
- Review detected values for accuracy
- Add any missing technologies your project uses

### 5. Version and Date

- Set initial version (e.g., 1.0.0)
- Set ratification date
- Consider semantic versioning for constitution updates

## Completing Validation

After reviewing a section:

1. Make any necessary changes to the content
2. Remove the `<!-- NEEDS_VALIDATION: ... -->` comment
3. Run `specify constitution validate` again to check progress

When all markers are removed, validation passes:

```bash
$ specify constitution validate

✓ Constitution is fully validated

No NEEDS_VALIDATION markers found.
Your constitution is ready for use.
```

## CI Integration

Add to your CI pipeline to ensure the constitution stays validated:

```yaml
# GitHub Actions
- name: Validate Constitution
  run: specify constitution validate

# GitLab CI
constitution-check:
  script:
    - specify constitution validate
```

The command exits with status 1 if validation markers are found, and 0 if validation passes.

## Example Workflow

Here's a typical validation workflow:

```bash
# 1. Create constitution
specify init --here

# 2. Check what needs validation
specify constitution validate

# Found 5 section(s) requiring validation:
#   1. Project name
#   2. Quality standards
#   3. Git workflow
#   4. Technology stack
#   5. Version and date

# 3. Edit constitution (memory/constitution.md)
# - Update project name
# - Remove NEEDS_VALIDATION comments as you complete each section

# 4. Re-check validation
specify constitution validate

# Found 2 section(s) requiring validation:
#   1. Technology stack
#   2. Version and date

# 5. Continue until validation passes
specify constitution validate

# ✓ Constitution is fully validated
```

## Verbose Mode

For more details, use the `--verbose` flag:

```bash
specify constitution validate --verbose
```

This shows additional context about each validation marker.

## Custom Constitution Path

If your constitution is in a non-standard location:

```bash
specify constitution validate --path path/to/custom-constitution.md
```

## Common Validation Markers

| Marker | What to Update |
|--------|---------------|
| Project name | Replace `[PROJECT_NAME]` with your project's actual name |
| Quality standards | Adjust test coverage, code review requirements |
| Git workflow | Update branch naming, PR requirements |
| Technology stack | Add/verify programming languages, frameworks |
| Version and date | Set initial version and ratification date |

## Best Practices

1. **Complete validation before starting development** - The constitution guides all work
2. **Review with your team** - Get buy-in on standards and processes
3. **Keep markers during draft phase** - Only remove when you're confident
4. **Document rationale** - Add comments explaining why you chose certain values
5. **Version your constitution** - Update version number when making significant changes

## Troubleshooting

### "Constitution not found"

```bash
$ specify constitution validate
Error: Constitution not found at /path/to/memory/constitution.md
Tip: Run 'specify init --here' to create one
```

**Solution**: Run `specify init --here` in your project root to create the constitution.

### Markers remain after editing

If you edit the constitution but markers still appear:

1. Ensure you removed the entire `<!-- NEEDS_VALIDATION: ... -->` comment
2. Check for typos in the marker format
3. Re-run the validation command

### Validation passes but sections are still generic

The validation only checks for `NEEDS_VALIDATION` markers. You should still review all sections to ensure they match your project's needs, even if no markers remain.
