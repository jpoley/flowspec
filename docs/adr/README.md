# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records documenting significant architectural decisions.

## Purpose

ADRs capture architectural decisions and their rationale:
- **Context**: What is the issue we're trying to solve?
- **Decision**: What decision did we make?
- **Consequences**: What are the implications (positive and negative)?
- **Alternatives**: What other options were considered?

## Format

ADRs follow the Michael Nygard format and are named `ADR-{NNN}-{title}.md`.

Use the template in `../../templates/adr-template.md` for new ADRs.

## Usage

ADRs are created by the `/jpspec:plan` workflow (Project Architect agent):

```bash
/jpspec:plan
```

Each significant architectural decision should be documented in an ADR.

## Existing ADRs

- [ADR-001: Backlog.md Integration](./ADR-001-backlog-md-integration.md)

## Related Workflows

- **Created By**: `/jpspec:plan` workflow
- **Reference**: See [Architecture Decision Records](https://adr.github.io/)
- **Templates**: See `templates/adr-template.md`
