---
description: Execute research and business validation workflow using specialized agents.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Instructions

This command orchestrates comprehensive research and business validation using two specialized agents working sequentially.

### Phase 1: Research

Use the Task tool to launch the **researcher** agent with the following prompt:

```
Conduct comprehensive research on: [USER INPUT TOPIC]

Provide detailed findings covering:
1. Market Analysis: Market size, growth trends, customer segments
2. Competitive Landscape: Key competitors, their strengths/weaknesses, market positioning
3. Technical Feasibility: Available technologies, implementation complexity, technical risks
4. Industry Trends: Emerging patterns, best practices, future outlook

Deliver a structured research report with:
- Executive Summary (key findings)
- Detailed Market Analysis
- Competitive Analysis
- Technical Feasibility Assessment
- Industry Trends and Future Outlook
- Sources and references
```

### Phase 2: Business Validation

After receiving the research findings, use the Task tool to launch the **business-validator** agent with the following prompt:

```
Based on the research findings provided, conduct a comprehensive business validation assessment for: [USER INPUT TOPIC]

Research Context:
[PASTE RESEARCH FINDINGS FROM PHASE 1]

Provide detailed validation covering:
1. Market Opportunity Assessment (TAM, SAM, SOM)
2. Financial Viability Analysis (revenue model, cost structure, unit economics)
3. Operational Feasibility (resource requirements, capability gaps)
4. Strategic Fit Analysis
5. Risk Analysis and Mitigation

Deliver a structured validation report with:
- Executive Assessment (Go/No-Go recommendation with confidence level)
- Detailed Opportunity Score (1-10 across key dimensions)
- Strengths and Opportunities
- Weaknesses and Threats
- Critical Assumptions
- Risk Register
- Financial Projections Review
- Recommendations and Next Steps
```

### Final Output

Consolidate both reports into a comprehensive research and validation package that enables informed decision-making.
