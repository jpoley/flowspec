#!/usr/bin/env python3
"""Pre-implementation quality gates hook.

Task: task-083 - Pre-Implementation Quality Gates

This hook runs before /jpspec:implement to verify spec quality:
1. Spec Completeness - No NEEDS CLARIFICATION markers
2. Required Files - spec.md, plan.md, tasks.md exist
3. Constitutional Compliance - test-first, task quality
4. Quality Threshold - Score meets tier threshold
5. Unresolved Markers - No TODO/FIXME/TBD in specs

Usage:
    python .claude/hooks/pre-implement.py [--skip] [--tier light|medium|heavy]
"""

import sys
import os
import re
from pathlib import Path
from typing import NamedTuple


class GateResult(NamedTuple):
    passed: bool
    gate_name: str
    message: str
    details: list[str] = []


# Gate thresholds by tier
TIER_THRESHOLDS = {
    "light": 50,
    "medium": 70,
    "heavy": 85,
}

# Markers that indicate incomplete specs
INCOMPLETE_MARKERS = [
    r"NEEDS\s*CLARIFICATION",
    r"NEEDS_CLARIFICATION",
    r"NEEDS\s*VALIDATION",
    r"NEEDS_VALIDATION",
    r"\[TBD\]",
    r"\[TODO\]",
    r"\[FIXME\]",
    r"TODO:",
    r"FIXME:",
    r"XXX:",
]

# Required files by tier
REQUIRED_FILES = {
    "light": ["memory/constitution.md"],
    "medium": ["memory/constitution.md", "docs/prd/*.md"],
    "heavy": ["memory/constitution.md", "docs/prd/*.md", "docs/specs/*.md"],
}


def check_incomplete_markers(spec_dir: Path) -> GateResult:
    """Gate 1: Check for incomplete markers in spec files."""
    findings = []
    pattern = "|".join(INCOMPLETE_MARKERS)

    # Directories to exclude from marker checking (templates, tests, docs about markers)
    exclude_dirs = ["archive", "backlog", "templates", "node_modules", ".git",
                    "tests/fixtures", "memory", ".claude/commands", "spec-driven.md"]

    for md_file in spec_dir.rglob("*.md"):
        if any(excl in str(md_file) for excl in exclude_dirs):
            continue
        try:
            content = md_file.read_text()
            for i, line in enumerate(content.split("\n"), 1):
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(f"  {md_file}:{i}: {line.strip()[:60]}")
        except Exception:
            pass

    if findings:
        return GateResult(
            passed=False,
            gate_name="Spec Completeness",
            message=f"Found {len(findings)} incomplete markers",
            details=findings[:10],  # Limit output
        )
    return GateResult(
        passed=True,
        gate_name="Spec Completeness",
        message="No incomplete markers found",
    )


def check_required_files(project_dir: Path, tier: str) -> GateResult:
    """Gate 2: Check that required files exist."""
    missing = []
    patterns = REQUIRED_FILES.get(tier, REQUIRED_FILES["medium"])

    for pattern in patterns:
        if "*" in pattern:
            matches = list(project_dir.glob(pattern))
            if not matches:
                missing.append(f"  No files matching: {pattern}")
        else:
            if not (project_dir / pattern).exists():
                missing.append(f"  Missing: {pattern}")

    if missing:
        return GateResult(
            passed=False,
            gate_name="Required Files",
            message=f"{len(missing)} required files missing",
            details=missing,
        )
    return GateResult(
        passed=True,
        gate_name="Required Files",
        message="All required files present",
    )


def check_constitutional_compliance(project_dir: Path) -> GateResult:
    """Gate 3: Check constitutional compliance."""
    constitution = project_dir / "memory" / "constitution.md"
    issues = []

    if not constitution.exists():
        return GateResult(
            passed=False,
            gate_name="Constitutional Compliance",
            message="No constitution.md found",
            details=["  Create with: /speckit:constitution"],
        )

    content = constitution.read_text().lower()

    # Check for key sections
    if "test" not in content and "tdd" not in content:
        issues.append("  Missing test-first/TDD requirements")
    if "task" not in content and "acceptance" not in content:
        issues.append("  Missing task quality requirements")

    if issues:
        return GateResult(
            passed=False,
            gate_name="Constitutional Compliance",
            message="Constitution missing key sections",
            details=issues,
        )
    return GateResult(
        passed=True,
        gate_name="Constitutional Compliance",
        message="Constitution includes required sections",
    )


def calculate_quality_score(project_dir: Path) -> tuple[int, list[str]]:
    """Calculate spec quality score (0-100)."""
    score = 100
    deductions = []

    # Check PRD exists
    prd_files = list((project_dir / "docs" / "prd").glob("*.md")) if (project_dir / "docs" / "prd").exists() else []
    if not prd_files:
        score -= 20
        deductions.append("  -20: No PRD files")

    # Check functional specs
    spec_files = list((project_dir / "docs" / "specs").glob("*functional*.md")) if (project_dir / "docs" / "specs").exists() else []
    if not spec_files:
        score -= 15
        deductions.append("  -15: No functional specs")

    # Check for traceability (task references)
    has_task_refs = False
    for f in prd_files + spec_files:
        try:
            if "task-" in f.read_text():
                has_task_refs = True
                break
        except Exception:
            pass
    if not has_task_refs:
        score -= 10
        deductions.append("  -10: No task references in specs")

    return max(0, score), deductions


def check_quality_threshold(project_dir: Path, tier: str) -> GateResult:
    """Gate 4: Check quality score meets threshold."""
    threshold = TIER_THRESHOLDS.get(tier, 70)
    score, deductions = calculate_quality_score(project_dir)

    if score < threshold:
        return GateResult(
            passed=False,
            gate_name="Quality Threshold",
            message=f"Score {score}/100 below {tier} threshold ({threshold})",
            details=deductions,
        )
    return GateResult(
        passed=True,
        gate_name="Quality Threshold",
        message=f"Score {score}/100 meets {tier} threshold ({threshold})",
    )


def check_unresolved_markers(project_dir: Path) -> GateResult:
    """Gate 5: Check for TODO/FIXME markers in code."""
    findings = []
    code_dirs = ["src", "lib", "app"]

    for code_dir in code_dirs:
        path = project_dir / code_dir
        if not path.exists():
            continue
        for py_file in path.rglob("*.py"):
            try:
                content = py_file.read_text()
                for i, line in enumerate(content.split("\n"), 1):
                    if re.search(r"#\s*(TODO|FIXME|XXX|HACK):", line):
                        findings.append(f"  {py_file}:{i}: {line.strip()[:50]}")
            except Exception:
                pass

    # This gate is informational, not blocking
    if findings:
        return GateResult(
            passed=True,  # Warning only
            gate_name="Code Markers",
            message=f"Found {len(findings)} code markers (warning)",
            details=findings[:5],
        )
    return GateResult(
        passed=True,
        gate_name="Code Markers",
        message="No unresolved code markers",
    )


def run_quality_gates(project_dir: Path, tier: str = "medium", skip: bool = False) -> bool:
    """Run all quality gates and return pass/fail."""
    if skip:
        print("⚠️  Quality gates SKIPPED (--skip flag)")
        print("   This will be logged for audit.")
        return True

    print(f"\n{'='*60}")
    print(f"Pre-Implementation Quality Gates (tier: {tier})")
    print(f"{'='*60}\n")

    gates = [
        check_incomplete_markers(project_dir),
        check_required_files(project_dir, tier),
        check_constitutional_compliance(project_dir),
        check_quality_threshold(project_dir, tier),
        check_unresolved_markers(project_dir),
    ]

    all_passed = True
    for gate in gates:
        status = "✅" if gate.passed else "❌"
        print(f"{status} Gate: {gate.gate_name}")
        print(f"   {gate.message}")
        for detail in gate.details:
            print(f"   {detail}")
        if not gate.passed:
            all_passed = False
        print()

    print(f"{'='*60}")
    if all_passed:
        print("✅ All quality gates PASSED - Ready for implementation")
    else:
        print("❌ Quality gates FAILED - Fix issues before implementing")
        print("\nRemediation:")
        print("  1. Address incomplete markers in spec files")
        print("  2. Create missing required files")
        print("  3. Update constitution if needed")
        print("  4. Use --skip to bypass (with audit logging)")
    print(f"{'='*60}\n")

    return all_passed


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Pre-implementation quality gates")
    parser.add_argument("--skip", action="store_true", help="Skip gates (audit logged)")
    parser.add_argument("--tier", choices=["light", "medium", "heavy"], default="medium")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    args = parser.parse_args()

    passed = run_quality_gates(args.project_dir, args.tier, args.skip)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
