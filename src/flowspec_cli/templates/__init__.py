"""Template registry for loading templates from disk."""

from pathlib import Path
from typing import Dict


class TemplateRegistry:
    """Registry for loading and caching templates from disk.

    Provides backward-compatible access to templates that were previously
    embedded as strings in __init__.py.
    """

    def __init__(self, base_path: Path | None = None):
        """Initialize the template registry.

        Args:
            base_path: Base directory containing template subdirectories.
                      Defaults to the templates/ directory in this package.
        """
        if base_path is None:
            base_path = Path(__file__).parent
        self.base_path = base_path
        self._cache: Dict[str, str] = {}

    def _load_template(self, category: str, name: str) -> str:
        """Load a template from disk.

        Args:
            category: Template category subdirectory (e.g., 'agents', 'constitution')
            name: Template filename (with or without .md extension)

        Returns:
            Template content as string

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        # Ensure .md extension
        if not name.endswith('.md'):
            name = f"{name}.md"

        cache_key = f"{category}/{name}"

        # Return cached version if available
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Load from disk
        template_path = self.base_path / category / name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        content = template_path.read_text()
        self._cache[cache_key] = content
        return content

    def get_agent_template(self, name: str) -> str:
        """Load an agent template.

        Args:
            name: Agent template name (e.g., 'flow.assess.agent.md')

        Returns:
            Template content
        """
        return self._load_template("agents", name)

    def get_constitution_template(self, tier: str) -> str:
        """Load a constitution template.

        Args:
            tier: Constitution tier ('light', 'medium', or 'heavy')

        Returns:
            Template content
        """
        return self._load_template("constitution", tier)

    def get_all_agent_templates(self) -> Dict[str, str]:
        """Load all agent templates.

        Returns:
            Dictionary mapping template names to content
        """
        agents_dir = self.base_path / "agents"
        if not agents_dir.exists():
            return {}

        templates = {}
        for template_file in sorted(agents_dir.glob("flow.*.agent.md")):
            name = template_file.name
            templates[name] = self._load_template("agents", name)

        return templates

    def get_all_constitution_templates(self) -> Dict[str, str]:
        """Load all constitution templates.

        Returns:
            Dictionary mapping tier names to content
        """
        constitution_dir = self.base_path / "constitution"
        if not constitution_dir.exists():
            return {}

        templates = {}
        for template_file in sorted(constitution_dir.glob("*.md")):
            tier = template_file.stem  # filename without .md
            templates[tier] = self._load_template("constitution", tier)

        return templates

    def clear_cache(self):
        """Clear the template cache.

        Useful for testing or if templates are modified at runtime.
        """
        self._cache.clear()


# Global registry instance for backward compatibility
_global_registry = TemplateRegistry()


def get_agent_template(name: str) -> str:
    """Load an agent template from the global registry.

    Args:
        name: Agent template name (e.g., 'flow.assess.agent.md')

    Returns:
        Template content
    """
    return _global_registry.get_agent_template(name)


def get_constitution_template(tier: str) -> str:
    """Load a constitution template from the global registry.

    Args:
        tier: Constitution tier ('light', 'medium', or 'heavy')

    Returns:
        Template content
    """
    return _global_registry.get_constitution_template(tier)


def get_all_agent_templates() -> Dict[str, str]:
    """Load all agent templates from the global registry.

    Returns:
        Dictionary mapping template names to content
    """
    return _global_registry.get_all_agent_templates()


def get_all_constitution_templates() -> Dict[str, str]:
    """Load all constitution templates from the global registry.

    Returns:
        Dictionary mapping tier names to content
    """
    return _global_registry.get_all_constitution_templates()
