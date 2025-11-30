# Product Requirements Documents (PRDs)

This directory contains Product Requirements Documents (PRDs) for features.

## Purpose

PRDs define the complete specification for a feature including:
- **Problem Statement**: What problem are we solving and why?
- **Success Metrics**: How do we measure success?
- **Requirements**: Functional and non-functional requirements
- **User Stories**: Who needs this and what do they need?
- **Acceptance Criteria**: What defines "done"?
- **Dependencies**: What other systems or features are required?

## Structure

Each PRD is named `prd-{feature-name}.md` and follows the template in `../../templates/prd-template.md`.

## Usage

PRDs are created by the `/jpspec:specify` workflow after an assessment has been approved:

```bash
/jpspec:specify
```

PRDs serve as the authoritative source for feature requirements and are used by all downstream workflows.

## Related Workflows

- **Previous Step**: Assessment in `docs/assess/`
- **Next Step**: Planning with `/jpspec:plan` generates ADRs and platform docs
- **Templates**: See `templates/prd-template.md`
