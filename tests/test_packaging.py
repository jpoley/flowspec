"""Packaging regression tests.

The wheel build broke once because `src/flowspec_cli/templates` was listed in
`[tool.hatch.build.targets.wheel.force-include]` while already being inside the
`packages` entry. Hatchling then added every template twice and failed with
"A second file is being added to the wheel archive at the same path".

These tests pin the invariants that keep `uv build` working, without paying the
cost of an actual build.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

# The wheel must ship every template; a large drop means templates stopped being
# packaged even though the build still succeeds.
MIN_TEMPLATE_FILE_COUNT = 100


def get_project_root() -> Path:
    """Get the project root directory reliably."""
    return Path(__file__).resolve().parent.parent


def load_pyproject() -> dict:
    """Load and parse pyproject.toml from the project root."""
    path = get_project_root() / "pyproject.toml"
    assert path.exists(), f"pyproject.toml not found: {path}"
    with open(path, "rb") as f:
        return tomllib.load(f)


def wheel_config() -> dict:
    """Return the [tool.hatch.build.targets.wheel] table."""
    return (
        load_pyproject()
        .get("tool", {})
        .get("hatch", {})
        .get("build", {})
        .get("targets", {})
        .get("wheel", {})
    )


class TestWheelBuildConfig:
    def test_packages_includes_flowspec_cli(self) -> None:
        packages = wheel_config().get("packages", [])
        assert "src/flowspec_cli" in packages, (
            f"src/flowspec_cli missing from wheel packages: {packages}"
        )

    def test_templates_are_not_force_included(self) -> None:
        # src/flowspec_cli/templates is already covered by the packages entry.
        # Force-including it duplicates every template and breaks `uv build`.
        force_include = wheel_config().get("force-include", {})
        for source in force_include:
            assert "templates" not in source, (
                "src/flowspec_cli/templates must not be force-included; it is "
                f"already inside the packages entry. Offending key: {source!r}"
            )

    def test_no_force_include_overlaps_the_package_path(self) -> None:
        force_include = wheel_config().get("force-include", {})
        for source in force_include:
            normalized = source.replace("\\", "/").rstrip("/")
            assert not normalized.startswith("src/flowspec_cli/"), (
                f"force-include key {source!r} is inside the packaged path and "
                "will produce duplicate wheel entries"
            )


class TestTemplatesArePackageable:
    def test_templates_directory_exists_inside_the_package(self) -> None:
        templates = get_project_root() / "src" / "flowspec_cli" / "templates"
        assert templates.is_dir(), f"Templates directory not found: {templates}"

    def test_templates_directory_is_populated(self) -> None:
        templates = get_project_root() / "src" / "flowspec_cli" / "templates"
        files = [
            p
            for p in templates.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        ]
        assert len(files) >= MIN_TEMPLATE_FILE_COUNT, (
            f"Only {len(files)} template files found; expected at least "
            f"{MIN_TEMPLATE_FILE_COUNT}"
        )

    def test_dotfile_templates_are_present(self) -> None:
        # Dotfiles are the ones the broken force-include was meant to rescue.
        templates = get_project_root() / "src" / "flowspec_cli" / "templates"
        for name in (".mcp.json", ".flowspec", ".github"):
            assert (templates / name).exists(), f"Missing template entry: {name}"
