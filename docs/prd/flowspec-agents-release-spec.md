# Product Requirements Document: Independent flowspec-agents Release Process

**Version:** 1.0
**Status:** Draft
**Created:** 2025-12-25
**Author:** Product Requirements Manager (@pm-planner)
**Related Task:** task-556

---

## 1. Executive Summary

### Problem Statement

Developers using flowspec agents currently face significant delays in receiving critical updates. Agent improvements and bug fixes are locked to the flowspec core release cadence, which is infrequent (weeks to months between releases). Additionally, when upstream tools like Claude Code evolve with new features or bug fixes, flowspec agents cannot leverage these improvements until the next flowspec release.

**Current Pain Points:**
- **Delayed agent improvements**: Bug fixes and new agent capabilities wait weeks/months for flowspec core releases
- **No upstream tracking**: No mechanism to detect or respond to Claude Code version updates
- **User frustration**: Developers can't get agent-only updates without upgrading all of flowspec
- **Security lag**: Security patches in agent code must wait for full release cycle

### Solution Overview

Implement an independent release workflow for flowspec-agents that:
1. **Releases independently** when agents change OR when Claude Code updates are detected
2. **Maintains same-repo architecture** for single source of truth (agents are tightly coupled to flowspec commands)
3. **Uses independent versioning** (e.g., flowspec-agents v1.5.0 while flowspec core is v0.3.011)
4. **Leverages existing infrastructure** (sync-copilot-agents.sh, validate-agent-sync.yml)
5. **Provides clear tracking** of Claude Code versions used by each agents release

### Business Value

**For Developers:**
- ✅ Fast access to agent improvements (days vs. weeks)
- ✅ Stay current with Claude Code capabilities
- ✅ Receive security patches quickly
- ✅ Optional upgrade (agents separate from core)

**For Maintainers:**
- ✅ Faster iteration on agent improvements
- ✅ Reduced coupling between agent and core releases
- ✅ Clear audit trail of Claude Code compatibility
- ✅ Better security posture (fast patch deployment)

### Success Metrics

- **Release Frequency**: Agents release ≥2x per month (vs. current ~1x per month with core)
- **Time to Patch**: Security patches in agents deployed within 24-48 hours
- **Claude Code Lag**: Flowspec agents support latest Claude Code within 7 days of release
- **Adoption Rate**: ≥60% of users on latest agents version within 2 weeks of release

---

## 2. User Stories and Use Cases

### Primary User Personas

**Persona 1: Active Flowspec Developer**
- Uses flowspec daily for feature development
- Relies on agents for code review, implementation, security scanning
- Needs: Latest agent improvements without full flowspec upgrade

**Persona 2: Security-Conscious Developer**
- Runs security scans via `/sec:scan`, `/sec:triage`, `/sec:fix`
- Needs: Fast security patches when vulnerabilities are found in agent code
- Pain: Current delays expose projects to known vulnerabilities

**Persona 3: Early Adopter**
- Tracks Claude Code releases closely
- Wants: Agents that leverage latest Claude Code features
- Pain: Flowspec agents lag behind Claude Code by weeks

### User Stories

#### Story 1: Fast Agent Bug Fix
**As a** flowspec developer
**I want** agent bug fixes released independently
**So that** I don't have to wait weeks for the next flowspec core release

**Acceptance Criteria:**
- Agent bug fixes release within 48 hours of merge
- No flowspec core upgrade required
- Release notes clearly identify which agents changed

**Current State:** Bug fix waits for next flowspec release (weeks)
**Desired State:** Bug fix released within 48 hours

---

#### Story 2: Claude Code Feature Support
**As an** early adopter of Claude Code
**I want** flowspec agents to support new Claude Code features quickly
**So that** I can leverage the latest capabilities

**Acceptance Criteria:**
- Flowspec agents track Claude Code version
- New agents release triggers when Claude Code updates
- Release notes show Claude Code compatibility

**Current State:** No Claude Code tracking, agents lag by weeks
**Desired State:** Agents support new Claude Code within 7 days

---

#### Story 3: Security Patch Deployment
**As a** security-conscious developer
**I want** security patches in agents deployed immediately
**So that** my projects aren't exposed to known vulnerabilities

**Acceptance Criteria:**
- Security patches release within 24 hours
- Automated security scanning triggers agent releases
- Clear CVE/vulnerability identification in release notes

**Current State:** Security patches wait for flowspec release
**Desired State:** Security patches deployed within 24 hours

---

#### Story 4: Optional Agent Upgrade
**As a** flowspec user
**I want** to upgrade agents independently of flowspec core
**So that** I can stay on a stable core version while getting agent improvements

**Acceptance Criteria:**
- `flowspec agents upgrade` command available
- Agents version displayed separately from core version
- Upgrade doesn't modify flowspec core

**Current State:** Agents tied to flowspec version
**Desired State:** Independent agents version and upgrade path

---

### Use Case Flows

#### Use Case 1: Agent-Only Release (Path Change Trigger)

**Trigger:** Developer merges PR updating `.github/agents/` files

**Flow:**
1. PR merges to main with agent file changes
2. `release-agents.yml` detects path changes to `.github/agents/**`
3. Workflow extracts next version from `agents-version.json`
4. Creates release tag `agents/v1.5.0`
5. Packages agents-only archive
6. Creates GitHub release with changelog
7. Updates `agents-version.json` to v1.5.1-dev

**Success Criteria:**
- Release completes within 5 minutes of merge
- Archive contains only agent files + metadata
- Release notes auto-generated from commits

---

#### Use Case 2: Claude Code Update Trigger

**Trigger:** Daily cron job detects new Claude Code version

**Flow:**
1. Cron job checks Claude Code GitHub releases API
2. Compares latest Claude Code version to `claude-code-version.txt`
3. If new version found:
   - Updates `claude-code-version.txt`
   - Commits change with message "chore(agents): update Claude Code to vX.Y.Z"
   - Push triggers `release-agents.yml` via path change
4. Agents release proceeds with updated Claude Code version in metadata

**Success Criteria:**
- Daily check runs reliably
- Version tracking file updated atomically
- Release triggered automatically

---

#### Use Case 3: Manual Emergency Release

**Trigger:** Maintainer discovers critical security vulnerability

**Flow:**
1. Maintainer merges hotfix PR to main
2. Maintainer manually triggers `release-agents.yml` via workflow_dispatch
3. Enters version override (e.g., `v1.4.1`) for patch release
4. Workflow creates release with emergency tag in release notes
5. Users notified via GitHub release notification

**Success Criteria:**
- Manual trigger available in GitHub UI
- Version override supported
- Emergency releases clearly marked

---

## 3. DVF+V Risk Assessment

### Value Risk (Desirability)

**Risk Level:** 🟢 Low

**Evidence:**
- Task-556 assessment already identified independent release as preferred option
- User pain clearly documented (agent updates delayed by core releases)
- Security vulnerabilities in agents create real exposure

**Validation Approach:**
- ✅ Already validated via task-556 assessment
- Future: Track release adoption rates (target: 60% adoption in 2 weeks)
- Future: Survey users on release frequency satisfaction

**Mitigation:**
- Monitor release notes engagement
- Gather feedback on version upgrade experience
- Track GitHub release download counts

---

### Usability Risk (Experience)

**Risk Level:** 🟡 Medium

**Concerns:**
1. **Version confusion**: Users may not understand agents vs. core versioning
2. **Upgrade complexity**: New upgrade workflow for agents
3. **Compatibility**: Agents version compatibility with core unclear

**Validation Approach:**
- **Discovery Testing**: Create mock release notes and test user comprehension
- **Prototype**: Build `flowspec agents version` command and test with beta users
- **Documentation Review**: Have 3-5 users review upgrade docs for clarity

**Mitigation Strategies:**
1. **Clear version display**: `flowspec version` shows both core and agents versions
2. **Simple upgrade**: `flowspec agents upgrade` handles everything
3. **Compatibility matrix**: Document which agents versions work with which core versions
4. **Release notes clarity**: Clearly distinguish agent-only vs. core releases

---

### Feasibility Risk (Technical)

**Risk Level:** 🟢 Low

**Technical Challenges:**
1. **Version tracking**: Need new version file for agents (separate from pyproject.toml)
2. **Packaging**: Agent-only packages (no Python wheel, just template zips)
3. **CI coordination**: release.yml and release-agents.yml must not conflict
4. **Claude Code tracking**: API calls to GitHub releases, rate limiting

**Validation Approach:**
- ✅ Existing infrastructure (sync-copilot-agents.sh) proves feasibility
- ✅ validate-agent-sync.yml pattern shows path-based triggers work
- Spike: Test GitHub API rate limits for daily version checks
- Spike: Validate agent packaging without Python build

**Proven Patterns (Existing Codebase):**
- **Path-based triggers**: `.github/workflows/validate-agent-sync.yml` (lines 5-9) uses `paths:` filter
- **Conditional workflows**: `release.yml` (lines 37-40) shows `if:` conditional execution
- **Version extraction**: `release.yml` (lines 73-79) extracts version from branch name
- **Agent packaging**: `create-release-packages.sh` (lines 251-343) shows packaging logic

**Feasibility Rating:** ✅ High - All components have proven patterns

---

### Business Viability Risk (Organizational)

**Risk Level:** 🟢 Low

**Business Considerations:**
1. **Maintenance burden**: Two release workflows to maintain
2. **Support complexity**: Users on different agent versions
3. **Documentation overhead**: More docs needed for two version tracks
4. **Testing matrix**: Need to test agents against multiple core versions

**Validation Approach:**
- **Cost Analysis**: Estimate maintainer time for dual workflows (< 2 hours/month)
- **Support Review**: Analyze support tickets for version-related issues
- **Documentation Spike**: Create draft docs and estimate maintenance effort

**Viability Evidence:**
- ✅ Task-556 assessment endorsed independent release
- ✅ Existing CI infrastructure supports conditional workflows
- ✅ Agent sync automation reduces manual work
- Risk is acceptable given user value (fast security patches)

**Mitigation:**
- Automate version compatibility checks in CI
- Create compatibility matrix generator
- Use same release note template for both workflows
- Invest in clear upgrade path documentation

---

## 4. Functional Requirements

### FR-1: Agent Version Management

**Requirement:** Independent version tracking for flowspec-agents separate from flowspec core

**Details:**
- **Version file**: `agents-version.json` at project root
- **Format**:
  ```json
  {
    "version": "1.5.0",
    "claude_code_version": "2024.12.20",
    "release_date": "2025-12-25T14:30:00Z",
    "changelog_url": "https://github.com/jpoley/flowspec/releases/tag/agents/v1.5.0"
  }
  ```
- **Versioning scheme**: Semantic versioning (MAJOR.MINOR.PATCH)
  - MAJOR: Breaking changes to agent interface
  - MINOR: New agents, feature additions
  - PATCH: Bug fixes, security patches

**Acceptance Criteria:**
- ✅ `agents-version.json` file created and tracked in git
- ✅ Version follows semver strictly
- ✅ File updated atomically by release workflow
- ✅ Tracks associated Claude Code version

---

### FR-2: Claude Code Version Tracking

**Requirement:** Automated tracking of Claude Code releases to trigger agent updates

**Details:**
- **Tracking file**: `claude-code-version.txt` at project root
- **Content**: Single line with version string (e.g., `2024.12.20`)
- **Update mechanism**: Daily cron job via GitHub Actions
- **Source**: Claude Code GitHub releases API
- **Comparison logic**: String comparison to detect new versions

**Acceptance Criteria:**
- ✅ Daily cron job runs reliably (5:00 UTC)
- ✅ Version file updated when new Claude Code detected
- ✅ Commit message format: `chore(agents): update Claude Code to vX.Y.Z`
- ✅ GitHub API rate limits respected (use `GITHUB_TOKEN`)

---

### FR-3: Independent Release Workflow

**Requirement:** `release-agents.yml` workflow for agent-only releases

**Triggers:**
1. **Path-based**: Changes to `.github/agents/**` merged to main
2. **Version-based**: Changes to `claude-code-version.txt` merged to main
3. **Manual**: `workflow_dispatch` with optional version override

**Workflow Steps:**
1. Detect trigger type (path change, version update, manual)
2. Extract next version from `agents-version.json`
3. Validate version format (semver)
4. Create git tag `agents/vX.Y.Z`
5. Package agent files into archive
6. Generate release notes from commits
7. Create GitHub release
8. Bump version in `agents-version.json` to next dev version

**Acceptance Criteria:**
- ✅ Workflow triggers correctly for all 3 trigger types
- ✅ Runs only when agents change (no false positives)
- ✅ Creates valid semver tags with `agents/` prefix
- ✅ Completes within 5 minutes
- ✅ Fails fast on validation errors

**Example Workflow File Structure:**
```yaml
name: Release Agents

on:
  push:
    branches: [main]
    paths:
      - '.github/agents/**'
      - 'claude-code-version.txt'
  workflow_dispatch:
    inputs:
      version:
        description: 'Version override (e.g., v1.4.1)'
        required: false

jobs:
  release-agents:
    runs-on: ubuntu-latest
    steps:
      - name: Determine version
        # Extract from agents-version.json or use input override
      - name: Create tag
        # Tag with agents/vX.Y.Z format
      - name: Package agents
        # Create agents-only archive
      - name: Create release
        # GitHub release with changelog
```

---

### FR-4: Agent Packaging

**Requirement:** Create distributable agent packages separate from flowspec core

**Package Contents:**
- All `.github/agents/*.agent.md` files (49 files)
- `agents-version.json` (metadata)
- `claude-code-version.txt` (compatibility info)
- `AGENTS-README.md` (installation instructions)

**Package Format:**
- **Filename**: `flowspec-agents-vX.Y.Z.zip`
- **Size**: < 1MB (agents are markdown files)
- **Structure**:
  ```
  flowspec-agents-v1.5.0/
  ├── agents/
  │   ├── flow-implement.agent.md
  │   ├── flow-validate.agent.md
  │   └── ... (47 more)
  ├── agents-version.json
  ├── claude-code-version.txt
  └── README.md
  ```

**Acceptance Criteria:**
- ✅ Package includes all agent files
- ✅ Metadata files included
- ✅ README with clear installation steps
- ✅ Archive size < 1MB
- ✅ Compatible with existing agent sync infrastructure

---

### FR-5: Release Coordination

**Requirement:** Prevent conflicts between core and agents releases

**Coordination Mechanisms:**
1. **Tag namespacing**: Core uses `v*` tags, agents use `agents/v*` tags
2. **Workflow conditions**: `release.yml` ignores `agents/**` path changes
3. **Version isolation**: Core version in `pyproject.toml`, agents in `agents-version.json`
4. **Mutual exclusion**: Workflows check for in-progress releases

**Acceptance Criteria:**
- ✅ Core and agents workflows never trigger simultaneously
- ✅ Tag namespaces prevent collisions
- ✅ Both workflows can run on same day without conflicts
- ✅ Release notes clearly distinguish core vs. agents releases

**Implementation Pattern:**
```yaml
# In release.yml
on:
  pull_request:
    types: [closed]
    branches: [main]
    paths-ignore:
      - '.github/agents/**'
      - 'claude-code-version.txt'
```

---

### FR-6: Automated Release Notes

**Requirement:** Generate release notes from git commits since last agents release

**Release Note Sections:**
1. **Summary**: One-line description of release type
2. **Agent Changes**: List of modified agents
3. **Claude Code Compatibility**: Supported Claude Code version
4. **Breaking Changes**: If any (for MAJOR version bumps)
5. **Full Changelog**: Link to commit diff

**Template:**
```markdown
# flowspec-agents v1.5.0

**Release Type:** Agent improvements
**Claude Code Compatibility:** v2024.12.20 and later
**Release Date:** 2025-12-25

## What's Changed

### Agent Updates
- `flow-implement`: Fixed code review timeout issue (#1234)
- `sec-scan`: Added support for Rust scanning (#1235)
- `qa-test`: Improved test coverage reporting (#1236)

## Compatibility

- **Flowspec Core:** v0.3.0 and later
- **Claude Code:** v2024.12.20 and later

## Full Changelog
https://github.com/jpoley/flowspec/compare/agents/v1.4.0...agents/v1.5.0
```

**Acceptance Criteria:**
- ✅ Release notes auto-generated from commits
- ✅ All sections populated correctly
- ✅ Markdown formatting validates
- ✅ Links to full changelog work

---

### FR-7: Version Display

**Requirement:** Display both core and agents versions in CLI

**Command Output:**
```bash
$ flowspec version
Flowspec: v0.3.011
Agents:   v1.5.0 (Claude Code: v2024.12.20)
```

**Details:**
- Read `pyproject.toml` for core version
- Read `agents-version.json` for agents version
- Read `claude-code-version.txt` for Claude Code compatibility
- Show all three in version output

**Acceptance Criteria:**
- ✅ `flowspec version` shows core + agents versions
- ✅ Claude Code version displayed
- ✅ Output is machine-readable (JSON flag available)
- ✅ Handles missing version files gracefully

---

## 5. Non-Functional Requirements

### NFR-1: Performance

**Requirement:** Agent releases complete quickly without blocking development

**Metrics:**
- **Workflow duration**: < 5 minutes from trigger to published release
- **Package size**: < 1MB for agent archive
- **API rate limits**: Claude Code version checks respect GitHub API limits (5000/hour)
- **Concurrent releases**: Support 1 agent release while core release in progress (separate namespaces)

**Acceptance Criteria:**
- ✅ 95% of releases complete within 5 minutes
- ✅ No GitHub API rate limit errors
- ✅ Archive downloads in < 10 seconds on typical connections

---

### NFR-2: Reliability

**Requirement:** Release workflow is robust and handles failures gracefully

**Reliability Measures:**
- **Idempotency**: Re-running workflow produces same result
- **Atomic operations**: Tag creation and version bumps are atomic
- **Rollback capability**: Failed releases don't leave partial state
- **Error reporting**: Clear error messages for validation failures

**Acceptance Criteria:**
- ✅ Workflow can be safely re-run on failure
- ✅ Failed releases don't create orphaned tags
- ✅ All errors logged to GitHub Actions summary
- ✅ 99% success rate for valid releases

**Error Handling:**
- Version validation failures → Fail fast with clear message
- Tag already exists → Fail with conflict message
- Package creation fails → Rollback tag creation
- GitHub API errors → Retry with exponential backoff

---

### NFR-3: Security

**Requirement:** Release process maintains security posture

**Security Measures:**
- **Tag signing**: All `agents/v*` tags are GPG signed by release bot
- **Audit trail**: All version changes committed to git
- **Token scoping**: GitHub Actions token has minimal required permissions
- **Version immutability**: Published versions cannot be modified

**Acceptance Criteria:**
- ✅ All tags include GPG signature
- ✅ Version files tracked in git (no manual edits)
- ✅ Workflow uses `contents: write` permission only (not `admin`)
- ✅ Published releases are immutable

**Permissions Matrix:**
```yaml
permissions:
  contents: write  # For tag creation and release publishing
  # NO admin, workflow, or packages permissions
```

---

### NFR-4: Observability

**Requirement:** Release process is transparent and auditable

**Observability Features:**
- **Release dashboard**: GitHub releases page shows all agents releases
- **Version history**: Git log shows version bump commits
- **Trigger tracking**: Workflow logs show which trigger fired (path, version, manual)
- **Metrics**: Track release frequency, size, duration

**Acceptance Criteria:**
- ✅ Every release has clear trigger source in logs
- ✅ Version history visible in git log
- ✅ Release notes link to triggering commits
- ✅ GitHub Actions summary shows key metrics

**Metrics to Track:**
- Releases per month
- Average time from commit to release
- Average archive size
- Failed release count and reasons

---

### NFR-5: Maintainability

**Requirement:** Release workflow is easy to understand and modify

**Maintainability Measures:**
- **Documentation**: Inline comments explain each workflow step
- **Modularity**: Reusable scripts for version extraction, packaging
- **Consistency**: Follow patterns from existing `release.yml`
- **Testing**: Scripts testable locally with act

**Acceptance Criteria:**
- ✅ Workflow has < 300 lines (similar to release.yml)
- ✅ Each step has clear comment explaining purpose
- ✅ Reuses existing scripts where possible (e.g., sync-copilot-agents.sh)
- ✅ Can be tested locally via `act` tool

**Code Quality:**
- Follow existing workflow patterns (see release.yml lines 1-232)
- Reuse validation patterns (see validate-agent-sync.yml lines 1-195)
- Use existing script patterns (see sync-copilot-agents.sh lines 1-1114)

---

### NFR-6: Compatibility

**Requirement:** Agent releases are backward compatible with flowspec core

**Compatibility Rules:**
1. **Minor/Patch agent releases**: Compatible with current core MAJOR version
2. **Major agent releases**: May require specific core version
3. **Core releases**: Always bundle latest agents version at release time
4. **Version matrix**: Document compatibility in README

**Acceptance Criteria:**
- ✅ Compatibility matrix auto-generated and published
- ✅ Agent releases specify minimum core version
- ✅ Core releases include current agents version
- ✅ Users can check compatibility via CLI

**Compatibility Matrix Example:**
| Agents Version | Min Core Version | Claude Code Version |
|----------------|------------------|---------------------|
| v1.5.0         | v0.3.0           | v2024.12.20         |
| v1.4.0         | v0.3.0           | v2024.12.01         |
| v1.3.0         | v0.2.0           | v2024.11.15         |

---

## 6. Task Breakdown (Backlog Tasks)

### 6.1 Design Phase Tasks

These tasks define the architecture and approach before implementation begins.

#### task-557: Design agent version management system
**Priority:** High | **Assignee:** @pm-planner | **Labels:** design, agents, versioning

Create agents-version.json schema and version bumping strategy. Define semver rules for agents.

**Acceptance Criteria:**
- agents-version.json schema defined with version, claude_code_version, release_date, changelog_url
- Semver rules documented for agent releases
- Version bump strategy defined (auto vs manual)
- Compatibility with existing sync-copilot-agents.sh validated

**Dependencies:** None
**Estimated Effort:** 2-4 hours

---

#### task-558: Design Claude Code version tracking mechanism
**Priority:** High | **Assignee:** @pm-planner | **Labels:** design, agents, tracking

Design daily cron job to check Claude Code GitHub releases and trigger agent releases when new versions detected.

**Acceptance Criteria:**
- Cron job schedule defined (daily at 5:00 UTC)
- GitHub API interaction pattern documented with rate limit handling
- claude-code-version.txt format and location specified
- Trigger logic for agent releases on version updates designed

**Dependencies:** None
**Estimated Effort:** 2-3 hours

---

#### task-559: Design release-agents.yml workflow architecture
**Priority:** High | **Assignee:** @pm-planner | **Labels:** design, ci-cd, workflow

Design GitHub Actions workflow for agent-only releases with trigger conditions and coordination with release.yml.

**Acceptance Criteria:**
- Workflow triggers designed: paths filter, claude-code-version.txt watch, workflow_dispatch
- Workflow steps documented: version extraction, tagging, packaging, release creation
- Coordination mechanism with release.yml designed (tag namespacing, path-ignore)
- Error handling and rollback strategy defined

**Dependencies:** task-557, task-558
**Estimated Effort:** 3-4 hours

---

#### task-560: Design agent packaging and distribution strategy
**Priority:** Medium | **Assignee:** @pm-planner | **Labels:** design, packaging, agents

Design how agents are packaged separately from flowspec core with installation process and compatibility tracking.

**Acceptance Criteria:**
- Package format designed: flowspec-agents-vX.Y.Z.zip structure
- Package contents specified: agents/, metadata files, README
- Installation instructions drafted
- Compatibility matrix format designed

**Dependencies:** task-557
**Estimated Effort:** 2-3 hours

---

### 6.2 Implementation Phase Tasks

These tasks implement the designed architecture.

#### task-561: Implement agents-version.json and version management
**Priority:** High | **Labels:** implementation, agents, versioning

Create agents-version.json file with initial v1.0.0 version and implement version management utilities.

**Acceptance Criteria:**
- agents-version.json created at project root
- Version read/write utilities implemented
- Semver validation added
- Tests pass for version management

**Dependencies:** task-557
**Estimated Effort:** 3-4 hours

---

#### task-562: Implement Claude Code version tracking cron job
**Priority:** High | **Labels:** implementation, ci-cd, tracking

Create .github/workflows/track-claude-code.yml with daily cron schedule and GitHub API integration.

**Acceptance Criteria:**
- track-claude-code.yml workflow created
- Daily cron job at 5:00 UTC configured
- GitHub API interaction implemented with rate limit handling
- claude-code-version.txt updates committed automatically

**Dependencies:** task-558
**Estimated Effort:** 4-5 hours

---

#### task-563: Implement release-agents.yml workflow
**Priority:** High | **Labels:** implementation, ci-cd, workflow

Create .github/workflows/release-agents.yml with path and version triggers for agent-only releases.

**Acceptance Criteria:**
- release-agents.yml workflow created
- Path-based triggers working (.github/agents/**, claude-code-version.txt)
- Version extraction from agents-version.json implemented
- Tag creation with agents/v* format working
- GitHub release creation functional

**Dependencies:** task-559, task-561
**Estimated Effort:** 6-8 hours

---

#### task-564: Implement agent packaging script
**Priority:** High | **Labels:** implementation, packaging, agents

Create .github/workflows/scripts/package-agents.sh to build agent-only archives.

**Acceptance Criteria:**
- package-agents.sh script created
- Script packages all 49 agent files
- Metadata files included (agents-version.json, claude-code-version.txt, README)
- Archive size < 1MB
- Package structure validated

**Dependencies:** task-560, task-561
**Estimated Effort:** 3-4 hours

---

#### task-565: Implement automated release notes generation
**Priority:** Medium | **Labels:** implementation, ci-cd, documentation

Create script to generate release notes from commits since last agents tag.

**Acceptance Criteria:**
- generate-agents-release-notes.sh script created
- Release notes include agent changes section
- Claude Code compatibility shown
- Full changelog link generated
- Markdown format validates

**Dependencies:** task-563
**Estimated Effort:** 3-4 hours

---

#### task-566: Add agents version display to flowspec CLI
**Priority:** Medium | **Labels:** implementation, cli, versioning

Extend flowspec version command to show both core and agents versions with Claude Code compatibility.

**Acceptance Criteria:**
- flowspec version shows core version
- flowspec version shows agents version
- Claude Code version displayed
- JSON output format supported (--json flag)
- Handles missing version files gracefully

**Dependencies:** task-561
**Estimated Effort:** 2-3 hours

---

#### task-567: Update release.yml to coordinate with agents releases
**Priority:** High | **Labels:** implementation, ci-cd, coordination

Modify .github/workflows/release.yml to ignore agent path changes and prevent conflicts.

**Acceptance Criteria:**
- paths-ignore added for .github/agents/** and claude-code-version.txt
- Core release still triggers on other path changes
- Tag namespaces prevent conflicts (v* vs agents/v*)
- Both workflows tested to run on same day without conflicts

**Dependencies:** task-563
**Estimated Effort:** 2-3 hours

---

### 6.3 Testing and Documentation Phase Tasks

These tasks ensure quality and usability.

#### task-568: Write integration tests for agent release workflow
**Priority:** Medium | **Labels:** testing, ci-cd, agents

Create test suite for release-agents.yml workflow covering all trigger types.

**Acceptance Criteria:**
- Test path-based trigger (agent file change)
- Test version-based trigger (claude-code-version.txt change)
- Test manual trigger (workflow_dispatch)
- Test tag creation validation
- Test package contents validation
- All tests pass in CI

**Dependencies:** task-563, task-564, task-565
**Estimated Effort:** 4-5 hours

---

#### task-569: Document agent release process
**Priority:** Medium | **Labels:** documentation, agents

Create comprehensive documentation for agent releases covering all aspects of the process.

**Acceptance Criteria:**
- docs/guides/agent-release-process.md created
- Release triggers documented with examples
- Version upgrade process documented
- Compatibility matrix template created
- Troubleshooting section with common issues

**Dependencies:** task-563, task-566
**Estimated Effort:** 3-4 hours

---

### 6.4 Future Enhancement Tasks

These tasks provide additional value but are not required for MVP.

#### task-570: Create agent upgrade command (flowspec agents upgrade)
**Priority:** Low | **Labels:** implementation, cli, agents

Implement CLI command to upgrade agents independently of core flowspec.

**Acceptance Criteria:**
- flowspec agents upgrade command implemented
- Command downloads latest release from GitHub
- Agents extracted to correct location
- Local version tracking updated
- Dry-run mode supported (--dry-run)
- Tests pass for upgrade command

**Dependencies:** task-566, task-569
**Estimated Effort:** 4-5 hours

---

#### task-571: Create compatibility matrix generator
**Priority:** Low | **Labels:** implementation, documentation, versioning

Implement script to auto-generate compatibility matrix between versions.

**Acceptance Criteria:**
- generate-compatibility-matrix.sh script created
- Matrix includes agents version, min core version, Claude Code version
- Markdown table format validated
- Script integrated into release workflow
- Matrix published to docs/

**Dependencies:** task-569
**Estimated Effort:** 2-3 hours

---

### Task Summary

**Total Tasks:** 15
- Design: 4 tasks (High: 3, Medium: 1)
- Implementation: 7 tasks (High: 4, Medium: 2, Low: 1)
- Testing/Documentation: 2 tasks (Medium: 2)
- Future Enhancements: 2 tasks (Low: 2)

**Critical Path:**
1. task-557 → task-561 → task-563 → task-567 → task-568
2. task-558 → task-562 → task-563
3. task-559 → task-563

**Estimated Total Effort:** 40-52 hours

**Recommended Iteration Plan:**
- **Sprint 1 (Week 1)**: Design tasks (557-560) + Version management (561)
- **Sprint 2 (Week 2)**: Core implementation (562-564, 567)
- **Sprint 3 (Week 3)**: Release notes + CLI (565-566) + Testing (568)
- **Sprint 4 (Week 4)**: Documentation (569) + Future enhancements (570-571)

---

## 7. Discovery and Validation Plan

### Discovery Activities (Pre-Implementation)

#### D1: Technical Feasibility Spike - GitHub API Rate Limits

**Objective:** Validate daily Claude Code version checks won't hit rate limits

**Method:**
1. Review GitHub API rate limit docs (authenticated: 5000 requests/hour)
2. Calculate requests needed: 1 API call/day = 30 calls/month
3. Verify authenticated requests use `GITHUB_TOKEN` from Actions
4. Test API call locally with curl

**Success Criteria:**
- Daily checks use < 0.02% of rate limit (1 of 5000)
- `GITHUB_TOKEN` in Actions confirmed to provide authentication
- API response format validated

**Timeline:** 1 hour
**Status:** ✅ Already validated - GitHub Actions provides GITHUB_TOKEN automatically

---

#### D2: Concierge Test - Version Display Usability

**Objective:** Validate users understand dual version display (core + agents)

**Method:**
1. Create mockup of `flowspec version` output
2. Show to 3-5 developers (outside team)
3. Ask: "What versions are installed? Which can you upgrade independently?"
4. Iterate on output format based on feedback

**Mockup:**
```bash
$ flowspec version
Flowspec: v0.3.011
Agents:   v1.5.0 (Claude Code: v2024.12.20)
```

**Success Criteria:**
- 80%+ of testers correctly identify both versions
- 80%+ understand agents can upgrade independently
- No confusion about Claude Code version meaning

**Timeline:** 2-3 hours
**Status:** Pending (task-566 implementation)

---

#### D3: Usability Test - Release Notes Clarity

**Objective:** Validate users distinguish agent vs. core releases

**Method:**
1. Create mock release notes for agent-only release
2. Show to 3-5 developers alongside core release notes
3. Ask: "What changed? Do you need to upgrade flowspec core?"
4. Iterate on format based on confusion points

**Success Criteria:**
- 90%+ correctly identify as agent-only release
- 90%+ understand core upgrade not needed
- Release note template validated

**Timeline:** 2 hours
**Status:** Pending (task-565 implementation)

---

### Validation Checkpoints (During Implementation)

#### V1: Version Management Validation (After task-561)

**Tests:**
- agents-version.json parses correctly
- Semver validation rejects invalid versions
- Version read/write operations are atomic
- Concurrent access doesn't corrupt file

**Validation Method:** Unit tests + manual inspection

---

#### V2: Workflow Trigger Validation (After task-563)

**Tests:**
- Path change to .github/agents/** triggers workflow
- Change to claude-code-version.txt triggers workflow
- Manual workflow_dispatch works
- Core release paths do NOT trigger agents workflow
- Agents release paths do NOT trigger core workflow

**Validation Method:** Integration tests with act + CI runs

---

#### V3: Package Integrity Validation (After task-564)

**Tests:**
- All 49 agent files included in archive
- Metadata files present and valid
- Archive size < 1MB
- Extraction creates correct directory structure
- No extra files included

**Validation Method:** Automated tests + manual extraction verification

---

#### V4: End-to-End Release Validation (After task-567)

**Scenario:** Complete release cycle from commit to published release

**Steps:**
1. Commit agent file change to main
2. Wait for workflow to trigger
3. Verify tag created with agents/v* format
4. Verify package uploaded to GitHub release
5. Verify release notes generated correctly
6. Download and extract package
7. Verify all contents present

**Success Criteria:**
- Complete cycle in < 5 minutes
- All artifacts present and valid
- No manual intervention required

**Validation Method:** End-to-end test in staging environment

---

### Risk Mitigation Through Discovery

**Risk:** Users confused by dual versioning  
**Mitigation:** D2 concierge test validates version display clarity

**Risk:** Workflows conflict and trigger incorrectly  
**Mitigation:** V2 trigger validation ensures mutual exclusion

**Risk:** Releases fail silently or leave partial state  
**Mitigation:** V4 end-to-end validation tests complete flow

**Risk:** Package corruption or missing files  
**Mitigation:** V3 package integrity validation with automated tests

---

## 8. Acceptance Criteria and Testing

### System-Level Acceptance Criteria

#### AC-1: Independent Release Capability

**Criterion:** Agent releases work without triggering core release

**Test:**
1. Modify single agent file in `.github/agents/`
2. Commit and push to main
3. Verify only `release-agents.yml` triggers
4. Verify core `release.yml` does not trigger
5. Verify agents release published

**Pass Criteria:**
- Agents release published within 5 minutes
- Core release NOT triggered
- Tag uses `agents/v*` format

---

#### AC-2: Claude Code Version Tracking

**Criterion:** System detects and responds to Claude Code updates

**Test:**
1. Mock Claude Code release via API (test environment)
2. Wait for cron job (or trigger manually)
3. Verify claude-code-version.txt updated
4. Verify agents release triggered
5. Verify release notes mention Claude Code version

**Pass Criteria:**
- Version file updated within 24 hours of Claude Code release
- Agents release triggered automatically
- Release notes show new Claude Code version

---

#### AC-3: Manual Emergency Release

**Criterion:** Maintainers can trigger emergency releases manually

**Test:**
1. Navigate to Actions → Release Agents workflow
2. Click "Run workflow"
3. Enter version override (e.g., v1.4.1 for patch)
4. Verify release created with correct version
5. Verify release marked as emergency in notes

**Pass Criteria:**
- Manual trigger completes successfully
- Version override respected
- Release notes indicate manual trigger

---

#### AC-4: Version Display Accuracy

**Criterion:** CLI shows correct core and agents versions

**Test:**
1. Install flowspec v0.3.011 with agents v1.5.0
2. Run `flowspec version`
3. Verify output shows both versions
4. Run `flowspec version --json`
5. Verify JSON structure includes all version fields

**Pass Criteria:**
```bash
$ flowspec version
Flowspec: v0.3.011
Agents:   v1.5.0 (Claude Code: v2024.12.20)

$ flowspec version --json
{
  "core": "0.3.011",
  "agents": "1.5.0",
  "claude_code": "2024.12.20"
}
```

---

#### AC-5: Release Coordination

**Criterion:** Core and agents releases don't conflict

**Test:**
1. Trigger core release (merge release/v* PR)
2. While core release running, commit agent change
3. Verify agents release waits or runs in parallel
4. Verify both complete successfully
5. Verify distinct tags created (v0.3.012 vs agents/v1.5.1)

**Pass Criteria:**
- Both releases complete successfully
- No tag collisions
- Both GitHub releases published
- Release notes clearly distinguish releases

---

### Component-Level Testing

#### Unit Tests (task-561)

**Coverage:** Version management utilities
- `read_version()` - reads agents-version.json
- `write_version()` - writes agents-version.json atomically
- `validate_semver()` - validates version format
- `bump_version()` - increments version numbers

**Test Cases:**
- Valid version reads correctly
- Invalid JSON returns error
- Missing file returns default
- Write creates file if missing
- Concurrent writes don't corrupt file
- Invalid semver rejected
- Bump logic: 1.2.3 → 1.2.4 (patch), 1.2.3 → 1.3.0 (minor), 1.2.3 → 2.0.0 (major)

---

#### Integration Tests (task-568)

**Workflow:** release-agents.yml
- Path-based trigger test
- Version-based trigger test
- Manual trigger test
- Tag creation test
- Package creation test
- Release notes generation test

**Test Environment:** GitHub Actions with `act` for local testing

---

#### End-to-End Tests

**Scenario 1: Agent Bug Fix Release**
1. Developer fixes bug in `flow-implement.agent.md`
2. PR merged to main
3. release-agents.yml triggers
4. Version bumped from v1.5.0 to v1.5.1
5. Package created and uploaded
6. Release notes show bug fix

**Expected Result:** Release published within 5 minutes, users can download v1.5.1

---

**Scenario 2: Claude Code Update**
1. Claude Code releases v2024.12.25
2. Daily cron job detects new version
3. claude-code-version.txt updated via commit
4. Commit triggers release-agents.yml
5. Version bumped from v1.5.1 to v1.6.0 (minor)
6. Release notes show Claude Code v2024.12.25 compatibility

**Expected Result:** Agents release within 24 hours of Claude Code release

---

### Performance Testing

**Test:** Release workflow duration
- **Metric:** Time from trigger to published release
- **Target:** < 5 minutes for 95% of releases
- **Method:** Track workflow durations over 20 releases

**Test:** Package size
- **Metric:** Archive size in bytes
- **Target:** < 1MB
- **Method:** Automated check in CI

**Test:** API rate limit usage
- **Metric:** GitHub API calls per day
- **Target:** < 10 calls/day (well under 5000/hour limit)
- **Method:** Monitor API usage in Actions logs

---

### Security Testing

**Test:** Tag signature validation
- **Method:** `git tag -v agents/v1.5.0`
- **Expected:** Valid GPG signature from github-actions[bot]

**Test:** Token permissions
- **Method:** Review workflow permissions in .github/workflows/release-agents.yml
- **Expected:** Only `contents: write`, no admin/workflow/packages

**Test:** Version file integrity
- **Method:** Git log shows all version changes committed
- **Expected:** No manual edits, all changes via workflow

---

### Regression Testing

**Test:** Core release still works
- **Method:** Trigger core release after agents release deployed
- **Expected:** Core release completes without errors, ignores agent paths

**Test:** Existing agent sync works
- **Method:** Run sync-copilot-agents.sh after agents release
- **Expected:** No drift detected, agents remain in sync

---

## 9. Dependencies and Constraints

### External Dependencies

#### D1: GitHub Actions Infrastructure

**Dependency:** GitHub Actions availability and performance
**Impact:** All workflows depend on GitHub Actions runtime
**Risk:** Medium - GitHub occasionally has outages
**Mitigation:**
- Workflows are idempotent (can be re-run)
- Manual fallback available (workflow_dispatch)
- Monitor GitHub status: https://www.githubstatus.com/

---

#### D2: GitHub API

**Dependency:** GitHub REST API for Claude Code version checks
**Impact:** Daily cron job requires API access
**Risk:** Low - API is highly reliable
**Constraints:**
- Rate limit: 5000 requests/hour (authenticated)
- API changes could break version checking
**Mitigation:**
- Use conservative rate limit (1 request/day = negligible)
- Version API responses and handle changes gracefully
- Fallback to manual trigger if API fails

---

#### D3: Claude Code Release Schedule

**Dependency:** Claude Code publishes releases to GitHub
**Impact:** Version tracking depends on Claude Code using GitHub releases
**Risk:** Low - Claude Code consistently uses GitHub releases
**Constraints:**
- No control over Claude Code release schedule
- Version format may change
**Mitigation:**
- Flexible version parsing (regex-based)
- Manual override available if auto-detection fails

---

### Internal Dependencies

#### D4: Existing Agent Sync Infrastructure

**Dependency:** sync-copilot-agents.sh script (lines 1-1114)
**Impact:** Agents release uses existing sync logic
**Risk:** Low - script is mature and tested
**Benefits:**
- Reuses proven patterns
- No need to rewrite sync logic
**Constraints:**
- Changes to sync script may affect releases
**Mitigation:**
- Test agent releases when sync script changes
- Version sync script if needed

---

#### D5: Flowspec Core Version in pyproject.toml

**Dependency:** Core version management via pyproject.toml
**Impact:** Agents version must coordinate with core version
**Risk:** Low - well-established pattern
**Constraints:**
- Agents version independent but compatible
- Must maintain compatibility matrix
**Mitigation:**
- Document compatibility rules clearly
- Automated compatibility validation in CI

---

### Technical Constraints

#### C1: Same Repository Architecture

**Constraint:** Agents must stay in same repo as core
**Rationale:** Agents tightly coupled to flowspec commands (templates/commands/)
**Impact:** Cannot use separate repo for agents
**Benefits:**
- Single source of truth
- Atomic changes (commands + agents)
- Simplified development workflow
**Trade-offs:**
- More complex release coordination
- Dual workflow maintenance

---

#### C2: Backward Compatibility

**Constraint:** Agent releases must be backward compatible with core MAJOR version
**Rationale:** Users may upgrade agents without upgrading core
**Impact:** Breaking changes require MAJOR version bump
**Enforcement:**
- Document compatibility in release notes
- Test agents against current core version
- Breaking changes trigger compatibility warning

---

#### C3: Tag Namespace Separation

**Constraint:** Core uses `v*` tags, agents use `agents/v*` tags
**Rationale:** Prevent tag collisions between core and agents releases
**Impact:** Tooling must handle both tag formats
**Benefits:**
- Clear separation of releases
- No possibility of collision
**Implementation:**
- Workflows filter by tag prefix
- Git tag listing shows clear separation

---

### Resource Constraints

#### R1: CI/CD Minutes

**Constraint:** GitHub Actions free tier: 2000 minutes/month
**Impact:** Each agents release uses ~5 minutes
**Calculation:**
- Agents releases: ~8/month × 5 min = 40 min/month
- Core releases: ~4/month × 10 min = 40 min/month
- Other CI: ~1000 min/month
- **Total:** ~1080 min/month (well under limit)
**Risk:** Low - plenty of headroom
**Mitigation:** Monitor usage monthly

---

#### R2: Storage (GitHub Releases)

**Constraint:** GitHub releases storage (no hard limit for small projects)
**Impact:** Each agents release adds ~1MB archive
**Calculation:**
- Agents releases: ~8/month × 1MB = 8MB/month
- Core releases: ~4/month × 50MB = 200MB/month
- **Total:** ~208MB/month ≈ 2.5GB/year
**Risk:** Very low - well under any reasonable limit
**Mitigation:** Prune old releases periodically (scripts/bash/prune-releases.sh)

---

#### R3: Maintainer Time

**Constraint:** Limited maintainer bandwidth
**Impact:** Dual workflows require more maintenance
**Estimation:**
- Initial setup: 40-52 hours (one-time)
- Ongoing maintenance: ~2 hours/month
- Emergency fixes: ~4 hours/incident (rare)
**Risk:** Medium - time commitment
**Mitigation:**
- Automate as much as possible
- Reuse existing patterns
- Clear documentation for self-service

---

### Dependency Matrix

| Dependency | Type | Impact | Risk | Mitigation |
|-----------|------|--------|------|-----------|
| GitHub Actions | External | High | Medium | Idempotent workflows |
| GitHub API | External | Medium | Low | Conservative rate limits |
| Claude Code releases | External | Medium | Low | Flexible parsing |
| sync-copilot-agents.sh | Internal | High | Low | Test on changes |
| pyproject.toml | Internal | Low | Low | Compatibility matrix |
| Same repo constraint | Technical | High | N/A | Conditional CI |
| Backward compatibility | Technical | Medium | Low | Semver enforcement |
| Tag namespacing | Technical | Low | Very Low | Prefix filtering |

---

## 10. Success Metrics (Outcome-Focused)

### North Star Metric

**Metric:** Time from agent improvement to user deployment
**Baseline:** ~14 days (tied to core releases)
**Target:** ≤ 3 days (24-48 hours release + 1-2 days adoption)
**Measurement:** Track commit timestamp to release timestamp to download timestamp

**Why this metric:**
- Directly measures customer value (fast access to improvements)
- Captures entire value delivery chain
- Aligns with SVPG outcome-over-output principle

---

### Primary Success Metrics

#### M1: Release Frequency

**Metric:** Agents releases per month
**Baseline:** ~1 release/month (tied to core)
**Target:** ≥ 2 releases/month (independent of core)
**Measurement:** Count GitHub releases with `agents/v*` tags per month

**Why it matters:** More frequent releases = faster delivery of value to users

---

#### M2: Security Patch Deployment Time

**Metric:** Time from security vulnerability discovery to patch release
**Baseline:** ~14 days (next core release)
**Target:** ≤ 48 hours (emergency release)
**Measurement:** Track vulnerability report timestamp to agents release timestamp

**Why it matters:** Security vulnerabilities expose users; fast patching reduces risk

---

#### M3: Claude Code Compatibility Lag

**Metric:** Days between Claude Code release and flowspec agents support
**Baseline:** ~21 days (no tracking, manual process)
**Target:** ≤ 7 days (automated tracking + quick release)
**Measurement:** Track Claude Code release date to agents release date (from release notes)

**Why it matters:** Users want to leverage latest Claude Code features; lag frustrates early adopters

---

#### M4: User Adoption Rate

**Metric:** Percentage of users on latest agents version within 2 weeks
**Baseline:** N/A (no independent agents releases yet)
**Target:** ≥ 60% adoption within 2 weeks of release
**Measurement:** Track download counts from GitHub releases API

**Why it matters:** Releases only create value if users actually upgrade

---

### Secondary Success Metrics

#### M5: Release Success Rate

**Metric:** Percentage of agents releases that complete without errors
**Target:** ≥ 99% success rate
**Measurement:** Count successful vs. failed workflow runs

**Why it matters:** Failed releases waste time and delay value delivery

---

#### M6: Workflow Duration

**Metric:** Time from trigger to published release
**Target:** 95th percentile ≤ 5 minutes
**Measurement:** GitHub Actions duration logs

**Why it matters:** Fast releases reduce context switching and enable rapid iteration

---

#### M7: User Confusion Rate

**Metric:** Support tickets/questions about agent vs. core versioning
**Baseline:** N/A (no dual versioning yet)
**Target:** ≤ 2 questions/month after documentation published
**Measurement:** Track GitHub issues/discussions tagged with "versioning"

**Why it matters:** Confusion indicates poor usability; reduces trust

---

#### M8: Breaking Change Frequency

**Metric:** Percentage of releases requiring MAJOR version bump
**Target:** ≤ 5% of releases (mostly MINOR/PATCH)
**Measurement:** Analyze version number changes (X.0.0 vs. 0.X.0 vs. 0.0.X)

**Why it matters:** Breaking changes force user upgrades; should be rare

---

### Measurement Dashboard

**Location:** GitHub repository README.md
**Update Frequency:** Monthly

**Dashboard Contents:**
```markdown
## Agents Release Metrics (Last 30 Days)

| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Releases/Month | ≥2 | 3 | ↑ |
| Time to Patch | ≤48h | 36h | ✓ |
| Claude Code Lag | ≤7d | 5d | ✓ |
| Adoption @ 2wk | ≥60% | 68% | ↑ |
| Success Rate | ≥99% | 100% | ✓ |
| Avg Duration | ≤5min | 4.2min | ✓ |
```

---

### Success Criteria Validation

**At 1 Month Post-Launch:**
- M1: Released agents ≥2 times
- M2: At least 1 security patch deployed (if vulnerability found)
- M6: 95% of releases complete in <5 minutes

**At 3 Months Post-Launch:**
- M3: Claude Code lag ≤7 days for ≥80% of Claude Code releases
- M4: User adoption ≥60% within 2 weeks for ≥75% of releases
- M7: User confusion ≤2 questions/month

**At 6 Months Post-Launch:**
- All primary metrics hitting targets consistently
- North Star Metric: Time to deployment ≤3 days for 90% of releases
- M8: Breaking changes ≤5% of releases

---

### Leading vs. Lagging Indicators

**Leading Indicators (Predict Success):**
- Agent file commits per week → Predicts release frequency
- Workflow run success rate → Predicts release reliability
- Documentation views → Predicts user awareness

**Lagging Indicators (Measure Success):**
- Actual release frequency → Confirms value delivery
- Adoption rate → Confirms user uptake
- Support tickets → Confirms usability

---

### OKR Alignment

**Objective:** Enable rapid delivery of agent improvements to users

**Key Results:**
1. **KR1:** Increase agents release frequency from 1/month to ≥2/month (M1)
2. **KR2:** Reduce security patch deployment time from 14 days to ≤48 hours (M2)
3. **KR3:** Achieve ≥60% user adoption of latest agents within 2 weeks (M4)
4. **KR4:** Maintain ≥99% release success rate with <5min duration (M5, M6)

**Tracking Cadence:** Monthly review with quarterly OKR assessment

---

## All Needed Context

### Examples from Existing Codebase

These examples provide proven patterns to reuse in the implementation:

#### Example 1: Path-Based Workflow Triggers
**File:** `.github/workflows/validate-agent-sync.yml` (lines 5-9)

```yaml
on:
  push:
    branches: [main]
    paths:
      - '.github/agents/**'
      - 'templates/commands/**'
      - 'scripts/bash/sync-copilot-agents.sh'
```

**Relevance:** Shows how to trigger workflows only when specific paths change. Use this pattern for `release-agents.yml` to trigger on `.github/agents/**` and `claude-code-version.txt` changes.

---

#### Example 2: Conditional Workflow Execution
**File:** `.github/workflows/release.yml` (lines 37-40)

```yaml
if: |
  github.event_name == 'workflow_dispatch' ||
  (github.event.pull_request.merged == true &&
   startsWith(github.event.pull_request.head.ref, 'release/v'))
```

**Relevance:** Shows how to conditionally run workflows based on event type. Use this pattern to support manual `workflow_dispatch` triggers alongside automatic path-based triggers.

---

#### Example 3: Version Extraction from Branch Names
**File:** `.github/workflows/release.yml` (lines 73-79)

```yaml
# Extract version from branch name (release/v0.2.344 -> v0.2.344)
VERSION="${PR_BRANCH#release/}"
echo "PR-based release from branch: $PR_BRANCH"

VERSION_NUM="${VERSION#v}"

# Validate version format
if ! [[ "$VERSION_NUM" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "::error::Invalid version format: $VERSION_NUM"
  exit 1
fi
```

**Relevance:** Shows version extraction and semver validation. Adapt this pattern to extract version from `agents-version.json` instead of branch name.

---

#### Example 4: Agent Packaging Logic
**File:** `.github/workflows/scripts/create-release-packages.sh` (lines 251-343)

```bash
build_variant() {
  local agent=$1 script=$2
  local base_dir="$GENRELEASES_DIR/sdd-${agent}-package-${script}"
  echo "Building $agent ($script) package..."
  mkdir -p "$base_dir"

  # Copy base structure but filter scripts by variant
  SPEC_DIR="$base_dir/.flowspec"
  mkdir -p "$SPEC_DIR"

  [[ -d memory ]] && { cp -r memory "$SPEC_DIR/"; echo "Copied memory -> .flowspec"; }

  # ... (packaging logic continues)

  ( cd "$base_dir" && zip -r "../spec-kit-template-${agent}-${script}-${NEW_VERSION}.zip" . )
  echo "Created $GENRELEASES_DIR/spec-kit-template-${agent}-${script}-${NEW_VERSION}.zip"
}
```

**Relevance:** Shows how to package files into versioned zip archives. Adapt this pattern to package agent files into `flowspec-agents-vX.Y.Z.zip`.

---

#### Example 5: Agent Sync Validation
**File:** `scripts/bash/sync-copilot-agents.sh` (lines 824-843)

```bash
elif [[ "$VALIDATE" == true ]]; then
  # Compare with existing file
  if [[ -f "$output_file" ]]; then
    local existing
    # Normalize line endings and trailing whitespace for cross-platform comparison
    existing=$(cat "$output_file" | tr -d '\r')
    local normalized_output
    normalized_output=$(printf '%s' "$output" | tr -d '\r')
    if [[ "$existing" != "$normalized_output" ]]; then
      log_error "Drift detected: ${role}-${command}.agent.md"
      ERRORS=$((ERRORS + 1))
      return 1
    fi
    log_verbose "Validated: ${role}-${command}.agent.md"
  else
    log_error "Missing: ${role}-${command}.agent.md"
    ERRORS=$((ERRORS + 1))
    return 1
  fi
fi
```

**Relevance:** Shows validation pattern for checking if generated files match expectations. Use this pattern to validate package contents in CI.

---

### Architectural Decisions

#### Decision 1: Same Repo with Conditional CI (Already Made)

**Context:** task-556 assessment evaluated separate repo vs. conditional CI

**Decision:** Use conditional CI in same repo with independent versioning

**Rationale:**
- Agents are tightly coupled to flowspec commands in `templates/commands/`
- Single source of truth prevents drift
- Atomic changes possible (command + agent in same PR)
- Simpler development workflow

**Trade-offs:**
- More complex release coordination (two workflows)
- Dual versioning requires careful documentation
- BUT: Benefits outweigh complexity

---

#### Decision 2: Tag Namespacing (agents/v* vs v*)

**Context:** Need to prevent tag collisions between core and agents releases

**Decision:** Core uses `v*` tags, agents use `agents/v*` tags

**Benefits:**
- Clear visual separation in git log
- Impossible to have tag collisions
- Workflows can filter by prefix
- Release pages clearly distinguished

**Implementation:** Workflows use tag prefix filtering

---

#### Decision 3: Independent Versioning (Not Tied to Core)

**Context:** Agents may need to release more frequently than core

**Decision:** Agents have independent semver version (tracked in agents-version.json)

**Benefits:**
- Agents can release on their own schedule
- Users can upgrade agents without core upgrade
- Clear signal of what changed (agents vs. core)

**Trade-offs:**
- Users must track two versions
- Compatibility matrix needed
- BUT: Flexibility worth the complexity

---

### Critical File Locations

**Version Management:**
- `/agents-version.json` - Agents version metadata
- `/claude-code-version.txt` - Tracked Claude Code version
- `/pyproject.toml` - Core version (existing)

**Workflows:**
- `/.github/workflows/release-agents.yml` - Agents release workflow (new)
- `/.github/workflows/track-claude-code.yml` - Version tracking cron (new)
- `/.github/workflows/release.yml` - Core release workflow (modify: add paths-ignore)

**Scripts:**
- `/.github/workflows/scripts/package-agents.sh` - Agent packaging (new)
- `/.github/workflows/scripts/generate-agents-release-notes.sh` - Release notes (new)
- `/scripts/bash/sync-copilot-agents.sh` - Agent sync (existing, reuse)

**Documentation:**
- `/docs/guides/agent-release-process.md` - User-facing release guide (new)
- `/docs/prd/flowspec-agents-release-spec.md` - This PRD (new)

---

### Glossary

**Agent:** A markdown file in `.github/agents/` that defines a Copilot agent (e.g., `flow-implement.agent.md`)

**Agents Release:** A GitHub release tagged with `agents/v*` containing only agent files and metadata

**Claude Code:** The upstream tool (Claude.ai/code) that flowspec agents are designed for

**Core Release:** A GitHub release tagged with `v*` containing the full flowspec Python package

**Independent Release:** Agent releases that occur separately from core releases, on their own schedule

**Semver:** Semantic versioning (MAJOR.MINOR.PATCH) for version numbers

**Tag Namespace:** Prefix used for git tags to prevent collisions (e.g., `agents/` vs. none)

**Version Tracking:** Automated detection of upstream tool (Claude Code) version changes

---

### Open Questions (To Be Resolved During Implementation)

1. **Q:** Should agents version auto-increment MINOR or PATCH by default?
   - **Answer needed by:** task-557 (design phase)
   - **Options:** PATCH for bug fixes, MINOR for new agents, MAJOR for breaking changes

2. **Q:** What constitutes a "breaking change" for agents?
   - **Answer needed by:** task-557 (design phase)
   - **Examples:** Removing an agent? Changing agent interface? Changing command structure?

3. **Q:** Should `flowspec agents upgrade` command be in MVP or future enhancement?
   - **Answer needed by:** Before sprint planning
   - **Current:** Marked as low priority (task-570)
   - **Consideration:** May increase adoption if included in MVP

4. **Q:** How often should compatibility matrix be regenerated?
   - **Answer needed by:** task-571 (future enhancement)
   - **Options:** Every release? Weekly? On-demand?

---

### Related Documentation

**SVPG Principles:**
- Product Operating Model (POM) - Empowered teams, outcomes over outputs
- Continuous Discovery - Weekly validation, fast learning
- DVF+V Risk Framework - Value, Usability, Feasibility, Viability

**Flowspec Documentation:**
- `docs/guides/backlog-user-guide.md` - Backlog.md integration
- `docs/guides/workflow-architecture.md` - SDD workflow overview
- `docs/reference/agent-loop-classification.md` - Agent role classification

**GitHub Actions:**
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [GitHub releases API](https://docs.github.com/en/rest/releases)

---

## Summary and Next Steps

### Executive Summary

This PRD defines the **independent flowspec-agents release process**, enabling agent improvements and Claude Code compatibility updates to release independently from flowspec core releases. The solution uses conditional CI in the same repository with independent versioning, leveraging existing infrastructure while providing rapid value delivery to users.

**Key Benefits:**
- Agents release 2x more frequently (target: ≥2/month vs. current ~1/month)
- Security patches deployed in 48 hours (vs. current ~14 days)
- Claude Code compatibility within 7 days (vs. current ~21 days)
- Users upgrade agents independently of core

**Implementation Scope:**
- 15 tasks across 4 phases (design, implementation, testing, future enhancements)
- Estimated 40-52 hours total effort
- 4-week delivery timeline (sprints mapped in section 6)

---

### Immediate Next Steps

1. **Review and Approve PRD** (This Document)
   - Stakeholders review sections 1-10
   - Validate DVF+V risk assessment (section 3)
   - Approve task breakdown (section 6)
   - **Timeline:** 2-3 days

2. **Begin Design Phase** (Sprint 1, Week 1)
   - Execute tasks 557-560 (design tasks)
   - Conduct discovery activities (section 7)
   - Validate version management design
   - **Timeline:** 1 week

3. **Implement Core Functionality** (Sprint 2, Week 2)
   - Execute tasks 561-564, 567 (high-priority implementation)
   - Validate workflows via V1-V3 checkpoints (section 7)
   - **Timeline:** 1 week

4. **Complete Testing and Documentation** (Sprint 3-4, Weeks 3-4)
   - Execute tasks 565-566, 568-569
   - Run end-to-end validation (V4)
   - Publish documentation
   - **Timeline:** 2 weeks

---

### Success Criteria for This PRD

This PRD is successful if:
- All stakeholders understand the problem, solution, and benefits
- DVF+V risks are identified and mitigated
- Task breakdown is actionable and estimated
- Implementation can proceed without ambiguity
- Success metrics are clear and measurable

---

### Stakeholder Sign-Off

**Product Manager:** ____________________ Date: __________  
**Tech Lead:** ____________________ Date: __________  
**Engineering Team:** ____________________ Date: __________

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-25  
**Status:** Draft - Pending Review
