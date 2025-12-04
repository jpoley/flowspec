# PRD: JP Spec Kit Platform & DevSecOps

**Related Tasks**: task-085, task-136, task-168, task-171, task-184, task-195, task-196, task-197, task-249

---

## Requirements Traceability Matrix

| Task ID | Task Title | Domain | Priority | Functional Req |
|---------|-----------|--------|----------|----------------|
| task-184 | Add permissions.deny Security Rules | Security Layer | High | FR-SEC-001, FR-SEC-002 |
| task-249 | Implement Tool Dependency Management Module | Tool Management | High | FR-TOOL-001 to FR-TOOL-005 |
| task-085 | Local CI Simulation Script | CI/CD | Medium | FR-CI-001, FR-CI-002, FR-CI-003 |
| task-168 | Add macOS CI Matrix Testing | CI/CD | Low | FR-CI-004 |
| task-136 | Add Primary Support for claude-trace Observability | Observability | Medium | FR-OBS-001, FR-OBS-002 |
| task-171 | Research library documentation MCP replacement | Developer Experience | Medium | FR-DX-001 |
| task-195 | Create JP Spec Kit Plugin Package | Developer Experience | Low | FR-DX-002 (deferred) |
| task-196 | Experiment with Output Styles for Workflow Phases | Developer Experience | Low | FR-DX-003 (exploratory) |
| task-197 | Create Custom Statusline with Workflow Context | Developer Experience | Low | FR-DX-004 (future) |

---

**Feature Group**: Platform Infrastructure, Security, Observability, CI/CD
**Created**: 2025-12-04
**Status**: Draft
**Strategic Focus**: Elite DORA Metrics, Security by Default, Developer Velocity First

## Executive Summary

### Problem Statement

JP Spec Kit users face several critical platform and developer experience challenges:

1. **Security Gaps**: No default protection against accidental exposure of sensitive files (.env, credentials, secrets) or destructive operations (sudo, rm -rf)
2. **Slow Feedback Loops**: Developers wait for GitHub Actions to discover CI failures (5-15 minutes), increasing lead time and reducing deployment frequency
3. **Limited Observability**: No visibility into AI agent decision-making, token usage, or workflow execution for debugging complex /jpspec commands
4. **Cross-Platform Fragility**: Scripts and tools may fail on macOS without testing, reducing developer experience
5. **Tool Management Overhead**: Manual installation of Semgrep, CodeQL, act creates friction and version inconsistency
6. **Missing Developer Tooling**: No packaging mechanism for easy distribution, unclear workflow phase visibility, inconsistent output formatting

These problems directly impact DORA metrics:
- **Lead Time**: Slow CI feedback increases lead time to >1 hour
- **Deployment Frequency**: Manual tool management and slow feedback reduce deployment frequency
- **Change Failure Rate**: Lack of local CI increases failures in production
- **MTTR**: Limited observability increases mean time to recovery

### Proposed Solution

Build a comprehensive platform infrastructure layer for JP Spec Kit that addresses security, observability, CI/CD, and developer experience:

**1. Security Layer** (High Priority)
- Default permissions.deny rules protecting sensitive files and blocking dangerous commands
- Audit logging for security-sensitive operations
- Override mechanism with user confirmation for legitimate exceptions

**2. Local CI/CD** (High Priority)
- act-based local GitHub Actions runner providing <1 minute feedback
- Cross-platform testing (Linux + macOS) ensuring environment parity
- Selective job execution for fast inner loop development

**3. Observability Foundation** (Medium Priority)
- claude-trace integration for debugging complex workflows
- Token usage tracking and performance profiling
- Troubleshooting guides with concrete examples

**4. Tool Dependency Management** (High Priority)
- Auto-installation of Semgrep, CodeQL, act with version pinning
- Cache management with size monitoring and LRU eviction
- Offline mode support for air-gapped environments

**5. Developer Experience** (Low Priority, Future)
- Plugin packaging for easy distribution
- Custom output styles for workflow phases (PM, Architect, QA personas)
- Statusline showing workflow context and progress
- Library documentation MCP integration

### Success Metrics

**North Star Metric**: Developer Velocity Score = (Deployments/Day) × (1 - Failure Rate) × (1 / MTTR Hours)
- **Target**: Elite DORA (10 deploys/day, <15% failure rate, <1hr MTTR) = 8.5+ velocity score
- **Current Baseline**: ~2 deploys/day, ~20% failure rate, 2hr MTTR = 0.8 velocity score
- **Expected Impact**: 10x improvement in developer velocity

**Key Outcomes**:
1. **Lead Time**: <1 hour (Elite) - enabled by local CI feedback
2. **Deployment Frequency**: 5-10/day (Elite) - enabled by fast, secure inner loop
3. **Change Failure Rate**: <15% (Elite) - enabled by local CI catching issues pre-push
4. **MTTR**: <1 hour (Elite) - enabled by observability and debugging tools

### Business Value and Strategic Alignment

**Strategic Alignment**:
- **Security by Default** principle: Prevent security incidents through default-deny policies
- **Developer Velocity First** principle: Fast feedback loops enable rapid iteration
- **Observable by Default** principle: Built-in debugging and profiling capabilities
- **Environment Parity** principle: Local dev matches CI/CD for consistency
- **Composability Over Monoliths** principle: Small, focused tools with clear interfaces

**Business Value**:
1. **Risk Reduction**: Security defaults prevent accidental exposure of secrets and credentials
2. **Cost Savings**: Local CI reduces GitHub Actions costs by 60-80%
3. **Productivity Gains**: <1 min local feedback vs 5-15 min remote CI = 5-15x faster inner loop
4. **Quality Improvement**: Local testing catches issues earlier, reducing production failures
5. **Platform Maturity**: Tool packaging enables community adoption and contribution

## User Stories and Use Cases

### Primary User Personas

**Persona 1: Solo Developer (Sarah)**
- Uses JP Spec Kit for personal projects
- Works on laptop, often offline or with limited connectivity
- Needs fast feedback and minimal setup friction
- Values security defaults to avoid mistakes

**Persona 2: Team Lead (Tom)**
- Uses JP Spec Kit for team projects (3-5 developers)
- Responsible for CI/CD, security, and code quality standards
- Needs observability for debugging team workflow issues
- Values cross-platform compatibility (team uses mix of Linux/macOS)

**Persona 3: Platform Engineer (Patricia)**
- Evaluating JP Spec Kit for enterprise adoption
- Needs air-gapped/offline support for regulated environments
- Requires audit logging and security compliance
- Values plugin packaging for controlled distribution

### User Journey Maps

#### Journey 1: Fast Inner Loop Development (Sarah - P1)

**Context**: Sarah is implementing a new feature. She wants to catch linting, testing, and security issues before pushing to GitHub to avoid CI failure embarrassment and delays.

**Current Pain Points**:
- Push to GitHub, wait 5-15 minutes for CI
- CI fails on linting issue she could have caught locally
- Fixes issue, pushes again, waits another 5-15 minutes
- Total wasted time: 10-30 minutes per iteration

**Desired Journey**:
1. Sarah makes code changes
2. Runs `scripts/bash/run-local-ci.sh`
3. Receives feedback in <1 minute (lint, test, security checks)
4. Fixes issues immediately
5. Re-runs local CI until passing
6. Pushes to GitHub with confidence (CI passes first time)

**Value**: 10-30 minutes saved per development iteration, 5-15x faster feedback

---

#### Journey 2: Protected from Security Mistakes (Sarah - P1)

**Context**: Sarah is debugging a feature and wants to inspect environment variables. She accidentally tries to commit .env file or runs a destructive command.

**Current Pain Points**:
- No protection against committing .env files
- No protection against dangerous bash commands
- Easy to accidentally expose secrets in git history
- Cleanup requires git history rewriting

**Desired Journey**:
1. Sarah tries to read .env file via Claude Code
2. System blocks read with clear error: "Access denied: .env protected by permissions.deny"
3. Sarah tries to run `sudo rm -rf /tmp/cache`
4. System blocks command with warning: "Dangerous command blocked: sudo"
5. Sarah learns safe alternatives from error messages

**Value**: Prevents security incidents, protects against data loss, educates on safe practices

---

#### Journey 3: Debugging Complex Workflows (Tom - P2)

**Context**: Tom's team is using /jpspec:implement but the workflow is failing mysteriously. He needs to understand what the AI agents are doing and why.

**Current Pain Points**:
- No visibility into AI agent decision-making
- Can't see which tools were invoked or their outputs
- Token usage unknown, can't optimize
- Trial-and-error debugging wastes hours

**Desired Journey**:
1. Tom runs `/jpspec:implement` with claude-trace enabled
2. Workflow fails partway through
3. Tom opens claude-trace web UI
4. Reviews trace: sees exact prompt templates, tool calls, LLM responses
5. Identifies issue: agent is missing context from spec.md
6. Fixes spec.md, re-runs successfully
7. Reviews token usage report, optimizes prompt templates

**Value**: Hours saved on debugging, actionable insights for optimization

---

#### Journey 4: Cross-Platform Team Development (Tom - P2)

**Context**: Tom's team uses mix of Linux (3 developers) and macOS (2 developers). Scripts that work on Linux fail on macOS, causing frustration.

**Current Pain Points**:
- run-local-ci.sh works on Linux but untested on macOS
- macOS developers can't use local CI
- Platform-specific bash issues cause failures
- Team productivity reduced by platform fragmentation

**Desired Journey**:
1. Tom adds macOS to CI matrix
2. CI automatically tests run-local-ci.sh on both platforms
3. Discovers macOS-specific issue (bash version difference)
4. Fixes script to use portable POSIX features
5. Both platforms now supported equally
6. macOS developers can use local CI

**Value**: Team productivity parity, reduced platform-specific bugs

---

#### Journey 5: Tool Installation and Management (Patricia - P2)

**Context**: Patricia is evaluating JP Spec Kit for enterprise use. She needs to run security scans (Semgrep, CodeQL) but doesn't want to manually install tools or manage versions.

**Current Pain Points**:
- Must manually install Semgrep (pip install)
- Must manually download CodeQL (license check required)
- Version mismatches cause inconsistent results
- No offline support for air-gapped environments
- Tool cache grows unbounded, consuming disk space

**Desired Journey**:
1. Patricia runs `/jpspec:validate` (includes security scanning)
2. System detects Semgrep not installed
3. System auto-installs Semgrep 1.87.0 (pinned version)
4. System checks CodeQL license, downloads if licensed
5. System caches tools in ~/.cache/specify/tools/ (with 500MB limit)
6. Subsequent runs use cached tools (fast)
7. Patricia can enable offline mode for air-gapped deployment

**Value**: Zero-friction tool adoption, consistent versions, predictable disk usage

---

#### Journey 6: Community Plugin Distribution (Patricia - P3)

**Context**: Patricia wants to package JP Spec Kit as a Claude Code plugin for easy distribution to her 50-person engineering team.

**Current Pain Points**:
- Must manually copy .claude/ directories
- Configuration inconsistencies across team
- Difficult to version and update
- No marketplace distribution

**Desired Journey**:
1. Patricia runs plugin packaging command
2. System creates .claude-plugin/ with manifest.json
3. Patricia tests plugin installation locally
4. Patricia publishes plugin to GitHub releases
5. Team members install via `/plugin install jp-spec-kit`
6. Automatic updates via plugin manager

**Value**: Streamlined enterprise adoption, version control, easy updates

---

### Edge Cases

**Security Edge Cases**:
- What happens when user legitimately needs to read .env for debugging? → Override mechanism with confirmation
- How does system handle .env.example vs .env? → .env.* pattern covers all variants
- What if user needs to run sudo for legitimate reasons? → Explicit override flag with warning
- How are permissions enforced across different tools (Bash, Read, Edit)? → Unified permission checker

**CI/CD Edge Cases**:
- What happens when act is not installed and auto-install fails? → Clear error with manual install instructions
- How does system handle Docker daemon not running? → Check before running, error with actionable message
- What if GitHub Actions uses features act doesn't support (OIDC)? → Document limitations, graceful degradation
- How does macOS handle act's Docker requirement? → Document Docker Desktop requirement

**Tool Management Edge Cases**:
- What happens when tool download fails (network issue)? → Retry with exponential backoff, fallback to manual
- How does system handle corrupted cache? → Checksum validation, auto-repair or re-download
- What if cache exceeds 500MB limit? → Alert user, LRU eviction policy for oldest tools
- How does offline mode work when tool not cached? → Clear error, instructions for pre-caching

**Observability Edge Cases**:
- What if claude-trace is not installed? → Documentation only, not required dependency
- How does system handle claude-trace indexing hangs (Issue #46)? → Document workaround, link to upstream issue
- What about PII in traces? → Document privacy concerns, recommend local-only usage
- How long to retain traces? → User configurable, recommend 7-day retention

## DVF+V Risk Assessment

### Value Risk (Desirability)

**Question**: Will developers actually use these platform features?

**Validation Plan**:
1. **Developer Interviews** (n=10): Survey existing JP Spec Kit users about pain points
   - Questions: How long does your CI typically take? How often do you accidentally commit secrets?
2. **Usage Analytics**: Track adoption rates of local CI script after implementation
   - Target: 60% of active users run local CI at least once per week
3. **Feedback Collection**: GitHub Discussions post-launch
   - Target: Positive sentiment >70%, feature requests for enhancements

**High-Risk Areas**:
- Local CI adoption depends on Docker availability (not universal)
- claude-trace value unclear for simple workflows (may only help power users)
- Plugin packaging low value until community grows

**Mitigation**:
- Graceful degradation when Docker unavailable
- Make claude-trace optional, documentation-only
- Defer plugin packaging (P3) until demonstrated demand

### Usability Risk (Experience)

**Question**: Can users figure out how to use these tools effectively?

**Validation Plan**:
1. **Usability Testing**: 5 users attempt to run local CI without instructions
   - Target: 80% successfully run local CI on first try
2. **Documentation Review**: Technical writer reviews all docs for clarity
   - Target: All commands have examples, error messages have solutions
3. **Onboarding Flow**: New user runs `specify init`, receives setup guidance
   - Target: 90% complete initial setup without asking for help

**High-Risk Areas**:
- act installation and Docker setup (complex for non-DevOps users)
- claude-trace setup (npm install, SQLite dependencies)
- Understanding permissions.deny errors (could be cryptic)

**Mitigation**:
- Detailed error messages with actionable solutions
- Auto-install scripts for act and claude-trace
- Permission errors include examples of correct usage

### Feasibility Risk (Technical)

**Question**: Can we build this with available time, skills, and technology?

**Validation Plan**:
1. **Technical Spike**: Prototype act integration in 2 days
   - Validate: Can we reliably run GitHub Actions locally?
2. **Architecture Review**: Security engineer reviews permissions.deny design
   - Validate: Is the security model sound?
3. **Cross-Platform Testing**: Test on Linux (Ubuntu), macOS (M1/Intel), Windows (WSL)
   - Validate: Do scripts work on all target platforms?

**High-Risk Areas**:
- act has known limitations (OIDC, some GitHub Actions features)
- Permissions enforcement requires hooking multiple Claude Code APIs
- Tool version pinning complexity (Semgrep updates frequently)

**Mitigation**:
- Document act limitations clearly, don't promise 100% parity
- Start with file-based permissions (simple), expand to command blocking later
- Use versions.lock.json for reproducible tool versions

**Technical Constraints**:
- Requires Docker for act (not available in all environments)
- Requires Node.js 16+ for claude-trace (dependency)
- Requires Python 3.11+ for Semgrep (existing JP Spec Kit dependency)

### Business Viability Risk (Organizational)

**Question**: Does this work for all aspects of the business/project?

**Validation Plan**:
1. **Cost Analysis**: Calculate GitHub Actions savings from local CI adoption
   - Target: 60-80% reduction in CI minutes (ROI positive)
2. **Legal Review**: Ensure CodeQL licensing handled correctly
   - Validate: License check before download, compliance with terms
3. **Maintenance Impact**: Estimate ongoing maintenance burden
   - Target: <5 hours/month maintenance after initial implementation

**High-Risk Areas**:
- CodeQL licensing complexity (not free for all use cases)
- Tool version updates require ongoing maintenance
- Security model needs ongoing refinement based on user feedback

**Mitigation**:
- Automated license check for CodeQL, clear error if unlicensed
- Automated tool update checks (monthly), documented update process
- Security model designed for extension (add rules without code changes)

**Stakeholder Concerns**:
- **Solo Developers**: Worried about complexity and setup time
  - Mitigation: Zero-config defaults, auto-install, clear docs
- **Enterprise Users**: Need air-gapped support, audit logging
  - Mitigation: Offline mode, permissions audit log
- **Contributors**: Worried about maintenance burden
  - Mitigation: Simple designs, comprehensive tests, clear architecture docs

## Functional Requirements

### FR-001: Security Layer - File Protection

**FR-001.1**: System MUST block read access to .env and .env.* files via permissions.deny rules
**FR-001.2**: System MUST block write access to CLAUDE.md and memory/constitution.md via permissions.deny rules
**FR-001.3**: System MUST block write access to lock files (uv.lock, package-lock.json, Cargo.lock) via permissions.deny rules
**FR-001.4**: System MUST block read/write access to secrets/ directory via permissions.deny rules
**FR-001.5**: System MUST provide override mechanism requiring explicit user confirmation for blocked operations
**FR-001.6**: System MUST log all blocked access attempts to .claude/audit.log with timestamp, file, and reason

### FR-002: Security Layer - Command Protection

**FR-002.1**: System MUST block dangerous bash commands via permissions.deny rules:
- `sudo` (privilege escalation)
- `rm -rf /` and `rm -rf ~` (data destruction)
- `dd` with output to disk devices (data destruction)
- `mkfs` (filesystem formatting)

**FR-002.2**: System MUST provide safe alternatives in error messages (e.g., suggest `rm -i` instead of `rm -rf`)
**FR-002.3**: System MUST allow command override with explicit --force flag and warning
**FR-002.4**: System MUST log all blocked command attempts to .claude/audit.log

### FR-003: Local CI - Core Functionality

**FR-003.1**: System MUST provide scripts/bash/run-local-ci.sh for running GitHub Actions locally
**FR-003.2**: System MUST check for act installation and provide auto-install option if missing
**FR-003.3**: System MUST check for Docker daemon availability and provide clear error if unavailable
**FR-003.4**: System MUST support selective job execution (e.g., `run-local-ci.sh lint test`)
**FR-003.5**: System MUST run all jobs if no specific jobs specified
**FR-003.6**: System MUST fail fast on first job failure (don't continue if lint fails)
**FR-003.7**: System MUST complete full CI run (lint + test + build + security) in <5 minutes on typical hardware

### FR-004: Local CI - Jobs

**FR-004.1**: System MUST run lint job via act, executing ruff check, ruff format --check, and mypy
**FR-004.2**: System MUST run test job via act, executing pytest with coverage report
**FR-004.3**: System MUST run build job via act, executing uv build and twine check
**FR-004.4**: System MUST run security job via act, executing Semgrep SAST scan
**FR-004.5**: System MUST display job output in real-time for debugging
**FR-004.6**: System MUST provide --list flag to show available jobs without running

### FR-005: Local CI - Cross-Platform Support

**FR-005.1**: System MUST support Linux (Ubuntu 22.04+, Fedora 38+) for local CI
**FR-005.2**: System MUST support macOS (12.0+ Monterey) for local CI
**FR-005.3**: System MUST use POSIX-compliant bash 3.2+ features for broad compatibility
**FR-005.4**: System MUST document platform-specific requirements (Docker vs Docker Desktop)
**FR-005.5**: System MUST add macOS to GitHub Actions CI matrix for automated testing

### FR-006: Observability - claude-trace Integration

**FR-006.1**: System MUST provide documentation at docs/guides/claude-trace-integration.md
**FR-006.2**: Documentation MUST explain what claude-trace is and why it's valuable for SDD workflows
**FR-006.3**: Documentation MUST include installation instructions (npm install -g claude-trace, prerequisites)
**FR-006.4**: Documentation MUST include usage guide for capturing /jpspec:* command traces with examples
**FR-006.5**: Documentation MUST include troubleshooting for known issues (#46 indexing hangs, #48 native binaries)
**FR-006.6**: Documentation MUST include privacy and security guidance (PII risks, data retention)
**FR-006.7**: Documentation MUST include example trace analysis walkthrough for debugging failed workflows

### FR-007: Observability - Integration

**FR-007.1**: System MUST add claude-trace reference to CLAUDE.md troubleshooting section
**FR-007.2**: System MUST add claude-trace reference to docs/reference/outer-loop.md observability section
**FR-007.3**: System MUST document integration with backlog.md (task context in traces)
**FR-007.4**: Documentation MUST explain how claude-trace complements headless mode

### FR-008: Tool Dependency Management - Core

**FR-008.1**: System MUST implement ToolDependencyManager module for tool installation
**FR-008.2**: System MUST implement tool discovery chain: PATH → venv → cache → download
**FR-008.3**: System MUST cache downloaded tools in ~/.cache/specify/tools/
**FR-008.4**: System MUST support version pinning via versions.lock.json
**FR-008.5**: System MUST support offline mode (use cached tools only, no network)

### FR-009: Tool Dependency Management - Semgrep

**FR-009.1**: System MUST auto-install Semgrep via pip with pinned version (1.87.0+)
**FR-009.2**: System MUST check for Semgrep in virtualenv before system-wide installation
**FR-009.3**: System MUST validate Semgrep installation with `semgrep --version`

### FR-010: Tool Dependency Management - CodeQL

**FR-010.1**: System MUST check CodeQL license eligibility before download
**FR-010.2**: System MUST download CodeQL CLI from GitHub releases if licensed
**FR-010.3**: System MUST skip CodeQL if license check fails (optional tool)
**FR-010.4**: System MUST cache CodeQL binary in ~/.cache/specify/tools/codeql/

### FR-011: Tool Dependency Management - act

**FR-011.1**: System MUST auto-install act from GitHub releases if not found in PATH
**FR-011.2**: System MUST detect platform (Linux/macOS/Windows) and download appropriate binary
**FR-011.3**: System MUST validate act installation with `act --version`
**FR-011.4**: System MUST provide manual installation instructions if auto-install fails

### FR-012: Tool Dependency Management - Cache Management

**FR-012.1**: System MUST monitor cache size and alert if exceeding 500MB
**FR-012.2**: System MUST implement LRU (Least Recently Used) eviction policy for cache management
**FR-012.3**: System MUST preserve versions.lock.json pinned tools during eviction
**FR-012.4**: System MUST provide `specify tools clean` command to manually clear cache
**FR-012.5**: System MUST provide `specify tools list` command to show cached tools and versions

### FR-013: Developer Experience - MCP Library Documentation [NEEDS CLARIFICATION]

**FR-013.1**: System SHOULD identify at least 3 candidate MCP servers for library documentation
**FR-013.2**: System SHOULD evaluate candidates for: API key requirements, reliability, documentation coverage
**FR-013.3**: System SHOULD integrate selected MCP server into .mcp.json
**FR-013.4**: [NEEDS CLARIFICATION: Which libraries need coverage? Python stdlib? TypeScript? Rust? All?]
**FR-013.5**: [NEEDS CLARIFICATION: Is API-key-free requirement mandatory or just preferred?]

### FR-014: Developer Experience - Plugin Packaging (Future)

**FR-014.1**: System MAY create .claude-plugin/ directory structure for plugin distribution
**FR-014.2**: System MAY create manifest.json with plugin metadata (name, version, author)
**FR-014.3**: Plugin MAY include commands, skills, hooks, and default settings
**FR-014.4**: System MAY support plugin installation via `/plugin install jp-spec-kit`
**FR-014.5**: [FUTURE: Not required for MVP, deferred to P3]

### FR-015: Developer Experience - Output Styles (Future)

**FR-015.1**: System MAY implement PM output style for /jpspec:specify (bullet points, user stories)
**FR-015.2**: System MAY implement Architect output style for /jpspec:plan (diagrams, ADRs, patterns)
**FR-015.3**: [FUTURE: Exploratory, implement only if value demonstrated]

### FR-016: Developer Experience - Custom Statusline (Future)

**FR-016.1**: System MAY provide statusline script showing workflow context
**FR-016.2**: Statusline MAY display: current workflow phase, active backlog task, AC progress, git branch
**FR-016.3**: [FUTURE: Nice-to-have, low priority]

### Key Entities

**Entity: Security Rule**
- **Represents**: A permissions.deny rule blocking file access or command execution
- **Key Attributes**: rule type (file/command), pattern (glob/regex), action (deny read/write/execute), override allowed (boolean)
- **Relationships**: Stored in .claude/settings.json, enforced by permission checker, logged to audit.log

**Entity: Tool Installation**
- **Represents**: An installed tool (Semgrep, CodeQL, act) with version and location
- **Key Attributes**: tool name, version, install path, install date, last used date
- **Relationships**: Tracked in versions.lock.json, cached in ~/.cache/specify/tools/, discovered by ToolDependencyManager

**Entity: CI Job**
- **Represents**: A GitHub Actions job executed locally via act
- **Key Attributes**: job name (lint/test/build/security), status (pass/fail), duration, output log
- **Relationships**: Defined in .github/workflows/ci.yml, executed by run-local-ci.sh, depends on Docker daemon

**Entity: Audit Log Entry**
- **Represents**: A record of blocked security operation
- **Key Attributes**: timestamp, operation type (file read/write, command), target (file path/command), reason (which rule blocked), user override (if any)
- **Relationships**: Appended to .claude/audit.log, queryable for security review

## Non-Functional Requirements

### Performance Requirements

**NFR-001**: Local CI full run (lint + test + build + security) MUST complete in <5 minutes on typical hardware (4-core, 8GB RAM)
**NFR-002**: Local CI lint job MUST complete in <30 seconds
**NFR-003**: Local CI test job MUST complete in <2 minutes
**NFR-004**: Tool auto-install (Semgrep, act) MUST complete in <1 minute on 10 Mbps connection
**NFR-005**: Permission checks MUST add <10ms overhead to file operations
**NFR-006**: Tool discovery (PATH → venv → cache) MUST complete in <100ms

### Scalability Requirements

**NFR-007**: Tool cache MUST support up to 10 different tools with 500MB total size limit
**NFR-008**: Audit log MUST support 10,000+ entries without performance degradation
**NFR-009**: Local CI MUST support repositories up to 100MB size without timeout

### Security Requirements

**NFR-010**: System MUST prevent privilege escalation via sudo blocking
**NFR-011**: System MUST prevent data destruction via rm -rf, dd, mkfs blocking
**NFR-012**: System MUST prevent secret exposure via .env, secrets/ blocking
**NFR-013**: System MUST log all security events to tamper-evident audit log
**NFR-014**: System MUST validate tool checksums before execution (prevent supply chain attacks)
**NFR-015**: System MUST use HTTPS for all tool downloads (prevent MITM attacks)

### Accessibility Requirements

**NFR-016**: All documentation MUST be written in plain language (8th-grade reading level)
**NFR-017**: All error messages MUST include actionable solutions
**NFR-018**: All scripts MUST support --help flag with usage examples
**NFR-019**: All CLI output MUST be machine-parseable (JSON mode for automation)

### Compliance Requirements

**NFR-020**: System MUST comply with CodeQL license terms (check eligibility before download)
**NFR-021**: System MUST comply with Docker license terms (document commercial use restrictions)
**NFR-022**: System MUST document data privacy for claude-trace (local-only, PII risks)

## Task Breakdown (Backlog Tasks)

**CRITICAL**: The following backlog tasks are created to implement this PRD. Each task maps to specific functional requirements and includes acceptance criteria, priority, and labels.

### Created Implementation Tasks

The following tasks already exist in backlog.md and implement this PRD:

- **task-184**: Add permissions.deny Security Rules to settings.json (Priority: HIGH, Labels: security, platform)
  - Implements: FR-001, FR-002, NFR-010, NFR-011, NFR-012, NFR-013
  - Dependencies: None

- **task-249**: Implement Tool Dependency Management Module (Priority: HIGH, Labels: platform, tools)
  - Implements: FR-008, FR-009, FR-010, FR-011, FR-012, NFR-014, NFR-015
  - Dependencies: None

- **task-085**: Local CI Simulation Script (Priority: MEDIUM, Labels: cicd, inner-loop)
  - Implements: FR-003, FR-004, NFR-001, NFR-002, NFR-003
  - Dependencies: task-249 (needs act auto-install)

- **task-168**: Add macOS CI Matrix Testing (Priority: LOW, Labels: cicd, platform)
  - Implements: FR-005
  - Dependencies: task-085 (needs run-local-ci.sh)

- **task-136**: Add Primary Support for claude-trace Observability Tool (Priority: MEDIUM, Labels: observability, docs)
  - Implements: FR-006, FR-007
  - Dependencies: None

- **task-171**: Research and integrate library documentation MCP replacement (Priority: MEDIUM, Labels: mcp, research)
  - Implements: FR-013 (partial - needs clarification)
  - Dependencies: None

- **task-195**: Create JP Spec Kit Plugin Package (Priority: LOW, Labels: distribution, future)
  - Implements: FR-014 (deferred)
  - Dependencies: All other tasks (needs stable platform first)

- **task-196**: Experiment with Output Styles for Workflow Phases (Priority: LOW, Labels: ux, exploratory)
  - Implements: FR-015 (exploratory)
  - Dependencies: None

- **task-197**: Create Custom Statusline with Workflow Context (Priority: LOW, Labels: ux, future)
  - Implements: FR-016 (nice-to-have)
  - Dependencies: None

### Task Prioritization and Dependencies

**P0 (High Priority - Must Have)**:
1. task-184: Security Layer (blocks security incidents)
2. task-249: Tool Management (enables other features)

**P1 (Medium Priority - Should Have)**:
3. task-085: Local CI (depends on task-249 for act install)
4. task-136: Observability (independent, documentation-only)
5. task-171: MCP Documentation (independent, research phase)

**P2 (Low Priority - Could Have)**:
6. task-168: macOS CI (depends on task-085)
7. task-195: Plugin Packaging (depends on all, future)
8. task-196: Output Styles (exploratory, may not implement)
9. task-197: Statusline (nice-to-have, lowest priority)

**Recommended Implementation Order**:
1. task-249 (Tool Management) - foundational
2. task-184 (Security Layer) - foundational
3. task-136 (claude-trace) - independent, documentation
4. task-171 (MCP Research) - independent, research
5. task-085 (Local CI) - builds on tool management
6. task-168 (macOS CI) - builds on local CI
7. task-195, 196, 197 (Future) - deferred to later releases

## Discovery and Validation Plan

### Learning Goals and Hypotheses

**Hypothesis 1: Local CI Adoption**
- **Claim**: Developers will adopt local CI if feedback is <1 minute (10x faster than remote)
- **Learning Goal**: Measure actual adoption rate and time savings
- **Success Criteria**: 60% of active users run local CI at least weekly

**Hypothesis 2: Security Defaults**
- **Claim**: Default-deny permissions will prevent security incidents without excessive friction
- **Learning Goal**: Measure blocked incidents vs. legitimate override requests
- **Success Criteria**: <10% of blocked operations require override

**Hypothesis 3: Tool Auto-Install**
- **Claim**: Auto-install reduces friction and increases tool adoption
- **Learning Goal**: Compare adoption rates (auto-install vs. manual)
- **Success Criteria**: 90% successful auto-installs, 80% adoption increase

**Hypothesis 4: Observability Value**
- **Claim**: claude-trace helps debug complex workflows faster
- **Learning Goal**: Measure time-to-resolution for workflow failures
- **Success Criteria**: 50% reduction in debugging time for complex workflows

### Validation Experiments

**Experiment 1: Local CI Usability Test (Week 1)**
- **Method**: 5 users attempt to run local CI without documentation
- **Metrics**: Success rate, time to first run, error messages encountered
- **Go/No-Go**: 80% success rate required to proceed

**Experiment 2: Security Rules Beta (Week 2)**
- **Method**: Enable permissions.deny for 10 beta users, collect feedback
- **Metrics**: Number of blocked operations, override requests, false positives
- **Go/No-Go**: <15% override rate required (most blocks are legitimate)

**Experiment 3: Tool Auto-Install Reliability (Week 3)**
- **Method**: Test auto-install on 20 different environments (Linux/macOS, various versions)
- **Metrics**: Success rate, failure modes, fallback documentation clarity
- **Go/No-Go**: 85% success rate required

**Experiment 4: claude-trace Adoption (Week 4-8)**
- **Method**: Document claude-trace, announce in community, track usage
- **Metrics**: Installation rate, trace captures, GitHub Discussions feedback
- **Go/No-Go**: Positive sentiment >60% (not all users need this)

### Go/No-Go Decision Points

**Checkpoint 1 (End of Week 2): Security Foundation**
- ✅ Go: Permissions.deny implementation complete, <15% override rate
- ❌ No-Go: High override rate (>30%) or major usability issues → redesign security model

**Checkpoint 2 (End of Week 4): CI/CD Platform**
- ✅ Go: Local CI <1 min feedback, 60%+ adoption, tool auto-install >85% success
- ❌ No-Go: Local CI slow (>2 min) or low adoption (<30%) → reassess value proposition

**Checkpoint 3 (End of Week 8): Full Platform Validation**
- ✅ Go: DORA metrics improving (lead time <1hr, deploy freq increasing), positive feedback
- ❌ No-Go: No measurable improvement or negative feedback → pivot strategy

## Acceptance Criteria and Testing

### Acceptance Test Scenarios

**Scenario 1: Security - Blocked File Access**
```
Given: User attempts to read .env file via Claude Code Read tool
When: Permission checker intercepts request
Then: Access denied with error: "permissions.deny: .env files blocked"
And: Event logged to .claude/audit.log with timestamp and reason
```

**Scenario 2: Security - Legitimate Override**
```
Given: User needs to read .env for legitimate debugging
When: User runs command with --override-permissions flag
Then: System prompts for confirmation: "Confirm access to .env? [y/N]"
And: User confirms 'y'
Then: Access granted, override logged to audit.log
```

**Scenario 3: Local CI - First Run Success**
```
Given: User has Docker running and no act installed
When: User runs scripts/bash/run-local-ci.sh
Then: System detects act missing, prompts: "Install act automatically? [Y/n]"
And: User accepts (default)
Then: act installed successfully
And: All CI jobs (lint, test, build, security) execute and pass
And: Total time <5 minutes
```

**Scenario 4: Local CI - Selective Job Execution**
```
Given: User wants to run only lint and test jobs
When: User runs scripts/bash/run-local-ci.sh lint test
Then: Only lint and test jobs execute (skip build and security)
And: Feedback time <2 minutes
```

**Scenario 5: Tool Management - Semgrep Auto-Install**
```
Given: Semgrep not installed on system
When: User runs /jpspec:validate (includes security scan)
Then: System detects Semgrep missing
And: System auto-installs Semgrep 1.87.0 via pip
And: Semgrep version recorded in versions.lock.json
And: Subsequent runs use cached Semgrep (no re-install)
```

**Scenario 6: Tool Management - Cache Size Alert**
```
Given: Tool cache size exceeds 500MB
When: User runs tool auto-install command
Then: System displays warning: "Cache size 520MB exceeds 500MB limit"
And: System suggests: "Run 'specify tools clean' to free space"
And: User can proceed or clean cache
```

**Scenario 7: Cross-Platform - macOS CI Success**
```
Given: GitHub Actions CI runs on ubuntu-latest and macos-latest matrix
When: Developer pushes commit
Then: CI passes on both Linux and macOS runners
And: run-local-ci.sh works identically on both platforms
```

**Scenario 8: Observability - claude-trace Debugging**
```
Given: /jpspec:implement workflow fails mysteriously
When: User reviews docs/guides/claude-trace-integration.md
And: User installs claude-trace via npm
And: User re-runs workflow with tracing enabled
Then: User opens claude-trace web UI
And: User sees exact prompts, tool calls, and LLM responses
And: User identifies root cause from trace data
```

### Definition of Done

**For Each Task**:
1. ✅ All acceptance criteria in task file checked
2. ✅ Unit tests pass with >80% coverage
3. ✅ Integration tests pass on Linux and macOS
4. ✅ Documentation updated (CLAUDE.md, relevant guides)
5. ✅ Security review completed (for security-sensitive changes)
6. ✅ Manual testing on clean environment (validate auto-install)
7. ✅ No regressions (existing tests still pass)
8. ✅ Implementation notes added to task (what changed and why)

**For Full Platform Feature Group**:
1. ✅ All P0/P1 tasks complete (task-184, task-249, task-085, task-136, task-171)
2. ✅ DORA metrics baseline established and improving
3. ✅ Security defaults preventing incidents (audit log shows blocked attempts)
4. ✅ Local CI adoption >60% of active users
5. ✅ Tool auto-install success rate >85%
6. ✅ Comprehensive documentation published
7. ✅ Community feedback collected and positive (>70% sentiment)
8. ✅ Platform stable for 2 weeks (no critical bugs)

### Quality Gates

**Pre-Implementation Gates**:
- ✅ PRD reviewed and approved by stakeholders
- ✅ Security model reviewed by security engineer
- ✅ Architecture design documented (ADR-013 for tools, ADR-014 for security)
- ✅ Cross-platform compatibility plan documented

**During Implementation Gates**:
- ✅ Each task passes acceptance test scenarios before marking Done
- ✅ Code review completed by another developer
- ✅ Security-sensitive changes reviewed by security engineer
- ✅ Documentation peer-reviewed for clarity

**Post-Implementation Gates**:
- ✅ All quality gates from Definition of Done met
- ✅ Beta users provide feedback (minimum 10 users, 7-day trial)
- ✅ No P0/P1 bugs in issue tracker
- ✅ Rollout plan documented (gradual rollout, rollback plan)

### Test Coverage Requirements

**Unit Tests**:
- 80% code coverage for ToolDependencyManager module
- 80% code coverage for permission checker module
- 100% coverage for security-critical code paths (permission enforcement)

**Integration Tests**:
- Local CI script execution on Linux (Ubuntu 22.04, 24.04)
- Local CI script execution on macOS (12.0 Monterey, 13.0 Ventura)
- Tool auto-install on clean environments (no tools pre-installed)
- Permission enforcement across Read, Edit, Write, Bash tools

**End-to-End Tests**:
- Full /jpspec:validate workflow with auto-installed Semgrep
- Full /jpspec:implement workflow with local CI pre-push validation
- Security incident prevention (attempt to commit .env, blocked)

**Performance Tests**:
- Local CI full run <5 minutes (baseline hardware)
- Permission check overhead <10ms (benchmark)
- Tool discovery <100ms (benchmark)

## Dependencies and Constraints

### Technical Dependencies

**External Dependencies**:
- Docker (required for act, local CI)
  - Constraint: Not available in all environments (some CI runners, lightweight VMs)
  - Mitigation: Graceful degradation, clear error messages
- Node.js 16+ (required for claude-trace)
  - Constraint: Optional dependency, not required for core functionality
  - Mitigation: Documentation-only, users install if needed
- Python 3.11+ (existing JP Spec Kit requirement)
  - Constraint: Already required, not a new dependency

**Internal Dependencies**:
- task-249 (Tool Management) must complete before task-085 (Local CI)
  - Reason: Local CI needs act auto-install from tool manager
- task-085 (Local CI) must complete before task-168 (macOS CI)
  - Reason: macOS CI tests run-local-ci.sh

### External Dependencies

**Upstream Projects**:
- act (GitHub Actions local runner)
  - Risk: Upstream bugs, limited feature parity with GitHub Actions
  - Mitigation: Document limitations, contribute fixes upstream
- Semgrep (SAST scanner)
  - Risk: Frequent updates may break version pinning
  - Mitigation: Version locking via versions.lock.json, quarterly update reviews
- CodeQL (SAST scanner)
  - Risk: Licensing complexity, not free for all use cases
  - Mitigation: License check before download, make optional
- claude-trace (observability tool)
  - Risk: Known issues (#46 indexing, #48 native binaries)
  - Mitigation: Document workarounds, optional dependency

**GitHub Actions**:
- Dependency: .github/workflows/ci.yml defines jobs for local execution
- Risk: Changes to workflow file may break local CI
- Mitigation: Integration tests validate act compatibility

### Timeline Constraints

**Target Milestones**:
- Week 1-2: Security Layer (task-184, task-249)
- Week 3-4: Local CI (task-085) + Observability Docs (task-136)
- Week 5-6: macOS CI (task-168) + MCP Research (task-171)
- Week 7-8: Beta testing, bug fixes, documentation polish
- Week 9: Release Platform v1.0

**Critical Path**:
1. task-249 (Tool Management) - 1 week
2. task-184 (Security Layer) - 1 week (parallel with #1)
3. task-085 (Local CI) - 1.5 weeks (depends on #1)
4. task-168 (macOS CI) - 0.5 weeks (depends on #3)

Total: 4 weeks critical path, 8 weeks total with buffer

### Resource Constraints

**Development Resources**:
- 1 full-time developer (primary implementer)
- 1 part-time security reviewer (20% time)
- 1 part-time technical writer (20% time, documentation)
- 10 beta users for validation testing

**Infrastructure Resources**:
- GitHub Actions minutes: 2000 minutes/month free tier (sufficient for CI matrix)
- Storage: 500MB tool cache per user (acceptable)
- Network: Tool downloads (Semgrep ~50MB, CodeQL ~300MB, act ~20MB)

### Risk Factors

**High-Risk Factors**:
1. **Docker Availability**: Not universal, limits local CI adoption
   - Impact: High (blocks core feature)
   - Probability: Medium (most developers have Docker)
   - Mitigation: Graceful degradation, clear requirements doc

2. **Cross-Platform Compatibility**: Bash scripts may break on macOS
   - Impact: High (breaks macOS users)
   - Probability: Low (using POSIX features)
   - Mitigation: CI matrix testing, extensive platform testing

3. **Tool Version Drift**: Semgrep updates frequently, may break pinning
   - Impact: Medium (inconsistent results)
   - Probability: Medium (quarterly updates)
   - Mitigation: versions.lock.json, automated update testing

**Medium-Risk Factors**:
4. **act Feature Parity**: Some GitHub Actions features unsupported
   - Impact: Medium (some workflows can't run locally)
   - Probability: High (known limitation)
   - Mitigation: Document limitations, focus on common cases (lint/test/build)

5. **CodeQL Licensing**: Complex terms, may not be eligible
   - Impact: Low (CodeQL optional)
   - Probability: Medium (small projects usually eligible)
   - Mitigation: License check, graceful skip if unlicensed

**Low-Risk Factors**:
6. **claude-trace Adoption**: Users may not see value
   - Impact: Low (optional tool)
   - Probability: Medium (power users only)
   - Mitigation: Documentation-only, no code dependencies

## Success Metrics (Outcome-Focused)

### North Star Metric

**Developer Velocity Score** = (Deployments/Day) × (1 - Failure Rate) × (1 / MTTR Hours)

**Current Baseline**: 0.8
- 2 deploys/day
- 20% failure rate
- 2 hour MTTR

**Target (Elite DORA)**: 8.5+
- 10 deploys/day
- 15% failure rate
- 1 hour MTTR

**Measurement Approach**:
- Track deployments via GitHub releases API
- Track failures via CI status (passed/failed commits)
- Track MTTR via GitHub Issues (time from bug report to fix deployed)

### Leading Indicators (Early Signals)

**LI-001: Local CI Adoption Rate**
- **Definition**: Percentage of active contributors running local CI at least weekly
- **Target**: 60% by Week 8
- **Measurement**: Usage analytics (local script execution logs)

**LI-002: Security Block Rate**
- **Definition**: Number of blocked security operations per user per week
- **Target**: 2-5 blocks/user/week (indicates protection working without excessive friction)
- **Measurement**: Audit log analysis

**LI-003: Tool Auto-Install Success Rate**
- **Definition**: Percentage of auto-install attempts that succeed
- **Target**: 85% success rate
- **Measurement**: Installation logs, error tracking

**LI-004: CI Feedback Time**
- **Definition**: Time from code change to CI feedback (local vs. remote)
- **Target**: Local <1 min (vs. remote 5-15 min) = 5-15x improvement
- **Measurement**: Timing logs in run-local-ci.sh

**LI-005: Documentation Engagement**
- **Definition**: Views and positive feedback on platform documentation
- **Target**: 100+ views, 70% positive sentiment by Week 8
- **Measurement**: GitHub Analytics, Discussions sentiment analysis

### Lagging Indicators (Final Outcomes)

**LG-001: Deployment Frequency**
- **Definition**: Number of production deployments per day
- **Baseline**: 2 deploys/day
- **Target**: 10 deploys/day (Elite DORA)
- **Measurement**: GitHub releases, git tags

**LG-002: Change Failure Rate**
- **Definition**: Percentage of deployments causing production failure
- **Baseline**: 20%
- **Target**: <15% (Elite DORA)
- **Measurement**: Ratio of failed CI runs to total deployments

**LG-003: Lead Time for Changes**
- **Definition**: Time from commit to production deployment
- **Baseline**: 2-4 hours
- **Target**: <1 hour (Elite DORA)
- **Measurement**: Git commit timestamp to release timestamp

**LG-004: Mean Time to Recovery (MTTR)**
- **Definition**: Average time from failure detection to fix deployed
- **Baseline**: 2 hours
- **Target**: <1 hour (Elite DORA)
- **Measurement**: Issue creation to closing with fix deployed

**LG-005: Security Incident Prevention**
- **Definition**: Number of potential security incidents blocked by permissions.deny
- **Target**: >50 blocks over 8 weeks (indicates real value)
- **Measurement**: Audit log analysis (blocked .env access, sudo attempts, etc.)

### Target Values and Timelines

| Metric | Baseline | Week 4 Target | Week 8 Target | Elite Target |
|--------|----------|---------------|---------------|--------------|
| Developer Velocity Score | 0.8 | 2.0 | 5.0 | 8.5+ |
| Deployment Frequency | 2/day | 4/day | 7/day | 10/day |
| Change Failure Rate | 20% | 18% | 15% | <15% |
| Lead Time | 2-4 hrs | 1-2 hrs | <1 hr | <1 hr |
| MTTR | 2 hrs | 1.5 hrs | 1 hr | <1 hr |
| Local CI Adoption | 0% | 30% | 60% | 80%+ |
| Auto-Install Success | N/A | 80% | 85% | 90%+ |
| CI Feedback Time | 5-15 min | 2 min | <1 min | <1 min |

## Appendix: Platform Principles

### 1. Security by Default

**Principle**: Prevent security incidents through default-deny policies rather than relying on user vigilance.

**Application**:
- Block .env, secrets/ by default (prevent secret exposure)
- Block sudo, rm -rf by default (prevent privilege escalation, data loss)
- Require explicit override for exceptions (friction for dangerous operations)
- Audit log all security events (detective control)

**Trade-offs**:
- Pro: Prevents mistakes, protects against accidents
- Con: May block legitimate operations, requires override mechanism

### 2. Developer Velocity First

**Principle**: Optimize for fast feedback loops and minimal friction in the inner development loop.

**Application**:
- Local CI <1 min feedback (vs. 5-15 min remote)
- Auto-install tools (vs. manual setup)
- Selective job execution (run only what you need)
- Fail-fast on errors (don't waste time on dependent jobs)

**Trade-offs**:
- Pro: Faster iteration, higher productivity
- Con: Requires Docker (additional dependency)

### 3. Observable by Default

**Principle**: Built-in debugging and profiling capabilities for troubleshooting complex workflows.

**Application**:
- claude-trace integration for workflow debugging
- Audit logs for security events
- Performance metrics (CI timing, token usage)
- Clear error messages with actionable solutions

**Trade-offs**:
- Pro: Faster debugging, better insights
- Con: Additional documentation, optional dependencies

### 4. Environment Parity

**Principle**: Local development environment should match CI/CD for consistent behavior.

**Application**:
- Local CI runs same jobs as GitHub Actions (act)
- Cross-platform testing (Linux + macOS CI matrix)
- Version pinning (versions.lock.json) for reproducibility
- Tool caching for offline support

**Trade-offs**:
- Pro: Catch issues earlier, consistent results
- Con: Requires Docker, some features unsupported by act

### 5. Composability Over Monoliths

**Principle**: Small, focused tools with clear interfaces rather than monolithic frameworks.

**Application**:
- Modular tool management (ToolDependencyManager)
- Optional dependencies (claude-trace, CodeQL)
- Plugin packaging for distribution
- Clear separation: security layer, CI layer, tool layer

**Trade-offs**:
- Pro: Flexibility, easier maintenance, optional features
- Con: More integration points, potential for inconsistency

---

**End of PRD**
