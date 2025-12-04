"""Tool dependency manager for security scanners.

Handles installation, version management, and caching for Semgrep and CodeQL.
Supports on-demand download, version pinning, and offline mode.
"""

import json
import shutil
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ToolStatus(Enum):
    """Status of a tool installation."""

    NOT_INSTALLED = "not_installed"
    INSTALLED = "installed"
    OUTDATED = "outdated"
    ERROR = "error"


@dataclass
class ToolInfo:
    """Information about a tool."""

    name: str
    status: ToolStatus
    version: Optional[str] = None
    path: Optional[str] = None
    error: Optional[str] = None
    size_mb: float = 0.0


@dataclass
class ToolConfig:
    """Configuration for tool management."""

    cache_dir: Path = field(default_factory=lambda: Path.home() / ".specify" / "tools")
    offline_mode: bool = False
    max_cache_size_mb: float = 500.0
    semgrep_version: str = "latest"
    codeql_version: str = "latest"

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "ToolConfig":
        """Load configuration from file or defaults."""
        if config_path and config_path.exists():
            with open(config_path) as f:
                data = json.load(f)
                return cls(
                    cache_dir=Path(data.get("cache_dir", cls().cache_dir)),
                    offline_mode=data.get("offline_mode", False),
                    max_cache_size_mb=data.get("max_cache_size_mb", 500.0),
                    semgrep_version=data.get("semgrep_version", "latest"),
                    codeql_version=data.get("codeql_version", "latest"),
                )
        return cls()


class ToolManager:
    """Manages security tool installations and caching."""

    def __init__(self, config: Optional[ToolConfig] = None):
        """Initialize tool manager.

        Args:
            config: Tool configuration (uses defaults if not provided)
        """
        self.config = config or ToolConfig()
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)
        self._installers: Dict[str, "BaseInstaller"] = {}
        self._load_installers()

    def _load_installers(self) -> None:
        """Load available tool installers."""
        from .installers import SemgrepInstaller, CodeQLInstaller

        self._installers = {
            "semgrep": SemgrepInstaller(self.config),
            "codeql": CodeQLInstaller(self.config),
        }

    def get_status(self, tool_name: str) -> ToolInfo:
        """Get status of a specific tool.

        Args:
            tool_name: Name of the tool (semgrep, codeql)

        Returns:
            ToolInfo with current status
        """
        if tool_name not in self._installers:
            return ToolInfo(
                name=tool_name,
                status=ToolStatus.ERROR,
                error=f"Unknown tool: {tool_name}",
            )

        installer = self._installers[tool_name]
        return installer.get_status()

    def get_all_status(self) -> List[ToolInfo]:
        """Get status of all managed tools.

        Returns:
            List of ToolInfo for all tools
        """
        return [self.get_status(name) for name in self._installers]

    def ensure_installed(
        self, tool_name: str, required_version: Optional[str] = None
    ) -> ToolInfo:
        """Ensure a tool is installed, installing if necessary.

        Args:
            tool_name: Name of the tool
            required_version: Specific version to install (optional)

        Returns:
            ToolInfo with installation result

        Raises:
            RuntimeError: If offline mode and tool not cached
        """
        if tool_name not in self._installers:
            return ToolInfo(
                name=tool_name,
                status=ToolStatus.ERROR,
                error=f"Unknown tool: {tool_name}",
            )

        installer = self._installers[tool_name]
        status = installer.get_status()

        # Already installed and up to date
        if status.status == ToolStatus.INSTALLED:
            if required_version is None or status.version == required_version:
                return status

        # Check offline mode
        if self.config.offline_mode:
            if status.status != ToolStatus.INSTALLED:
                return ToolInfo(
                    name=tool_name,
                    status=ToolStatus.ERROR,
                    error="Offline mode: tool not in cache",
                )
            return status

        # Install or update
        return installer.install(required_version)

    def get_cache_size(self) -> float:
        """Get total size of tool cache in MB.

        Returns:
            Cache size in megabytes
        """
        total = 0
        for path in self.config.cache_dir.rglob("*"):
            if path.is_file():
                total += path.stat().st_size
        return total / (1024 * 1024)

    def check_cache_size(self) -> Optional[str]:
        """Check if cache exceeds size limit.

        Returns:
            Warning message if cache exceeds limit, None otherwise
        """
        size = self.get_cache_size()
        if size > self.config.max_cache_size_mb:
            return f"Tool cache ({size:.1f}MB) exceeds limit ({self.config.max_cache_size_mb}MB)"
        return None

    def clear_cache(self) -> None:
        """Clear the tool cache directory."""
        if self.config.cache_dir.exists():
            shutil.rmtree(self.config.cache_dir)
            self.config.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Cleared tool cache: {self.config.cache_dir}")

    def get_tool_path(self, tool_name: str) -> Optional[Path]:
        """Get the path to a tool's executable.

        Args:
            tool_name: Name of the tool

        Returns:
            Path to executable or None if not installed
        """
        if tool_name not in self._installers:
            return None

        installer = self._installers[tool_name]
        status = installer.get_status()

        if status.status == ToolStatus.INSTALLED and status.path:
            return Path(status.path)
        return None


class BaseInstaller:
    """Base class for tool installers."""

    def __init__(self, config: ToolConfig):
        self.config = config

    def get_status(self) -> ToolInfo:
        """Get current installation status."""
        raise NotImplementedError

    def install(self, version: Optional[str] = None) -> ToolInfo:
        """Install the tool."""
        raise NotImplementedError

    def _run_command(
        self, cmd: List[str], capture: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a command and return result."""
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=300,  # 5 minute timeout
        )
