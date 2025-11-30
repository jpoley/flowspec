# Research and Validation Reports

This directory contains research reports and validation documentation.

## Purpose

Research reports document investigation and validation work:
- **Technical Research**: Investigation of technologies, libraries, and approaches
- **Business Validation**: Market research, user validation, viability analysis
- **Feasibility Studies**: Technical and business feasibility assessments
- **Competitive Analysis**: Analysis of alternative solutions

## Structure

Research documents are named descriptively (e.g., `{topic}-research.md` or `{feature}-validation.md`).

Templates are available in `../../templates/`:
- `research-template.md` - Technical research format
- `business-validation-template.md` - Business viability analysis

## Usage

Research reports are created by the `/jpspec:research` workflow:

```bash
/jpspec:research
```

Research typically happens before or during the specification phase.

## Existing Research

- [Pipecat Voice Integration Summary](./pipecat-voice-integration-summary.md)
- [Spec Kit Voice](./spec-kit-voice.md)
- [Task to Agent Mapping](./task2agent.md)

## Related Workflows

- **Created By**: `/jpspec:research` workflow
- **When**: Before specification or during planning
- **Templates**: See `templates/research-template.md` and `templates/business-validation-template.md`
