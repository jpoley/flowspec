"""Template registry for flowspec agent and workflow templates.

This module provides a centralized registry for loading templates from disk
rather than embedding them as strings in __init__.py.
"""

from pathlib import Path
from typing import Dict, Optional
import importlib.resources


class TemplateRegistry:
    """Registry for loading and managing flowspec templates.

    Templates are organized into three categories:
    - agents: AI agent configurations (e.g., flow.assess.agent.md)
    - workflows: Workflow definitions
    - configs: Configuration templates
    """

    def __init__(self, base_path: Optional[Path] = None):
        self._cache: Dict[str, str] = {}
        self.base_path = base_path or Path(__file__).parent
        self._template_base = self.base_path  # For backward compatibility

    def get_agent_template(self, name: str) -> str:
        """Get an agent template by name.

        Args:
            name: Template filename (e.g., "flow.assess.agent.md")
                 .md extension is optional and will be added if missing.

        Returns:
            Template content as string

        Raises:
            FileNotFoundError: If template does not exist
        """
        # Add .md extension if not present
        if not name.endswith('.md'):
            name = f"{name}.md"

        cache_key = f"agents/{name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        template_path = self._template_base / "agents" / name
        if not template_path.exists():
            raise FileNotFoundError(f"Agent template not found: {name}")

        content = template_path.read_text(encoding="utf-8")
        self._cache[cache_key] = content
        return content

    def get_workflow_template(self, name: str) -> Optional[str]:
        """Get a workflow template by name.

        Args:
            name: Template filename

        Returns:
            Template content as string, or None if not found
        """
        cache_key = f"workflow:{name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        template_path = self._template_base / "workflows" / name
        if not template_path.exists():
            return None

        content = template_path.read_text(encoding="utf-8")
        self._cache[cache_key] = content
        return content

    def get_config_template(self, name: str) -> Optional[str]:
        """Get a configuration template by name.

        Args:
            name: Template filename

        Returns:
            Template content as string, or None if not found
        """
        cache_key = f"config:{name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        template_path = self._template_base / "configs" / name
        if not template_path.exists():
            return None

        content = template_path.read_text(encoding="utf-8")
        self._cache[cache_key] = content
        return content

    def list_agent_templates(self) -> list[str]:
        """List all available agent templates.

        Returns:
            List of agent template filenames
        """
        agents_dir = self._template_base / "agents"
        if not agents_dir.exists():
            return []
        return [f.name for f in agents_dir.glob("*.md")]

    def get_all_agent_templates(self) -> Dict[str, str]:
        """Get all agent templates as a dictionary.

        Returns:
            Dictionary mapping template names to content
        """
        templates = {}
        for name in self.list_agent_templates():
            content = self.get_agent_template(name)
            if content:
                templates[name] = content
        return templates

    def get_constitution_template(self, tier: str) -> str:
        """Get a constitution template by tier.

        Args:
            tier: Constitution tier (light, medium, heavy)

        Returns:
            Template content as string

        Raises:
            FileNotFoundError: If template does not exist
        """
        cache_key = f"constitution/{tier}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Constitution templates are embedded in __init__.py for now
        # This will be migrated to files later
        from flowspec_cli import CONSTITUTION_TEMPLATES
        if tier not in CONSTITUTION_TEMPLATES:
            raise FileNotFoundError(f"Constitution template not found: {tier}")

        content = CONSTITUTION_TEMPLATES[tier]
        self._cache[cache_key] = content
        return content

    def get_all_constitution_templates(self) -> Dict[str, str]:
        """Get all constitution templates as a dictionary.

        Returns:
            Dictionary mapping tier names to content
        """
        from flowspec_cli import CONSTITUTION_TEMPLATES
        return dict(CONSTITUTION_TEMPLATES)

    def clear_cache(self):
        """Clear the template cache."""
        self._cache.clear()


# Global registry instance
registry = TemplateRegistry()


# Convenience functions for global registry access
def get_agent_template(name: str) -> str:
    """Get an agent template by name (convenience function).

    Args:
        name: Template filename (e.g., "flow.assess.agent.md")

    Returns:
        Template content as string
    """
    return registry.get_agent_template(name)


def get_constitution_template(tier: str) -> str:
    """Get a constitution template by tier (convenience function).

    Args:
        tier: Constitution tier (light, medium, heavy)

    Returns:
        Template content as string
    """
    return registry.get_constitution_template(tier)


def get_all_agent_templates() -> Dict[str, str]:
    """Get all agent templates (convenience function).

    Returns:
        Dictionary mapping template names to content
    """
    return registry.get_all_agent_templates()


def get_all_constitution_templates() -> Dict[str, str]:
    """Get all constitution templates (convenience function).

    Returns:
        Dictionary mapping tier names to content
    """
    return registry.get_all_constitution_templates()


__all__ = [
    "TemplateRegistry",
    "registry",
    "get_agent_template",
    "get_constitution_template",
    "get_all_agent_templates",
    "get_all_constitution_templates",
]
