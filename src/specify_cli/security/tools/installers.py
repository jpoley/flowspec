"""Tool installers for security scanners.

Implements installation logic for Semgrep and CodeQL.
"""

import os
import platform
import shutil
import subprocess
import sys
from typing import Optional
import logging
import urllib.request
import zipfile

from .manager import BaseInstaller, ToolInfo, ToolStatus

logger = logging.getLogger(__name__)


class SemgrepInstaller(BaseInstaller):
    """Installer for Semgrep static analysis tool."""

    TOOL_NAME = "semgrep"

    def get_status(self) -> ToolInfo:
        """Get Semgrep installation status."""
        # Check if semgrep is in PATH
        semgrep_path = shutil.which("semgrep")

        if semgrep_path:
            try:
                result = subprocess.run(
                    ["semgrep", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    return ToolInfo(
                        name=self.TOOL_NAME,
                        status=ToolStatus.INSTALLED,
                        version=version,
                        path=semgrep_path,
                    )
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        # Check cached installation
        cached_path = self.config.cache_dir / "semgrep" / "bin" / "semgrep"
        if cached_path.exists():
            try:
                result = subprocess.run(
                    [str(cached_path), "--version"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    return ToolInfo(
                        name=self.TOOL_NAME,
                        status=ToolStatus.INSTALLED,
                        version=version,
                        path=str(cached_path),
                    )
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        return ToolInfo(
            name=self.TOOL_NAME,
            status=ToolStatus.NOT_INSTALLED,
        )

    def install(self, version: Optional[str] = None) -> ToolInfo:
        """Install Semgrep via pip.

        Args:
            version: Specific version to install (e.g., "1.50.0")

        Returns:
            ToolInfo with installation result
        """
        version = version or self.config.semgrep_version

        # Build pip install command
        package = "semgrep" if version == "latest" else f"semgrep=={version}"

        try:
            logger.info(f"Installing {package}...")

            # Use pip to install to user site-packages or virtualenv
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", package],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode != 0:
                return ToolInfo(
                    name=self.TOOL_NAME,
                    status=ToolStatus.ERROR,
                    error=f"pip install failed: {result.stderr}",
                )

            # Verify installation
            return self.get_status()

        except subprocess.TimeoutExpired:
            return ToolInfo(
                name=self.TOOL_NAME,
                status=ToolStatus.ERROR,
                error="Installation timed out",
            )
        except Exception as e:
            return ToolInfo(
                name=self.TOOL_NAME,
                status=ToolStatus.ERROR,
                error=str(e),
            )


class CodeQLInstaller(BaseInstaller):
    """Installer for CodeQL security analysis tool."""

    TOOL_NAME = "codeql"
    GITHUB_RELEASE_URL = (
        "https://github.com/github/codeql-cli-binaries/releases/latest/download"
    )

    def get_status(self) -> ToolInfo:
        """Get CodeQL installation status."""
        # Check if codeql is in PATH
        codeql_path = shutil.which("codeql")

        if codeql_path:
            try:
                result = subprocess.run(
                    ["codeql", "version"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    # Parse version from output (e.g., "CodeQL command-line toolchain release 2.15.0")
                    version = result.stdout.strip().split("\n")[0]
                    return ToolInfo(
                        name=self.TOOL_NAME,
                        status=ToolStatus.INSTALLED,
                        version=version,
                        path=codeql_path,
                    )
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        # Check cached installation
        cached_path = self.config.cache_dir / "codeql" / "codeql"
        if platform.system() == "Windows":
            cached_path = cached_path.with_suffix(".exe")

        if cached_path.exists():
            try:
                result = subprocess.run(
                    [str(cached_path), "version"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    version = result.stdout.strip().split("\n")[0]
                    return ToolInfo(
                        name=self.TOOL_NAME,
                        status=ToolStatus.INSTALLED,
                        version=version,
                        path=str(cached_path),
                    )
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        return ToolInfo(
            name=self.TOOL_NAME,
            status=ToolStatus.NOT_INSTALLED,
        )

    def _check_license_acceptance(self) -> bool:
        """Check if user has accepted GitHub CodeQL license.

        CodeQL is free for research and OSS but requires license acceptance
        for commercial use.

        Returns:
            True if license is accepted or user is in OSS/research context
        """
        # Check environment variable for pre-accepted license
        if os.environ.get("CODEQL_LICENSE_ACCEPTED", "").lower() == "true":
            return True

        # Check for marker file
        license_marker = self.config.cache_dir / "codeql" / ".license_accepted"
        if license_marker.exists():
            return True

        return False

    def _accept_license(self) -> None:
        """Mark CodeQL license as accepted."""
        license_dir = self.config.cache_dir / "codeql"
        license_dir.mkdir(parents=True, exist_ok=True)
        license_marker = license_dir / ".license_accepted"
        license_marker.write_text(
            "CodeQL license accepted for research/OSS use.\n"
            "See: https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md\n"
        )

    def _get_download_url(self) -> str:
        """Get platform-specific download URL."""
        system = platform.system().lower()

        if system == "linux":
            return f"{self.GITHUB_RELEASE_URL}/codeql-linux64.zip"
        elif system == "darwin":
            return f"{self.GITHUB_RELEASE_URL}/codeql-osx64.zip"
        elif system == "windows":
            return f"{self.GITHUB_RELEASE_URL}/codeql-win64.zip"
        else:
            raise ValueError(f"Unsupported platform: {system}")

    def install(self, version: Optional[str] = None) -> ToolInfo:
        """Install CodeQL by downloading from GitHub.

        Args:
            version: Specific version (currently only 'latest' supported)

        Returns:
            ToolInfo with installation result
        """
        # Check license
        if not self._check_license_acceptance():
            return ToolInfo(
                name=self.TOOL_NAME,
                status=ToolStatus.ERROR,
                error=(
                    "CodeQL requires license acceptance. "
                    "Set CODEQL_LICENSE_ACCEPTED=true for OSS/research use, "
                    "or review license at https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md"
                ),
            )

        try:
            download_url = self._get_download_url()
            install_dir = self.config.cache_dir / "codeql"
            install_dir.mkdir(parents=True, exist_ok=True)

            # Download
            zip_path = install_dir / "codeql.zip"
            logger.info(f"Downloading CodeQL from {download_url}...")

            try:
                urllib.request.urlretrieve(download_url, zip_path)
            except Exception as e:
                return ToolInfo(
                    name=self.TOOL_NAME,
                    status=ToolStatus.ERROR,
                    error=f"Download failed: {e}",
                )

            # Extract
            logger.info("Extracting CodeQL...")
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(install_dir)

            # Clean up zip
            zip_path.unlink()

            # Make executable on Unix
            if platform.system() != "Windows":
                codeql_bin = install_dir / "codeql" / "codeql"
                if codeql_bin.exists():
                    codeql_bin.chmod(0o755)

            # Mark license accepted
            self._accept_license()

            return self.get_status()

        except Exception as e:
            return ToolInfo(
                name=self.TOOL_NAME,
                status=ToolStatus.ERROR,
                error=str(e),
            )


def get_available_installers() -> dict:
    """Get all available tool installers."""
    return {
        "semgrep": SemgrepInstaller,
        "codeql": CodeQLInstaller,
    }
