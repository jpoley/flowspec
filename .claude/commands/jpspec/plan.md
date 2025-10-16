---
description: Execute planning workflow using project architect and platform engineer agents (builds out /speckit.constitution).
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Instructions

This command creates comprehensive architectural and platform planning using two specialized agents working in parallel, building out /speckit.constitution.

### Parallel Phase: Architecture & Platform Planning

**IMPORTANT**: Launch both agents in parallel using a single message with two Task tool calls for maximum efficiency.

#### Task 1: System Architecture

Use the Task tool to launch the **software-architect-enhanced** agent with the following prompt:

```
Design comprehensive system architecture for: [USER INPUT PROJECT]

Context:
[Include PRD, requirements, constraints from previous phases]

Apply Gregor Hohpe's architectural principles and create:

1. **Strategic Framing (Penthouse View)**
   - Business objectives and strategic value
   - Organizational impact
   - Investment justification using Selling Options framework

2. **Architectural Blueprint (Engine Room View)**
   - System architecture overview and diagrams
   - Component design and boundaries
   - Integration patterns (using Enterprise Integration Patterns taxonomy)
   - Data flow and communication protocols
   - Technology stack decisions with rationale

3. **Architecture Decision Records (ADRs)**
   - Key architectural decisions
   - Context and problem statements
   - Considered options with trade-offs
   - Decision rationale
   - Consequences and implications

4. **Platform Quality (7 C's Assessment)**
   - Clarity, Consistency, Compliance
   - Composability, Coverage
   - Consumption (Developer Experience)
   - Credibility (Reliability)

5. **For /speckit.constitution - Architectural Principles**
   - Core architectural constraints
   - Design patterns and anti-patterns
   - Integration standards
   - Quality attributes and trade-offs
   - Evolution strategy

Deliver comprehensive architecture documentation ready for implementation.
```

#### Task 2: Platform & Infrastructure Planning

Use the Task tool to launch the **platform-engineer-enhanced** agent with the following prompt:

```
Design platform and infrastructure architecture for: [USER INPUT PROJECT]

Context:
[Include PRD, requirements, constraints from previous phases]

Apply DevOps/Platform Engineering best practices and create:

1. **DORA Elite Performance Design**
   - Deployment frequency strategy
   - Lead time optimization approach
   - Change failure rate minimization
   - Mean time to restore planning

2. **CI/CD Pipeline Architecture**
   - Build and test pipeline design
   - Deployment automation strategy
   - GitOps workflow
   - Build acceleration (caching, predictive testing)

3. **Infrastructure Architecture**
   - Cloud platform selection and justification
   - Kubernetes architecture (if applicable)
   - Service mesh considerations
   - Scalability and high availability design
   - Disaster recovery planning

4. **DevSecOps Integration**
   - Security scanning gates (SAST, DAST, SCA)
   - SBOM generation
   - Secure software supply chain (SLSA compliance)
   - Secret management approach
   - Compliance automation

5. **Observability Architecture**
   - Metrics collection (Prometheus/OpenTelemetry)
   - Logging aggregation (structured logs)
   - Distributed tracing
   - Alerting strategy
   - Dashboard design

6. **For /speckit.constitution - Platform Principles**
   - Platform engineering standards
   - Infrastructure as Code requirements
   - CI/CD best practices
   - Security and compliance mandates
   - Operational procedures

Deliver comprehensive platform documentation ready for implementation.
```

### Integration Phase

After both agents complete:

1. **Consolidate Findings**
   - Merge architecture and platform designs
   - Resolve any conflicts or gaps
   - Ensure alignment between layers

2. **Build /speckit.constitution**
   - Architectural principles and constraints
   - Platform engineering standards
   - Infrastructure requirements
   - CI/CD and deployment guidelines
   - Security and compliance requirements
   - Operational standards
   - Quality gates and acceptance criteria

3. **Deliverables**
   - Complete system architecture document
   - Platform and infrastructure design
   - Updated /speckit.constitution
   - ADRs for key decisions
   - Implementation readiness assessment
