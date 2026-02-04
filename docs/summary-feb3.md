# Flowspec Simplification Summary - Feb 3, 2026

## Open GitHub Issues Validation

### Issue #1186 - [Bug] Flowspec init doesn't produce commands
**Status:** ✅ FIXED - PR #1201

**Problem:** Reporter claims `flowspec init my-project --ai claude` does not generate commands.

**Root Cause Identified (Feb 4):**
The issue was **NOT** about commands deployment - that works correctly. The actual bug was a **Windows Unicode encoding crash** in the banner display:

- Windows terminals using legacy `cp1252` encoding cannot display Unicode box-drawing characters (█, ╔, ═, etc.)
- When `flowspec init` tried to display the banner via Rich, it crashed with `UnicodeEncodeError`
- The crash happened **before** template deployment, making it appear commands weren't created
- On macOS/Linux with UTF-8, the banner displays correctly so the issue wasn't reproducible

**Fix Applied (PR #1201):**
1. Added `BANNER_ASCII` constant - figlet-style ASCII fallback banner
2. Added `_can_encode_unicode()` helper - detects encoding support upfront
3. Modified `show_banner()` to select appropriate banner based on encoding
4. Handles edge cases: stdout None, encoding None/empty, TypeError for non-string encoding
5. Added 15 comprehensive tests in `tests/test_banner_encoding.py`

**Validation:**
- ✅ Commands deployment verified working via direct Python test
- ✅ ASCII banner displays correctly on Windows cp1252
- ✅ All 15 CI checks pass
- ✅ Copilot review approved

---

### Issue #1187 - [Feature] Consolidate all flowspec config files into .flowspec directory
**Status:** VALID - MEDIUM PRIORITY

**Problem:** Flowspec configuration is scattered across 15+ directories:
- `.claude/commands/`, `.claude/skills/`, `.claude/agents/`, `.claude/hooks/`, `.claude/rules/`
- `memory/`, `logs/`, `docs/prp/`, `security-rules/`, `partials/`
- `.flowspec/` (already exists but underutilized)

**Impact:**
- New project setup requires copying many directories
- Hard to understand what belongs to flowspec vs. project-specific
- Difficult to upgrade flowspec in existing projects
- No single location for gitignore rules

**Proposed Structure:**
```
.flowspec/
├── workflow.yml          # State machine config
├── agents/               # Agent definitions
├── commands/             # Slash commands
├── hooks/                # Hook scripts
├── skills/               # Model-invoked skills
├── memory/               # Constitution, repo-facts
├── rules/                # Always-follow guidelines
├── logs/                 # Generated content
└── templates/            # PRP templates
```

**Considerations:**
- Breaking change - needs migration path
- Some tools expect `.claude/` directory
- Could make flowspec-specific vs Claude Code-standard clearer

---

## Simplification Opportunities from everything-claude-code

### 1. CRITICAL: Command File Bloat
**Flowspec:** 10,963 lines across 28 command files
**everything-claude-code:** ~25 smaller command files, typically 50-300 lines each

| Flowspec Command | Lines | ECC Equivalent | Lines |
|------------------|-------|----------------|-------|
| `/flow:validate` | 1,735 | `/verify` | ~40 |
| `/flow:submit-n-watch-pr` | 1,037 | N/A | - |
| `/flow:plan` | 600+ | `/plan` | 114 |
| `/flow:tdd` | 407 | `/tdd` | 327 |

**Action Items:**
- [ ] Slim `/flow:validate` from 1,735 to <200 lines
- [ ] Slim `/flow:submit-n-watch-pr` from 1,037 to <300 lines
- [ ] Extract common patterns to partials/includes
- [ ] Remove verbose inline examples from commands
- [ ] Task #583 (SPEC-012) already targets <100 lines per agent - apply to commands

### 2. Cross-Platform Hooks (Windows Support)
**Flowspec:** Bash/Python hooks that fail on Windows
**everything-claude-code:** Node.js hooks with cross-platform support

**everything-claude-code approach:**
```javascript
// Single hooks.json file with inline Node.js
{
  "hooks": [{
    "type": "command",
    "command": "node -e \"const fs=require('fs');...\""
  }]
}
```

**Action Items:**
- [ ] Convert `.claude/hooks/*.sh` to Node.js (task #600 - SPEC-008)
- [ ] Convert `.claude/hooks/*.py` to Node.js
- [ ] Single `hooks.json` instead of multiple script files
- [ ] Add package manager detection for npm/pnpm/yarn/bun

### 3. ARCHITECTURAL: Remove Security Skills from Flowspec
**Flowspec:** 22 skill directories - **11 are security-related** (50%!)
**everything-claude-code:** 28 skill directories (domain-focused patterns)

**Problem:** Flowspec is a Spec-Driven Development workflow toolkit. Security scanning/analysis is a **completely separate domain** that does not belong here.

**Security skills that MUST be removed from flowspec core:**
- `security-analyst`, `security-fixer`, `security-reporter`, `security-reviewer`
- `security-triage`, `security-workflow`, `security-codeql`, `security-custom-rules`
- `security-dast`, `exploit-researcher`, `fuzzing-strategist`, `patch-engineer`

**Where they should go:**
1. **Separate package:** `flowspec-security` or `speckit-security`
2. **Optional MCP server:** Security tools as MCP integration
3. **Dedicated project:** Move to `ps/dev-guard` (already planned in prj portfolio)

**Action Items:**
- [ ] **MOVE 12 security skills** to `ps/dev-guard/` (park for later use)
- [ ] **MOVE 5 security commands** to `ps/dev-guard/`
- [ ] **MOVE security templates** to `ps/dev-guard/`
- [ ] Update flowspec templates to NOT include security content
- [ ] Add pattern-based skills from ECC: `coding-standards/`, `backend-patterns/`
- [ ] Later: Create `flowspec-security` plugin that pulls from `ps/dev-guard`

### 4. Continuous Learning Integration
**everything-claude-code approach:**
- Stop hook extracts patterns at session end
- Saves to `~/.claude/skills/learned/`
- Confidence scoring on extracted patterns
- `/learn` command for mid-session extraction

**Flowspec status:** Has `/flow:learn` (task #598) but not yet production-ready

**Action Items:**
- [ ] Complete `/flow:learn` implementation
- [ ] Add Stop hook for automatic pattern extraction
- [ ] Create `~/.flowspec/learned/` directory for extracted patterns

### 5. Agent Simplification
**Flowspec agents:** 559 total lines (already lean)
**everything-claude-code agents:** 5,104 total lines (more verbose)

**Flowspec is ahead here.** The ECC agents include full example outputs inline, which bloats them. Flowspec's approach of referencing skills/examples is better.

### 6. MCP Context Management
**everything-claude-code advice:**
> "Your 200k context window can shrink to 70k with too many tools enabled."
> "Have 20-30 MCPs configured, but keep under 10 enabled / under 80 tools active."

**Action Items:**
- [ ] Add MCP health check to `flowspec init` (was in #579.15 - archived)
- [ ] Document recommended MCP configuration
- [ ] Add `disabledMcpServers` guidance to CLAUDE.md template

---

## Priority Task List

### P0 - Critical (Bug Fix)
1. ~~**Investigate #1186**: Works on macOS, may be Windows-specific~~ ✅ **FIXED (PR #1201)**
   - Root cause: Windows Unicode encoding crash in banner display (cp1252 can't encode █, ╔, ═)
   - Fix: ASCII fallback banner with encoding detection
   - 15 comprehensive tests added

### P1 - High Priority (Simplification)
2. **Slim command files** to <200 lines each
   - Start with `/flow:validate` (1,735 → 200 lines)
   - Extract verbose examples to separate docs
   - Use partials for common patterns

3. **Convert hooks to Node.js** for cross-platform
   - Priority: session-start, pre-tool-use guards
   - Single hooks.json vs multiple scripts

### P2 - Medium Priority (Architecture)
4. **Evaluate .flowspec consolidation** (#1187)
   - Design migration path
   - Consider Claude Code plugin compatibility
   - Create RFC/ADR for directory structure

5. **MOVE all security content to `ps/dev-guard/`** (park for separate package)
   - Move 12 security skills from `.claude/skills/` → `ps/dev-guard/skills/`
   - Move 5 security commands → `ps/dev-guard/commands/`
   - Move security templates → `ps/dev-guard/templates/`
   - Update flowspec templates to exclude security content
   - Future: Create `flowspec-security` plugin that imports from dev-guard

### P3 - Nice to Have
6. **Complete `/flow:learn`** continuous learning
7. **Add MCP health check** to init
8. **Add pattern-based skills** (coding-standards, backend-patterns)

---

## Metrics to Track

| Metric | Current | Target |
|--------|---------|--------|
| Command lines (total) | 10,963 | <3,000 |
| Largest command file | 1,735 lines | <300 lines |
| Security skills in core | 12 | **0** (moved to ps/dev-guard) |
| Security commands in core | 5 | **0** (moved to ps/dev-guard) |
| Skills (SDD-focused) | 10 | 8-10 |
| Windows-compatible hooks | ~0% | 100% |
| Init produces commands | ✅ YES (PR #1201) | YES |

---

## Related Existing Tasks

- Task #583: SPEC-012 Slim agent definitions to <100 lines
- Task #600: SPEC-008 Convert hooks to Node.js
- Task #598: SPEC-004 Implement continuous learning
- Task #601: SPEC-009 Standalone flow-verify command
- Task #579.11: P1.5 Remove spec commands from templates

## Security Content Inventory (for separate package)

### Skills (12 total - MOVE to `flowspec-security` or `ps/dev-guard`)

| Skill | Purpose |
|-------|---------|
| `security-analyst` | OWASP expertise, CVSS scoring, compliance mapping (SOC2, ISO27001, PCI-DSS) |
| `security-codeql` | CodeQL SARIF interpretation, dataflow/taint analysis |
| `security-custom-rules` | Create custom Semgrep/Bandit rules for org-specific vulnerabilities |
| `security-dast` | Dynamic web app testing with Playwright (OWASP Top 10) |
| `security-fixer` | Generate patches for SQL injection, XSS, path traversal, CSRF |
| `security-reporter` | Audit reports, OWASP compliance checklists, executive summaries |
| `security-reviewer` | Code review for vulnerabilities, threat modeling, SLSA compliance |
| `security-triage` | AI triage of findings, risk scoring, false positive detection |
| `security-workflow` | Create backlog tasks from findings, CI/CD integration |
| `exploit-researcher` | Attack surface analysis, PoC exploits, vulnerability chaining |
| `fuzzing-strategist` | Fuzzing strategy, tool selection, crash analysis |
| `patch-engineer` | Security fix validation, regression prevention |

### Commands (5 total - MOVE to `flowspec-security`)

| Command | Purpose | Loop |
|---------|---------|------|
| `/flow:security_fix` | Generate and apply patches for TP findings | Inner |
| `/flow:security_report` | Comprehensive audit report for stakeholders | Outer |
| `/flow:security_triage` | AI-powered triage with personas | Both |
| `/flow:security_web` | DAST web app testing with Playwright | Both |
| `/flow:security_workflow` | Full security workflow (scan→triage→report→fix→tasks) | Both |

### Templates/Config to Move

- `templates/docs/security/` - Security doc templates
- `.flowspec/security-config.yml` - Scanner configuration
- Security-related workflow states in `flowspec_workflow.yml`

### Destination: `ps/dev-guard/`

**Recommended:** Park all security content in `ps/dev-guard/` (already planned in prj portfolio as "Developer security toolchain (shift-left)")

**Directory structure:**
```
ps/dev-guard/
├── skills/              # 12 security skills
├── commands/            # 5 security commands
├── templates/           # Security doc templates
├── config/              # Security scanner config
└── README.md            # How to use with flowspec
```

**Future options:**
1. **`flowspec-security` plugin** - Optional install that imports from dev-guard
2. **Claude Code Plugin** - Distribute via plugin marketplace
3. **Standalone package** - Independent security toolkit

**Estimated content:** ~70k lines of security-specific content

---

## Next Steps

1. **Today:** Create task for #1186 fix (P0)
2. **This week:** Start command slimming (P1)
3. **This sprint:** Node.js hook conversion (P1)
4. **Next sprint:** Evaluate consolidation approach (P2)
