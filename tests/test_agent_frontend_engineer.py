"""Tests for the frontend-engineer agent."""

import re
from pathlib import Path

import pytest


@pytest.fixture
def agent_file_path() -> Path:
    """Return path to frontend-engineer agent file."""
    return Path(".claude/agents/frontend-engineer.md")


@pytest.fixture
def template_file_path() -> Path:
    """Return path to frontend-engineer template file."""
    return Path("templates/agents/frontend-engineer.md")


@pytest.fixture
def agent_content(agent_file_path: Path) -> str:
    """Return content of the frontend-engineer agent file."""
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


class TestFrontendEngineerAgentFile:
    """Test the frontend-engineer agent file exists and is valid."""

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


class TestFrontendEngineerFrontmatter:
    """Test the YAML frontmatter of the frontend-engineer agent."""

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
        assert frontmatter["name"] == "frontend-engineer"

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
        assert frontmatter["color"] == "cyan"


class TestFrontendEngineerTools:
    """Test the tools configuration for the frontend-engineer agent."""

    def test_tools_list(self, frontmatter: dict):
        """Frontend engineer should have appropriate tools."""
        tools = frontmatter.get("tools", "").split(", ")
        expected_tools = ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]

        assert len(tools) > 0, "Agent should have tools configured"

        for tool in expected_tools:
            assert tool in tools, f"Frontend engineer should have {tool} tool"

    def test_has_file_manipulation_tools(self, frontmatter: dict):
        """Frontend engineer should have file manipulation tools."""
        tools = frontmatter.get("tools", "").split(", ")

        # Frontend engineers need to read and write code
        assert "Read" in tools, "Frontend engineer needs Read tool"
        assert "Write" in tools, "Frontend engineer needs Write tool"
        assert "Edit" in tools, "Frontend engineer needs Edit tool"

    def test_has_code_search_tools(self, frontmatter: dict):
        """Frontend engineer should have code search tools."""
        tools = frontmatter.get("tools", "").split(", ")

        # Frontend engineers need to search codebases
        assert "Glob" in tools, "Frontend engineer needs Glob tool"
        assert "Grep" in tools, "Frontend engineer needs Grep tool"

    def test_has_bash_tool(self, frontmatter: dict):
        """Frontend engineer should have Bash tool for running commands."""
        tools = frontmatter.get("tools", "").split(", ")

        # Frontend engineers need to run build tools, linters, tests
        assert "Bash" in tools, "Frontend engineer needs Bash tool"


class TestFrontendEngineerDescription:
    """Test the description field matches the agent's purpose."""

    def test_description_mentions_frontend(self, frontmatter: dict):
        """Description should mention frontend development."""
        description = frontmatter["description"].lower()
        assert "frontend" in description, (
            "Description should mention 'frontend' development"
        )

    def test_description_mentions_react(self, frontmatter: dict):
        """Description should mention React as a key technology."""
        description = frontmatter["description"].lower()
        assert "react" in description, "Description should mention React"

    def test_description_mentions_typescript(self, frontmatter: dict):
        """Description should mention TypeScript."""
        description = frontmatter["description"].lower()
        assert "typescript" in description or "ts" in description, (
            "Description should mention TypeScript"
        )

    def test_description_mentions_ui(self, frontmatter: dict):
        """Description should mention UI-related work."""
        description = frontmatter["description"].lower()
        ui_terms = ["ui", "component", "styling", "accessibility", "browser"]
        assert any(term in description for term in ui_terms), (
            "Description should mention UI-related work"
        )


class TestFrontendEngineerContent:
    """Test the content of the frontend-engineer agent."""

    def test_has_core_technologies_section(self, agent_content: str):
        """Agent should document core technologies."""
        assert "## Core Technologies" in agent_content, (
            "Agent should have Core Technologies section"
        )

    def test_mentions_react(self, agent_content: str):
        """Agent should mention React."""
        assert "React" in agent_content, "Agent should mention React"

    def test_mentions_nextjs(self, agent_content: str):
        """Agent should mention Next.js."""
        assert "Next.js" in agent_content or "NextJS" in agent_content, (
            "Agent should mention Next.js"
        )

    def test_mentions_typescript(self, agent_content: str):
        """Agent should mention TypeScript."""
        assert "TypeScript" in agent_content, "Agent should mention TypeScript"

    def test_has_implementation_standards(self, agent_content: str):
        """Agent should have implementation standards section."""
        assert "## Implementation Standards" in agent_content, (
            "Agent should have Implementation Standards section"
        )

    def test_has_testing_approach(self, agent_content: str):
        """Agent should have testing approach section."""
        assert "## Testing Approach" in agent_content, (
            "Agent should have Testing Approach section"
        )

    def test_mentions_accessibility(self, agent_content: str):
        """Agent should mention accessibility."""
        content_lower = agent_content.lower()
        assert "accessibility" in content_lower or "a11y" in content_lower, (
            "Agent should mention accessibility"
        )

    def test_mentions_performance(self, agent_content: str):
        """Agent should mention performance."""
        assert (
            "performance" in agent_content.lower() or "Performance" in agent_content
        ), "Agent should mention performance"

    def test_has_code_quality_checklist(self, agent_content: str):
        """Agent should have a code quality checklist."""
        assert (
            "## Code Quality Checklist" in agent_content
            or "Code Quality" in agent_content
        ), "Agent should have code quality checklist"

    def test_has_checkbox_items(self, agent_content: str):
        """Agent should have checkbox items for verification."""
        assert "- [ ]" in agent_content, "Agent should have checkbox items"
