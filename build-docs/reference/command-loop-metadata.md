# Command Loop Metadata Reference

## Overview

Every `/flow:*` command in Flowspec includes **loop metadata** that classifies which development loop it belongs to. This metadata enables:

- **Intelligent routing** to appropriate agents and models
- **Context-aware safety rules** per loop type
- **Performance optimization** based on loop characteristics
- **Workflow orchestration** and state management

## Loop Classifications

### Inner Loop (`loop: inner`)

**Purpose**: Fast, local iteration cycles focused on developer velocity and rapid feedback.

**Characteristics**:
- Edit → run/tests → debug → repeat cycles
- Pre-commit validation and testing
- Local development environment
- Instant feedback (< 2s hot reload target)
- Focus on developer flow state

**Commands**:
- `/flow:implement` - Write production code with fast iteration
- `/flow:security fix` - Apply security patches during development

**Agent Routing**:
- Implementation agents: frontend-engineer, backend-engineer, ai-ml-engineer
- Code review agents: frontend-code-reviewer, backend-code-reviewer, python-code-reviewer
- Testing agents: quality-guardian, playwright-test-generator
- Language specialists: go-expert-developer, java-developer, js-ts-expert-developer

**Safety Rules**:
- Pre-commit hooks enforced
- Local CI simulation encouraged
- Fast unit tests required
- Real-time linting and formatting

### Outer Loop (`loop: outer`)

**Purpose**: Post-commit CI/CD pipeline focused on organizational safety, compliance, and production reliability.

**Characteristics**:
- PR → build → test → package → attest → deploy → observe cycles
- CI/CD automation and orchestration
- Production deployment and operations
- Comprehensive validation and compliance
- Governance and audit trails

**Commands**:
- `/flow:assess` - Evaluate SDD workflow suitability
- `/flow:specify` - Create product requirements (PRD)
- `/flow:research` - Conduct research and business validation
- `/flow:plan` - Design architecture and create ADRs
- `/flow:intake` - Process feature intake documents
- `/flow:operate` - Deploy and manage production infrastructure
- `/flow:security report` - Generate compliance and audit reports

**Agent Routing**:
- Planning agents: product-requirements-manager, software-architect, platform-engineer
- Research agents: researcher, business-validator
- Operations agents: sre-agent, release-manager
- Documentation agents: tech-writer, star-framework-writer

**Safety Rules**:
- Required status checks before merge
- Branch protection enforcement
- Artifact signing and provenance
- SLSA compliance validation
- Automated security scanning
- Complete audit trails

### Both Loops (`loop: both`)

**Purpose**: Commands that bridge or span both inner and outer loops.

**Characteristics**:
- Perform inner loop activities (testing, code review)
- Generate outer loop artifacts (compliance reports, release notes)
- Transition point between development and deployment
- Dual-context operation

**Commands**:
- `/flow:validate` - Quality assurance bridging development to deployment
- `/flow:security` - Security workflow integration (scan in inner, report in outer)
- `/flow:security triage` - Vulnerability analysis (local + CI/CD)
- `/flow:security web` - Web security testing (dev + pipeline)

**Agent Routing**:
- Quality agents: quality-guardian, playwright-test-healer, playwright-test-planner
- Security agents: secure-by-design-engineer
- Documentation agents: tech-writer
- Release agents: release-manager

**Safety Rules**:
- Combined inner + outer loop validations
- Local testing with CI/CD reporting
- Pre-commit hooks + pipeline checks
- Immediate feedback + compliance tracking

### Setup (`loop: setup`)

**Purpose**: One-time or infrequent configuration commands outside regular development cycles.

**Characteristics**:
- Project initialization and configuration
- Workflow customization
- Infrastructure setup
- One-time or periodic execution

**Commands**:
- `/flow:init` - Initialize project constitution
- `/flow:reset` - Reconfigure workflow settings

**Agent Routing**:
- Minimal agent routing (primarily template-based)
- Interactive prompts for configuration
- File generation and project setup

**Safety Rules**:
- Validation of configuration choices
- Backup existing files before modification
- Idempotent operations where possible

### Utility (`loop: utility`)

**Purpose**: Helper commands that support both loops without modifying code or workflow state.

**Characteristics**:
- Context generation and documentation
- Code analysis and mapping
- Non-destructive operations
- Stateless execution

**Commands**:
- `/flow:generate-prp` - Generate Product Requirements Prompts
- `/flow:map-codebase` - Generate directory tree listings

**Agent Routing**:
- Documentation agents: tech-writer
- Analysis agents (read-only mode)
- Context generation agents

**Safety Rules**:
- Read-only codebase access
- No workflow state modifications
- No code changes

## Loop Routing Implications

### Model Selection

Different loops may route to different model tiers based on task complexity:

**Inner Loop**:
- Fast models for rapid feedback (Sonnet, Haiku)
- Cost-optimized for high-frequency operations
- Real-time responsiveness prioritized

**Outer Loop**:
- Powerful models for complex planning (Opus, Sonnet)
- Accuracy and completeness prioritized
- Extended thinking for architecture decisions

**Both Loops**:
- Context-dependent model selection
- Fast models for validation, powerful for reporting
- Hybrid approach balancing speed and quality

### Agent Assignment

Loop metadata determines which agents are invoked:

```yaml
# Example from flowspec_workflow.yml
workflows:
  implement:
    command: "/flow:implement"
    loop: inner
    agents:
      - frontend-engineer
      - backend-engineer
      - frontend-code-reviewer
      - backend-code-reviewer
    input_states: ["Planned"]
    output_state: "In Implementation"

  operate:
    command: "/flow:operate"
    loop: outer
    agents:
      - sre-agent
      - release-manager
    input_states: ["Validated"]
    output_state: "Deployed"
```

### Safety Rules Application

Loop classification determines which safety mechanisms apply:

**Inner Loop Safety**:
```bash
# Pre-commit hooks
git commit -m "feat: new feature"
# → Triggers: linting, formatting, unit tests, type checking

# Local validation
pytest tests/unit/  # Fast feedback
ruff check .        # Immediate linting
mypy src/          # Type checking
```

**Outer Loop Safety**:
```yaml
# CI/CD pipeline (.github/workflows/ci.yml)
jobs:
  validate:
    steps:
      - SAST scanning (Semgrep, CodeQL)
      - SCA dependency scanning
      - Container vulnerability scanning (Trivy)
      - SBOM generation
      - Artifact signing
      - Provenance attestation
      - SLSA compliance check
```

**Both Loops Safety**:
```bash
# Local execution with CI reporting
/flow:validate task-123
# → Runs: tests, security scans, documentation checks
# → Generates: QA report, security report, release notes
# → Updates: task state, creates PR with full context
```

### Performance Characteristics

**Inner Loop**:
- Target: < 2s hot reload
- Parallel execution of fast checks
- Incremental builds and testing
- Cached dependencies
- Local mocks and emulators

**Outer Loop**:
- Target: Complete validation in reasonable time (< 10 min)
- Comprehensive test suites
- Full security scanning
- Artifact generation and signing
- Deployment orchestration

**Both Loops**:
- Tiered execution: fast checks first, comprehensive later
- Progressive validation
- Local fast path, CI comprehensive path

## Metadata Format

Loop metadata is specified in YAML frontmatter at the top of each command file:

```yaml
---
description: Command description here
loop: inner|outer|both|setup|utility
# Loop Classification: HUMAN_READABLE_NAME
# Explanation of why this command belongs to this loop
---
```

### Example: Inner Loop Command

```yaml
---
description: Execute implementation using specialized frontend and backend engineer agents with code review.
loop: inner
# Loop Classification: INNER LOOP
# This command is part of the inner loop (implementation/execution phase). It writes
# production code with fast iteration cycles (edit → run/tests → debug → repeat).
---
```

### Example: Outer Loop Command

```yaml
---
description: Execute operations workflow using SRE agent for CI/CD, Kubernetes, DevSecOps, observability, and operational excellence.
loop: outer
# Loop Classification: OUTER LOOP
# This command is part of the outer loop (post-commit CI/CD phase). It handles deployment,
# infrastructure, monitoring, and production operations after code has been validated.
---
```

### Example: Both Loops Command

```yaml
---
description: Execute validation and quality assurance using QA, security, documentation, and release management agents.
loop: both
# Loop Classification: BOTH LOOPS (BRIDGE)
# This command spans both inner and outer loops. It performs inner loop quality checks
# (testing, code review) while preparing artifacts for outer loop deployment (release
# management, documentation). It bridges the transition from development to deployment.
---
```

## Command Loop Summary

| Command | Loop | Primary Purpose | Key Agents |
|---------|------|-----------------|------------|
| `/flow:assess` | outer | Evaluate SDD workflow suitability | workflow-assessor |
| `/flow:specify` | outer | Create product requirements | product-requirements-manager |
| `/flow:research` | outer | Conduct research and validation | researcher, business-validator |
| `/flow:plan` | outer | Design architecture and ADRs | software-architect, platform-engineer |
| `/flow:implement` | inner | Write production code | frontend-engineer, backend-engineer |
| `/flow:validate` | both | Quality assurance and testing | quality-guardian, secure-by-design-engineer |
| `/flow:operate` | outer | Deploy and manage infrastructure | sre-agent, release-manager |
| `/flow:init` | setup | Initialize project constitution | (template-based) |
| `/flow:reset` | setup | Reconfigure workflow settings | (template-based) |
| `/flow:intake` | outer | Process feature intake documents | (task creation) |
| `/flow:generate-prp` | utility | Generate context bundles | (read-only analysis) |
| `/flow:map-codebase` | utility | Generate directory trees | (read-only analysis) |
| `/flow:security` | both | Security workflow integration | secure-by-design-engineer |
| `/flow:security fix` | inner | Apply security patches | (automated patching) |
| `/flow:security report` | outer | Generate compliance reports | security-reporter |
| `/flow:security triage` | both | Analyze vulnerabilities | (AI triage) |
| `/flow:security web` | both | Web security testing | (DAST testing) |

## Best Practices

### For Command Authors

1. **Always specify loop metadata** in command frontmatter
2. **Document the reasoning** in comments explaining loop classification
3. **Consider routing implications** when designing command behavior
4. **Test in appropriate context** (local for inner, CI for outer)
5. **Respect loop boundaries** (don't mix local dev tasks with CI/CD in same command)

### For Users

1. **Use inner loop commands** for rapid development iteration
2. **Use outer loop commands** for planning and deployment
3. **Understand both loop commands** bridge development to production
4. **Run setup commands** only when needed (project init, workflow changes)
5. **Leverage utility commands** for context and documentation

### For Platform Engineers

1. **Configure CI/CD** to respect loop classifications
2. **Optimize inner loop** for speed (< 2s hot reload target)
3. **Ensure outer loop** completeness (all safety checks)
4. **Monitor loop performance** (DORA metrics, cycle time)
5. **Implement progressive delivery** for both loops transitions

## Future Enhancements

Loop metadata enables future capabilities:

- **Dynamic model selection** based on loop and task complexity
- **Cost optimization** using faster models for inner loop
- **Workflow parallelization** of independent loop operations
- **Loop-specific metrics** and performance tracking
- **Automated loop transition** detection and orchestration
- **Context-aware rate limiting** per loop type
- **Loop-specific caching strategies** for performance

## References

- [Agent Loop Classification](./agent-loop-classification.md) - Detailed agent assignments per loop
- [Inner Loop Principles](./inner-loop.md) - Inner loop objectives and requirements
- [Outer Loop Principles](./outer-loop.md) - Outer loop objectives and requirements
- [Workflow Architecture](../guides/workflow-architecture.md) - Overall workflow design
- [Flowspec Workflow Reference](./flowspec-workflow-reference.md) - Complete workflow specification
