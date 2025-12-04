# Muckross Security Architecture Plan

**Date:** 2025-12-04
**Author:** Enterprise Software Architect
**Context:** /jpspec:plan execution for muckross host
**Scope:** 11 security tasks assigned to muckross
**Branch:** muckross-security-architecture

---

## Executive Summary (Penthouse View)

This document consolidates the architecture planning for 11 security-related tasks assigned to the muckross host. These tasks implement the core AI-powered security capabilities for JP Spec Kit's `/jpspec:security` commands, spanning four domains:

1. **Core AI/Triage** (4 tasks): AI-powered vulnerability classification and fix generation
2. **Configuration** (3 tasks): Policy-as-code and security configuration systems
3. **Integration** (4 tasks): Workflow integration, reporting, and documentation

The strategic framing follows Gregor Hohpe's architecture philosophy: understand the business problem, assess alternatives, make principled decisions, and provide clear implementation guidance.

### Strategic Dependencies

This architecture builds upon established ADRs:
- **ADR-005**: Scanner Orchestration Pattern - Pluggable scanner adapter architecture
- **ADR-006**: AI Triage Engine Design - LLM-powered classification with risk scoring
- **ADR-007**: Unified Security Finding Format - Canonical data model (UFFormat)
- **ADR-008**: Security MCP Server Architecture - v2.0 agent composition (future)

### Business Value

**Problem Statement:** Security scanners produce 30% false positive rates, overwhelming developers with noise. Manual triage requires deep expertise and significant time (4+ hours for 50 findings).

**Solution:** AI-powered triage engine that:
- Classifies findings as TP/FP/NI with 85%+ accuracy
- Generates fixes automatically with 75%+ quality
- Reduces triage time from 4 hours to <1 hour
- Provides plain-English explanations for non-experts

**Success Metrics:**
| Metric | Target | Timeline |
|--------|--------|----------|
| AI Triage Accuracy | >85% | v1.0 |
| Fix Quality | >75% | v1.0 |
| Triage Time Reduction | >75% | v1.0 |
| Developer Satisfaction | NPS >40 | 3 months post-launch |

---

## Task Portfolio Overview

### Core AI/Triage Domain (HIGH Priority)

#### task-212: Build AI-Powered Vulnerability Triage Engine
**Strategic Context:** Foundation for all AI-powered security analysis. Without accurate triage, downstream fix generation and reporting are undermined.

**Architecture Highlights:**
- **Pattern:** Content Enricher (EIP) + Strategy (GoF)
- **LLM Integration:** Claude Sonnet 4.5 with specialized classifiers per CWE
- **Risk Scoring:** Raptor formula: `(Impact × Exploitability) / Detection_Time`
- **Clustering:** Group by CWE, file, and architectural pattern for systemic fixes

**Key Components:**
```
TriageEngine
├── Specialized Classifiers (5 CWE types: SQL, XSS, Path Traversal, Secrets, Crypto)
├── Risk Scorer (Raptor formula implementation)
├── Clustering Engine (CWE, file, pattern-based)
└── Explanation Generator (What, Why, How to Exploit, How to Fix)
```

**Implementation Complexity:** 17-26 hours (2-3 days)
- LLM client integration with retry logic
- 5 specialized classifiers with 85% accuracy target
- Interactive mode for developer confirmation
- Git blame integration for detection time

**Dependencies:**
- Anthropic Python SDK (anthropic)
- Rich library for interactive UI
- Git CLI for detection time calculation

**Risk Assessment:**
- **High Risk:** AI accuracy below 85% → Mitigation: Extensive benchmarking (task-280), interactive mode, specialized classifiers
- **Medium Risk:** LLM API costs → Mitigation: Aggressive caching, smaller models for simple cases

---

#### task-213: Implement Automated Fix Generation and Patch Application
**Strategic Context:** Converts triage results into actionable remediation. Critical for closing the loop from detection to resolution.

**Architecture Highlights:**
- **Pattern:** Strategy Pattern (different fix strategies per language/CWE)
- **Fix Pattern Library:** 20+ patterns covering 5 CWE categories (4 patterns each)
- **Multi-Language Support:** Python, JavaScript/TypeScript, Go with framework detection
- **Patch Generation:** Unified diff format with syntax validation

**Key Components:**
```
FixGenerator
├── Pattern Library (20+ fix templates by CWE)
├── Language Strategies (Python, JS, Go with framework awareness)
├── Patch Generator (unified diff with validation)
└── Patch Applicator (with rollback and confirmation workflow)
```

**Implementation Complexity:** 22-31 hours (3-4 days)
- Fix pattern library (20+ patterns)
- AI-powered patch generation with confidence scoring
- Syntax validation (ast.parse for Python, esprima for JS)
- Rollback mechanism with .orig backups

**Dependencies:**
- Anthropic Python SDK (for LLM)
- difflib (stdlib) for patch generation
- patch command (system) for application
- ast (stdlib) for Python syntax validation

**Risk Assessment:**
- **High Risk:** Fixes break functionality → Mitigation: Conservative fixes, syntax validation, dry-run mode by default, create backups
- **Medium Risk:** Patch conflicts → Mitigation: Detect conflicts before applying, offer manual resolution

---

#### task-221: Implement Security Expert Personas
**Strategic Context:** Enhances AI capabilities with specialized security knowledge on-demand. Borrowed from Raptor's approach but adapted for progressive disclosure (token efficiency).

**Architecture Highlights:**
- **Pattern:** Progressive Disclosure + Persona-Based Prompting
- **4 Personas:** @security-analyst, @patch-engineer, @fuzzing-strategist, @exploit-researcher
- **Token Optimization:** Load personas only when invoked (80-90% token savings vs. Raptor's upfront loading)
- **Integration:** Claude skills system (.claude/skills/)

**Key Components:**
```
Persona System
├── @security-analyst (OWASP expertise, risk assessment, compliance)
├── @patch-engineer (Fix quality, language idioms, testing strategy)
├── @fuzzing-strategist (Dynamic testing, fuzzing targets) [v2.0]
└── @exploit-researcher (Attack scenarios, exploitability analysis)
```

**Implementation Complexity:** 15-21 hours (2-3 days)
- 4 persona prompt templates (Markdown skills)
- Progressive disclosure loader (lazy initialization)
- Integration with triage engine and fix generator
- Persona routing (select appropriate specialist)

**Dependencies:**
- Claude API (already used by triage/fix engines)
- Markdown parser (for persona skill files)
- LRU cache (for persona caching)

**Design Decision - Progressive Disclosure:**
- **Raptor:** Loads all 5 personas upfront (5000+ tokens)
- **JP Spec Kit:** Loads on-demand (200-500 tokens per persona)
- **Justification:** 80-90% token savings when personas not used

---

#### task-280: Benchmark AI Triage Engine Accuracy
**Strategic Context:** Validation task to ensure AI triage meets 85% accuracy target. Provides feedback loop for improving classifiers.

**Architecture Highlights:**
- **Benchmark Dataset:** 100+ labeled findings (40% TP, 40% FP, 20% NI)
- **Expert Validation:** 2-3 security experts label ground truth
- **Metrics:** Overall accuracy, per-classifier accuracy, precision, recall, F1, confidence calibration
- **Continuous Benchmarking:** CI/CD integration to catch regressions

**Key Components:**
```
Benchmark System
├── Dataset Curator (100+ diverse findings across 5 CWE categories)
├── Ground Truth Validator (expert consensus with 90%+ agreement)
├── Benchmark Script (automated accuracy measurement)
├── Failure Mode Analyzer (categorize and remediate failures)
└── CI Integration (regression detection)
```

**Implementation Complexity:** 23-31 hours (3-4 days)
- Dataset curation (100+ findings with expert labels)
- Benchmark automation script
- Confidence calibration analysis
- Comparative analysis (with vs. without LLM, with vs. without personas)
- Failure mode analysis and remediation

**Dependencies:**
- Triage engine (task-212) must be complete
- Expert validation (manual)
- scikit-learn (for metrics)

**Success Criteria:**
- Overall accuracy >85%
- Per-classifier accuracy documented and actionable
- Failure modes identified with remediation plans

---

### Configuration Domain (MEDIUM Priority)

#### task-217: Build Security Configuration System
**Strategic Context:** Enables project-specific security policies via `.jpspec/security-config.yml`. Foundation for task-252 (policy-as-code).

**Architecture Highlights:**
- **Pattern:** Strategy Pattern (scanner-specific configurations)
- **Configuration:** Scanner enable/disable, severity thresholds, path exclusions, AI settings
- **CLI Integration:** Config file + CLI argument merging (CLI takes precedence)

**Key Components:**
```
Configuration System
├── Config Schema (Pydantic models)
├── Config Loader (YAML parsing with validation)
├── CLI Merger (config file + CLI args)
└── Config Commands (init, validate, show, set)
```

**Implementation Complexity:** 10 hours (1.25 days)
- Config schema definition (Pydantic)
- Loader with fallback to defaults
- CLI integration (merge logic)
- Config management commands

**Dependencies:**
- Security scan command (task-210, assigned to other host)

---

#### task-223: Implement Custom Security Rules System
**Strategic Context:** Allows users to define project-specific security patterns via `.jpspec/security-rules/` directory.

**Architecture Highlights:**
- **Pattern:** Plugin Architecture (load custom Semgrep rules)
- **Directory Structure:** `.jpspec/security-rules/{language}/{custom-rule}.yml`
- **Validation:** Semgrep --validate for rule syntax
- **Integration:** Auto-load custom rules at scan time

**Key Components:**
```
Custom Rules System
├── Rules Directory Structure (.jpspec/security-rules/)
├── Rule Loader (discover and validate rules)
├── Rule Validator (Semgrep syntax check)
└── Integration (pass --config to Semgrep)
```

**Implementation Complexity:** 10 hours (1.25 days)
- Directory structure creation
- Rule loader with validation
- Semgrep integration
- Documentation and examples

**Dependencies:**
- Semgrep installed
- Security scan command

---

#### task-252: Implement Security Policy as Code Configuration
**Strategic Context:** Enterprise-grade policy enforcement via `.jpspec/security-policy.yml`. Supports compliance gates (pre-commit, PR, main branch) and finding exemptions.

**Architecture Highlights:**
- **Pattern:** Policy Engine with Gates
- **Configuration:** Severity gates (block_on, warn_on), tool config, exemptions (with expiration)
- **Compliance:** OWASP Top 10, SOC2, ISO 27001 mappings
- **Exemptions:** Path-based and finding-specific with justification and expiration

**Key Components:**
```
Policy Engine
├── Policy Schema (gates, tools, triage, reporting, exemptions)
├── Policy Parser (YAML with Pydantic validation)
├── Enforcement Engine (gate evaluation, exemption checking)
└── Policy Commands (init, validate, show, exempt add/list/remove)
```

**Implementation Complexity:** 12 hours (1.5 days)
- Policy schema (YAML + Pydantic)
- Enforcement engine (gates + exemptions)
- Default policy template (OWASP Top 10 compliance)
- Policy management commands

**Dependencies:**
- Security scan command
- Finding data models (ADR-007)

**Enterprise Features:**
- Version-controlled policies (Git)
- Exemption audit trail
- Compliance reporting (SOC2, ISO 27001, HIPAA)

---

### Integration Domain (HIGH Priority)

#### task-214: Build Security Audit Report Generator
**Strategic Context:** Converts scan results into professional reports for stakeholders. Supports multiple formats (Markdown, HTML, PDF, SARIF).

**Architecture Highlights:**
- **Pattern:** Template Method (GoF) + Message Translator (EIP)
- **Report Template:** Executive summary, risk assessment, OWASP Top 10 compliance, remediation roadmap
- **Multi-Format:** Markdown, HTML, PDF, SARIF 2.1.0
- **Compliance Modes:** SOC2, ISO 27001, HIPAA

**Key Components:**
```
Report Generator
├── Security Report Template (Jinja2)
├── OWASP Top 10 Compliance Checker
├── Security Posture Calculator (risk scoring)
├── Multi-Format Exporters (Markdown, HTML, PDF, SARIF)
└── Compliance Modes (SOC2, ISO 27001, HIPAA)
```

**Implementation Complexity:** 20-27 hours (2.5-3.5 days)
- Report template (comprehensive Jinja2)
- OWASP Top 10 mapping (CWE → OWASP categories)
- Security posture calculator (risk formula)
- Multi-format exporters (especially PDF via weasyprint)
- Remediation roadmap prioritization

**Dependencies:**
- Jinja2 (template engine)
- markdown (Markdown → HTML)
- weasyprint or reportlab (PDF generation)
- SARIF JSON schema (validation)

**Risk Assessment:**
- **Medium Risk:** PDF generation failures → Mitigation: HTML export as fallback, document PDF setup
- **Medium Risk:** SARIF incompatibility → Mitigation: Validate against official schema, test GitHub upload

---

#### task-216: Integrate /jpspec:security with Workflow and Backlog
**Strategic Context:** Wires security commands into jpspec_workflow.yml state machine and enables automatic backlog task creation for findings.

**Architecture Highlights:**
- **Workflow Integration:** Add "Security Reviewed" state or extend "Validated" workflow
- **Backlog Integration:** `--create-tasks` flag auto-generates tasks for critical/high findings
- **CI/CD:** Examples for GitHub Actions, GitLab CI, Jenkins
- **SARIF Output:** Enable GitHub Code Scanning integration

**Key Components:**
```
Workflow Integration
├── jpspec_workflow.yml (add security state/workflow)
├── Backlog Task Generator (create tasks from findings)
├── CI/CD Examples (GitHub Actions, GitLab, Jenkins)
└── SARIF Exporter (GitHub Security tab integration)
```

**Implementation Complexity:** 12 hours (1.5 days)
- Workflow configuration (jpspec_workflow.yml)
- `--create-tasks` flag implementation
- SARIF export (already covered in ADR-007)
- CI/CD integration examples

**Dependencies:**
- Workflow system implementation
- Backlog.md MCP tools
- Security scan command

**Design Decision - Workflow Integration:**
Two options documented:
1. **Option A:** Add optional "Security Reviewed" state (dedicated)
2. **Option B:** Extend "Validated" workflow with security-scanner agent (integrated)

---

#### task-218: Write Comprehensive Security Commands Documentation
**Strategic Context:** User-facing documentation for all security commands and workflows.

**Documentation Portfolio:**
1. **Security Quickstart Guide** - 5-minute tutorial (docs/guides/security-quickstart.md)
2. **Command Reference** - All commands with flags, examples, exit codes (docs/reference/jpspec-security-commands.md)
3. **CI/CD Integration Guide** - Step-by-step for GitHub Actions, GitLab, Jenkins (docs/guides/security-cicd-integration.md)
4. **Threat Model and Limitations** - What it protects/doesn't protect (docs/security/threat-model.md)
5. **AI Privacy Policy** - Data usage, opt-out, compliance (docs/security/ai-privacy-policy.md)
6. **Custom Rule Writing Guide** - Semgrep rule examples (docs/guides/custom-security-rules.md)

**Implementation Complexity:** 12 hours (1.5 days)
- 6 documentation guides
- Command reference with examples
- CI/CD integration examples
- Threat model and privacy policy

**Dependencies:**
- All security commands implemented

---

#### task-220: Resolve Relationship with task-198 Unified Vulnerability Scanner
**Strategic Context:** Clarify integration between /jpspec:security (SAST with Semgrep/CodeQL) and task-198 (Trivy + Snyk for dependency/container scanning).

**Architecture Decision:** Complementary, not overlapping

```yaml
# Recommended Integration Architecture
/jpspec:security scan   # SAST (code analysis)
  - Semgrep: Code vulnerabilities (SQL injection, XSS, etc.)
  - CodeQL: Advanced dataflow analysis (optional)

/jpspec:security deps   # Dependency scanning (NEW, integrates task-198)
  - Trivy: Container images + dependencies
  - Snyk: Dependency vulnerabilities (optional)

/jpspec:security web    # DAST (task-222, future)
  - Playwright-based testing
```

**Key Insight:** All three produce unified finding format (UFFormat) for triage/fix/audit.

**Implementation Complexity:** 8 hours (1 day)
- Review task-198 design
- Create tool comparison matrix
- Document integration architecture (ADR-009 already exists)
- Update PRD and task-198

**Dependencies:**
- task-198 design document

**Outcome:** ADR-009 (already exists) documents this decision. Task is primarily documentation and coordination.

---

## Component Relationships and Data Flow

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MUCKROSS SECURITY DOMAIN                      │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              SCANNER ORCHESTRATOR (ADR-005)              │   │
│  │  - Discovers and executes scanners (Semgrep, CodeQL)    │   │
│  │  - Normalizes to Unified Finding Format (ADR-007)       │   │
│  │  - Deduplicates findings by fingerprint                 │   │
│  └────────────────────┬─────────────────────────────────────┘   │
│                       │                                          │
│                       │ List[Finding] (UFFormat)                │
│                       │                                          │
│  ┌────────────────────▼─────────────────────────────────────┐   │
│  │              AI TRIAGE ENGINE (task-212)                 │   │
│  │  - Classifies TP/FP/NI with 85%+ accuracy              │   │
│  │  - Risk scores using Raptor formula                     │   │
│  │  - Clusters by CWE, file, pattern                       │   │
│  │  - Generates plain-English explanations                 │   │
│  │                                                          │   │
│  │  Uses:                                                   │   │
│  │  - Security Expert Personas (task-221)                  │   │
│  │  - Benchmarked on 100+ examples (task-280)             │   │
│  └────────────┬─────────────────────────────────────────────┘   │
│               │                                                  │
│               │ List[TriageResult]                              │
│               │                                                  │
│  ┌────────────▼──────────────┬──────────────────────────────┐   │
│  │                           │                              │   │
│  │  ┌────────────────────┐   │   ┌────────────────────┐    │   │
│  │  │  FIX GENERATOR     │   │   │  REPORT GENERATOR  │    │   │
│  │  │  (task-213)        │   │   │  (task-214)        │    │   │
│  │  │                    │   │   │                    │    │   │
│  │  │ - 20+ fix patterns │   │   │ - OWASP Top 10     │    │   │
│  │  │ - Syntax validation│   │   │ - Multi-format     │    │   │
│  │  │ - Patch generation │   │   │ - Compliance modes │    │   │
│  │  └────────────────────┘   │   └────────────────────┘    │   │
│  │                           │                              │   │
│  └───────────────────────────┼──────────────────────────────┘   │
│                               │                                  │
│  ┌────────────────────────────▼──────────────────────────────┐   │
│  │              WORKFLOW INTEGRATION (task-216)              │   │
│  │  - Backlog task creation (--create-tasks)                │   │
│  │  - jpspec_workflow.yml state machine                     │   │
│  │  - CI/CD integration (GitHub Actions, GitLab)            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │          CONFIGURATION LAYER (tasks 217, 223, 252)       │   │
│  │  - security-config.yml (scanner settings)                │   │
│  │  - custom rules (.jpspec/security-rules/)                │   │
│  │  - policy-as-code (.jpspec/security-policy.yml)          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Sequence

1. **Scan Phase** (Scanner Orchestrator)
   - Input: Target directory, scanner config
   - Output: `List[Finding]` in Unified Finding Format (UFFormat)
   - Deduplication: Fingerprint-based merging

2. **Triage Phase** (AI Triage Engine - task-212)
   - Input: `List[Finding]`
   - Process: Classification (TP/FP/NI), risk scoring, clustering
   - Personas: Invoke @security-analyst, @patch-engineer as needed (task-221)
   - Output: `List[TriageResult]` with classifications, scores, explanations

3. **Remediation Phase** (Fix Generator - task-213)
   - Input: `List[TriageResult]` (filtered to TP only)
   - Process: Pattern matching, AI patch generation, syntax validation
   - Output: `List[Patch]` with unified diffs and confidence scores

4. **Reporting Phase** (Report Generator - task-214)
   - Input: `List[Finding]` + `List[TriageResult]` + `List[Patch]`
   - Process: Template population, OWASP mapping, compliance checking
   - Output: Multi-format reports (Markdown, HTML, PDF, SARIF)

5. **Integration Phase** (Workflow Integration - task-216)
   - Input: Triaged findings (TP with severity critical/high)
   - Process: Create backlog tasks with ACs
   - Output: Tasks in backlog.md with workflow:Planned label

### Cross-Task Dependencies

**Critical Path:**
```
task-212 (Triage Engine)
   ↓
task-213 (Fix Generator) ← depends on triage results
   ↓
task-214 (Report Generator) ← depends on triage + fixes
   ↓
task-216 (Workflow Integration) ← depends on report format

task-280 (Benchmark) ← validates task-212
task-221 (Personas) → enhances task-212 and task-213
```

**Configuration Tasks (Parallel Track):**
```
task-217 (Config System)
   ↓
task-252 (Policy as Code) ← extends task-217

task-223 (Custom Rules) ← independent, integrates at scan time
```

**Documentation (Post-Implementation):**
```
task-218 (Documentation) ← requires all commands implemented
task-220 (Scanner Resolution) ← coordination with task-198 team
```

---

## Integration Patterns (Enterprise Integration Patterns Taxonomy)

### 1. Content Enricher Pattern (EIP)
**Where Applied:** AI Triage Engine (task-212)

Original security finding lacks context:
```json
{
  "id": "SEMGREP-001",
  "severity": "high",
  "title": "SQL Injection",
  "file": "auth.py",
  "line": 42
}
```

Enriched with AI analysis:
```json
{
  "id": "SEMGREP-001",
  "classification": "TRUE_POSITIVE",
  "confidence": 0.92,
  "risk_score": 8.5,
  "explanation": "User input directly concatenated into SQL query...",
  "attack_scenario": "Attacker can inject SQL commands via username parameter...",
  "fix_guidance": "Use parameterized queries with cursor.execute(query, params)"
}
```

### 2. Message Translator Pattern (EIP)
**Where Applied:** Scanner Orchestrator (ADR-005), Report Generator (task-214)

Translates scanner-specific formats → UFFormat → Export formats:
```
Semgrep JSON → UFFormat → SARIF 2.1.0
CodeQL SARIF → UFFormat → Markdown Report
Trivy JSON   → UFFormat → HTML Dashboard
```

### 3. Adapter Pattern (GoF)
**Where Applied:** Scanner Orchestrator (ADR-005)

Each scanner has a dedicated adapter:
- `SemgrepAdapter` - Translates Semgrep JSON to UFFormat
- `CodeQLAdapter` - Translates CodeQL SARIF to UFFormat
- `TrivyAdapter` - Translates Trivy JSON to UFFormat

### 4. Strategy Pattern (GoF)
**Where Applied:** AI Triage Engine (task-212), Fix Generator (task-213)

Different strategies for different vulnerability types:
- `SQLInjectionClassifier` - Specialized for CWE-89
- `XSSClassifier` - Specialized for CWE-79
- `PythonFixStrategy` - Language-specific fix generation
- `JavaScriptFixStrategy` - Framework-aware (React, Vue)

### 5. Template Method Pattern (GoF)
**Where Applied:** Report Generator (task-214)

Report generation follows template structure:
1. Executive Summary
2. Risk Assessment
3. OWASP Top 10 Compliance
4. Detailed Findings
5. Remediation Roadmap

Subclasses implement format-specific rendering (Markdown, HTML, PDF).

### 6. Decorator Pattern (GoF)
**Where Applied:** AI Triage Engine (task-212)

`InteractiveTriageEngine` wraps `TriageEngine`:
- Base: Automatic AI classification
- Decorator: Adds interactive confirmation prompts

---

## Technology Stack Consolidation

### Core Dependencies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| LLM Client | Anthropic Python SDK | latest | Claude Sonnet 4.5 API |
| Security Scanner | Semgrep | 1.45+ | SAST scanning |
| Security Scanner | CodeQL CLI | 2.15+ | Advanced dataflow analysis |
| Dependency Scanner | Trivy | 0.48+ | Container/dependency scanning |
| UI Library | Rich | 13.7+ | Interactive CLI (task-212) |
| Template Engine | Jinja2 | 3.1+ | Report generation (task-214) |
| Markdown Renderer | markdown | 3.5+ | Markdown → HTML conversion |
| PDF Generator | weasyprint | 60+ | HTML → PDF conversion |
| Validation | Pydantic | 2.5+ | Config schema validation |
| Git Integration | GitPython | 3.1+ | Git blame for detection time |

### Python Standard Library Usage

- `dataclasses` - UFFormat models (ADR-007)
- `ast` - Python syntax validation (task-213)
- `difflib` - Patch generation (task-213)
- `subprocess` - External tool execution (scanners, git blame)
- `hashlib` - Finding fingerprinting (ADR-007)
- `json` - Serialization/deserialization
- `pathlib` - Cross-platform file path handling

### External Tools (System Commands)

- `semgrep` - SAST scanning
- `codeql` - SARIF-based scanning (optional)
- `trivy` - Dependency/container scanning
- `git` - Git blame for detection time
- `patch` - Patch application (GNU patch)

---

## Risk Assessment and Mitigations

### High Risks

#### Risk 1: AI Triage Accuracy Below 85% Target
**Impact:** Undermines trust in AI recommendations, developers ignore results (alert fatigue)

**Likelihood:** Medium

**Mitigations:**
1. **Extensive Benchmarking** (task-280): Validate on 100+ labeled examples before launch
2. **Specialized Classifiers** (task-212): Use CWE-specific prompts, not generic LLM
3. **Interactive Mode** (task-212): Allow human override for uncertain classifications
4. **Feedback Loop** (task-221): Collect developer corrections to improve prompts
5. **Confidence Scores** (task-212): Display AI certainty, highlight low-confidence decisions

**Contingency:** If accuracy <85%, increase interactive mode usage until prompt refinement achieves target.

---

#### Risk 2: Generated Fixes Break Functionality
**Impact:** Developers lose trust, manual review required for all fixes

**Likelihood:** Medium

**Mitigations:**
1. **Conservative Fix Generation** (task-213): Minimal changes, avoid complex refactors
2. **Syntax Validation** (task-213): ast.parse() for Python, esprima for JS before suggesting
3. **Dry-Run by Default** (task-213): Show patch preview, require explicit confirmation
4. **Backup Creation** (task-213): Create .orig files before applying patches
5. **Rollback Mechanism** (task-213): One-command undo if fix breaks tests

**Contingency:** If fix quality <75%, increase pattern library coverage and reduce AI-only fixes.

---

### Medium Risks

#### Risk 3: LLM API Costs Exceed Budget
**Impact:** Cost overruns, need to limit AI features

**Likelihood:** Medium

**Mitigations:**
1. **Aggressive Caching** (task-212): Same finding fingerprint → cached classification
2. **Smaller Models** (task-212): Use Claude Haiku for simple classifications, Sonnet for complex
3. **Batch Requests** (task-212): Parallel LLM calls reduce overhead
4. **Progressive Disclosure** (task-221): Load personas only when needed (80-90% token savings)

**Monitoring:** Track LLM costs per scan, alert if exceeds $0.50/scan threshold.

---

#### Risk 4: Patch Application Conflicts
**Impact:** Manual merge conflicts, workflow disruption

**Likelihood:** Medium

**Mitigations:**
1. **Conflict Detection** (task-213): Dry-run patch before applying, detect conflicts
2. **Manual Resolution** (task-213): Offer to open file in editor if conflict detected
3. **Patch Editing** (task-213): Allow developer to modify patch before applying

---

### Low Risks

#### Risk 5: SARIF Export Incompatibility
**Impact:** GitHub Code Scanning integration fails

**Likelihood:** Low (SARIF is well-specified)

**Mitigations:**
1. **Schema Validation** (task-214): Validate against official SARIF 2.1.0 schema
2. **Test Upload** (task-214): Test SARIF upload to GitHub before launch
3. **Reference Implementation** (ADR-007): Follow CodeQL's SARIF export as reference

---

## Implementation Recommendations

### Recommended Implementation Order

**Phase 1: Core AI Capabilities (Weeks 1-2)**
1. **task-212** (AI Triage Engine) - 2-3 days
   - Foundation for all downstream work
   - Implement with default classifier first, add specialized classifiers iteratively
2. **task-221** (Security Personas) - 2-3 days
   - Enhances task-212 accuracy
   - Can be implemented in parallel with task-212
3. **task-280** (Benchmark) - 3-4 days
   - Validates task-212 accuracy
   - Critical for v1.0 quality gate

**Phase 2: Remediation and Reporting (Weeks 3-4)**
4. **task-213** (Fix Generator) - 3-4 days
   - Depends on task-212 triage results
   - Implement pattern library first, AI generation second
5. **task-214** (Report Generator) - 2.5-3.5 days
   - Depends on task-212 and task-213
   - Implement Markdown first, HTML/PDF later

**Phase 3: Configuration and Integration (Weeks 5-6)**
6. **task-217** (Config System) - 1.25 days
   - Foundation for task-252
7. **task-252** (Policy as Code) - 1.5 days
   - Extends task-217
8. **task-216** (Workflow Integration) - 1.5 days
   - Depends on all commands being functional
9. **task-223** (Custom Rules) - 1.25 days
   - Independent, can be done anytime

**Phase 4: Documentation and Coordination (Week 7)**
10. **task-218** (Documentation) - 1.5 days
    - Requires all commands implemented
11. **task-220** (Scanner Resolution) - 1 day
    - Coordination with task-198 team

**Total Estimated Effort:** 22-30 days (4-6 weeks with parallelization)

### Parallelization Opportunities

**Week 1-2:**
- task-212 (AI Triage) + task-221 (Personas) can run in parallel
- task-280 (Benchmark) starts after task-212 core is functional

**Week 3-4:**
- task-213 (Fix Generator) and task-214 (Report Generator) can run in parallel after task-212 complete

**Week 5-6:**
- task-217 (Config), task-223 (Custom Rules) can run in parallel
- task-252 (Policy) starts after task-217

**Week 7:**
- task-218 (Docs) and task-220 (Coordination) can run in parallel

**Optimistic Timeline with Parallelization:** 5-6 weeks with 2 engineers
**Conservative Timeline:** 7-8 weeks with 1 engineer

---

## Quality Gates and Acceptance Criteria

### Task-Level Gates (Must Pass Before Marking Complete)

#### task-212: AI Triage Engine
- [ ] AI classification accuracy >85% on benchmark dataset (task-280)
- [ ] Risk scoring produces sensible rankings (critical > high > medium)
- [ ] Clustering groups 3+ findings meaningfully (not over/under clustered)
- [ ] Explanations are clear and actionable (manual review of 20 samples)
- [ ] Interactive mode provides good UX (usability test with 5 developers)
- [ ] Performance: 50 findings in <2 minutes

#### task-213: Fix Generator
- [ ] Fix pattern library covers 5 CWE categories with 4+ patterns each
- [ ] AI generates syntactically valid fixes >95% of time (ast.parse test)
- [ ] Fix quality >75% (correct or mostly correct, manual review of 30 fixes)
- [ ] Patches apply cleanly >90% of time (test on 20 codebases)
- [ ] Rollback mechanism works reliably (test 10 rollback scenarios)

#### task-221: Security Personas
- [ ] 4 personas implemented and accessible
- [ ] Progressive disclosure reduces token usage (measure: only load when needed)
- [ ] Persona responses are high-quality and specialized (manual review)
- [ ] Integration with triage and fix engines works seamlessly
- [ ] Token overhead is minimal (<10% when not invoked)

#### task-280: Benchmark
- [ ] Dataset includes 100+ labeled findings across 5 CWE categories
- [ ] Overall accuracy >85% (target met)
- [ ] Per-classifier accuracy documented and actionable
- [ ] Failure modes identified with remediation plans
- [ ] Benchmark process is automated and repeatable

#### task-217: Config System
- [ ] Config parser handles valid YAML with schema validation
- [ ] Config parser rejects invalid YAML with clear errors
- [ ] CLI argument merging works (CLI takes precedence)
- [ ] Config management commands work end-to-end

#### task-223: Custom Rules
- [ ] Rule loader discovers rules in `.jpspec/security-rules/`
- [ ] Rule validator rejects invalid Semgrep syntax
- [ ] Custom rules integrate into scan command
- [ ] Documentation with examples provided

#### task-252: Policy as Code
- [ ] Policy parser handles valid YAML with schema validation
- [ ] Gate enforcement blocks correctly (critical/high findings)
- [ ] Gate enforcement warns correctly (medium findings)
- [ ] Path exemptions work (tests/** excluded)
- [ ] Finding exemptions work with expiration (expired exemptions ignored)

#### task-214: Report Generator
- [ ] Report includes all required sections per template
- [ ] OWASP Top 10 compliance checker covers all 10 categories
- [ ] Security posture calculation is accurate (manual validation)
- [ ] Multi-format export works (Markdown, HTML, PDF, SARIF)
- [ ] SARIF validates against official 2.1.0 schema

#### task-216: Workflow Integration
- [ ] jpspec_workflow.yml updated with security state or workflow
- [ ] `--create-tasks` flag creates backlog tasks for TP findings
- [ ] SARIF export works (GitHub Security tab integration)
- [ ] CI/CD examples provided and tested

#### task-218: Documentation
- [ ] Security Quickstart Guide (5-minute tutorial)
- [ ] Command Reference (all commands with examples)
- [ ] CI/CD Integration Guide (GitHub Actions, GitLab, Jenkins)
- [ ] Threat Model and Limitations
- [ ] AI Privacy Policy
- [ ] Custom Rule Writing Guide

#### task-220: Scanner Resolution
- [ ] Tool comparison matrix created
- [ ] Integration architecture documented (complementary tools)
- [ ] ADR-009 reviewed and confirmed
- [ ] PRD and task-198 updated

---

### Cross-Task Integration Tests

**Test 1: End-to-End Security Workflow**
```bash
# 1. Scan codebase
specify security scan --scanners semgrep --fail-on critical,high

# 2. Triage findings
specify security triage --interactive

# 3. Generate fixes
specify security fix --apply=false  # Dry-run

# 4. Generate report
specify security audit --format markdown,sarif

# 5. Create backlog tasks
specify security scan --create-tasks

# Verify:
# - Findings detected and classified
# - Fixes generated and validated
# - Report generated with all sections
# - Tasks created in backlog.md
```

**Test 2: Policy Enforcement**
```bash
# 1. Initialize policy
specify security policy init

# 2. Run scan with policy
specify security scan --gate-type pull_request

# Verify:
# - Critical findings block (exit code 1)
# - Medium findings warn (exit code 0)
# - Exempted findings ignored
```

**Test 3: Custom Rules**
```bash
# 1. Add custom rule
specify security rules add --file .jpspec/security-rules/python/api-auth-bypass.yml

# 2. Validate rule
specify security rules validate

# 3. Scan with custom rules
specify security scan --scanners semgrep

# Verify:
# - Custom rule executed
# - Custom findings detected
```

---

## Architecture Decision Records (ADRs) Summary

### Existing ADRs Referenced

**ADR-005: Scanner Orchestration Pattern**
- **Decision:** Pluggable adapter architecture
- **Rationale:** Clean separation, composability, testability
- **Impact:** All scanners implement ScannerAdapter interface

**ADR-006: AI Triage Engine Design**
- **Decision:** LLM-powered triage with specialized classifiers
- **Rationale:** 85%+ accuracy, scalable, generates explanations
- **Impact:** Foundation for task-212, task-221

**ADR-007: Unified Security Finding Format (UFFormat)**
- **Decision:** Domain-driven data model with SARIF compatibility
- **Rationale:** Clean Python API, SARIF export, extensible
- **Impact:** All components use UFFormat (scan → triage → fix → report)

**ADR-008: Security MCP Server Architecture**
- **Decision:** MCP server with tools + resources (v2.0 feature)
- **Rationale:** Agent composition, cross-repo queries, IDE integration
- **Impact:** Future expansion, not in scope for v1.0

**ADR-009: task-198 Scanner Resolution**
- **Decision:** Complementary tools (SAST + dependency scanning)
- **Rationale:** Broader coverage, unified interface
- **Impact:** `/jpspec:security scan` (SAST) + `/jpspec:security deps` (dependencies)

### Potential New ADRs (To Be Written During Implementation)

**ADR-010: Security Policy Engine Design** (task-252)
- **Decision:** Policy-as-code with version control
- **Rationale:** Enterprise governance, compliance, exemption audit trail

**ADR-011: Fix Pattern Library Architecture** (task-213)
- **Decision:** Pattern-based fixes with AI fallback
- **Rationale:** High-quality fixes for common patterns, AI for edge cases

---

## Gaps and Concerns

### Identified Gaps

1. **Performance at Scale** (100K+ LOC codebases)
   - **Concern:** AI triage with 500+ findings may exceed 10-minute timeout
   - **Mitigation:** Implement incremental scanning (only changed files), parallel LLM requests
   - **Status:** Defer to v1.5, document limitation in v1.0

2. **Multi-Repo Dashboard** (Cross-Project View)
   - **Concern:** No way to aggregate security status across projects in v1.0
   - **Mitigation:** Implement MCP server (ADR-008) in v2.0 for cross-repo queries
   - **Status:** v2.0 feature, documented in roadmap

3. **Historical Trending** (Security Posture Over Time)
   - **Concern:** No way to track security improvements/regressions over time
   - **Mitigation:** Store scan results with timestamps, implement trend analysis in v1.5
   - **Status:** v1.5 feature, current focus is point-in-time analysis

4. **IDE Integration** (Real-Time Vulnerability Highlighting)
   - **Concern:** Developers want in-editor feedback, not separate CLI
   - **Mitigation:** Implement VS Code extension using MCP server (v2.0)
   - **Status:** v2.0 feature, provide CLI workflow in v1.0

5. **Dependency Scanning Integration** (task-198 Coordination)
   - **Concern:** Overlap/confusion between /jpspec:security scan and task-198
   - **Mitigation:** Clear documentation (ADR-009), coordinated commands
   - **Status:** task-220 addresses this, ADR-009 exists

### Concerns for Product Owner

1. **LLM API Costs at Scale**
   - **Question:** What is acceptable $/scan budget for enterprise?
   - **Recommendation:** Set target at <$0.50/scan (50 findings), monitor actual costs

2. **False Positive Rate Tolerance**
   - **Question:** Is 15% false positive rate acceptable (85% accuracy)?
   - **Recommendation:** Start at 85%, aim for 90% in v1.5 with feedback loop

3. **Fix Application Risk**
   - **Question:** Should auto-apply be enabled by default or require flag?
   - **Recommendation:** Dry-run by default, require `--apply` flag for safety

4. **Compliance Requirements**
   - **Question:** Which compliance frameworks are required (SOC2, ISO 27001, HIPAA)?
   - **Recommendation:** Support SOC2 and ISO 27001 in v1.0, HIPAA in v1.5

---

## Conclusion and Next Steps

This architecture plan consolidates 11 security tasks into a cohesive design based on established ADRs (005, 006, 007, 008, 009). The recommended implementation order prioritizes core AI capabilities (triage, fix generation) before configuration and integration.

### Key Architectural Principles Applied

1. **Composability** - Pluggable scanners, specialized classifiers, multi-format exports
2. **Consistency** - Unified Finding Format (UFFormat) across all components
3. **Clarity** - Clear data flow: scan → triage → fix → report → integrate
4. **Correctness** - Extensive validation (benchmarking, syntax validation, confidence scores)
5. **Changeability** - Add scanners, classifiers, personas without breaking core

### Critical Success Factors

1. **AI Triage Accuracy >85%** - Task-280 benchmark is non-negotiable quality gate
2. **Fix Quality >75%** - Extensive pattern library + syntax validation
3. **Developer Trust** - Interactive mode, confidence scores, rollback mechanism
4. **Enterprise Governance** - Policy-as-code, exemptions, compliance reporting

### Immediate Next Actions

1. **Update Task Labels** - Mark all 11 tasks as `workflow:Planned` in backlog.md
2. **Commit Architecture Plan** - Push to `muckross-security-architecture` branch with DCO sign-off
3. **Create PR** - Open PR for review with summary of architectural decisions
4. **Begin Implementation** - Start with task-212 (AI Triage Engine) as foundation

**Architect Sign-Off:** This architecture plan is ready for implementation. Proceed with Phase 1 (Core AI Capabilities) upon PR approval.

---

## Appendix: Task Summary Table

| Task ID | Title | Priority | Effort | Phase | Dependencies |
|---------|-------|----------|--------|-------|--------------|
| task-212 | AI-Powered Vulnerability Triage Engine | HIGH | 17-26h | 1 | ADR-006, Anthropic SDK |
| task-221 | Security Expert Personas | HIGH | 15-21h | 1 | ADR-006, task-212 |
| task-280 | Benchmark AI Triage Engine Accuracy | HIGH | 23-31h | 1 | task-212 complete |
| task-213 | Automated Fix Generation and Patch Application | HIGH | 22-31h | 2 | task-212 |
| task-214 | Security Audit Report Generator | HIGH | 20-27h | 2 | task-212, task-213 |
| task-217 | Security Configuration System | MEDIUM | 10h | 3 | ADR-005 |
| task-252 | Security Policy as Code Configuration | MEDIUM | 12h | 3 | task-217 |
| task-223 | Custom Security Rules System | MEDIUM | 10h | 3 | ADR-005 |
| task-216 | Integrate /jpspec:security with Workflow and Backlog | HIGH | 12h | 3 | task-212, task-214 |
| task-218 | Write Comprehensive Security Commands Documentation | HIGH | 12h | 4 | All tasks complete |
| task-220 | Resolve Relationship with task-198 Unified Scanner | HIGH | 8h | 4 | ADR-009 |

**Total Estimated Effort:** 161-213 hours (22-30 days)
**Timeline:** 5-8 weeks (depending on parallelization and engineer count)
