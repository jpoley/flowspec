"""Packaging regression tests.

The wheel build broke once because `src/flowspec_cli/templates` was listed in
`[tool.hatch.build.targets.wheel.force-include]` while already being inside the
`packages` entry. Hatchling then added every template twice and failed with
"A second file is being added to the wheel archive at the same path".

These tests pin the invariants that keep `uv build` working, without paying the
cost of an actual build.
"""

from __future__ import annotations

import shutil
import subprocess
import tarfile
import tomllib
import zipfile
from pathlib import Path

import pytest

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


def tracked_template_files() -> set[str]:
    """Template paths git tracks, relative to src/flowspec_cli."""
    result = subprocess.run(
        ["git", "ls-files", "src/flowspec_cli/templates"],
        cwd=get_project_root(),
        capture_output=True,
        text=True,
        check=True,
    )
    prefix = "src/flowspec_cli/"
    return {
        line[len(prefix) :]
        for line in result.stdout.splitlines()
        if line.startswith(prefix)
    }


@pytest.fixture(scope="module")
def built(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build the wheel and sdist once for the whole module."""
    if shutil.which("uv") is None:
        pytest.skip("uv not available")
    out = tmp_path_factory.mktemp("dist")
    result = subprocess.run(
        ["uv", "build", "--out-dir", str(out)],
        cwd=get_project_root(),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"uv build failed:\n{result.stdout}\n{result.stderr}")
    return out


@pytest.mark.slow
class TestBuiltArtifactsContainTemplates:
    """Assert against the real artifacts, not just pyproject text.

    The config-level tests above cannot catch a Hatch `exclude` rule that drops
    templates from the distribution while leaving the source tree untouched.
    """

    def test_wheel_contains_every_tracked_template(self, built: Path) -> None:
        wheels = list(built.glob("*.whl"))
        assert len(wheels) == 1, f"expected exactly one wheel, got {wheels}"
        with zipfile.ZipFile(wheels[0]) as zf:
            names = set(zf.namelist())
        expected = {f"flowspec_cli/{rel}" for rel in tracked_template_files()}
        missing = expected - names
        assert not missing, (
            f"{len(missing)} template(s) missing from wheel: {sorted(missing)[:10]}"
        )

    def test_wheel_has_no_duplicate_entries(self, built: Path) -> None:
        # The exact failure mode that broke `uv build` under hatchling 1.32.
        wheels = list(built.glob("*.whl"))
        with zipfile.ZipFile(wheels[0]) as zf:
            names = zf.namelist()
        duplicates = {n for n in names if names.count(n) > 1}
        assert not duplicates, f"duplicate wheel entries: {sorted(duplicates)}"

    def test_sdist_contains_every_tracked_template(self, built: Path) -> None:
        sdists = list(built.glob("*.tar.gz"))
        assert len(sdists) == 1, f"expected exactly one sdist, got {sdists}"
        with tarfile.open(sdists[0]) as tf:
            names = {n.split("/", 1)[1] for n in tf.getnames() if "/" in n}
        expected = {f"src/flowspec_cli/{rel}" for rel in tracked_template_files()}
        missing = expected - names
        assert not missing, (
            f"{len(missing)} template(s) missing from sdist: {sorted(missing)[:10]}"
        )
