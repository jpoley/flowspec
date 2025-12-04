"""Tests for security tool dependency management."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch


from specify_cli.security.tools.manager import (
    ToolConfig,
    ToolInfo,
    ToolManager,
    ToolStatus,
)


class TestToolConfig:
    """Tests for ToolConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ToolConfig()

        assert config.cache_dir == Path.home() / ".specify" / "tools"
        assert config.offline_mode is False
        assert config.max_cache_size_mb == 500.0
        assert config.semgrep_version == "latest"
        assert config.codeql_version == "latest"

    def test_load_from_file(self, tmp_path):
        """Test loading config from JSON file."""
        config_file = tmp_path / "tools.json"
        config_file.write_text(
            json.dumps(
                {
                    "cache_dir": str(tmp_path / "cache"),
                    "offline_mode": True,
                    "max_cache_size_mb": 200.0,
                    "semgrep_version": "1.50.0",
                    "codeql_version": "2.15.0",
                }
            )
        )

        config = ToolConfig.load(config_file)

        assert config.cache_dir == tmp_path / "cache"
        assert config.offline_mode is True
        assert config.max_cache_size_mb == 200.0
        assert config.semgrep_version == "1.50.0"
        assert config.codeql_version == "2.15.0"

    def test_load_missing_file_returns_defaults(self, tmp_path):
        """Test loading from non-existent file returns defaults."""
        config = ToolConfig.load(tmp_path / "nonexistent.json")

        assert config.offline_mode is False
        assert config.max_cache_size_mb == 500.0


class TestToolInfo:
    """Tests for ToolInfo dataclass."""

    def test_tool_info_creation(self):
        """Test creating ToolInfo."""
        info = ToolInfo(
            name="semgrep",
            status=ToolStatus.INSTALLED,
            version="1.50.0",
            path="/usr/local/bin/semgrep",
        )

        assert info.name == "semgrep"
        assert info.status == ToolStatus.INSTALLED
        assert info.version == "1.50.0"
        assert info.path == "/usr/local/bin/semgrep"
        assert info.error is None

    def test_tool_info_with_error(self):
        """Test ToolInfo with error."""
        info = ToolInfo(
            name="codeql",
            status=ToolStatus.ERROR,
            error="Download failed",
        )

        assert info.status == ToolStatus.ERROR
        assert info.error == "Download failed"
        assert info.version is None


class TestToolManager:
    """Tests for ToolManager."""

    def test_creates_cache_dir(self, tmp_path):
        """Test that manager creates cache directory."""
        cache_dir = tmp_path / "cache"
        config = ToolConfig(cache_dir=cache_dir)

        assert not cache_dir.exists()
        ToolManager(config)
        assert cache_dir.exists()

    def test_get_status_unknown_tool(self, tmp_path):
        """Test getting status of unknown tool."""
        config = ToolConfig(cache_dir=tmp_path)
        manager = ToolManager(config)

        status = manager.get_status("unknown_tool")

        assert status.status == ToolStatus.ERROR
        assert "Unknown tool" in status.error

    def test_get_all_status(self, tmp_path):
        """Test getting status of all tools."""
        config = ToolConfig(cache_dir=tmp_path)
        manager = ToolManager(config)

        statuses = manager.get_all_status()

        assert len(statuses) == 2  # semgrep and codeql
        names = [s.name for s in statuses]
        assert "semgrep" in names
        assert "codeql" in names

    def test_get_cache_size(self, tmp_path):
        """Test getting cache size."""
        config = ToolConfig(cache_dir=tmp_path)
        manager = ToolManager(config)

        # Initially empty
        assert manager.get_cache_size() == 0.0

        # Add a file
        test_file = tmp_path / "test.bin"
        test_file.write_bytes(b"x" * 1024 * 1024)  # 1MB

        size = manager.get_cache_size()
        assert 0.9 < size < 1.1  # Approximately 1MB

    def test_check_cache_size_under_limit(self, tmp_path):
        """Test cache size check when under limit."""
        config = ToolConfig(cache_dir=tmp_path, max_cache_size_mb=100.0)
        manager = ToolManager(config)

        warning = manager.check_cache_size()
        assert warning is None

    def test_check_cache_size_over_limit(self, tmp_path):
        """Test cache size check when over limit."""
        config = ToolConfig(cache_dir=tmp_path, max_cache_size_mb=0.5)
        manager = ToolManager(config)

        # Add a file that exceeds limit
        test_file = tmp_path / "test.bin"
        test_file.write_bytes(b"x" * 1024 * 1024)  # 1MB

        warning = manager.check_cache_size()
        assert warning is not None
        assert "exceeds limit" in warning

    def test_clear_cache(self, tmp_path):
        """Test clearing cache."""
        config = ToolConfig(cache_dir=tmp_path)
        manager = ToolManager(config)

        # Add files
        (tmp_path / "file1.txt").write_text("test")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file2.txt").write_text("test")

        manager.clear_cache()

        # Cache dir should exist but be empty
        assert tmp_path.exists()
        assert list(tmp_path.iterdir()) == []

    def test_offline_mode_not_installed(self, tmp_path):
        """Test offline mode when tool not cached."""
        config = ToolConfig(cache_dir=tmp_path, offline_mode=True)
        manager = ToolManager(config)

        # Mock the installer to return not installed
        with patch.object(
            manager._installers["semgrep"],
            "get_status",
            return_value=ToolInfo(name="semgrep", status=ToolStatus.NOT_INSTALLED),
        ):
            result = manager.ensure_installed("semgrep")

        assert result.status == ToolStatus.ERROR
        assert "Offline mode" in result.error

    def test_get_tool_path_installed(self, tmp_path):
        """Test getting tool path when installed."""
        config = ToolConfig(cache_dir=tmp_path)
        manager = ToolManager(config)

        # Mock installed tool
        with patch.object(
            manager._installers["semgrep"],
            "get_status",
            return_value=ToolInfo(
                name="semgrep",
                status=ToolStatus.INSTALLED,
                path="/usr/bin/semgrep",
            ),
        ):
            path = manager.get_tool_path("semgrep")

        assert path == Path("/usr/bin/semgrep")

    def test_get_tool_path_not_installed(self, tmp_path):
        """Test getting tool path when not installed."""
        config = ToolConfig(cache_dir=tmp_path)
        manager = ToolManager(config)

        with patch.object(
            manager._installers["semgrep"],
            "get_status",
            return_value=ToolInfo(name="semgrep", status=ToolStatus.NOT_INSTALLED),
        ):
            path = manager.get_tool_path("semgrep")

        assert path is None


class TestSemgrepInstaller:
    """Tests for SemgrepInstaller."""

    def test_get_status_in_path(self, tmp_path):
        """Test status when semgrep is in PATH."""
        from specify_cli.security.tools.installers import SemgrepInstaller

        config = ToolConfig(cache_dir=tmp_path)
        installer = SemgrepInstaller(config)

        with patch("shutil.which", return_value="/usr/local/bin/semgrep"):
            with patch(
                "subprocess.run",
                return_value=MagicMock(returncode=0, stdout="1.50.0\n"),
            ):
                status = installer.get_status()

        assert status.status == ToolStatus.INSTALLED
        assert status.version == "1.50.0"
        assert status.path == "/usr/local/bin/semgrep"

    def test_get_status_not_installed(self, tmp_path):
        """Test status when semgrep is not installed."""
        from specify_cli.security.tools.installers import SemgrepInstaller

        config = ToolConfig(cache_dir=tmp_path)
        installer = SemgrepInstaller(config)

        with patch("shutil.which", return_value=None):
            status = installer.get_status()

        assert status.status == ToolStatus.NOT_INSTALLED

    def test_install_success(self, tmp_path):
        """Test successful installation."""
        from specify_cli.security.tools.installers import SemgrepInstaller

        config = ToolConfig(cache_dir=tmp_path)
        installer = SemgrepInstaller(config)

        with patch(
            "subprocess.run",
            side_effect=[
                MagicMock(returncode=0, stdout="", stderr=""),  # pip install
            ],
        ):
            with patch.object(
                installer,
                "get_status",
                return_value=ToolInfo(
                    name="semgrep",
                    status=ToolStatus.INSTALLED,
                    version="1.50.0",
                ),
            ):
                result = installer.install()

        assert result.status == ToolStatus.INSTALLED


class TestCodeQLInstaller:
    """Tests for CodeQLInstaller."""

    def test_license_check_env_var(self, tmp_path, monkeypatch):
        """Test license acceptance via environment variable."""
        from specify_cli.security.tools.installers import CodeQLInstaller

        monkeypatch.setenv("CODEQL_LICENSE_ACCEPTED", "true")

        config = ToolConfig(cache_dir=tmp_path)
        installer = CodeQLInstaller(config)

        assert installer._check_license_acceptance() is True

    def test_license_check_marker_file(self, tmp_path):
        """Test license acceptance via marker file."""
        from specify_cli.security.tools.installers import CodeQLInstaller

        config = ToolConfig(cache_dir=tmp_path)
        installer = CodeQLInstaller(config)

        # Create marker file
        codeql_dir = tmp_path / "codeql"
        codeql_dir.mkdir()
        (codeql_dir / ".license_accepted").write_text("accepted")

        assert installer._check_license_acceptance() is True

    def test_license_not_accepted(self, tmp_path, monkeypatch):
        """Test installation fails without license acceptance."""
        from specify_cli.security.tools.installers import CodeQLInstaller

        monkeypatch.delenv("CODEQL_LICENSE_ACCEPTED", raising=False)

        config = ToolConfig(cache_dir=tmp_path)
        installer = CodeQLInstaller(config)

        result = installer.install()

        assert result.status == ToolStatus.ERROR
        assert "license acceptance" in result.error.lower()

    def test_get_download_url_linux(self, tmp_path):
        """Test download URL for Linux."""
        from specify_cli.security.tools.installers import CodeQLInstaller

        config = ToolConfig(cache_dir=tmp_path)
        installer = CodeQLInstaller(config)

        with patch("platform.system", return_value="Linux"):
            url = installer._get_download_url()

        assert "linux64" in url

    def test_get_download_url_macos(self, tmp_path):
        """Test download URL for macOS."""
        from specify_cli.security.tools.installers import CodeQLInstaller

        config = ToolConfig(cache_dir=tmp_path)
        installer = CodeQLInstaller(config)

        with patch("platform.system", return_value="Darwin"):
            url = installer._get_download_url()

        assert "osx64" in url

    def test_get_download_url_windows(self, tmp_path):
        """Test download URL for Windows."""
        from specify_cli.security.tools.installers import CodeQLInstaller

        config = ToolConfig(cache_dir=tmp_path)
        installer = CodeQLInstaller(config)

        with patch("platform.system", return_value="Windows"):
            url = installer._get_download_url()

        assert "win64" in url
