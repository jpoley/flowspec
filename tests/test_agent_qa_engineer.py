"""Tests for the qa-engineer agent."""

import re
from pathlib import Path

import pytest


@pytest.fixture
def agent_file_path() -> Path:
    """Return path to qa-engineer agent file."""
    return Path(".claude/agents/qa-engineer.md")


@pytest.fixture
def template_file_path() -> Path:
    """Return path to qa-engineer template file."""
    return Path("templates/agents/qa-engineer.md")


@pytest.fixture
def agent_content(agent_file_path: Path) -> str:
    """Return content of the qa-engineer agent file."""
    return agent_file_path.read_text()


@pytest.fixture
def frontmatter(agent_content: str) -> dict:
    """Extract and parse YAML frontmatter from agent content."""
    match = re.match(r"^---\n(.*?)\n---\n", agent_content, re.DOTALL)
    if not match:
        pytest.fail("No YAML frontmatter found in agent file")

    # Parse frontmatter manually since description contains colons
    frontmatter_text = match.group(1)
    result = {}

    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()

    return result


class TestQAEngineerAgentFile:
    """Test the qa-engineer agent file exists and is valid."""

    def test_agent_file_exists(self, agent_file_path: Path):
        """Agent file should exist in .claude/agents/."""
        assert agent_file_path.exists(), f"Agent file not found at {agent_file_path}"

    def test_template_file_exists(self, template_file_path: Path):
        """Template file should exist in templates/agents/."""
        assert template_file_path.exists(), (
            f"Template file not found at {template_file_path}"
        )

    def test_files_are_identical(self, agent_file_path: Path, template_file_path: Path):
        """Agent file and template file should be identical."""
        agent_content = agent_file_path.read_text()
        template_content = template_file_path.read_text()
        assert agent_content == template_content, (
            "Agent file and template file should be identical"
        )


class TestQAEngineerFrontmatter:
    """Test the YAML frontmatter of the qa-engineer agent."""

    def test_has_frontmatter(self, agent_content: str):
        """Agent file should have YAML frontmatter."""
        assert agent_content.startswith("---\n"), (
            "Agent file should start with YAML frontmatter delimiter"
        )
        assert "\n---\n" in agent_content, (
            "Agent file should have closing YAML frontmatter delimiter"
        )

    def test_frontmatter_is_valid(self, frontmatter: dict):
        """Frontmatter should be parseable as key-value pairs."""
        assert isinstance(frontmatter, dict), "Frontmatter should be a dictionary"
        assert len(frontmatter) > 0, "Frontmatter should have at least one field"

    def test_has_name_field(self, frontmatter: dict):
        """Frontmatter should have a name field."""
        assert "name" in frontmatter, "Frontmatter should have a 'name' field"
        assert frontmatter["name"] == "qa-engineer"

    def test_has_description_field(self, frontmatter: dict):
        """Frontmatter should have a description field."""
        assert "description" in frontmatter, (
            "Frontmatter should have a 'description' field"
        )
        assert isinstance(frontmatter["description"], str), (
            "Description should be a string"
        )
        assert len(frontmatter["description"]) > 50, "Description should be substantial"

    def test_has_tools_field(self, frontmatter: dict):
        """Frontmatter should have a tools field."""
        assert "tools" in frontmatter, "Frontmatter should have a 'tools' field"

    def test_has_color_field(self, frontmatter: dict):
        """Frontmatter should have a color field."""
        assert "color" in frontmatter, "Frontmatter should have a 'color' field"
        assert frontmatter["color"] == "yellow"


class TestQAEngineerTools:
    """Test the tools configuration for the qa-engineer agent."""

    def test_tools_list(self, frontmatter: dict):
        """QA engineer should have appropriate tools."""
        tools = frontmatter.get("tools", "").split(", ")
        expected_tools = ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]

        assert len(tools) > 0, "Agent should have tools configured"

        for tool in expected_tools:
            assert tool in tools, f"QA engineer should have {tool} tool"

    def test_has_file_manipulation_tools(self, frontmatter: dict):
        """QA engineer should have file manipulation tools."""
        tools = frontmatter.get("tools", "").split(", ")

        # QA engineers need to read code and write tests
        assert "Read" in tools, "QA engineer needs Read tool"
        assert "Write" in tools, "QA engineer needs Write tool"
        assert "Edit" in tools, "QA engineer needs Edit tool"

    def test_has_code_search_tools(self, frontmatter: dict):
        """QA engineer should have code search tools."""
        tools = frontmatter.get("tools", "").split(", ")

        # QA engineers need to search codebases for test coverage gaps
        assert "Glob" in tools, "QA engineer needs Glob tool"
        assert "Grep" in tools, "QA engineer needs Grep tool"

    def test_has_bash_tool(self, frontmatter: dict):
        """QA engineer should have Bash tool for running tests."""
        tools = frontmatter.get("tools", "").split(", ")

        # QA engineers need to run test suites
        assert "Bash" in tools, "QA engineer needs Bash tool"


class TestQAEngineerDescription:
    """Test the description field matches the agent's purpose."""

    def test_description_mentions_testing(self, frontmatter: dict):
        """Description should mention testing."""
        description = frontmatter["description"].lower()
        assert "test" in description, "Description should mention testing"

    def test_description_mentions_qa(self, frontmatter: dict):
        """Description should mention QA or quality assurance."""
        description = frontmatter["description"].lower()
        assert "qa" in description or "quality" in description, (
            "Description should mention QA or quality"
        )

    def test_description_mentions_coverage(self, frontmatter: dict):
        """Description should mention test coverage."""
        description = frontmatter["description"].lower()
        assert "coverage" in description, "Description should mention test coverage"


class TestQAEngineerContent:
    """Test the content of the qa-engineer agent."""

    def test_has_core_testing_stack_section(self, agent_content: str):
        """Agent should document core testing stack."""
        assert (
            "## Core Testing Stack" in agent_content
            or "## Testing Stack" in agent_content
        ), "Agent should have Testing Stack section"

    def test_mentions_pytest(self, agent_content: str):
        """Agent should mention pytest."""
        assert "pytest" in agent_content, "Agent should mention pytest"

    def test_mentions_testing_pyramid(self, agent_content: str):
        """Agent should mention testing pyramid or testing strategy."""
        content_lower = agent_content.lower()
        assert "testing pyramid" in content_lower or "pyramid" in agent_content, (
            "Agent should mention testing pyramid"
        )

    def test_has_test_implementation_section(self, agent_content: str):
        """Agent should have test implementation section."""
        assert (
            "## Test Implementation" in agent_content
            or "Testing Approach" in agent_content
        ), "Agent should have test implementation guidance"

    def test_mentions_unit_tests(self, agent_content: str):
        """Agent should mention unit tests."""
        content_lower = agent_content.lower()
        assert "unit test" in content_lower, "Agent should mention unit tests"

    def test_mentions_integration_tests(self, agent_content: str):
        """Agent should mention integration tests."""
        content_lower = agent_content.lower()
        assert "integration test" in content_lower, (
            "Agent should mention integration tests"
        )

    def test_mentions_e2e_tests(self, agent_content: str):
        """Agent should mention E2E tests."""
        content_lower = agent_content.lower()
        assert "e2e" in content_lower or "end-to-end" in content_lower, (
            "Agent should mention E2E tests"
        )

    def test_mentions_coverage_guidelines(self, agent_content: str):
        """Agent should mention coverage guidelines or targets."""
        content_lower = agent_content.lower()
        assert "coverage" in content_lower, (
            "Agent should mention test coverage guidelines"
        )

    def test_has_quality_checklist(self, agent_content: str):
        """Agent should have a quality checklist."""
        assert "## Quality Checklist" in agent_content or "Quality" in agent_content, (
            "Agent should have quality checklist"
        )

    def test_has_checkbox_items(self, agent_content: str):
        """Agent should have checkbox items for verification."""
        assert "- [ ]" in agent_content, "Agent should have checkbox items"

    def test_mentions_fixtures(self, agent_content: str):
        """Agent should mention test fixtures."""
        content_lower = agent_content.lower()
        assert "fixture" in content_lower, "Agent should mention test fixtures"

    def test_mentions_mocking(self, agent_content: str):
        """Agent should mention mocking."""
        content_lower = agent_content.lower()
        assert "mock" in content_lower, "Agent should mention mocking"
