"""Tests for the qa-engineer agent.

This module validates the qa-engineer agent definition and template files,
ensuring they contain all required metadata, tools, and documentation sections
for effective test automation and quality assurance workflows.
"""

import re
from pathlib import Path
from typing import Dict

import pytest


# Constants for file paths and expected values
AGENT_FILE_NAME = "qa-engineer.md"
AGENT_DIR = ".claude/agents"
TEMPLATE_DIR = "templates/agents"
EXPECTED_AGENT_NAME = "qa-engineer"
EXPECTED_COLOR = "yellow"
EXPECTED_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
MIN_DESCRIPTION_LENGTH = 50


def _read_file_safely(file_path: Path) -> str:
    """Read file content with proper encoding and error handling.

    Args:
        file_path: Path to the file to read

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise IOError(f"Failed to read {file_path}: {e}") from e


def _parse_frontmatter(content: str) -> Dict[str, str]:
    """Extract and parse YAML frontmatter from markdown content.

    Args:
        content: Markdown file content with YAML frontmatter

    Returns:
        Dictionary of frontmatter key-value pairs

    Raises:
        ValueError: If frontmatter is missing or malformed
    """
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found in content")

    # Parse frontmatter manually since description contains colons
    frontmatter_text = match.group(1)
    result: Dict[str, str] = {}

    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()

    return result


@pytest.fixture
def agent_file_path() -> Path:
    """Return path to qa-engineer agent file.

    Returns:
        Path object pointing to the agent definition file
    """
    return Path(AGENT_DIR) / AGENT_FILE_NAME


@pytest.fixture
def template_file_path() -> Path:
    """Return path to qa-engineer template file.

    Returns:
        Path object pointing to the template file
    """
    return Path(TEMPLATE_DIR) / AGENT_FILE_NAME


@pytest.fixture
def agent_content(agent_file_path: Path) -> str:
    """Return content of the qa-engineer agent file.

    Args:
        agent_file_path: Path to agent file

    Returns:
        Agent file content as string
    """
    return _read_file_safely(agent_file_path)


@pytest.fixture
def template_content(template_file_path: Path) -> str:
    """Return content of the qa-engineer template file.

    Args:
        template_file_path: Path to template file

    Returns:
        Template file content as string
    """
    return _read_file_safely(template_file_path)


@pytest.fixture
def frontmatter(agent_content: str) -> Dict[str, str]:
    """Extract and parse YAML frontmatter from agent content.

    Args:
        agent_content: Agent file content

    Returns:
        Dictionary of frontmatter fields
    """
    try:
        return _parse_frontmatter(agent_content)
    except ValueError as e:
        pytest.fail(f"Failed to parse frontmatter: {e}")


class TestQAEngineerAgentFile:
    """Test the qa-engineer agent file exists and is valid.

    Validates that both the agent definition and template files exist,
    are readable, and contain identical content.
    """

    def test_agent_file_exists(self, agent_file_path: Path) -> None:
        """Agent file should exist in .claude/agents/.

        Args:
            agent_file_path: Path to agent file
        """
        assert agent_file_path.exists(), (
            f"Agent file not found at {agent_file_path}. "
            f"Expected location: {AGENT_DIR}/{AGENT_FILE_NAME}"
        )
        assert agent_file_path.is_file(), (
            f"Path exists but is not a file: {agent_file_path}"
        )

    def test_template_file_exists(self, template_file_path: Path) -> None:
        """Template file should exist in templates/agents/.

        Args:
            template_file_path: Path to template file
        """
        assert template_file_path.exists(), (
            f"Template file not found at {template_file_path}. "
            f"Expected location: {TEMPLATE_DIR}/{AGENT_FILE_NAME}"
        )
        assert template_file_path.is_file(), (
            f"Path exists but is not a file: {template_file_path}"
        )

    def test_files_are_identical(
        self, agent_content: str, template_content: str
    ) -> None:
        """Agent file and template file should be identical.

        Args:
            agent_content: Content of agent file
            template_content: Content of template file
        """
        assert agent_content == template_content, (
            "Agent file and template file content must be identical. "
            f"Agent has {len(agent_content)} chars, "
            f"template has {len(template_content)} chars. "
            "Run: diff .claude/agents/qa-engineer.md templates/agents/qa-engineer.md"
        )


class TestQAEngineerFrontmatter:
    """Test the YAML frontmatter of the qa-engineer agent.

    Validates frontmatter structure, required fields, and field values.
    """

    def test_has_frontmatter(self, agent_content: str) -> None:
        """Agent file should have YAML frontmatter.

        Args:
            agent_content: Content of agent file
        """
        assert agent_content.startswith("---\n"), (
            "Agent file must start with YAML frontmatter opening delimiter '---\\n'. "
            f"File starts with: {agent_content[:50]!r}"
        )
        assert "\n---\n" in agent_content, (
            "Agent file must have closing YAML frontmatter delimiter '\\n---\\n'. "
            "Check for proper frontmatter formatting."
        )

    def test_frontmatter_is_valid(self, frontmatter: Dict[str, str]) -> None:
        """Frontmatter should be parseable as key-value pairs.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        assert isinstance(frontmatter, dict), (
            f"Frontmatter must be a dictionary, got {type(frontmatter).__name__}"
        )
        assert len(frontmatter) > 0, (
            "Frontmatter must have at least one field. Empty frontmatter is not valid."
        )

    def test_has_name_field(self, frontmatter: Dict[str, str]) -> None:
        """Frontmatter should have a name field with correct value.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        assert "name" in frontmatter, (
            "Frontmatter must have a 'name' field. "
            f"Available fields: {list(frontmatter.keys())}"
        )
        assert frontmatter["name"] == EXPECTED_AGENT_NAME, (
            f"Agent name must be '{EXPECTED_AGENT_NAME}', "
            f"got '{frontmatter.get('name')}'"
        )

    def test_has_description_field(self, frontmatter: Dict[str, str]) -> None:
        """Frontmatter should have a description field.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        assert "description" in frontmatter, (
            "Frontmatter must have a 'description' field. "
            f"Available fields: {list(frontmatter.keys())}"
        )
        description = frontmatter["description"]
        assert isinstance(description, str), (
            f"Description must be a string, got {type(description).__name__}"
        )
        assert len(description) > MIN_DESCRIPTION_LENGTH, (
            f"Description must be substantial (>{MIN_DESCRIPTION_LENGTH} chars). "
            f"Current length: {len(description)} chars"
        )

    def test_has_tools_field(self, frontmatter: Dict[str, str]) -> None:
        """Frontmatter should have a tools field.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        assert "tools" in frontmatter, (
            "Frontmatter must have a 'tools' field. "
            f"Available fields: {list(frontmatter.keys())}"
        )

    def test_has_color_field(self, frontmatter: Dict[str, str]) -> None:
        """Frontmatter should have a color field with correct value.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        assert "color" in frontmatter, (
            "Frontmatter must have a 'color' field. "
            f"Available fields: {list(frontmatter.keys())}"
        )
        assert frontmatter["color"] == EXPECTED_COLOR, (
            f"Agent color must be '{EXPECTED_COLOR}', got '{frontmatter.get('color')}'"
        )


class TestQAEngineerTools:
    """Test the tools configuration for the qa-engineer agent.

    Validates that all required tools are present for QA engineering tasks.
    """

    def test_tools_list(self, frontmatter: Dict[str, str]) -> None:
        """QA engineer should have all required tools.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        tools_str = frontmatter.get("tools", "")
        assert tools_str, (
            "Tools field must not be empty. "
            "QA engineer requires tools to perform testing tasks."
        )

        tools = [t.strip() for t in tools_str.split(",")]
        assert len(tools) > 0, (
            f"Agent must have at least one tool configured. Tools string: {tools_str!r}"
        )

        for tool in EXPECTED_TOOLS:
            assert tool in tools, (
                f"QA engineer must have {tool} tool. "
                f"Current tools: {tools}. "
                f"Expected tools: {EXPECTED_TOOLS}"
            )

    def test_has_file_manipulation_tools(self, frontmatter: Dict[str, str]) -> None:
        """QA engineer should have file manipulation tools.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        tools = [t.strip() for t in frontmatter.get("tools", "").split(",")]

        # QA engineers need to read code and write tests
        file_tools = ["Read", "Write", "Edit"]
        for tool in file_tools:
            assert tool in tools, (
                f"QA engineer needs {tool} tool for file operations. "
                f"Current tools: {tools}"
            )

    def test_has_code_search_tools(self, frontmatter: Dict[str, str]) -> None:
        """QA engineer should have code search tools.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        tools = [t.strip() for t in frontmatter.get("tools", "").split(",")]

        # QA engineers need to search codebases for test coverage gaps
        search_tools = ["Glob", "Grep"]
        for tool in search_tools:
            assert tool in tools, (
                f"QA engineer needs {tool} tool for code search. Current tools: {tools}"
            )

    def test_has_bash_tool(self, frontmatter: Dict[str, str]) -> None:
        """QA engineer should have Bash tool for running tests.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        tools = [t.strip() for t in frontmatter.get("tools", "").split(",")]

        # QA engineers need to run test suites
        assert "Bash" in tools, (
            f"QA engineer needs Bash tool to run test commands. Current tools: {tools}"
        )


class TestQAEngineerDescription:
    """Test the description field matches the agent's purpose.

    Validates that the description accurately represents QA engineering work.
    """

    def test_description_mentions_testing(self, frontmatter: Dict[str, str]) -> None:
        """Description should mention testing.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        description = frontmatter["description"].lower()
        assert "test" in description, (
            "Description must mention 'test' as core QA responsibility. "
            f"Current description: {frontmatter['description'][:100]}..."
        )

    def test_description_mentions_qa(self, frontmatter: Dict[str, str]) -> None:
        """Description should mention QA or quality assurance.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        description = frontmatter["description"].lower()
        assert "qa" in description or "quality" in description, (
            "Description must mention 'qa' or 'quality' for QA engineering role. "
            f"Current description: {frontmatter['description'][:100]}..."
        )

    def test_description_mentions_coverage(self, frontmatter: Dict[str, str]) -> None:
        """Description should mention test coverage.

        Args:
            frontmatter: Parsed frontmatter dictionary
        """
        description = frontmatter["description"].lower()
        assert "coverage" in description, (
            "Description must mention 'coverage' as QA metric. "
            f"Current description: {frontmatter['description'][:100]}..."
        )


class TestQAEngineerContent:
    """Test the content of the qa-engineer agent.

    Validates that the agent documentation includes all necessary sections
    and testing concepts for comprehensive QA work.
    """

    def test_has_core_testing_stack_section(self, agent_content: str) -> None:
        """Agent should document core testing stack.

        Args:
            agent_content: Content of agent file
        """
        assert (
            "## Core Testing Stack" in agent_content
            or "## Testing Stack" in agent_content
        ), (
            "Agent must have a Testing Stack section documenting tools. "
            "This helps QA engineers understand available testing frameworks."
        )

    def test_mentions_pytest(self, agent_content: str) -> None:
        """Agent should mention pytest.

        Args:
            agent_content: Content of agent file
        """
        assert "pytest" in agent_content, (
            "Agent must mention pytest as the primary Python testing framework. "
            "Search the content for testing tool documentation."
        )

    def test_mentions_testing_pyramid(self, agent_content: str) -> None:
        """Agent should mention testing pyramid or testing strategy.

        Args:
            agent_content: Content of agent file
        """
        content_lower = agent_content.lower()
        assert "testing pyramid" in content_lower or "pyramid" in agent_content, (
            "Agent must mention testing pyramid for test distribution strategy. "
            "This guides proper balance of unit/integration/e2e tests."
        )

    def test_has_test_implementation_section(self, agent_content: str) -> None:
        """Agent should have test implementation section.

        Args:
            agent_content: Content of agent file
        """
        assert (
            "## Test Implementation" in agent_content
            or "Testing Approach" in agent_content
        ), (
            "Agent must have test implementation guidance section. "
            "This provides patterns and examples for writing tests."
        )

    def test_mentions_unit_tests(self, agent_content: str) -> None:
        """Agent should mention unit tests.

        Args:
            agent_content: Content of agent file
        """
        content_lower = agent_content.lower()
        assert "unit test" in content_lower, (
            "Agent must mention unit tests as foundation of testing pyramid. "
            "Unit tests should be the most numerous test type."
        )

    def test_mentions_integration_tests(self, agent_content: str) -> None:
        """Agent should mention integration tests.

        Args:
            agent_content: Content of agent file
        """
        content_lower = agent_content.lower()
        assert "integration test" in content_lower, (
            "Agent must mention integration tests for API and database testing. "
            "These verify components work together correctly."
        )

    def test_mentions_e2e_tests(self, agent_content: str) -> None:
        """Agent should mention E2E tests.

        Args:
            agent_content: Content of agent file
        """
        content_lower = agent_content.lower()
        assert "e2e" in content_lower or "end-to-end" in content_lower, (
            "Agent must mention E2E tests for critical user journeys. "
            "These validate complete application workflows."
        )

    def test_mentions_coverage_guidelines(self, agent_content: str) -> None:
        """Agent should mention coverage guidelines or targets.

        Args:
            agent_content: Content of agent file
        """
        content_lower = agent_content.lower()
        assert "coverage" in content_lower, (
            "Agent must mention test coverage guidelines and targets. "
            "Coverage metrics help identify untested code paths."
        )

    def test_has_quality_checklist(self, agent_content: str) -> None:
        """Agent should have a quality checklist.

        Args:
            agent_content: Content of agent file
        """
        assert "## Quality Checklist" in agent_content or "Quality" in agent_content, (
            "Agent must have a quality checklist for validation. "
            "This ensures consistent quality standards across tests."
        )

    def test_has_checkbox_items(self, agent_content: str) -> None:
        """Agent should have checkbox items for verification.

        Args:
            agent_content: Content of agent file
        """
        assert "- [ ]" in agent_content, (
            "Agent must have checkbox items for task verification. "
            "Checklists ensure no quality steps are skipped."
        )

    def test_mentions_fixtures(self, agent_content: str) -> None:
        """Agent should mention test fixtures.

        Args:
            agent_content: Content of agent file
        """
        content_lower = agent_content.lower()
        assert "fixture" in content_lower, (
            "Agent must mention test fixtures for test setup/teardown. "
            "Fixtures provide reusable test data and state management."
        )

    def test_mentions_mocking(self, agent_content: str) -> None:
        """Agent should mention mocking.

        Args:
            agent_content: Content of agent file
        """
        content_lower = agent_content.lower()
        assert "mock" in content_lower, (
            "Agent must mention mocking for isolating test units. "
            "Mocks simulate dependencies for focused unit testing."
        )
