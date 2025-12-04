---
id: task-221
title: Implement Security Expert Personas
status: Done
assignee:
  - '@muckross'
created_date: '2025-12-03 02:15'
updated_date: '2025-12-04 21:24'
labels:
  - 'workflow:Planned'
  - security
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create 4 security-focused expert personas borrowed from Raptor patterns: @security-analyst, @patch-engineer, @fuzzing-strategist, @exploit-researcher. Use progressive disclosure to load expertise on-demand.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Create @security-analyst persona with OWASP expertise
- [x] #2 Create @patch-engineer persona for fix quality focus
- [x] #3 Create @fuzzing-strategist persona for dynamic testing guidance
- [x] #4 Create @exploit-researcher persona for attack surface analysis
- [x] #5 Implement progressive disclosure pattern for persona loading
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## CORRECTED Implementation Plan

**CRITICAL: No API calls. AI = Skills only.**

### Phase 1: Persona Skill Variants
- Create `.claude/skills/security-triage-beginner.md`
  - Simple language, basic explanations
  - Links to learning resources
  - Step-by-step remediation
- Create `.claude/skills/security-triage-expert.md`
  - Technical depth, CVE references
  - Advanced exploitation scenarios
  - Performance considerations
- Create `.claude/skills/security-triage-compliance.md`
  - Regulatory mapping (OWASP, CWE)
  - Audit requirements
  - Evidence collection format

### Phase 2: Configuration System
- Add persona selection to `docs/security/config.yaml`:
  ```yaml
  security:
    triage_persona: "expert"  # beginner|expert|compliance
  ```
- Update `.claude/commands/jpspec-security-triage.md`
  - Read config.yaml
  - Invoke appropriate skill variant

### Phase 3: Testing
- Test each persona with same findings
- Verify output differences:
  - Beginner: simple explanations
  - Expert: technical details
  - Compliance: regulatory mapping
- **NO API calls during test**

### Success Criteria
- [ ] Three persona skills created
- [ ] Config system selects persona
- [ ] Output varies by persona
- [ ] **ZERO API DEPENDENCIES**

### Files Created
- `.claude/skills/security-triage-beginner.md`
- `.claude/skills/security-triage-expert.md`
- `.claude/skills/security-triage-compliance.md`
- Updated `docs/security/config.yaml`
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented security expert personas as skill variants following the corrected architecture pattern (skills-only, zero API calls).

## Implementation Summary

Created three persona skill variants for security triage:

1. **Beginner Persona** (security-triage-beginner.md)
   - Simple, non-technical language
   - Step-by-step explanations under 100 words
   - Links to learning resources (OWASP, tutorials)
   - Focus on "what to do" with code examples

2. **Expert Persona** (security-triage-expert.md)
   - Technical depth with CWE/CVE references
   - Advanced exploitation scenarios and PoCs
   - Performance and edge case considerations
   - Defense in depth strategies
   - Research references (Exploit-DB, Metasploit)

3. **Compliance Persona** (security-triage-compliance.md)
   - OWASP Top 10 2021 mapping for each finding
   - CWE categorization
   - Regulatory compliance notes (PCI-DSS, SOC2, HIPAA, ISO 27001)
   - Audit evidence format with verification checklists
   - Remediation timeframes per policy

## Files Created

1. `.claude/skills/security-reviewer/security-triage-beginner.md` (219 lines)
2. `.claude/skills/security-reviewer/security-triage-expert.md` (673 lines)
3. `.claude/skills/security-reviewer/security-triage-compliance.md` (815 lines)
4. `memory/security/triage-guidelines.md` (documentation)
5. `docs/security/config-schema.yaml` (configuration examples)
6. `templates/commands/jpspec/security_triage.md` (command template)

## Configuration Integration

Personas are configured via `.jpspec/security-config.yml`:

```yaml
triage:
  enabled: true
  persona: "expert"  # Options: beginner, expert, compliance
  confidence_threshold: 0.7
  auto_dismiss_fp: false
  cluster_similar: true
```

The security_triage command reads this config and invokes the appropriate skill variant.

## Progressive Disclosure Pattern

Each persona cross-references the others:
- Beginners can access expert mode for technical depth
- Experts can reference compliance mode for audit requirements
- All personas maintain consistent finding structure

## Quality Measures

- Self-contained skills (no API dependencies)
- Consistent format across personas
- Clear differentiation in output style
- Comprehensive examples for each vulnerability type
- Standards references (OWASP, CWE, CVSS, regulatory frameworks)

## Testing Approach

To test personas:
1. Run security scan to generate findings
2. Configure persona in security-config.yml
3. Run /jpspec:security_triage command
4. Verify output matches persona characteristics
5. Test all three personas with same findings
6. Confirm no API calls during triage (skills-only execution)

## Documentation

- Persona comparison table in triage-guidelines.md
- Configuration examples in config-schema.yaml
- Output examples for each persona in command template
- Cross-references to ADR-006 and related docs
<!-- SECTION:NOTES:END -->
