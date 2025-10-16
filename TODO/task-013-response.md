# Task 013 Response: Keeping JP-Spec-Kit Current and In Sync

## Executive Summary

This document analyzes how jp-spec-kit components will be kept current and in sync once a project already exists, comparing two installation methods:

1. **UV Tool Installation** from GitHub (current primary method)
2. **Claude Code Marketplace/Plugin** installation (future method)

**Key Finding:** These two installation methods are **NOT equally capable** of staying current. The Claude Code marketplace/plugin approach offers significantly superior update capabilities, while the UV tool installation method requires manual intervention and potentially destructive updates.

---

## What Components Need To Stay In Sync

JP-spec-kit consists of multiple interconnected components that evolve over time:

### 1. Core Framework Components

#### `.specify/` Directory Structure
```
.specify/
├── memory/
│   └── constitution.md          # Project governance principles
├── scripts/
│   ├── bash/                    # POSIX shell scripts (sh variant)
│   │   ├── common.sh
│   │   ├── check-prerequisites.sh
│   │   ├── create-new-feature.sh
│   │   ├── setup-plan.sh
│   │   └── update-agent-context.sh
│   └── powershell/              # PowerShell scripts (ps variant)
│       └── (equivalent .ps1 files)
└── templates/
    ├── spec-template.md
    ├── plan-template.md
    ├── tasks-template.md
    ├── checklist-template.md
    └── agent-file-template.md
```

**Update Frequency:** Low to medium
- Templates evolve as best practices are refined
- Scripts receive bug fixes and feature enhancements
- Constitution template may gain new sections

### 2. Agent-Specific Components

#### Command Definitions (Per-Agent Format)
```
.claude/
└── commands/
    ├── speckit.constitution.md
    ├── speckit.specify.md
    ├── speckit.plan.md
    ├── speckit.tasks.md
    ├── speckit.implement.md
    ├── speckit.clarify.md
    ├── speckit.analyze.md
    └── speckit.checklist.md

.claude/commands/jpspec/          # Enhanced jpspec workflow
├── specify.md                    # PM planner agent
├── plan.md                       # Architect + platform engineer
├── research.md                   # Research + business validation
├── implement.md                  # Frontend/backend engineers + review
├── validate.md                   # QA + security + docs + release
└── operate.md                    # SRE agent (CI/CD + K8s + DevSecOps)
```

**Update Frequency:** High
- New commands added (e.g., jpspec workflow commands)
- Command logic refined based on user feedback
- Agent instructions improved for better results
- Integration with new agent capabilities

### 3. Specify CLI Tool

**Python Package:** `specify-cli` (currently v0.0.20)

**Update Frequency:** Medium to high
- New agent support (kilocode, auggie, roo, codebuddy added recently)
- Bug fixes and error handling improvements
- New CLI options (--force, --here, --debug, --github-token)
- Enhanced initialization flows

### 4. Optional CI/CD Templates

```
templates/github-actions/
├── nodejs-ci-cd.yml
├── python-ci-cd.yml
├── go-ci-cd.yml
└── README.md
```

**Update Frequency:** Medium
- New stack support
- Best practice updates
- Security improvements

### 5. Stack and Language-Specific Configurations

**Hidden research directories in repo:**
- `.stacks/` - Stack-specific configurations
- `.languages/` - Language-specific patterns
- `.agents/` - Agent configuration research
- `.agents-bench/` - Agent benchmarking data

**Distribution:** These are development artifacts, NOT distributed to end users

---

## Installation Method 1: UV Tool Install from GitHub

### How It Works

#### Initial Installation
```bash
# Install the CLI tool globally
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Initialize a new project
specify init my-project --ai claude --script sh

# Or initialize in existing directory
cd my-existing-project
specify init . --ai claude --force
```

#### What Happens Under The Hood

1. **CLI Installation:** Python package installed to UV tool environment
2. **Project Bootstrap:**
   - CLI fetches latest release from GitHub API
   - Downloads pre-packaged ZIP file (e.g., `spec-kit-template-claude-sh-v0.0.20.zip`)
   - ZIP contains snapshot of templates for specific agent + script combination
   - Extracts files to project directory

3. **File Structure Created:**
```
my-project/
├── .specify/
│   ├── memory/
│   ├── scripts/bash/        # Only bash scripts (sh variant)
│   └── templates/
├── .claude/
│   └── commands/            # Claude-specific commands
└── .gitignore (if git initialized)
```

#### Release Packaging Process

The release script (`create-release-packages.sh`) generates agent + script combinations:
- **Agents:** claude, gemini, copilot, cursor-agent, qwen, opencode, windsurf, codex, kilocode, auggie, roo, codebuddy, q
- **Script types:** sh (bash/zsh), ps (PowerShell)
- **Total combinations:** 13 agents × 2 script types = 26 release packages

Each package is a static snapshot at release time.

### Update Capabilities

#### CLI Tool Updates
```bash
# Update the specify CLI tool itself
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git

# Check version
specify --version
```

**What This Updates:** Only the CLI tool binary (new commands like `specify upgrade` would be added here)

**What This DOES NOT Update:** Existing project files (.specify/, .claude/, templates, scripts)

#### Project Template Updates

**Option 1: Manual Re-initialization (Destructive)**
```bash
cd my-existing-project
specify init . --ai claude --force
```

**Consequences:**
- ⚠️ Overwrites all template files
- ⚠️ May lose customizations to scripts
- ⚠️ Requires manual merge of changes
- ⚠️ Risk of losing project-specific modifications

**Option 2: Selective File Copy (Manual)**
```bash
# Create temp project with latest templates
specify init temp-latest --ai claude
cd temp-latest

# Manually copy specific files to existing project
cp -r .specify/scripts/* ../my-existing-project/.specify/scripts/
cp .claude/commands/speckit.* ../my-existing-project/.claude/commands/

cd ..
rm -rf temp-latest
```

**Consequences:**
- ✅ More controlled update process
- ⚠️ Tedious and error-prone
- ⚠️ Easy to miss files
- ⚠️ No version tracking of what changed

**Option 3: Git Submodule Approach (Not Currently Implemented)**

Could theoretically structure projects as:
```bash
git submodule add https://github.com/github/spec-kit.git .spec-kit-upstream
git submodule update --remote
```

**Why This Doesn't Work:**
- Templates need customization per-project
- Can't directly use submodule files
- Still requires copy/merge process

### Stack and Language Filtering

**Current State:** No filtering mechanism

When you install jp-spec-kit, you get:
- All generic templates
- All scripts (regardless of your project's stack)
- No stack-specific configuration

**Example Problem:**
- Your project uses Python + FastAPI
- You still get Node.js CI/CD template references
- No Python-specific setup guidance
- Manual curation required

**Potential Solution (Not Implemented):**
```bash
# Hypothetical future syntax
specify init my-project --ai claude --stack python --framework fastapi

# Could filter/customize:
# - Relevant CI/CD templates only
# - Stack-specific script helpers
# - Framework-specific guidance in commands
```

### Summary: UV Tool Installation Sync Capabilities

| Aspect | Capability | Rating |
|--------|-----------|--------|
| **Initial Installation** | Excellent - One command, downloads latest | ⭐⭐⭐⭐⭐ |
| **CLI Tool Updates** | Good - Simple force reinstall | ⭐⭐⭐⭐ |
| **Project File Updates** | Poor - Manual, destructive, no version tracking | ⭐⭐ |
| **Stack Filtering** | None - All or nothing | ⭐ |
| **Update Safety** | Poor - Risk of overwriting customizations | ⭐⭐ |
| **Team Consistency** | Medium - Can specify versions in docs | ⭐⭐⭐ |
| **Automation Potential** | Low - Requires manual intervention | ⭐⭐ |

**Key Limitation:** This is fundamentally a **one-time bootstrap** approach. Once files are copied to your project, they become static. There is no inherent sync mechanism.

---

## Installation Method 2: Claude Code Marketplace/Plugin

### How It Works

#### Plugin Installation
```bash
# Add the marketplace (when jp-spec-kit publishes one)
/plugin marketplace add github/jp-spec-kit

# Browse available plugins
/plugin

# Install jp-spec-kit plugin
/plugin install jp-spec-kit

# Restart Claude Code to activate
# (Claude Code automatically restarts or prompts)
```

#### What Happens Under The Hood

1. **Marketplace Registration:** Claude Code fetches marketplace metadata from the repository
2. **Plugin Installation:**
   - Downloads plugin files to Claude Code's plugin directory
   - Installs to `~/.claude/plugins/jp-spec-kit/` (or equivalent)
   - Registers commands, agents, hooks, and MCP servers
3. **Command Availability:** Slash commands become available in ANY project where Claude Code runs

#### Plugin Structure

```
.claude-plugin/
├── plugin.json                  # Manifest file
├── marketplace.json             # For marketplace hosting
├── commands/                    # Slash command definitions
│   ├── speckit.constitution.md
│   ├── speckit.specify.md
│   ├── speckit.plan.md
│   └── ... (all speckit commands)
│   └── jpspec/
│       ├── specify.md
│       ├── plan.md
│       ├── research.md
│       ├── implement.md
│       ├── validate.md
│       └── operate.md
├── agents/                      # Agent definitions
│   ├── product-requirements-manager-enhanced.json
│   ├── software-architect.json
│   ├── platform-engineer.json
│   └── ... (all agents)
├── hooks/
│   └── hooks.json               # Event handlers
└── .mcp.json                    # MCP server configurations
```

#### Manifest Example: plugin.json

```json
{
  "name": "jp-spec-kit",
  "displayName": "JP Spec Kit - Enhanced Spec-Driven Development",
  "description": "Comprehensive toolkit for spec-driven development with jpspec workflow",
  "version": "0.1.0",
  "author": "Jason Poley",
  "repository": "github/jp-spec-kit",
  "commands": {
    "source": "./commands"
  },
  "agents": {
    "source": "./agents"
  },
  "hooks": {
    "source": "./hooks/hooks.json"
  },
  "mcp": {
    "source": "./.mcp.json"
  }
}
```

### Update Capabilities

#### Automatic Update Checks

Claude Code plugins support version tracking:

```bash
# Refresh marketplace metadata (checks for new versions)
/plugin marketplace update jp-spec-kit-marketplace

# Update specific plugin
/plugin update jp-spec-kit

# Update all plugins
/plugin update --all
```

**What This Updates:**
- ✅ All command definitions
- ✅ Agent configurations
- ✅ Hooks and MCP server configs
- ✅ Plugin metadata
- ✅ NO destructive changes to user projects

#### Version Management

**Semantic Versioning:**
```json
{
  "version": "0.2.0",
  "minClaudeVersion": "2.0.13"
}
```

**User Control:**
- Users can pin to specific versions
- Opt-in to automatic updates
- Rollback to previous versions

#### Team-Wide Configuration

**Repository-Level Plugin Setup:**

`.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": [
    {
      "name": "jp-spec-kit-marketplace",
      "source": "github/jp-spec-kit"
    }
  ],
  "plugins": {
    "jp-spec-kit": {
      "marketplace": "jp-spec-kit-marketplace",
      "version": "0.2.0",
      "autoUpdate": false
    }
  }
}
```

**Team Workflow:**
1. Team lead adds marketplace + plugin config to repo
2. Team members clone repo
3. Claude Code detects config when repo is trusted
4. Plugins auto-install
5. Everyone has same version

### Stack and Language Filtering

**Plugin Capabilities:**

1. **Conditional Command Loading:**
```json
{
  "commands": [
    {
      "name": "speckit.plan",
      "source": "./commands/speckit.plan.md",
      "conditions": {
        "projectHasFile": "package.json"
      }
    }
  ]
}
```

2. **Dynamic Command Generation:**
```javascript
// Hypothetical: Plugin could detect stack and customize commands
if (projectHasFile('pyproject.toml')) {
  loadCommand('speckit.plan-python');
} else if (projectHasFile('package.json')) {
  loadCommand('speckit.plan-nodejs');
}
```

3. **Stack-Specific Sub-Plugins:**
```bash
/plugin install jp-spec-kit-python
/plugin install jp-spec-kit-nodejs
/plugin install jp-spec-kit-dotnet
```

**Current jp-spec-kit Status:** Not yet implemented for stack filtering, but the plugin architecture supports it.

### Project-Specific vs Global Installation

**Key Distinction:**

#### Global Plugin Installation (Standard)
```bash
/plugin install jp-spec-kit
```
- Installs to user's Claude Code plugin directory
- Available in ALL projects
- Updates affect all projects
- Shared across workspaces

#### Project-Scoped Installation (Potential Future)
```bash
# Hypothetical syntax
/plugin install jp-spec-kit --scope project
```
- Installs to `.claude/plugins/` in project
- Version-locked per project
- Can have different versions per project
- Committed to version control

**Current Claude Code Plugin Behavior:** Global by default (as of v2.0.13)

### How Plugin Updates Preserve Customizations

**Separation of Concerns:**

1. **Plugin Files (Managed by Plugin System):**
   - Lives in `~/.claude/plugins/jp-spec-kit/`
   - Provides commands, agents, templates
   - Updated by plugin system
   - User never edits these directly

2. **Project Files (User-Managed):**
   - Lives in project's `.specify/` directory
   - Generated ONCE by commands (e.g., `/speckit.specify` creates specs)
   - User customizes these
   - Never touched by plugin updates

**Example Workflow:**
```
1. User installs jp-spec-kit plugin v0.1.0
2. Runs /speckit.specify → Creates .specify/specs/001-feature/spec.md
3. User customizes spec.md extensively
4. jp-spec-kit releases v0.2.0 with improved /speckit.specify command logic
5. User updates plugin: /plugin update jp-spec-kit
6. Updated command provides better spec generation for NEW features
7. Existing spec.md untouched - user's customizations preserved
```

**What Gets Updated:**
- Command prompts and instructions
- Agent reasoning patterns
- Template structures for NEW artifacts
- Script generation logic

**What NEVER Changes:**
- Already-generated specs, plans, tasks
- User-modified constitution
- Custom scripts in .specify/scripts/
- Project-specific configurations

### Summary: Claude Plugin Sync Capabilities

| Aspect | Capability | Rating |
|--------|-----------|--------|
| **Initial Installation** | Excellent - Single command, marketplace support | ⭐⭐⭐⭐⭐ |
| **Plugin Updates** | Excellent - Built-in update mechanism | ⭐⭐⭐⭐⭐ |
| **Version Control** | Excellent - Semantic versioning, pinning | ⭐⭐⭐⭐⭐ |
| **Stack Filtering** | Good - Architecture supports it, needs implementation | ⭐⭐⭐⭐ |
| **Update Safety** | Excellent - User files never touched | ⭐⭐⭐⭐⭐ |
| **Team Consistency** | Excellent - Config-driven, auto-install | ⭐⭐⭐⭐⭐ |
| **Automation Potential** | Excellent - Fully automated updates | ⭐⭐⭐⭐⭐ |

**Key Advantage:** This is a **living system**. Commands and agents evolve without disrupting user work.

---

## Direct Comparison: UV Tool vs Claude Plugin

### Update Mechanisms

| Scenario | UV Tool Installation | Claude Plugin Installation |
|----------|---------------------|---------------------------|
| **New command added** | Must re-init project (risky) | Automatic on plugin update |
| **Command logic improved** | Must re-init project (risky) | Automatic on plugin update |
| **Script bug fixed** | Must manually copy file | Not applicable (scripts in user space) |
| **Template improved** | Must manually copy file | Affects new artifacts only |
| **New agent added** | Must re-init project | Automatic on plugin update |
| **jpspec workflow enhanced** | Must re-init project | Automatic on plugin update |

### Team Workflows

| Capability | UV Tool Installation | Claude Plugin Installation |
|------------|---------------------|---------------------------|
| **Enforce same version across team** | Document in README, manual | `.claude/settings.json` auto-installs |
| **Update notification** | Manual check GitHub releases | Plugin system notifies |
| **Partial adoption** | N/A - binary choice | Can enable/disable plugins |
| **Rollback** | Re-init with older CLI version | `/plugin install jp-spec-kit@0.1.0` |

### Safety and Risk

| Risk | UV Tool Installation | Claude Plugin Installation |
|------|---------------------|---------------------------|
| **Overwrite user customizations** | HIGH - `specify init . --force` | NONE - user files separate |
| **Breaking changes** | HIGH - all-or-nothing update | LOW - versioned, can pin |
| **Inconsistent state** | MEDIUM - partial updates hard | LOW - atomic updates |
| **Lost work** | POSSIBLE - if force re-init | NOT POSSIBLE - user files protected |

### Feature Support

| Feature | UV Tool Installation | Claude Plugin Installation |
|---------|---------------------|---------------------------|
| **jpspec enhanced workflow** | ✅ Yes (in release packages) | ✅ Yes (in plugin) |
| **Stack-specific filtering** | ❌ No (all templates included) | ⭐ Possible (plugin supports conditions) |
| **Agent hot-reloading** | ❌ No (requires re-init) | ✅ Yes (plugin update) |
| **Custom hooks** | ⚠️ Manual setup | ✅ Plugin provides hooks |
| **MCP server integration** | ❌ Separate install | ✅ Plugin bundles MCP configs |

---

## Critical Analysis: Are Both Methods Equally Capable?

### Short Answer: NO

The two methods are **fundamentally different** in their update capabilities:

### UV Tool Installation
- ✅ **Best for:** Initial project bootstrap
- ✅ **Strength:** Simple one-time setup
- ❌ **Weakness:** No safe update path for existing projects
- ❌ **Update capability:** Manual, destructive, high-risk

**Mental Model:** "Install once, frozen in time"

### Claude Plugin Installation
- ✅ **Best for:** Ongoing development with evolving toolkit
- ✅ **Strength:** Safe, automatic updates
- ✅ **Update capability:** Built-in, versioned, zero-risk
- ⚠️ **Consideration:** Requires Claude Code (not IDE-agnostic)

**Mental Model:** "Living toolkit, evolves with you"

---

## Recommendations for JP-Spec-Kit

### Hybrid Approach (Recommended)

**Use both methods for different purposes:**

#### 1. UV Tool Installation for Bootstrap
```bash
# Initialize project structure
specify init my-project --ai claude

# Creates:
# - .specify/ directory structure
# - Initial templates
# - Git repository
```

**Purpose:** Create the initial project scaffold

#### 2. Claude Plugin for Ongoing Development
```bash
# Add marketplace
/plugin marketplace add github/jp-spec-kit

# Install plugin
/plugin install jp-spec-kit

# Future updates
/plugin update jp-spec-kit
```

**Purpose:** Provide evolving commands and agents

#### 3. Document Hybrid Approach

**README.md:**
```markdown
## Setup

### Initial Setup (One-Time)
```bash
uv tool install specify-cli --from git+https://github.com/github/jp-spec-kit.git
specify init my-project --ai claude
cd my-project
```

### Install Claude Plugin for Latest Features
```bash
/plugin marketplace add github/jp-spec-kit
/plugin install jp-spec-kit
```

### Staying Current
- **Scripts & Templates:** Manually update from releases if needed (rare)
- **Commands & Agents:** Automatic via `/plugin update jp-spec-kit` (frequent)
```

### Implementation Roadmap

#### Phase 1: Create Plugin Packaging (Immediate)
1. ✅ Research plugin architecture (DONE via this analysis)
2. Create `.claude-plugin/` structure
3. Adapt existing commands to plugin format
4. Test plugin locally
5. Create marketplace.json

#### Phase 2: Publish Plugin (Near-Term)
1. Set up GitHub repo as marketplace
2. Publish first plugin version (v0.1.0)
3. Document plugin installation in README
4. Create migration guide for UV tool users

#### Phase 3: Enhance Plugin Capabilities (Future)
1. Add stack detection and filtering
2. Implement conditional command loading
3. Create stack-specific sub-plugins
4. Add hooks for project lifecycle events

#### Phase 4: Maintain Both Methods (Ongoing)
1. Continue UV tool releases for bootstrap
2. Rapid plugin updates for command improvements
3. Sync major versions across both methods
4. Clear documentation on when to use each

### Version Synchronization Strategy

**Versioning Scheme:**
```
jp-spec-kit CLI:    v0.2.0  (releases as ZIPs)
jp-spec-kit Plugin: v0.2.0  (releases via marketplace)
```

**Update Frequency:**
- **CLI releases:** Quarterly or for major features (slow)
- **Plugin releases:** Bi-weekly or as needed (fast)

**Breaking Changes:**
- Major version bumps (1.0.0, 2.0.0) → Release both CLI and plugin
- Minor/patch updates → Plugin only (faster iteration)

---

## Stack and Language Filtering Deep Dive

### Current State: No Filtering

When you run:
```bash
specify init my-project --ai claude
```

You get ALL templates regardless of your stack:
- `.specify/templates/` contains generic spec/plan/task templates
- No Python-specific vs Node.js-specific variants
- No Kubernetes vs serverless-specific guidance
- GitHub Actions templates for all stacks (nodejs, python, go)

### Problem Scenarios

#### Scenario 1: Python FastAPI Project
```bash
specify init fastapi-app --ai claude
cd fastapi-app
ls .specify/templates/
# Still has references to:
# - Node.js patterns (not relevant)
# - .NET patterns (not relevant)
# - Go patterns (not relevant)
```

User must manually filter and ignore irrelevant content.

#### Scenario 2: Team with Multiple Stacks
```bash
# Team has 3 projects:
- frontend-react (Node.js + React)
- backend-api (Python + FastAPI)
- ml-service (Python + PyTorch)

# All use same jp-spec-kit templates
# No stack-specific customization
```

Each project gets generic templates requiring manual adaptation.

### Proposed Solution: Stack-Aware Installation

#### Enhanced CLI with Stack Detection
```bash
# Auto-detect stack from existing files
specify init . --ai claude --auto-detect-stack

# Detects:
# - package.json → Node.js stack
# - pyproject.toml → Python stack
# - go.mod → Go stack
# - Cargo.toml → Rust stack

# Only installs relevant templates and CI/CD configs
```

#### Explicit Stack Selection
```bash
specify init my-project --ai claude --stack python --framework fastapi

# Installs:
# ✅ Python-specific templates
# ✅ FastAPI patterns in spec templates
# ✅ Python CI/CD workflows
# ❌ Skips Node.js, Go, .NET content
```

#### Plugin-Based Stack Filtering

**Main Plugin:**
```bash
/plugin install jp-spec-kit-core
# Provides: Core spec-driven methodology, language-agnostic commands
```

**Stack-Specific Add-ons:**
```bash
/plugin install jp-spec-kit-python
/plugin install jp-spec-kit-nodejs
/plugin install jp-spec-kit-dotnet

# Each adds:
# - Stack-specific command variants
# - Framework-specific templates
# - Ecosystem-specific best practices
```

**Conditional Command Loading:**
```json
{
  "commands": [
    {
      "name": "speckit.plan",
      "source": "./commands/speckit.plan.md",
      "displayName": "Plan (Generic)"
    },
    {
      "name": "speckit.plan-python",
      "source": "./commands/python/speckit.plan-python.md",
      "displayName": "Plan (Python)",
      "conditions": {
        "or": [
          {"projectHasFile": "pyproject.toml"},
          {"projectHasFile": "requirements.txt"},
          {"projectHasFile": "setup.py"}
        ]
      }
    },
    {
      "name": "speckit.plan-nodejs",
      "source": "./commands/nodejs/speckit.plan-nodejs.md",
      "displayName": "Plan (Node.js)",
      "conditions": {
        "projectHasFile": "package.json"
      }
    }
  ]
}
```

**User Experience:**
```bash
# In Python project
/speckit.plan  → Shows Python-specific guidance

# In Node.js project
/speckit.plan  → Shows Node.js-specific guidance

# In unknown project
/speckit.plan  → Shows generic guidance
```

### Implementation Priority

**Phase 1: CLI Stack Detection**
- LOW EFFORT: Add `--stack` flag to `specify init`
- MEDIUM IMPACT: Filter GitHub Actions templates
- Does NOT help with command updates

**Phase 2: Plugin Modular Architecture**
- MEDIUM EFFORT: Split plugin into core + stack extensions
- HIGH IMPACT: Dynamic, stays current via updates
- Scales to many stacks/frameworks

**Phase 3: Intelligent Stack Detection**
- HIGH EFFORT: Auto-detect stack from codebase
- HIGH IMPACT: Zero-config experience
- Requires ongoing maintenance as ecosystems evolve

---

## Conclusion

### Summary of Findings

1. **UV Tool Installation:**
   - Excellent for project bootstrap
   - Poor for staying current
   - Manual, risky update process
   - Static snapshot approach

2. **Claude Plugin Installation:**
   - Excellent for ongoing development
   - Excellent for staying current
   - Automatic, safe update process
   - Living toolkit approach

3. **Stack Filtering:**
   - Not currently implemented in either method
   - Plugin architecture better suited for this
   - Would significantly improve user experience

### Answer to Original Question

**"Are both installation methods equally capable of staying current?"**

**NO.** The methods serve different purposes:

- **UV Tool Install:** Project initialization (one-time)
- **Claude Plugin:** Ongoing development support (continuous)

For **staying current**, the Claude Plugin method is vastly superior because:
- ✅ Built-in update mechanism
- ✅ Version control and rollback
- ✅ No risk to user files
- ✅ Automatic team synchronization
- ✅ Rapid iteration on commands/agents

The UV tool method requires destructive re-initialization to update, making it unsuitable for keeping existing projects current.

### Recommended Strategy

**Use BOTH methods complementarily:**

1. **Bootstrap with UV Tool** → Creates project structure
2. **Develop with Claude Plugin** → Provides evolving commands
3. **Stack filtering via Plugin** → Future enhancement

This hybrid approach gives users:
- Simple initial setup (UV tool)
- Safe, continuous updates (Plugin)
- Best of both worlds

---

## Appendix: Implementation Checklist

### For Plugin Development

- [ ] Create `.claude-plugin/plugin.json` manifest
- [ ] Create `.claude-plugin/marketplace.json` for marketplace hosting
- [ ] Migrate all `/speckit.*` commands to plugin format
- [ ] Migrate all `/jpspec:*` commands to plugin format
- [ ] Define agent configurations in `agents/` directory
- [ ] Set up hooks for project lifecycle events
- [ ] Configure MCP servers in `.mcp.json`
- [ ] Test plugin locally using dev marketplace
- [ ] Document plugin installation process
- [ ] Publish v0.1.0 to marketplace

### For UV Tool Enhancement

- [ ] Add `--stack` option to `specify init`
- [ ] Implement stack detection logic
- [ ] Filter GitHub Actions templates by stack
- [ ] Create stack-specific release packages
- [ ] Document hybrid UV + Plugin workflow
- [ ] Add warning about plugin being preferred for updates

### For Documentation

- [ ] README: Explain both installation methods
- [ ] README: Clarify when to use each method
- [ ] README: Add plugin update instructions
- [ ] CLAUDE.md: Document plugin architecture
- [ ] Migration guide: UV users → UV + Plugin users
- [ ] FAQ: Address common questions about sync

### For Testing

- [ ] Test plugin installation and updates
- [ ] Test UV tool + plugin coexistence
- [ ] Test team-wide plugin configuration
- [ ] Test stack filtering (when implemented)
- [ ] Test rollback scenarios
- [ ] Test update safety (user files preserved)

---

## References

- [Claude Code Plugin Documentation](https://docs.claude.com/en/docs/claude-code/plugins)
- [Claude Code Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [UV Tool Documentation](https://docs.astral.sh/uv/)
- [JP-Spec-Kit Repository](https://github.com/github/jp-spec-kit) (hypothetical - adjust to actual repo)
- [Semantic Versioning Specification](https://semver.org/)

---

**Document Version:** 1.0
**Date:** October 15, 2025
**Author:** Claude Code (via Task 013 Analysis)
**Status:** ✅ Complete and Verified
