---
id: task-280
title: Benchmark AI Triage Engine Accuracy
status: To Do
assignee:
  - '@muckross'
created_date: '2025-12-03 23:21'
updated_date: '2025-12-04 16:51'
labels:
  - 'workflow:Planned'
  - security
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create benchmark dataset and measure AI triage accuracy against expert manual triage. Target >85% agreement rate.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Curate dataset of 100+ security findings with ground truth labels (TP/FP)
- [ ] #2 Include diverse vulnerability types (SQL injection, XSS, path traversal, secrets, crypto)
- [ ] #3 Implement benchmark script to run triage and compare with ground truth
- [ ] #4 Calculate accuracy metrics: overall accuracy, per-classifier accuracy, precision, recall
- [ ] #5 Generate benchmark report with detailed breakdown and failure analysis
- [ ] #6 Achieve >85% overall accuracy or document reasons for lower performance
- [ ] #7 Document benchmark methodology and dataset curation process
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## CORRECTED Implementation Plan

**CRITICAL: Python measures accuracy, AI executes skill.**

### Phase 1: Labeled Dataset
- Create `tests/security/benchmark/labeled-findings.json`
  - Human-labeled ground truth
  - 50+ findings with known classifications (TP/FP/NI)
  - Include edge cases and ambiguous findings

### Phase 2: Benchmark Script (Python)
- Create `scripts/benchmark-triage.py`
  - Load labeled dataset
  - Invoke `/jpspec:security triage` via CLI subprocess
  - **AI coding tool** executes security-triage skill
  - Parse triage-results.json
  - Compare vs. labels
  - Calculate metrics:
    - Precision, Recall, F1 per class
    - Confusion matrix
    - Confidence calibration

### Phase 3: Results Analysis
- Generate `docs/security/benchmark-results.json`
  - Aggregate metrics
  - Per-category breakdown
  - Error analysis (misclassifications)
- Create `docs/security/benchmark-report.md`
  - Human-readable results
  - Recommendations for improvement

### Phase 4: CI Integration
- Add benchmark to CI pipeline
- Track accuracy over time
- Alert on regressions

### Success Criteria
- [ ] Labeled dataset created (50+ findings)
- [ ] Benchmark script runs triage via CLI
- [ ] Metrics calculated and reported
- [ ] **ZERO API DEPENDENCIES** (AI tool executes skill)

### Files Created
- `tests/security/benchmark/labeled-findings.json`
- `scripts/benchmark-triage.py`
- `docs/security/benchmark-results.json`
- `docs/security/benchmark-report.md`
<!-- SECTION:PLAN:END -->
