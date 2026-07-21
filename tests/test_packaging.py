"""Tests for wheel packaging configuration in pyproject.toml.

Regression coverage for a build failure where `[tool.hatch.build.targets.wheel]`
`packages` and `force-include` both mapped `src/flowspec_cli/templates` into the
wheel. Newer hatchling versions reject the duplicate archive entry outright:

    ValueError: A second file is being added to the wheel archive at the same
    path: `flowspec_cli/templates/.mcp.json`.

This made `uv tool install .` fail on a clean checkout. Tests cover:
- No force-include target duplicates a path already shipped by `packages`
- The templates directory is still shipped via `packages`
"""

import tomllib
from pathlib import Path

# Templates must be bundled so `flowspec init` works from a standalone install.
TEMPLATES_RELATIVE_PATH = "templates"


def get_project_root() -> Path:
    """Get the project root directory reliably."""
    return Path(__file__).resolve().parent.parent


def load_pyproject() -> dict:
    """Load and parse pyproject.toml from the project root."""
    pyproject_path = get_project_root() / "pyproject.toml"
    assert pyproject_path.exists(), f"Not found: {pyproject_path}"
    with open(pyproject_path, "rb") as f:
        return tomllib.load(f)


def get_wheel_config(pyproject: dict) -> dict:
    """Get the [tool.hatch.build.targets.wheel] table, or an empty dict."""
    return (
        pyproject.get("tool", {})
        .get("hatch", {})
        .get("build", {})
        .get("targets", {})
        .get("wheel", {})
    )


class TestWheelPackaging:
    """Tests for the hatchling wheel build configuration."""

    def test_force_include_does_not_duplicate_packages(self) -> None:
        """force-include must not re-add paths already shipped by `packages`.

        Hatchling ships every file under each entry in `packages`. Adding the
        same source path via force-include produces duplicate wheel entries and
        fails the build.
        """
        wheel_config = get_wheel_config(load_pyproject())
        packages = wheel_config.get("packages", [])
        force_include = wheel_config.get("force-include", {})

        for source_path in force_include:
            normalized = Path(source_path).as_posix()
            for package in packages:
                package_path = Path(package).as_posix()
                assert not normalized.startswith(f"{package_path}/"), (
                    f"force-include entry '{source_path}' is already inside "
                    f"package '{package}'; this duplicates wheel entries and "
                    f"breaks the build"
                )

    def test_templates_shipped_via_packages(self) -> None:
        """Templates must live inside a packaged directory so they get bundled."""
        wheel_config = get_wheel_config(load_pyproject())
        packages = wheel_config.get("packages", [])
        assert packages, "pyproject.toml must declare wheel packages"

        project_root = get_project_root()
        templates_dirs = [
            project_root / package / TEMPLATES_RELATIVE_PATH for package in packages
        ]
        assert any(path.is_dir() for path in templates_dirs), (
            f"No templates directory found inside packaged dirs: {templates_dirs}"
        )
