# Functional Spec: Platform & DevSecOps

**Related Tasks**: task-085, task-136, task-168, task-171, task-184, task-195, task-196, task-197, task-249
**PRD Reference**: `docs/prd/platform-devsecops-prd.md`

---

## Requirements Traceability Matrix

| Task ID | Functional Requirements | Use Cases |
|---------|------------------------|-----------|
| task-184 | FR-SEC-001, FR-SEC-002, FR-SEC-003 | UC-1 (Secret Protection) |
| task-249 | FR-TOOL-001 to FR-TOOL-005 | UC-5 (Tool Auto-Install) |
| task-085 | FR-CI-001, FR-CI-002, FR-CI-003 | UC-2 (Fast Inner Loop) |
| task-168 | FR-CI-004 | UC-4 (Cross-Platform) |
| task-136 | FR-OBS-001, FR-OBS-002 | UC-3 (Workflow Debugging) |
| task-171 | FR-DX-001 | Research phase |
| task-195 | FR-DX-002 | Deferred to P3 |
| task-196 | FR-DX-003 | Exploratory |
| task-197 | FR-DX-004 | Future enhancement |

---

**Feature Group**: Platform Infrastructure, Security, Observability, CI/CD
**Created**: 2025-12-04
**Status**: Draft

## Overview

This functional specification defines the behaviors, capabilities, and interactions required for the Platform & DevSecOps infrastructure layer. The platform provides:

1. **Security Layer**: Default-deny permissions preventing accidental exposure of sensitive files and blocking dangerous commands
2. **Local CI/CD**: Fast local feedback via act-based GitHub Actions execution
3. **Observability**: Debugging and profiling capabilities through claude-trace integration
4. **Tool Management**: Automated installation, version pinning, and caching for Semgrep, CodeQL, and act
5. **Developer Experience**: Enhanced workflow visibility and cross-platform compatibility

The platform enables Elite DORA metrics (10 deploys/day, <15% failure rate, <1hr MTTR) through fast feedback loops, security defaults, and comprehensive observability.

---

## Functional Requirements

### Domain 1: Security Layer

#### FR-SEC-001: File Protection via permissions.deny

**Purpose**: Prevent accidental exposure of sensitive files and protect critical configuration files.

**Input**:
- Claude Code tool invocation (Read, Write, Edit) targeting a file path
- File path pattern matching against deny rules

**Output**:
- **Success**: Tool operation proceeds (file not in deny list)
- **Blocked**: Error message with clear explanation and safe alternatives
- **Audit Log**: Entry written to `.claude/audit.log` with timestamp, file, reason

**Rules**:
1. Block read/write access to:
   - `.env` and `.env.*` (environment variable files)
   - `secrets/` directory (any file within)
   - Lock files (write only): `uv.lock`, `package-lock.json`, `Cargo.lock`, `poetry.lock`
   - Configuration files (write only): `CLAUDE.md`, `memory/constitution.md`, `.claude/settings.json`

2. Pattern matching:
   - Glob patterns for file paths: `**/.env`, `**/.env.*`, `**/secrets/**`
   - Case-sensitive matching
   - Absolute and relative path resolution

3. Override mechanism:
   - User must explicitly confirm blocked operation
   - Warning displayed explaining risks
   - Override logged to audit.log with justification

**Error Messages**:
```
Access denied: .env files are protected by permissions.deny

Reason: Environment files may contain API keys, passwords, and credentials.

Safe alternatives:
  - Use .env.example for documentation
  - Access variables via environment (os.getenv)
  - Override with explicit confirmation if absolutely necessary

To override: Respond with 'yes' to confirm access (will be logged)
```

**Exceptions**:
1. `.env.example` and `.env.template` are NOT blocked (documentation files)
2. Reading lock files is allowed (writing blocked to prevent manual edits)
3. User can override with explicit confirmation (logged)

---

#### FR-SEC-002: Command Protection via permissions.deny

**Purpose**: Prevent destructive operations and privilege escalation through dangerous bash commands.

**Input**:
- Bash tool command string
- Command pattern matching against deny rules

**Output**:
- **Success**: Command executes (not in deny list)
- **Blocked**: Error message with explanation and safe alternatives
- **Audit Log**: Entry written to `.claude/audit.log`

**Rules**:
1. Block commands:
   - `sudo` and `sudo *` (privilege escalation)
   - `rm -rf /` and `rm -rf ~` (recursive deletion of critical paths)
   - `rm -rf /*` and `rm -rf ~/*` (recursive deletion patterns)
   - `dd if=* of=/dev/*` (disk device overwrite)
   - `mkfs.*` (filesystem formatting)

2. Pattern matching:
   - Regex matching on full command string
   - Detect variations: `sudo -s`, `sudo su`, `rm -rf /tmp && rm -rf /`
   - Whitespace normalization

3. Override mechanism:
   - `--force-dangerous-command` flag required
   - User must confirm understanding of risks
   - Override logged with full command

**Error Messages**:
```
Dangerous command blocked: sudo

Reason: Privilege escalation can cause security issues and system instability.

Safe alternatives:
  - Run specific commands without sudo
  - Use Docker/containers for isolated operations
  - Document why elevated privileges are needed

To override: Add --force-dangerous-command flag and confirm
```

**Exceptions**:
1. Commands within quoted strings (e.g., documenting commands in text)
2. Commands in comments (e.g., `# Example: sudo apt install`)
3. User explicit override with `--force-dangerous-command`

---

#### FR-SEC-003: Audit Logging

**Purpose**: Maintain tamper-evident log of all security events for review and compliance.

**Input**:
- Security event (blocked file access, blocked command, override request)
- Event metadata (timestamp, user, file/command, reason, override status)

**Output**:
- Append-only log entry in `.claude/audit.log`

**Rules**:
1. Log format (JSON Lines):
   ```json
   {
     "timestamp": "2025-12-04T10:30:00Z",
     "event_type": "file_access_denied",
     "target": ".env",
     "tool": "Read",
     "reason": "permissions.deny rule: **.env",
     "override": false
   }
   ```

2. Log rotation:
   - Max size: 10MB per file
   - Keep last 5 rotated logs (50MB total)
   - Rotation triggers at 10MB boundary

3. Query capabilities:
   - Filter by event_type, target pattern, date range
   - Export to CSV for analysis
   - Summary reports (blocked events per day/week)

**Data Requirements**:
- Timestamp: ISO 8601 format (UTC)
- Event types: `file_access_denied`, `command_blocked`, `override_granted`
- Target: Full file path or command string
- Tool: Claude Code tool name (Read, Write, Edit, Bash)
- Reason: Which deny rule matched
- Override: Boolean (was user override granted?)

---

### Domain 2: Local CI/CD

#### FR-CI-001: Local GitHub Actions Execution

**Purpose**: Run CI pipeline locally using act for fast feedback (<1 minute vs 5-15 minutes remote).

**Input**:
- Script invocation: `scripts/bash/run-local-ci.sh [job1 job2 ...]`
- Optional: Specific job names (lint, test, build, security)
- GitHub Actions workflow definition: `.github/workflows/ci.yml`

**Output**:
- **Success**: All jobs pass, exit code 0
- **Failure**: First failing job stops execution, exit code 1
- **Job logs**: Real-time output to stdout
- **Summary**: Pass/fail status for each job executed

**Rules**:
1. Prerequisites validation:
   - Check if Docker daemon is running
   - Check if act is installed (if not, prompt for auto-install)
   - Check if workflow file exists

2. Job execution:
   - Default: Run all jobs if no arguments provided
   - Selective: Run only specified jobs if arguments given
   - Fail-fast: Stop on first job failure (don't continue pipeline)
   - Real-time: Stream job output to console

3. Job definitions (from `.github/workflows/ci.yml`):
   - **lint**: `ruff check .`, `ruff format --check`, `mypy src/`
   - **test**: `pytest tests/ -v --cov`
   - **build**: `uv build`, `twine check dist/*`
   - **security**: `semgrep scan --config auto`

4. Performance targets:
   - Lint job: <30 seconds
   - Test job: <2 minutes
   - Build job: <1 minute
   - Security job: <1 minute
   - Full pipeline: <5 minutes

**Error Messages**:
```
Error: Docker daemon is not running

act requires Docker to run GitHub Actions containers locally.

Steps to fix:
  1. Start Docker: systemctl start docker (Linux)
  2. Or: Open Docker Desktop (macOS/Windows)
  3. Verify: docker ps

Once Docker is running, retry: scripts/bash/run-local-ci.sh
```

**Exceptions**:
1. Docker not available: Clear error, cannot proceed
2. act not installed: Prompt for auto-install
3. Workflow file missing: Error with path to expected file
4. GitHub Actions features not supported by act (OIDC): Documented limitation, graceful degradation

---

#### FR-CI-002: act Installation Management

**Purpose**: Automatically install act if missing, removing setup friction.

**Input**:
- act availability check: `command -v act`
- Platform detection: `uname -s` (Linux, Darwin, Windows)
- Architecture detection: `uname -m` (x86_64, arm64)

**Output**:
- **Already installed**: Use existing act binary
- **Auto-install**: Download and install act to `~/.local/bin/act`
- **Failure**: Error message with manual install instructions

**Rules**:
1. Discovery chain:
   - Check `$PATH` for existing act installation
   - Check `~/.local/bin/act` (user install location)
   - If not found, prompt for auto-install

2. Auto-install process:
   - Detect platform and architecture
   - Download binary from GitHub releases (latest stable)
   - Verify checksum (SHA256)
   - Install to `~/.local/bin/act`
   - Make executable: `chmod +x`
   - Add to PATH if needed

3. Platform-specific:
   - Linux: Download `act_Linux_x86_64.tar.gz`
   - macOS Intel: Download `act_Darwin_x86_64.tar.gz`
   - macOS ARM: Download `act_Darwin_arm64.tar.gz`
   - Windows: Not supported (WSL required)

**Error Messages**:
```
act not found and auto-install failed

Manual installation:
  1. Download: https://github.com/nektos/act/releases
  2. Extract: tar -xzf act_*.tar.gz
  3. Move: mv act ~/.local/bin/act
  4. Make executable: chmod +x ~/.local/bin/act
  5. Verify: act --version

Or use package manager:
  - Linux: brew install act
  - macOS: brew install act
```

**Exceptions**:
1. Network failure: Retry with exponential backoff (3 attempts)
2. Checksum mismatch: Refuse to install, clear error
3. Permission denied: Suggest alternative install location

---

#### FR-CI-003: Selective Job Execution

**Purpose**: Run only specific CI jobs for faster iteration during development.

**Input**:
- Job names as arguments: `run-local-ci.sh lint test`
- Available jobs from workflow file

**Output**:
- Execute only specified jobs
- Skip unspecified jobs (with message)
- Exit code reflects specified jobs only

**Rules**:
1. Job name validation:
   - Check job exists in `.github/workflows/ci.yml`
   - Error if job name not found
   - Suggest available jobs (via `--list` flag)

2. Execution order:
   - Respect job dependencies if defined in workflow
   - Run in order specified by user if no dependencies
   - Default order if no args: lint → test → build → security

3. `--list` flag:
   - Display all available jobs from workflow
   - Show job descriptions
   - Exit without running

**Example Usage**:
```bash
# Run all jobs
./run-local-ci.sh

# Run only lint and test
./run-local-ci.sh lint test

# List available jobs
./run-local-ci.sh --list
```

**Error Messages**:
```
Error: Unknown job 'validate'

Available jobs:
  - lint       Run code linting (ruff, mypy)
  - test       Run test suite (pytest)
  - build      Build package (uv build)
  - security   Run security scan (Semgrep)

Usage: ./run-local-ci.sh [job1 job2 ...]
```

---

#### FR-CI-004: Cross-Platform Compatibility

**Purpose**: Ensure local CI works identically on Linux and macOS.

**Input**:
- Platform: Linux (Ubuntu 22.04+) or macOS (12.0+)
- Shell: bash 3.2+ (POSIX-compliant)

**Output**:
- Identical behavior across platforms
- Same job results, timings, outputs
- Platform-specific errors handled gracefully

**Rules**:
1. Script compatibility:
   - Use POSIX bash features only (avoid bash 4.x+ features)
   - Avoid GNU-specific commands (use portable alternatives)
   - Test on bash 3.2 (default macOS version)

2. Docker requirements:
   - Linux: Docker Engine
   - macOS: Docker Desktop
   - Document platform-specific install steps

3. Path handling:
   - Use portable path separators
   - Handle spaces in paths correctly
   - Use `$HOME` instead of `~` in scripts

4. CI matrix testing:
   - GitHub Actions runs on `ubuntu-latest` AND `macos-latest`
   - Scripts validated on both platforms before merge

**Error Messages**:
```
Platform: macOS
Docker: Docker Desktop required

Docker Desktop not found or not running.

Steps to fix:
  1. Install: https://www.docker.com/products/docker-desktop
  2. Open Docker Desktop app
  3. Wait for "Docker Desktop is running" status
  4. Verify: docker ps

Retry after Docker Desktop is running.
```

**Exceptions**:
1. Windows: WSL2 required (not native Windows)
2. Old macOS (<12.0): Not officially supported
3. ARM Linux: Should work but not CI-tested

---

### Domain 3: Observability

#### FR-OBS-001: claude-trace Documentation

**Purpose**: Provide comprehensive guide for using claude-trace to debug complex SDD workflows.

**Input**:
- User needs to debug failed `/jpspec:*` workflow
- User wants to understand AI agent decision-making

**Output**:
- Documentation file: `docs/guides/claude-trace-integration.md`
- Installation instructions
- Usage examples with `/jpspec` commands
- Troubleshooting for known issues

**Rules**:
1. Documentation structure:
   - What is claude-trace and why use it?
   - Installation (Node.js 16+, npm install)
   - Basic usage (capturing traces)
   - Advanced usage (querying traces, analyzing patterns)
   - Troubleshooting (known issues #46, #48)
   - Privacy and security considerations

2. Example walkthroughs:
   - Debug failed `/jpspec:implement` workflow
   - Analyze token usage to optimize prompts
   - Profile performance bottlenecks
   - Inspect tool calls and responses

3. Integration points:
   - How claude-trace complements headless mode
   - Using traces with backlog task context
   - Exporting trace data for team debugging

**Content Requirements**:

**Section 1: What is claude-trace?**
- Overview of trace capture and analysis
- Use cases: debugging, optimization, learning
- When to use (complex workflows, mysterious failures)

**Section 2: Installation**
```bash
# Prerequisites
node --version  # 16.x or higher required

# Install
npm install -g claude-trace

# Verify
claude-trace --version
```

**Section 3: Capturing Traces**
```bash
# Start tracing
claude-trace start

# Run workflow (example)
/jpspec:implement

# Stop tracing
claude-trace stop

# View traces
claude-trace web
```

**Section 4: Troubleshooting**
- Issue #46: Indexing hangs on large traces
  - Workaround: Limit trace size, restart indexer
- Issue #48: Native binary compatibility on M1 Macs
  - Workaround: Use Rosetta or build from source

**Section 5: Privacy and Security**
- PII risks: Traces may contain code, secrets, file paths
- Recommendation: Local-only storage, no cloud upload
- Data retention: 7-day default, configurable
- Redaction: Manually redact sensitive data before sharing

**Exceptions**:
1. claude-trace is optional (not required for basic usage)
2. Node.js not available: Document as prerequisite
3. Known issues may require workarounds

---

#### FR-OBS-002: Integration with Existing Documentation

**Purpose**: Reference claude-trace in relevant troubleshooting and workflow documentation.

**Input**:
- Existing documentation files needing updates
- User troubleshooting workflows

**Output**:
- Updated references in:
  - `CLAUDE.md` (troubleshooting section)
  - `docs/reference/outer-loop.md` (observability section)
  - Backlog integration notes

**Rules**:
1. CLAUDE.md updates:
   - Add claude-trace to "Quick Troubleshooting" section
   - Link to comprehensive guide
   - One-line summary: "Debug complex workflows with claude-trace"

2. outer-loop.md updates:
   - Add to observability tooling section
   - Position as advanced debugging tool
   - Cross-reference with headless mode

3. Backlog integration:
   - Document how to capture task context in traces
   - Link traces to specific backlog task IDs
   - Example: Debugging task-123 implementation failure

**Example Reference (CLAUDE.md)**:
```markdown
## Quick Troubleshooting

# ... existing content ...

# Complex workflow failures
See [claude-trace integration guide](docs/guides/claude-trace-integration.md)
for debugging /jpspec command issues, token usage analysis, and performance profiling.
```

---

### Domain 4: Tool Dependency Management

#### FR-TOOL-001: Tool Discovery Chain

**Purpose**: Locate tools in order of preference: PATH → virtualenv → cache → download.

**Input**:
- Tool name (e.g., "semgrep", "codeql", "act")
- Tool requirements (version constraints)

**Output**:
- **Found**: Path to existing tool binary
- **Download**: Auto-install to cache, return path
- **Failure**: Error message with manual install instructions

**Rules**:
1. Discovery order:
   - **Step 1**: Check system PATH (`command -v semgrep`)
   - **Step 2**: Check virtualenv (`$VIRTUAL_ENV/bin/semgrep`)
   - **Step 3**: Check cache (`~/.cache/specify/tools/semgrep/1.87.0/semgrep`)
   - **Step 4**: Auto-download to cache

2. Version validation:
   - Run `tool --version` to get installed version
   - Compare against required version (exact or range)
   - Reject if version mismatch (download required version)

3. Cache structure:
   ```
   ~/.cache/specify/tools/
   ├── semgrep/
   │   ├── 1.87.0/
   │   │   └── semgrep (binary)
   │   └── 1.88.0/
   ├── codeql/
   │   └── 2.15.0/
   │       └── codeql (binary)
   └── act/
       └── 0.2.55/
           └── act (binary)
   ```

4. Performance:
   - Discovery completes in <100ms (cached lookups)
   - Binary validation (--version) in <1 second

**Error Messages**:
```
Tool not found: semgrep

Auto-install failed: Network timeout

Manual installation:
  pip install semgrep==1.87.0

Or retry when network is available.
```

**Exceptions**:
1. Offline mode: Skip auto-download, error if not cached
2. Permission denied: Suggest alternative cache location
3. Disk full: Clear cache or free space

---

#### FR-TOOL-002: Semgrep Auto-Installation

**Purpose**: Automatically install Semgrep via pip with version pinning.

**Input**:
- Tool request: "semgrep"
- Version requirement: "1.87.0" (from `versions.lock.json`)

**Output**:
- Installed Semgrep in virtualenv or cache
- Validated installation (`semgrep --version`)

**Rules**:
1. Installation strategy:
   - Prefer virtualenv install: `pip install semgrep==1.87.0`
   - Fallback to user install: `pip install --user semgrep==1.87.0`
   - Record installation in `versions.lock.json`

2. Version pinning:
   - Read version from `versions.lock.json` if exists
   - Default to 1.87.0 if no lock file
   - Create/update lock file after successful install

3. Validation:
   - Run `semgrep --version` after install
   - Verify version matches expected
   - Fail if version mismatch

4. Error handling:
   - Network failure: Retry 3 times with backoff
   - Permission denied: Suggest `--user` flag
   - Incompatible Python: Check Python 3.8+ requirement

**Installation Flow**:
```bash
# Detect Python environment
python --version  # Require 3.8+

# Install with version pin
pip install semgrep==1.87.0

# Validate
semgrep --version  # Must output "1.87.0"

# Record in lock file
echo '{"semgrep": "1.87.0"}' >> versions.lock.json
```

**Error Messages**:
```
Semgrep installation failed: Python 3.8+ required

Current Python version: 3.7.5

Please upgrade Python:
  - Ubuntu: sudo apt install python3.11
  - macOS: brew install python@3.11

Then retry.
```

---

#### FR-TOOL-003: CodeQL License Check and Download

**Purpose**: Check CodeQL license eligibility and download only if licensed.

**Input**:
- Tool request: "codeql"
- Repository information (for license check)

**Output**:
- **Licensed**: Download and install CodeQL
- **Unlicensed**: Skip with informational message (optional tool)
- **Unknown**: Prompt user to verify license status

**Rules**:
1. License eligibility (GitHub CodeQL):
   - Free for open-source repositories
   - Requires license for private/commercial use
   - Check via GitHub API (repository visibility)

2. Download process (if licensed):
   - Download from GitHub releases: `https://github.com/github/codeql-cli-binaries/releases`
   - Version: Latest stable or pinned version
   - Extract to cache: `~/.cache/specify/tools/codeql/2.15.0/`

3. Validation:
   - Run `codeql --version` after download
   - Verify checksum (SHA256) before extraction

4. Graceful degradation:
   - CodeQL is optional (not required for core workflows)
   - If unlicensed, log message and continue
   - Don't block user workflow

**License Check Flow**:
```bash
# Check repository visibility (GitHub API)
gh api repos/{owner}/{repo} --jq '.visibility'

# If "public" → licensed (free for open source)
# If "private" → check user license status
# If unknown → prompt user
```

**Error Messages**:
```
CodeQL license check inconclusive

CodeQL is free for open-source projects but requires a license for private/commercial use.

Options:
  1. Verify license: https://github.com/github/codeql/blob/main/LICENSE.md
  2. Skip CodeQL (recommended if unlicensed)
  3. Use Semgrep as alternative (already configured)

Continue without CodeQL? [Y/n]
```

**Exceptions**:
1. GitHub API failure: Prompt user to verify manually
2. Network failure: Skip CodeQL (don't block workflow)
3. User declines: Continue without CodeQL

---

#### FR-TOOL-004: Cache Management

**Purpose**: Monitor cache size, alert if exceeding limit, and provide cleanup commands.

**Input**:
- Cache location: `~/.cache/specify/tools/`
- Size limit: 500MB (configurable)

**Output**:
- **Under limit**: Normal operation
- **Exceeding limit**: Warning message with cleanup suggestions
- **Cache full**: Error, require cleanup before proceeding

**Rules**:
1. Size monitoring:
   - Calculate total cache size: `du -sh ~/.cache/specify/tools/`
   - Check before each tool download
   - Alert if total size > 500MB

2. LRU eviction policy:
   - Track last access time for each tool version
   - Evict oldest accessed tools first
   - Preserve tools in `versions.lock.json` (pinned versions)

3. Manual cleanup:
   - `specify tools clean`: Remove all cached tools
   - `specify tools clean --lru`: Remove only LRU tools until under limit
   - `specify tools list`: Show cached tools with sizes and last access

4. Automatic cleanup:
   - On cache full: Auto-evict LRU tools
   - Require user confirmation before eviction
   - Log evicted tools

**Cache Management Commands**:
```bash
# List cached tools
specify tools list
# Output:
# semgrep 1.87.0  (45MB, last used: 2025-12-01)
# codeql 2.15.0   (320MB, last used: 2025-11-28)
# act 0.2.55      (18MB, last used: 2025-12-04)
# Total: 383MB / 500MB (76% used)

# Clean all cache
specify tools clean
# Confirm: Remove all cached tools? [y/N]

# Clean only LRU (auto-clean to under limit)
specify tools clean --lru
# Removed: codeql 2.15.0 (320MB, last used 7 days ago)
# Cache now: 63MB / 500MB
```

**Error Messages**:
```
Cache size limit exceeded: 520MB / 500MB

Cached tools:
  - codeql 2.15.0: 320MB (last used 14 days ago)
  - semgrep 1.87.0: 45MB (last used today) [PINNED]
  - act 0.2.55: 18MB (last used today) [PINNED]

Cleanup options:
  1. specify tools clean --lru    # Remove oldest tools automatically
  2. specify tools clean          # Remove all cached tools
  3. Increase limit in settings.json (cacheMaxSize)

Run cleanup to proceed.
```

**Exceptions**:
1. Pinned tools never evicted (in `versions.lock.json`)
2. Cache on read-only filesystem: Warn, use system tools only
3. Disk full: Cannot download, clear cache mandatory

---

#### FR-TOOL-005: Offline Mode Support

**Purpose**: Support air-gapped environments by using only cached tools (no network).

**Input**:
- Offline mode flag: `--offline` or environment variable `SPECIFY_OFFLINE=1`
- Cached tools in `~/.cache/specify/tools/`

**Output**:
- **Success**: Use cached tools only
- **Failure**: Error if required tool not cached

**Rules**:
1. Offline mode behavior:
   - Skip tool discovery network steps (auto-download)
   - Use only PATH, virtualenv, and cache
   - Error if required tool not found (don't attempt download)

2. Pre-caching strategy:
   - Document required tools for offline use
   - Provide `specify tools download --all` command
   - Pre-cache on connected network before going offline

3. Validation:
   - Check all required tools cached before workflows
   - Warn if missing tools detected
   - Suggest pre-cache commands

**Offline Mode Setup**:
```bash
# Before going offline (connected network)
specify tools download --all
# Downloads: semgrep 1.87.0, codeql 2.15.0, act 0.2.55
# Cached to: ~/.cache/specify/tools/

# Enable offline mode
export SPECIFY_OFFLINE=1

# Or use flag
specify validate --offline
```

**Error Messages**:
```
Offline mode: Tool not cached

Required: semgrep 1.87.0
Status: Not found in cache

Offline mode requires pre-cached tools.

Steps to fix:
  1. Connect to network temporarily
  2. Run: specify tools download semgrep
  3. Disconnect and retry in offline mode

Or disable offline mode to auto-download.
```

**Exceptions**:
1. Network detected despite offline flag: Honor flag, don't download
2. Tool version mismatch: Error (cannot auto-update offline)
3. Cache corrupted: Cannot repair offline (need network)

---

### Domain 5: Developer Experience

#### FR-DX-001: Library Documentation MCP Research

**Purpose**: Identify and evaluate MCP servers for library documentation access.

**Input**:
- Research phase: Identify at least 3 candidate MCP servers
- Evaluation criteria: API key requirements, reliability, documentation coverage

**Output**:
- Comparison matrix documenting candidates
- Recommendation for integration
- Updated `.mcp.json` if candidate selected

**Rules**:
1. Candidate requirements:
   - API-key-free preferred (reduce friction)
   - Coverage: Python stdlib, TypeScript libraries, Rust docs
   - Reliability: Uptime, response time, community support

2. Evaluation criteria:
   - **API Keys**: Free tier sufficient? Rate limits?
   - **Reliability**: Uptime SLA, historical downtime
   - **Coverage**: Which languages/libraries supported?
   - **Latency**: Response time for documentation queries
   - **Maintenance**: Actively maintained? Recent updates?

3. Comparison matrix format:
   ```markdown
   | Candidate | API Key | Coverage | Reliability | Latency | Score |
   |-----------|---------|----------|-------------|---------|-------|
   | Candidate A | Free | Python, TypeScript | 99.9% | 200ms | 9/10 |
   | Candidate B | Required | Python only | 95% | 500ms | 6/10 |
   | Candidate C | Free | All languages | 99% | 300ms | 8/10 |
   ```

4. Recommendation:
   - Select candidate with highest score
   - Document pros/cons
   - Test integration in isolated environment
   - Update `.mcp.json` if approved

**Clarification Needed**:
- Which libraries need coverage? Python stdlib? TypeScript? Rust? All?
- Is API-key-free requirement mandatory or just preferred?
- What's the expected query volume (impacts rate limits)?

**Deliverable**:
- Research report in implementation notes (task-171)
- Recommendation with justification
- Integration guide if candidate selected

---

#### FR-DX-002: Plugin Packaging (Future)

**Purpose**: Package JP Spec Kit as Claude Code plugin for easy distribution.

**Input**:
- Plugin packaging command: `specify plugin create`
- Plugin metadata: name, version, author, description

**Output**:
- `.claude-plugin/` directory structure
- `manifest.json` with plugin metadata
- Packaged plugin ready for distribution

**Rules**:
1. Directory structure:
   ```
   .claude-plugin/
   ├── manifest.json
   ├── commands/
   │   ├── jpspec-specify.md
   │   ├── jpspec-implement.md
   │   └── ...
   ├── skills/
   │   ├── architect.md
   │   ├── pm-planner.md
   │   └── ...
   ├── hooks/
   │   └── pre-commit.sh
   └── settings.json (template)
   ```

2. Manifest format:
   ```json
   {
     "name": "jp-spec-kit",
     "version": "1.0.0",
     "author": "Your Name",
     "description": "Spec-Driven Development toolkit",
     "commands": ["jpspec-specify", "jpspec-implement", ...],
     "skills": ["architect", "pm-planner", ...],
     "hooks": ["pre-commit"],
     "settings": "settings.json"
   }
   ```

3. Installation:
   - User runs: `/plugin install jp-spec-kit`
   - Plugin copies files to `.claude/` directory
   - Merges settings with existing configuration

4. Distribution:
   - GitHub releases (versioned tarballs)
   - Plugin marketplace (future)

**Status**: Deferred to P3 (low priority, future work)

**Exceptions**:
1. Not required for MVP (focus on core platform first)
2. Depends on Claude Code plugin API stability
3. Community demand uncertain (validate need first)

---

#### FR-DX-003: Output Styles Experimentation (Future)

**Purpose**: Experiment with persona-specific output styles for workflow phases.

**Input**:
- Workflow command: `/jpspec:specify` (PM persona) or `/jpspec:plan` (Architect persona)
- Output style configuration

**Output**:
- Styled output matching persona expectations
- Findings report on value vs complexity

**Rules**:
1. PM persona (for `/jpspec:specify`):
   - Bullet points, user stories format
   - Focus on "what" and "why"
   - Plain language (avoid technical jargon)

2. Architect persona (for `/jpspec:plan`):
   - Diagrams (mermaid, PlantUML)
   - ADR format for decisions
   - Technical depth (APIs, data models)

3. Evaluation criteria:
   - Does style improve clarity?
   - Does it reduce cognitive load?
   - Is implementation complexity justified?
   - User feedback (positive vs negative)

**Status**: Exploratory (implement only if value demonstrated)

**Deliverable**:
- Prototype examples for PM and Architect styles
- Findings report with recommendation (adopt, defer, or skip)

---

#### FR-DX-004: Custom Statusline (Future)

**Purpose**: Provide statusline showing workflow context and progress.

**Input**:
- Workflow context (current phase, active task)
- Task progress (checked ACs / total ACs)
- Git branch

**Output**:
- Statusline display in terminal/editor
- Real-time updates as context changes

**Rules**:
1. Statusline format:
   ```
   [Phase: Implement] [Task: task-123] [ACs: 3/5] [Branch: feature/auth]
   ```

2. Color coding:
   - Green: On track (ACs progressing)
   - Yellow: Blocked (no AC progress in 1 hour)
   - Red: Failed (tests failing, CI failed)

3. Configuration:
   - Enable/disable: `.claude/settings.json` → `statusline.enabled`
   - Format customization: Template string

4. Data sources:
   - Workflow phase: `.claude/context` or current command
   - Active task: `backlog.md` (last "In Progress" task)
   - AC progress: Parse task file
   - Git branch: `git branch --show-current`

**Status**: Nice-to-have (low priority, deferred)

**Exceptions**:
1. Not supported in all terminal emulators
2. May conflict with existing statuslines (tmux, vim)
3. Low user demand (implement only if requested)

---

## Use Cases

### UC-001: Developer Prevented from Committing Secrets

**Actor**: Sarah (Solo Developer)

**Preconditions**:
- Sarah is debugging a feature
- She has `.env` file with API keys in project root
- permissions.deny rules are configured

**Flow**:
1. Sarah attempts to read `.env` file via Claude Code Read tool
2. Permission checker intercepts request
3. System matches `.env` against deny rule: `**/.env`
4. System blocks access and displays error message with alternatives
5. Sarah realizes mistake and uses `os.getenv()` instead
6. Audit log records blocked access attempt

**Postconditions**:
- `.env` file not exposed to AI agent
- Sarah learns safe pattern for accessing environment variables
- Security incident prevented

**Exceptions**:
- If Sarah legitimately needs to read `.env` (e.g., debugging configuration issue):
  - She confirms override
  - System logs override with justification
  - Access granted with warning

---

### UC-002: Fast Inner Loop with Local CI

**Actor**: Sarah (Solo Developer)

**Preconditions**:
- Sarah has made code changes
- Docker is running
- act is installed (or will be auto-installed)

**Flow**:
1. Sarah runs: `scripts/bash/run-local-ci.sh`
2. Script checks Docker is running (success)
3. Script checks act is installed (not found)
4. Script prompts: "Install act automatically? [Y/n]"
5. Sarah accepts (default Y)
6. Script downloads and installs act to `~/.local/bin/`
7. Script runs all CI jobs: lint → test → build → security
8. All jobs pass in <3 minutes
9. Sarah pushes to GitHub with confidence (CI will pass)

**Postconditions**:
- Sarah received feedback in <3 minutes (vs 5-15 minutes remote)
- No CI failures on GitHub (caught locally)
- act cached for future runs (even faster next time)

**Exceptions**:
- Docker not running: Error message with fix instructions, exit
- act auto-install fails: Error message with manual install steps
- Lint job fails: Stop execution (fail-fast), show errors, exit code 1

---

### UC-003: Debugging Complex Workflow with claude-trace

**Actor**: Tom (Team Lead)

**Preconditions**:
- Tom's team is using `/jpspec:implement` workflow
- Workflow is failing mysteriously (agent not producing expected code)
- Tom has installed claude-trace (Node.js 16+)

**Flow**:
1. Tom reads: `docs/guides/claude-trace-integration.md`
2. Tom starts tracing: `claude-trace start`
3. Tom runs workflow: `/jpspec:implement`
4. Workflow fails partway through (agent confused about requirements)
5. Tom stops tracing: `claude-trace stop`
6. Tom opens trace UI: `claude-trace web`
7. Tom reviews trace:
   - Sees exact prompt sent to agent
   - Identifies missing context from `spec.md`
   - Sees tool calls and responses
8. Tom fixes `spec.md` by adding missing details
9. Tom re-runs workflow successfully
10. Tom reviews token usage report, optimizes prompt templates

**Postconditions**:
- Tom identified root cause in <30 minutes (vs hours of trial-and-error)
- spec.md improved for future workflows
- Team learns to write better specs

**Exceptions**:
- claude-trace not installed: Installation instructions in guide
- Trace indexing hangs (Issue #46): Workaround documented in troubleshooting section
- PII in traces: Tom redacts sensitive data before sharing with team

---

### UC-004: Cross-Platform Team Development

**Actor**: Tom (Team Lead)

**Preconditions**:
- Tom's team uses mix of Linux (3 devs) and macOS (2 devs)
- `run-local-ci.sh` works on Linux but untested on macOS
- GitHub Actions CI includes macOS matrix

**Flow**:
1. Tom adds `macos-latest` to `.github/workflows/ci.yml` matrix
2. Tom pushes commit
3. GitHub Actions runs CI on both `ubuntu-latest` and `macos-latest`
4. macOS job fails: bash version difference (macOS has bash 3.2)
5. Tom reviews error: script uses bash 4.x feature (associative arrays)
6. Tom refactors script to use POSIX-compliant features
7. Tom re-runs CI: both platforms pass
8. macOS developers can now use local CI

**Postconditions**:
- Both Linux and macOS platforms supported
- Local CI works identically on both platforms
- Team productivity parity achieved

**Exceptions**:
- Docker Desktop not installed on macOS: Error message with install instructions
- Platform-specific path issues: Fixed via portable path handling

---

### UC-005: Tool Auto-Install in Air-Gapped Environment

**Actor**: Patricia (Platform Engineer)

**Preconditions**:
- Patricia is evaluating JP Spec Kit for enterprise use
- Environment is air-gapped (no internet access)
- Patricia needs Semgrep for security scanning

**Flow**:
1. Patricia (on connected network) runs: `specify tools download --all`
2. System downloads: Semgrep 1.87.0, CodeQL 2.15.0, act 0.2.55
3. System caches tools to: `~/.cache/specify/tools/`
4. Patricia transfers cache directory to air-gapped environment
5. Patricia enables offline mode: `export SPECIFY_OFFLINE=1`
6. Patricia runs: `/jpspec:validate`
7. System detects offline mode
8. System discovers Semgrep in cache (success)
9. System runs security scan using cached Semgrep

**Postconditions**:
- Semgrep runs successfully in air-gapped environment
- No network access required
- Security scanning enabled for regulated environment

**Exceptions**:
- Required tool not cached: Error message with pre-cache instructions
- Cache corrupted: Cannot repair offline (need network)
- Tool version mismatch: Error (cannot auto-update offline)

---

### UC-006: Cache Size Alert and Cleanup

**Actor**: Patricia (Platform Engineer)

**Preconditions**:
- Patricia has been using JP Spec Kit for 3 months
- Cache size is approaching 500MB limit
- Patricia wants to free space

**Flow**:
1. Patricia runs: `/jpspec:validate` (triggers CodeQL download)
2. System checks cache size: 490MB / 500MB
3. System calculates CodeQL size: 320MB
4. System calculates projected total: 810MB (exceeds limit)
5. System alerts: "Cache size would exceed 500MB limit"
6. System suggests: "Run 'specify tools clean --lru' to free space"
7. Patricia runs: `specify tools list`
8. Patricia sees: CodeQL 2.14.0 (last used 45 days ago)
9. Patricia runs: `specify tools clean --lru`
10. System removes CodeQL 2.14.0 (320MB)
11. System confirms: "Cache now 170MB / 500MB"
12. Patricia re-runs: `/jpspec:validate`
13. System downloads CodeQL 2.15.0 (latest)

**Postconditions**:
- Cache under limit (170MB → 490MB after new download)
- Old unused tools removed automatically
- Patricia understands cache management

**Exceptions**:
- All tools recently used: LRU eviction may remove needed tools (prompt user)
- Pinned tools never evicted: May need manual intervention or limit increase

---

## Data Requirements

### Entity: Security Rule

**Purpose**: Define permissions.deny rules for file and command protection.

**Attributes**:
- `rule_type`: "file" or "command"
- `pattern`: Glob pattern (files) or regex (commands)
- `action`: "deny_read", "deny_write", "deny_execute"
- `override_allowed`: Boolean (can user override?)
- `override_prompt`: String (confirmation message)

**Relationships**:
- Stored in: `.claude/settings.json`
- Enforced by: Permission checker module
- Logged to: `.claude/audit.log`

**Constraints**:
- At least one rule per category (file, command)
- Patterns must be valid (glob or regex)
- Override prompts must explain risks

**Example**:
```json
{
  "permissions": {
    "deny": [
      {
        "rule_type": "file",
        "pattern": "**/.env",
        "action": "deny_read",
        "override_allowed": true,
        "override_prompt": "Access to .env may expose secrets. Confirm? [y/N]"
      },
      {
        "rule_type": "command",
        "pattern": "^sudo\\s+.*",
        "action": "deny_execute",
        "override_allowed": true,
        "override_prompt": "Privilege escalation requested. Confirm? [y/N]"
      }
    ]
  }
}
```

---

### Entity: Tool Installation

**Purpose**: Track installed tools with versions and metadata.

**Attributes**:
- `tool_name`: "semgrep", "codeql", "act"
- `version`: "1.87.0", "2.15.0", etc.
- `install_path`: Absolute path to binary
- `install_date`: ISO 8601 timestamp
- `last_used`: ISO 8601 timestamp
- `install_strategy`: "pip", "binary_download", "system_package"
- `size_bytes`: Integer (for cache management)

**Relationships**:
- Tracked in: `versions.lock.json`
- Cached in: `~/.cache/specify/tools/`
- Discovered by: ToolDependencyManager

**Constraints**:
- Version must match semantic versioning format (X.Y.Z)
- Install path must be executable
- Last used updated on each invocation

**Example** (`versions.lock.json`):
```json
{
  "tools": {
    "semgrep": {
      "version": "1.87.0",
      "install_path": "/home/user/.cache/specify/tools/semgrep/1.87.0/semgrep",
      "install_date": "2025-12-04T10:00:00Z",
      "last_used": "2025-12-04T14:30:00Z",
      "install_strategy": "pip",
      "size_bytes": 47185920
    },
    "codeql": {
      "version": "2.15.0",
      "install_path": "/home/user/.cache/specify/tools/codeql/2.15.0/codeql",
      "install_date": "2025-11-28T09:00:00Z",
      "last_used": "2025-11-30T16:00:00Z",
      "install_strategy": "binary_download",
      "size_bytes": 335544320
    }
  }
}
```

---

### Entity: CI Job

**Purpose**: Define CI jobs executed locally via act.

**Attributes**:
- `job_name`: "lint", "test", "build", "security"
- `workflow_file`: Path to `.github/workflows/ci.yml`
- `steps`: List of commands to execute
- `dependencies`: List of job names (run order)
- `timeout`: Max execution time (seconds)
- `status`: "pending", "running", "passed", "failed"
- `duration`: Execution time (seconds)
- `output_log`: Path to job output file

**Relationships**:
- Defined in: `.github/workflows/ci.yml`
- Executed by: `scripts/bash/run-local-ci.sh`
- Depends on: Docker daemon, act binary

**Constraints**:
- Job name must be unique within workflow
- Steps must be valid shell commands
- Dependencies must reference existing jobs

**Example** (from `.github/workflows/ci.yml`):
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: ruff check .
      - run: ruff format --check
      - run: mypy src/

  test:
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - run: pytest tests/ -v --cov
```

---

### Entity: Audit Log Entry

**Purpose**: Record security events for compliance and debugging.

**Attributes**:
- `timestamp`: ISO 8601 format (UTC)
- `event_type`: "file_access_denied", "command_blocked", "override_granted"
- `target`: File path or command string
- `tool`: "Read", "Write", "Edit", "Bash"
- `reason`: Which deny rule matched
- `override`: Boolean (was override granted?)
- `justification`: String (if override granted)

**Relationships**:
- Stored in: `.claude/audit.log`
- Written by: Permission checker
- Queried by: Audit reporting tools

**Constraints**:
- Append-only (no deletions or edits)
- Log rotation at 10MB (keep last 5 rotations)
- Timestamps in UTC (consistent timezone)

**Example**:
```json
{"timestamp":"2025-12-04T10:30:00Z","event_type":"file_access_denied","target":".env","tool":"Read","reason":"permissions.deny rule: **/.env","override":false}
{"timestamp":"2025-12-04T10:31:00Z","event_type":"override_granted","target":".env","tool":"Read","reason":"User confirmed legitimate access","override":true,"justification":"Debugging configuration issue"}
```

---

## Error Handling and Edge Cases

### Security Layer Errors

**Error: Permission denied (file access)**
- **Cause**: File matches deny rule
- **Message**: "Access denied: .env files are protected by permissions.deny"
- **Resolution**: Use safe alternatives or override with confirmation
- **Logged**: Yes (`.claude/audit.log`)

**Error: Permission denied (command)**
- **Cause**: Command matches deny pattern
- **Message**: "Dangerous command blocked: sudo"
- **Resolution**: Run without privilege escalation or override with `--force-dangerous-command`
- **Logged**: Yes

**Edge Case: Legitimate override needed**
- **Scenario**: User needs to read `.env` for debugging
- **Handling**: Prompt for confirmation, explain risks, log override
- **Outcome**: Access granted after explicit confirmation

**Edge Case: .env.example vs .env**
- **Scenario**: User wants to read `.env.example` (documentation file)
- **Handling**: `.env.example` NOT in deny list (only `.env` and `.env.*` with actual values)
- **Outcome**: Access granted without prompt

---

### Local CI Errors

**Error: Docker not running**
- **Cause**: Docker daemon not started
- **Message**: "Docker daemon is not running. Start Docker and retry."
- **Resolution**: `systemctl start docker` (Linux) or open Docker Desktop (macOS)
- **Exit Code**: 1

**Error: act not installed and auto-install failed**
- **Cause**: Network timeout or permission denied
- **Message**: "act not found and auto-install failed. See manual install instructions."
- **Resolution**: Manual installation via package manager or GitHub releases
- **Exit Code**: 1

**Error: Unknown job name**
- **Cause**: User specified job not in workflow
- **Message**: "Unknown job 'validate'. Available jobs: lint, test, build, security"
- **Resolution**: Use `--list` flag to see available jobs
- **Exit Code**: 1

**Edge Case: GitHub Actions feature not supported by act**
- **Scenario**: Workflow uses OIDC authentication
- **Handling**: Documented limitation, graceful skip or error
- **Outcome**: User informed to run specific jobs on GitHub Actions

---

### Observability Errors

**Error: claude-trace not installed**
- **Cause**: User tries to use tracing without installation
- **Message**: "claude-trace not found. See installation guide: docs/guides/claude-trace-integration.md"
- **Resolution**: Install via npm: `npm install -g claude-trace`
- **Impact**: Documentation-only feature (not blocking)

**Error: claude-trace indexing hangs (Issue #46)**
- **Cause**: Large traces overwhelm indexer
- **Message**: "Indexing may hang on large traces. See workaround in troubleshooting guide."
- **Resolution**: Restart indexer, limit trace size
- **Impact**: Workaround documented

---

### Tool Management Errors

**Error: Tool not found and download failed**
- **Cause**: Network timeout, disk full, permission denied
- **Message**: "Semgrep installation failed: Network timeout. Retry when network is available."
- **Resolution**: Check network, free disk space, or install manually
- **Exit Code**: 1

**Error: Cache size exceeded**
- **Cause**: Cache > 500MB
- **Message**: "Cache size limit exceeded: 520MB / 500MB. Run 'specify tools clean --lru'."
- **Resolution**: Clean cache automatically or manually
- **Impact**: Blocks new tool downloads until cleaned

**Error: Offline mode but tool not cached**
- **Cause**: Required tool missing from cache in offline mode
- **Message**: "Offline mode: semgrep not cached. Pre-cache tools before going offline."
- **Resolution**: Connect to network, download tools, then go offline
- **Exit Code**: 1

**Edge Case: Tool version mismatch**
- **Scenario**: Cached tool version doesn't match required version
- **Handling**: Download correct version, evict old version if cache full
- **Outcome**: Correct version installed

---

### Developer Experience Errors

**Error: Library documentation MCP not found**
- **Cause**: No suitable MCP server identified yet
- **Message**: "Library documentation MCP research incomplete. See task-171."
- **Resolution**: Complete research task and integrate MCP server
- **Impact**: Optional feature (not blocking)

**Error: Plugin packaging not supported**
- **Cause**: Feature deferred to P3
- **Message**: "Plugin packaging not yet implemented. See task-195 for roadmap."
- **Resolution**: Wait for future release or contribute implementation
- **Impact**: Future feature (not available in MVP)

---

## Performance Requirements

### Security Layer Performance

- **Permission check overhead**: <10ms per file operation
- **Audit log write**: <5ms per event
- **Rule matching**: O(n) where n = number of rules (expect n < 20)

### Local CI Performance

- **Lint job**: <30 seconds
- **Test job**: <2 minutes
- **Build job**: <1 minute
- **Security job**: <1 minute
- **Full pipeline**: <5 minutes (all jobs)

### Tool Management Performance

- **Tool discovery**: <100ms (cached lookups)
- **Tool version check**: <1 second (`tool --version`)
- **Tool download**: <1 minute per tool (10 Mbps connection)
- **Cache size calculation**: <1 second (even with 500MB cache)

### Observability Performance

- **Trace capture**: <5% overhead on workflow execution
- **Trace indexing**: <30 seconds for typical workflow trace
- **Trace query**: <1 second for basic queries

---

## Acceptance Criteria

### Security Layer Acceptance

1. `.env` file access blocked via Read/Write/Edit tools
2. `secrets/` directory access blocked
3. Lock files (write) and configuration files (write) blocked
4. Dangerous bash commands blocked (sudo, rm -rf, dd, mkfs)
5. Override mechanism works with user confirmation
6. Audit log records all blocked operations
7. Error messages include safe alternatives
8. Documentation updated in CLAUDE.md

### Local CI Acceptance

1. `scripts/bash/run-local-ci.sh` executes all jobs via act
2. act auto-installs if missing
3. Docker daemon check with clear error if unavailable
4. Selective job execution works (e.g., `run-local-ci.sh lint test`)
5. Fail-fast on first job failure
6. Full pipeline completes in <5 minutes
7. Cross-platform support (Linux and macOS) validated in CI matrix
8. `--list` flag shows available jobs

### Observability Acceptance

1. `docs/guides/claude-trace-integration.md` created with comprehensive content
2. Installation instructions clear (Node.js 16+, npm install)
3. Usage examples with `/jpspec:*` commands
4. Troubleshooting section covers Issue #46 and #48
5. Privacy and security guidance included
6. CLAUDE.md and outer-loop.md reference claude-trace
7. Example trace analysis walkthrough provided

### Tool Management Acceptance

1. Semgrep auto-installs via pip with version pinning
2. CodeQL license check works, downloads if licensed
3. act auto-installs from GitHub releases
4. Cache size monitoring alerts at 500MB
5. LRU eviction policy works correctly
6. Offline mode supported with pre-cached tools
7. `specify tools list` and `specify tools clean` commands work
8. `versions.lock.json` tracks installed tools

### Developer Experience Acceptance

1. Library documentation MCP research completed (task-171)
2. At least 3 candidates evaluated with comparison matrix
3. Recommendation documented with pros/cons
4. Plugin packaging and output styles deferred to future (P3)
5. Statusline deferred to future (low priority)

---

## Dependencies and Constraints

### External Dependencies

**Security Layer**:
- Claude Code permission system (permissions.deny configuration)
- Filesystem access (audit log writing)

**Local CI/CD**:
- Docker (required for act)
- act (GitHub Actions local runner)
- GitHub Actions workflow files (`.github/workflows/ci.yml`)

**Observability**:
- Node.js 16+ (for claude-trace)
- claude-trace npm package
- SQLite 3+ (claude-trace dependency)

**Tool Management**:
- Python 3.8+ (for Semgrep via pip)
- GitHub API (for CodeQL license check and downloads)
- Network access (for tool downloads, unless offline mode)

### Platform Constraints

**Operating Systems**:
- Linux: Ubuntu 22.04+, Fedora 38+ (officially supported)
- macOS: 12.0+ Monterey (officially supported)
- Windows: WSL2 required (native Windows not supported)

**Shell**:
- bash 3.2+ (POSIX-compliant for cross-platform compatibility)
- zsh supported (via bash compatibility)

**Hardware**:
- Minimum: 4-core CPU, 8GB RAM (for local CI)
- Disk space: 1GB for tool cache + 500MB cache limit

### Version Constraints

**Pinned Versions** (in `versions.lock.json`):
- Semgrep: 1.87.0 (or later patch version)
- CodeQL: 2.15.0 (or later minor version)
- act: 0.2.55 (or later patch version)

**Version Update Policy**:
- Quarterly review of tool versions
- Automated testing before version bumps
- Backward compatibility maintained

---

## Future Enhancements

### Beyond MVP (P3 Priority)

1. **Plugin Packaging (task-195)**:
   - Enable easy distribution via Claude Code plugin marketplace
   - Target: 2026 Q1 (after community validation)

2. **Output Styles (task-196)**:
   - Persona-specific output for /jpspec commands
   - Target: Exploratory (implement only if value proven)

3. **Custom Statusline (task-197)**:
   - Workflow context display in terminal
   - Target: Nice-to-have (low priority)

4. **Advanced Tool Management**:
   - Multi-version support (parallel installations)
   - Tool update notifications
   - Dependency conflict resolution

5. **Enhanced Observability**:
   - Token usage dashboards
   - Performance profiling reports
   - Workflow optimization recommendations

6. **Security Enhancements**:
   - Machine learning-based anomaly detection
   - Integration with security scanning tools (Trivy, Bandit)
   - Automated secret detection in commits

---

## Appendix: Cross-References

### Related Documents

- **PRD**: [docs/prd/platform-devsecops-prd.md](../prd/platform-devsecops-prd.md)
- **Constitution**: [memory/constitution.md](../../memory/constitution.md) (Workflow State Diagram, Artifact Flow)
- **Backlog Tasks**: See Implementation Tasks section

### Implementation Tasks

| Task | Title | Priority | Dependencies |
|------|-------|----------|--------------|
| task-184 | Add permissions.deny Security Rules | HIGH | None |
| task-249 | Implement Tool Dependency Management | HIGH | None |
| task-085 | Local CI Simulation Script | MEDIUM | task-249 |
| task-168 | Add macOS CI Matrix Testing | LOW | task-085 |
| task-136 | Add claude-trace Observability Support | MEDIUM | None |
| task-171 | Research Library Documentation MCP | MEDIUM | None |
| task-195 | Create Plugin Package | LOW | All tasks (P3) |
| task-196 | Experiment with Output Styles | LOW | None (exploratory) |
| task-197 | Create Custom Statusline | LOW | None (future) |

### Functional Requirement to Task Mapping

| Functional Requirement | Implemented By |
|------------------------|----------------|
| FR-SEC-001, FR-SEC-002, FR-SEC-003 | task-184 |
| FR-TOOL-001 through FR-TOOL-005 | task-249 |
| FR-CI-001, FR-CI-002, FR-CI-003 | task-085 |
| FR-CI-004 | task-168 |
| FR-OBS-001, FR-OBS-002 | task-136 |
| FR-DX-001 | task-171 |
| FR-DX-002 | task-195 (P3) |
| FR-DX-003 | task-196 (exploratory) |
| FR-DX-004 | task-197 (future) |

---

**End of Functional Specification**
