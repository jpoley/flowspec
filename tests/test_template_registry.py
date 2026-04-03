"""Tests for template registry functionality."""

import pytest
from pathlib import Path

from flowspec_cli.templates import (
    TemplateRegistry,
    get_agent_template,
    get_constitution_template,
    get_all_agent_templates,
    get_all_constitution_templates,
)


class TestTemplateRegistry:
    """Test the TemplateRegistry class."""

    def test_registry_initialization(self):
        """Test that TemplateRegistry initializes correctly."""
        registry = TemplateRegistry()
        assert registry.base_path.name == "templates"
        assert registry._cache == {}

    def test_registry_custom_base_path(self):
        """Test TemplateRegistry with custom base path."""
        custom_path = Path("/tmp/custom_templates")
        registry = TemplateRegistry(base_path=custom_path)
        assert registry.base_path == custom_path

    def test_load_agent_template(self):
        """Test loading a specific agent template."""
        registry = TemplateRegistry()
        template = registry.get_agent_template("flow.assess.agent.md")

        # Verify template content
        assert "FlowAssess" in template
        assert "name: FlowAssess" in template
        assert "/flow:assess" in template
        assert "Feature Assessment" in template

    def test_load_agent_template_without_extension(self):
        """Test loading agent template without .md extension."""
        registry = TemplateRegistry()
        template = registry.get_agent_template("flow.assess.agent")

        # Should add .md automatically
        assert "FlowAssess" in template

    def test_load_constitution_template(self):
        """Test loading a specific constitution template."""
        registry = TemplateRegistry()

        for tier in ["light", "medium", "heavy"]:
            template = registry.get_constitution_template(tier)
            assert "[PROJECT_NAME]" in template
            assert "Constitution" in template
            assert f"TIER: {tier.capitalize()}" in template or tier in template.lower()

    def test_get_all_agent_templates(self):
        """Test loading all agent templates."""
        registry = TemplateRegistry()
        templates = registry.get_all_agent_templates()

        # Verify we got all 6 workflow agent templates
        expected_agents = [
            "flow.assess.agent.md",
            "flow.specify.agent.md",
            "flow.plan.agent.md",
            "flow.implement.agent.md",
            "flow.validate.agent.md",
            "flow.submit-n-watch-pr.agent.md",
        ]

        for agent_name in expected_agents:
            assert agent_name in templates
            assert len(templates[agent_name]) > 0

    def test_get_all_constitution_templates(self):
        """Test loading all constitution templates."""
        registry = TemplateRegistry()
        templates = registry.get_all_constitution_templates()

        # Verify we got all 3 tier templates
        assert "light" in templates
        assert "medium" in templates
        assert "heavy" in templates

        # Verify they contain expected content
        for tier, content in templates.items():
            assert len(content) > 0
            assert "[PROJECT_NAME]" in content

    def test_template_caching(self):
        """Test that templates are cached after first load."""
        registry = TemplateRegistry()

        # Load template first time
        template1 = registry.get_agent_template("flow.assess.agent.md")

        # Check it's in cache
        assert "agents/flow.assess.agent.md" in registry._cache

        # Load again - should come from cache
        template2 = registry.get_agent_template("flow.assess.agent.md")

        # Should be identical
        assert template1 == template2
        assert template1 is template2  # Same object in memory

    def test_clear_cache(self):
        """Test clearing the template cache."""
        registry = TemplateRegistry()

        # Load and cache a template
        registry.get_agent_template("flow.assess.agent.md")
        assert len(registry._cache) > 0

        # Clear cache
        registry.clear_cache()
        assert len(registry._cache) == 0

    def test_nonexistent_template_raises_error(self):
        """Test that loading a nonexistent template raises FileNotFoundError."""
        registry = TemplateRegistry()

        with pytest.raises(FileNotFoundError):
            registry.get_agent_template("nonexistent.agent.md")

        with pytest.raises(FileNotFoundError):
            registry.get_constitution_template("nonexistent")


class TestGlobalRegistryFunctions:
    """Test the global registry convenience functions."""

    def test_get_agent_template(self):
        """Test global get_agent_template function."""
        template = get_agent_template("flow.assess.agent.md")
        assert "FlowAssess" in template

    def test_get_constitution_template(self):
        """Test global get_constitution_template function."""
        template = get_constitution_template("light")
        assert "[PROJECT_NAME]" in template
        assert "Constitution" in template

    def test_get_all_agent_templates(self):
        """Test global get_all_agent_templates function."""
        templates = get_all_agent_templates()
        assert "flow.assess.agent.md" in templates
        assert len(templates) >= 6

    def test_get_all_constitution_templates(self):
        """Test global get_all_constitution_templates function."""
        templates = get_all_constitution_templates()
        assert "light" in templates
        assert "medium" in templates
        assert "heavy" in templates


class TestTemplateContent:
    """Test the actual content of templates for correctness."""

    def test_agent_template_structure(self):
        """Test that agent templates have correct YAML frontmatter."""
        templates = get_all_agent_templates()

        for name, content in templates.items():
            # Should start with YAML frontmatter
            assert content.startswith("---\n")

            # Should have required frontmatter fields
            assert "name:" in content
            assert "description:" in content
            assert "target:" in content
            assert "tools:" in content

    def test_constitution_template_placeholders(self):
        """Test that constitution templates have required placeholders."""
        templates = get_all_constitution_templates()

        for tier, content in templates.items():
            # Should have project name placeholder
            assert "[PROJECT_NAME]" in content

            # Should have tier indicator
            assert "TIER:" in content or tier in content.lower()

            # Should have validation markers (at least for some sections)
            if tier != "light":
                assert "NEEDS_VALIDATION" in content

    def test_backward_compatibility_keys(self):
        """Test that template keys match original embedded template keys."""
        # Agent templates should use original filenames
        agent_templates = get_all_agent_templates()
        expected_agent_keys = {
            "flow.assess.agent.md",
            "flow.specify.agent.md",
            "flow.plan.agent.md",
            "flow.implement.agent.md",
            "flow.validate.agent.md",
            "flow.submit-n-watch-pr.agent.md",
        }
        actual_agent_keys = set(agent_templates.keys())
        assert expected_agent_keys.issubset(actual_agent_keys)

        # Constitution templates should use tier names
        constitution_templates = get_all_constitution_templates()
        expected_constitution_keys = {"light", "medium", "heavy"}
        assert set(constitution_templates.keys()) == expected_constitution_keys
