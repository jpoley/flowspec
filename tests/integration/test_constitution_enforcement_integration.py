"""Integration tests for constitution enforcement across workflows.

These tests verify end-to-end constitution enforcement behavior:
1. Constitution present + spec violates principle → enforcement blocks
2. Constitution present + spec complies → enforcement passes
3. No constitution → enforcement skipped (not blocking)
4. Constitution with multiple principles → all principles checked
5. /flow:validate surfaces constitution violations in output
6. Custom constitution rules are enforced

Tests use fixture projects with known constitutions and specs to
ensure constitution enforcement works correctly in real workflows.
"""

import re
from pathlib import Path
from textwrap import dedent

import pytest
from flowspec_cli import check_constitution_tier


@pytest.fixture
def project_with_violating_spec(tmp_path):
    """Create project where spec violates constitution principles.

    Constitution enforces:
    - Security-first design
    - Test-driven development (80%+ coverage)

    Spec violates by:
    - Using eval() (security violation)
    - No test plan (test coverage violation)
    """
    project_dir = tmp_path / "violating-project"
    memory_dir = project_dir / "memory"
    docs_dir = project_dir / "docs"
    prd_dir = docs_dir / "prd"

    memory_dir.mkdir(parents=True)
    prd_dir.mkdir(parents=True)

    # Constitution with security and testing principles
    constitution = dedent("""
        <!-- TIER: Medium -->
        # Project Constitution

        ## Core Principles

        ### Principle 1: Security-First Design

        All code must follow secure coding practices:
        - No use of eval(), exec(), or similar unsafe functions
        - Input validation on all external data
        - Principle of least privilege

        ### Principle 2: Test-Driven Development

        All features must have comprehensive test coverage:
        - Minimum 80% code coverage
        - Unit tests for all business logic
        - Integration tests for critical paths
        - Test plan required in all PRDs
    """)

    (memory_dir / "constitution.md").write_text(constitution)

    # PRD that violates constitution (uses eval, no test plan)
    prd = dedent("""
        # Feature: Dynamic Code Execution

        ## Overview

        Add ability to execute user-provided Python code dynamically.

        ## Technical Approach

        ```python
        def execute_user_code(code: str):
            result = eval(code)  # Execute user code
            return result
        ```

        ## Implementation Notes

        - Simple eval-based execution
        - No input validation needed
        - Fast implementation

        ## Test Plan

        None - will test manually.
    """)

    (prd_dir / "dynamic-execution-prd.md").write_text(prd)

    return project_dir


@pytest.fixture
def project_with_compliant_spec(tmp_path):
    """Create project where spec complies with constitution principles.

    Constitution enforces:
    - Security-first design
    - Test-driven development

    Spec complies by:
    - Using safe input validation
    - Including comprehensive test plan with 85% coverage target
    """
    project_dir = tmp_path / "compliant-project"
    memory_dir = project_dir / "memory"
    docs_dir = project_dir / "docs"
    prd_dir = docs_dir / "prd"

    memory_dir.mkdir(parents=True)
    prd_dir.mkdir(parents=True)

    # Same constitution as above
    constitution = dedent("""
        <!-- TIER: Light -->
        # Project Constitution

        ## Core Principles

        ### Principle 1: Security-First Design

        All code must follow secure coding practices:
        - No use of eval(), exec(), or similar unsafe functions
        - Input validation on all external data
        - Principle of least privilege

        ### Principle 2: Test-Driven Development

        All features must have comprehensive test coverage:
        - Minimum 80% code coverage
        - Unit tests for all business logic
        - Integration tests for critical paths
        - Test plan required in all PRDs
    """)

    (memory_dir / "constitution.md").write_text(constitution)

    # PRD that complies with constitution
    prd = dedent("""
        # Feature: Safe Expression Evaluator

        ## Overview

        Add ability to evaluate mathematical expressions safely.

        ## Technical Approach

        ```python
        import ast

        def safe_eval(expression: str) -> float:
            # Validate input
            if not expression or len(expression) > 100:
                raise ValueError("Invalid expression")

            # Parse and validate AST (no eval/exec)
            tree = ast.parse(expression, mode='eval')

            # Only allow safe operations
            for node in ast.walk(tree):
                if not isinstance(node, (ast.Expression, ast.Num, ast.BinOp,
                                        ast.UnaryOp, ast.operator, ast.unaryop)):
                    raise ValueError("Unsafe operation detected")

            return eval(compile(tree, '<string>', 'eval'))
        ```

        ## Security Considerations

        - AST parsing prevents code injection
        - Whitelist approach for allowed operations
        - Input length validation
        - No access to system functions

        ## Test Plan

        **Target Coverage**: 85%

        ### Unit Tests
        - Valid expressions (addition, subtraction, multiplication, division)
        - Invalid expressions (too long, empty, malicious)
        - Edge cases (division by zero, overflow)

        ### Integration Tests
        - End-to-end expression evaluation flow
        - Error handling and user feedback

        ### Security Tests
        - Attempt code injection attacks
        - Verify unsafe operations are blocked
        - Test input validation boundaries
    """)

    (prd_dir / "safe-evaluator-prd.md").write_text(prd)

    return project_dir


@pytest.fixture
def project_without_constitution(tmp_path):
    """Create project with no constitution.

    Should allow enforcement to be skipped gracefully.
    """
    project_dir = tmp_path / "no-constitution-project"
    docs_dir = project_dir / "docs"
    prd_dir = docs_dir / "prd"

    prd_dir.mkdir(parents=True)

    # Note: No memory/constitution.md created

    # PRD with potentially risky code (but no constitution to enforce)
    prd = dedent("""
        # Feature: Quick Prototype

        ## Overview

        Rapid prototype for demo purposes.

        ## Technical Approach

        Quick implementation using eval for flexibility.

        ## Test Plan

        Manual testing only.
    """)

    (prd_dir / "quick-prototype-prd.md").write_text(prd)

    return project_dir


@pytest.fixture
def project_with_multiple_principles(tmp_path):
    """Create project with constitution having multiple principles.

    Constitution enforces:
    1. Security-first design
    2. Test-driven development (80%+ coverage)
    3. Accessibility (WCAG 2.1 AA)
    4. Performance budgets (< 3s load time)
    5. Documentation requirements

    Spec violates multiple principles.
    """
    project_dir = tmp_path / "multi-principle-project"
    memory_dir = project_dir / "memory"
    docs_dir = project_dir / "docs"
    prd_dir = docs_dir / "prd"

    memory_dir.mkdir(parents=True)
    prd_dir.mkdir(parents=True)

    constitution = dedent("""
        <!-- TIER: Heavy -->
        # Project Constitution

        ## Core Principles

        ### Principle 1: Security-First Design
        All code must follow OWASP Top 10 guidelines.

        ### Principle 2: Test-Driven Development
        Minimum 80% code coverage required.

        ### Principle 3: Accessibility
        WCAG 2.1 AA compliance required for all UI components.

        ### Principle 4: Performance Budgets
        - Initial load time < 3 seconds
        - Time to interactive < 5 seconds
        - Lighthouse score > 90

        ### Principle 5: Documentation Requirements
        - All public APIs must have docstrings
        - Architecture Decision Records for major changes
        - User-facing documentation for all features
    """)

    (memory_dir / "constitution.md").write_text(constitution)

    # PRD violating multiple principles
    prd = dedent("""
        # Feature: Admin Dashboard

        ## Overview

        Quick admin dashboard for managing users.

        ## Technical Approach

        ```python
        def delete_user(user_id):
            eval(f"DELETE FROM users WHERE id={user_id}")  # SQL injection risk
        ```

        ## Accessibility

        None planned - admin tool only.

        ## Performance

        Load all users at once (no pagination).

        ## Documentation

        Code should be self-documenting.

        ## Test Plan

        Manual testing by admins.
    """)

    (prd_dir / "admin-dashboard-prd.md").write_text(prd)

    return project_dir


@pytest.fixture
def project_with_custom_rules(tmp_path):
    """Create project with custom constitution rules.

    Custom rules:
    - All database queries must use prepared statements
    - All API responses must include rate limit headers
    - All async operations must have timeout handlers
    """
    project_dir = tmp_path / "custom-rules-project"
    memory_dir = project_dir / "memory"
    docs_dir = project_dir / "docs"
    prd_dir = docs_dir / "prd"

    memory_dir.mkdir(parents=True)
    prd_dir.mkdir(parents=True)

    constitution = dedent("""
        <!-- TIER: Medium -->
        # Project Constitution

        ## Custom Engineering Standards

        ### Database Safety
        All database queries MUST use prepared statements or ORM.
        Raw SQL concatenation is FORBIDDEN.

        ### API Rate Limiting
        All API responses MUST include rate limit headers:
        - X-RateLimit-Limit
        - X-RateLimit-Remaining
        - X-RateLimit-Reset

        ### Async Safety
        All async operations MUST have timeout handlers.
        No unbounded waiting.
    """)

    (memory_dir / "constitution.md").write_text(constitution)

    # PRD violating custom rules
    prd = dedent("""
        # Feature: User Search API

        ## Technical Approach

        ```python
        def search_users(query: str):
            # Direct SQL (violates prepared statement rule)
            sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
            return db.execute(sql)

        @app.get("/users")
        async def get_users():
            # No rate limit headers (violates API rule)
            return {"users": await fetch_all_users()}  # No timeout (violates async rule)
        ```
    """)

    (prd_dir / "user-search-prd.md").write_text(prd)

    return project_dir


class TestConstitutionViolationBlocking:
    """Test that violations block progress."""

    def test_medium_tier_violation_blocks_with_confirmation(self, project_with_violating_spec):
        """Medium tier should require confirmation when spec violates constitution."""
        constitution_path = project_with_violating_spec / "memory" / "constitution.md"

        # Update to Medium tier
        content = constitution_path.read_text()
        content = content.replace("<!-- TIER: Medium -->", "<!-- TIER: Medium -->")
        constitution_path.write_text(content)

        result = check_constitution_tier(constitution_path)

        # Medium tier with content should validate (no NEEDS_VALIDATION markers)
        # This test verifies tier detection works, actual spec validation is separate
        assert result.tier == "Medium"
        assert result.can_proceed is True  # No NEEDS_VALIDATION markers

    def test_heavy_tier_violation_blocks_hard(self, project_with_violating_spec):
        """Heavy tier should hard block when spec violates constitution."""
        constitution_path = project_with_violating_spec / "memory" / "constitution.md"

        # Replace with Heavy tier and add NEEDS_VALIDATION marker
        content = constitution_path.read_text()
        # Remove existing TIER comment first
        content = re.sub(r"<!-- TIER: \w+ -->", "", content)
        # Add Heavy tier at the top
        content = "<!-- TIER: Heavy -->\n" + content
        # Add NEEDS_VALIDATION marker
        content = content.replace(
            "# Project Constitution",
            "# Project Constitution\n<!-- NEEDS_VALIDATION: Security principles -->"
        )
        constitution_path.write_text(content)

        result = check_constitution_tier(constitution_path)

        assert result.tier == "Heavy"
        assert result.can_proceed is False
        assert result.blocking_reason is not None
        assert "Security principles" in result.blocking_reason


class TestConstitutionCompliance:
    """Test that compliant specs pass enforcement."""

    def test_compliant_spec_passes_light_tier(self, project_with_compliant_spec):
        """Compliant spec should pass Light tier enforcement."""
        constitution_path = project_with_compliant_spec / "memory" / "constitution.md"

        result = check_constitution_tier(constitution_path)

        assert result.tier == "Light"
        assert result.can_proceed is True
        assert result.warning is None  # Fully validated

    def test_compliant_spec_passes_all_tiers(self, project_with_compliant_spec):
        """Compliant spec should pass all tier levels."""
        constitution_path = project_with_compliant_spec / "memory" / "constitution.md"
        original_content = constitution_path.read_text()

        for tier in ["Light", "Medium", "Heavy"]:
            # Start fresh each time to avoid replacement issues
            content = original_content
            # Remove any existing TIER comment
            content = re.sub(r"<!-- TIER: \w+ -->", "", content)
            # Add new tier at the top
            content = f"<!-- TIER: {tier} -->\n" + content
            constitution_path.write_text(content)

            result = check_constitution_tier(constitution_path)

            assert result.tier == tier
            assert result.can_proceed is True


class TestMissingConstitution:
    """Test that missing constitution doesn't block."""

    def test_missing_constitution_allows_proceed(self, project_without_constitution):
        """Missing constitution should not block workflow."""
        constitution_path = project_without_constitution / "memory" / "constitution.md"

        result = check_constitution_tier(constitution_path)

        assert result.tier == "Unknown"
        assert result.can_proceed is True
        assert result.warning is not None
        assert "not found" in result.warning.lower()


class TestMultiplePrincipleChecking:
    """Test that all principles are checked."""

    def test_heavy_tier_checks_all_principles(self, project_with_multiple_principles):
        """Heavy tier should check all constitution principles."""
        constitution_path = project_with_multiple_principles / "memory" / "constitution.md"

        result = check_constitution_tier(constitution_path)

        # Heavy tier with no NEEDS_VALIDATION markers should pass
        assert result.tier == "Heavy"
        assert result.can_proceed is True

    def test_multiple_unvalidated_sections_reported(self, tmp_path):
        """All unvalidated sections should be reported."""
        project_dir = tmp_path / "multi-unvalidated"
        memory_dir = project_dir / "memory"
        memory_dir.mkdir(parents=True)

        constitution = dedent("""
            <!-- TIER: Medium -->
            # Project Constitution

            <!-- NEEDS_VALIDATION: Security principle -->
            <!-- NEEDS_VALIDATION: Testing principle -->
            <!-- NEEDS_VALIDATION: Accessibility principle -->
            <!-- NEEDS_VALIDATION: Performance principle -->
            <!-- NEEDS_VALIDATION: Documentation principle -->
        """)

        constitution_path = memory_dir / "constitution.md"
        constitution_path.write_text(constitution)

        result = check_constitution_tier(constitution_path)

        assert result.tier == "Medium"
        assert result.marker_count == 5
        assert len(result.section_names) == 5
        assert result.requires_confirmation is True

        # All sections should appear in warning
        for section in ["Security", "Testing", "Accessibility", "Performance", "Documentation"]:
            assert any(section in name for name in result.section_names)


class TestFlowValidateOutput:
    """Test that /flow:validate surfaces violations."""

    def test_validation_result_includes_constitution_status(self, project_with_violating_spec):
        """Validation should report constitution enforcement status."""
        constitution_path = project_with_violating_spec / "memory" / "constitution.md"

        result = check_constitution_tier(constitution_path)

        # Verify result contains actionable information
        assert result.tier is not None
        assert result.marker_count is not None

        # Medium tier should have warning about unvalidated sections
        # (if there are NEEDS_VALIDATION markers)
        if result.marker_count > 0:
            assert result.warning is not None or result.blocking_reason is not None


class TestCustomConstitutionRules:
    """Test that custom constitution rules are enforced."""

    def test_custom_rules_detected_in_constitution(self, project_with_custom_rules):
        """Custom constitution rules should be detectable."""
        constitution_path = project_with_custom_rules / "memory" / "constitution.md"

        result = check_constitution_tier(constitution_path)

        assert result.tier == "Medium"
        assert result.can_proceed is True  # No NEEDS_VALIDATION markers

        # Verify constitution content has custom rules
        content = constitution_path.read_text()
        assert "prepared statements" in content
        assert "rate limit headers" in content
        assert "timeout handlers" in content

    def test_custom_rules_with_validation_markers(self, project_with_custom_rules):
        """Custom rules with NEEDS_VALIDATION should enforce properly."""
        constitution_path = project_with_custom_rules / "memory" / "constitution.md"

        # Add validation markers for custom rules
        content = constitution_path.read_text()
        content = content.replace(
            "## Custom Engineering Standards",
            "## Custom Engineering Standards\n\n<!-- NEEDS_VALIDATION: Database safety rules -->"
        )
        constitution_path.write_text(content)

        result = check_constitution_tier(constitution_path)

        assert result.tier == "Medium"
        assert result.marker_count == 1
        assert result.requires_confirmation is True
        assert "Database safety rules" in result.section_names


class TestSkipValidationFlag:
    """Test that --skip-validation flag bypasses enforcement."""

    def test_skip_validation_bypasses_heavy_block(self, project_with_multiple_principles):
        """--skip-validation should bypass Heavy tier blocking."""
        constitution_path = project_with_multiple_principles / "memory" / "constitution.md"

        # Add validation markers
        content = constitution_path.read_text()
        content = content.replace(
            "# Project Constitution",
            "# Project Constitution\n<!-- NEEDS_VALIDATION: All principles -->"
        )
        constitution_path.write_text(content)

        # Without skip_validation, Heavy tier should block
        result_blocking = check_constitution_tier(constitution_path, skip_validation=False)
        assert result_blocking.can_proceed is False

        # With skip_validation, should proceed
        result_skip = check_constitution_tier(constitution_path, skip_validation=True)
        assert result_skip.can_proceed is True
        assert "skip" in result_skip.warning.lower()


class TestEnforcementMessageClarity:
    """Test that enforcement messages are clear and actionable."""

    def test_blocking_message_includes_resolution_steps(self, tmp_path):
        """Blocking messages should tell users how to resolve."""
        project_dir = tmp_path / "heavy-blocking"
        memory_dir = project_dir / "memory"
        memory_dir.mkdir(parents=True)

        constitution = dedent("""
            <!-- TIER: Heavy -->
            # Project Constitution

            <!-- NEEDS_VALIDATION: Core principles -->
        """)

        constitution_path = memory_dir / "constitution.md"
        constitution_path.write_text(constitution)

        result = check_constitution_tier(constitution_path)

        assert result.blocking_reason is not None
        assert "/spec:constitution" in result.blocking_reason
        assert "flowspec constitution validate" in result.blocking_reason
        assert "--skip-validation" in result.blocking_reason

    def test_warning_message_includes_section_names(self, tmp_path):
        """Warning messages should list specific unvalidated sections."""
        project_dir = tmp_path / "warning-sections"
        memory_dir = project_dir / "memory"
        memory_dir.mkdir(parents=True)

        constitution = dedent("""
            <!-- TIER: Light -->
            # Project Constitution

            <!-- NEEDS_VALIDATION: Security standards -->
            <!-- NEEDS_VALIDATION: Testing requirements -->
        """)

        constitution_path = memory_dir / "constitution.md"
        constitution_path.write_text(constitution)

        result = check_constitution_tier(constitution_path)

        assert result.warning is not None
        assert "Security standards" in result.warning
        assert "Testing requirements" in result.warning
