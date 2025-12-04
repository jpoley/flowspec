---
id: task-217
title: Build Security Configuration System
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-12-03 01:58'
updated_date: '2025-12-04 17:18'
labels:
  - 'workflow:Planned'
  - security
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement .jpspec/security-config.yml configuration file support with scanner selection, rulesets, and AI settings.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Parse security-config.yml with schema validation
- [x] #2 Support scanner enable/disable (Semgrep, CodeQL)
- [x] #3 Configurable severity thresholds (fail_on)
- [x] #4 Path exclusion patterns
- [x] #5 AI triage confidence threshold settings
- [x] #6 Custom Semgrep rule directory support
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## CORRECTED Implementation Plan

**CRITICAL: Configuration only, no AI logic.**

### Phase 1: Config Schema
- Create `src/specify_cli/config/security_config.py`
  - Define SecurityConfig dataclass
  - Fields: persona, severity_threshold, ignore_patterns, custom_rules_dir
  - Load from `docs/security/config.yaml`
  - **NO AI logic**

### Phase 2: YAML Validation
- Create `src/specify_cli/config/policy_validator.py`
  - JSON Schema for config.yaml
  - Validate on load
  - Provide helpful error messages

### Phase 3: Default Configuration
- Create `src/specify_cli/config/defaults.yaml`
  - Default scanners: [semgrep, bandit]
  - Default persona: expert
  - Default severity: medium
  - Default ignore patterns

### Phase 4: Integration
- Update scanners to read config
- Update slash commands to pass config to skills
- Skills receive config as context (not code)

### Success Criteria
- [ ] Config schema defined
- [ ] YAML validation working
- [ ] Defaults provided
- [ ] Scanners and skills use config
- [ ] **ZERO AI LOGIC in config system**

### Files Created
- `src/specify_cli/config/security_config.py`
- `src/specify_cli/config/policy_validator.py`
- `src/specify_cli/config/defaults.yaml`
- `docs/security/config.yaml` (template)
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Summary

The security configuration system was already largely implemented in PR #351. This task completed the documentation layer.

### Files Created

1. **memory/security/security-facts.md** - Comprehensive guide for AI tools
   - Core security principles (Zero API keys, scanner architecture)
   - Configuration hierarchy and validation
   - Scanner integration patterns
   - Best practices and common patterns

2. **memory/security/scanner-config.md** - Scanner defaults and profiles
   - Default configurations for Semgrep, CodeQL, Bandit
   - Environment-specific profiles (dev, CI/CD, audit)
   - Scanner performance characteristics
   - Custom rule directory setup

3. **docs/security/config-schema.yaml** - Fully documented example config
   - Complete YAML schema with inline documentation
   - All available options with explanations
   - Multiple profile examples (dev, CI/CD, audit, minimal)
   - ~300 lines of comprehensive documentation

4. **docs/security/README.md** - User-facing guide
   - Quick start instructions
   - Scanner overview and comparison
   - Configuration profile examples
   - Troubleshooting guide
   - Links to related documentation

### Existing Implementation (Pre-existing)

The core implementation was already complete from PR #351:
- `src/specify_cli/security/config/models.py` - Data models (275 lines)
- `src/specify_cli/security/config/loader.py` - Config loader (325 lines)
- `src/specify_cli/security/config/schema.py` - Validation (440 lines)
- `tests/security/config/` - Comprehensive tests (72 tests, all passing)

### All Acceptance Criteria Met

✓ AC1: Parse security-config.yml with schema validation
  - ConfigLoader with YAML parsing
  - ConfigSchema with comprehensive validation
  - Helpful error messages with path and expected/actual values

✓ AC2: Support scanner enable/disable (Semgrep, CodeQL, Bandit)
  - Each scanner has `enabled: bool` flag
  - get_enabled_scanners() method returns active scanners
  - Scanners can be independently enabled/disabled

✓ AC3: Configurable severity thresholds (fail_on)
  - fail_on: FailOnSeverity enum (critical, high, medium, low, none)
  - should_fail(severity) method checks threshold
  - Proper severity ordering and comparison

✓ AC4: Path exclusion patterns
  - ExclusionConfig with paths, patterns, file_extensions
  - matches_path() method with glob pattern matching
  - Comprehensive default exclusions (dependencies, generated code)

✓ AC5: AI triage confidence threshold settings
  - TriageConfig with confidence_threshold (0.0-1.0)
  - auto_dismiss_fp and cluster_similar options
  - Configurable AI behavior without LLM code in config system

✓ AC6: Custom Semgrep rule directory support
  - SemgrepConfig.custom_rules_dir: Path | None
  - Supports local custom rules in addition to registry
  - Documented in config-schema.yaml with examples

### Test Results

All 72 tests pass:
- 20 loader tests (file loading, parsing, validation)
- 22 model tests (defaults, serialization, methods)
- 30 schema validation tests (type checking, range validation)

```
============================== test session starts ==============================
tests/security/config/test_loader.py ... 20 passed
tests/security/config/test_models.py ... 22 passed
tests/security/config/test_schema.py ... 30 passed
============================== 72 passed in 0.09s ===============================
```

### Code Quality

- All code follows PEP 8 standards
- Type hints throughout
- Comprehensive docstrings
- No imports inside methods (learned from PR #351)
- Error messages match validation conditions exactly
- Zero LLM API calls in config system (as required)

### Documentation Quality

- Memory files for AI tools (security-facts.md, scanner-config.md)
- User-facing docs (README.md, config-schema.yaml)
- Examples for different use cases (dev, CI/CD, audit)
- Troubleshooting guide with common issues
- Links to related documentation (ADRs, guides)

### Key Design Decisions

1. **Separation of Concerns**: Config system is pure data (no AI logic)
2. **Sensible Defaults**: Works out-of-box, users only override what they need
3. **Comprehensive Validation**: Helpful error messages guide users
4. **Multiple Profiles**: Examples for different environments/use cases
5. **AI-Friendly**: Memory files help AI tools understand the system
<!-- SECTION:NOTES:END -->
