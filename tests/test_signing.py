"""Tests for GPG signing module.

This module tests the GPG key generation, git configuration, and key management
functionality for agent commit signing.
"""

from __future__ import annotations

import subprocess
from unittest.mock import patch

import pytest

from flowspec_cli.signing import (
    GPGConfigurationError,
    GPGError,
    GPGKeyGenerationError,
    configure_git_signing,
    delete_agent_key,
    generate_agent_key,
    get_key_fingerprint,
    get_key_info,
    is_git_signing_enabled,
    key_exists,
)


@pytest.fixture
def mock_keyring():
    """Mock the keyring module."""
    with patch("flowspec_cli.signing.keyring") as mock:
        yield mock


@pytest.fixture
def mock_gpg_commands():
    """Mock GPG command execution."""
    with patch("flowspec_cli.signing._run_gpg_command") as mock:
        yield mock


@pytest.fixture
def mock_git_commands():
    """Mock git command execution."""
    with patch("flowspec_cli.signing._run_git_command") as mock:
        yield mock


class TestKeyGeneration:
    """Tests for GPG key generation."""

    def test_generate_agent_key_success(self, mock_keyring, mock_gpg_commands):
        """Test successful key generation."""
        mock_keyring.get_password.return_value = None  # no existing key
        # Mock GPG generate-key command
        mock_gpg_commands.side_effect = [
            ("", "", 0),  # generate-key success
            ("fpr:::::::::ABCD1234ABCD1234ABCD1234ABCD1234ABCD1234:\n", "", 0),  # list-keys
        ]

        fingerprint = generate_agent_key()

        assert fingerprint == "ABCD1234ABCD1234ABCD1234ABCD1234ABCD1234"
        mock_keyring.set_password.assert_called_once_with(
            "flowspec-agent-gpg",
            "agent-key-fingerprint",
            "ABCD1234ABCD1234ABCD1234ABCD1234ABCD1234",
        )

    def test_generate_agent_key_already_exists(self, mock_keyring, mock_gpg_commands):
        """Test key generation when key already exists."""
        # Mock existing key
        mock_keyring.get_password.return_value = "EXISTING1234"

        fingerprint = generate_agent_key()

        # Should return existing fingerprint without generating new key
        assert fingerprint == "EXISTING1234"
        mock_gpg_commands.assert_not_called()

    def test_generate_agent_key_generation_fails(self, mock_keyring, mock_gpg_commands):
        """Test key generation failure."""
        mock_keyring.get_password.return_value = None
        mock_gpg_commands.return_value = ("", "GPG error", 1)

        with pytest.raises(GPGKeyGenerationError, match="Failed to generate GPG key"):
            generate_agent_key()

    def test_generate_agent_key_fingerprint_extraction_fails(
        self, mock_keyring, mock_gpg_commands
    ):
        """Test failure when fingerprint cannot be extracted."""
        mock_keyring.get_password.return_value = None
        mock_gpg_commands.side_effect = [
            ("", "", 0),  # generate-key success
            ("invalid output\n", "", 0),  # list-keys with no fingerprint
        ]

        with pytest.raises(
            GPGKeyGenerationError, match="Failed to extract fingerprint"
        ):
            generate_agent_key()

    def test_generate_agent_key_keyring_storage_fails(
        self, mock_keyring, mock_gpg_commands
    ):
        """Test failure when storing fingerprint in keyring fails."""
        mock_keyring.get_password.return_value = None
        mock_keyring.set_password.side_effect = Exception("Keyring error")
        mock_gpg_commands.side_effect = [
            ("", "", 0),  # generate-key success
            ("fpr:::::::::ABCD1234:\n", "", 0),  # list-keys
        ]

        with pytest.raises(
            GPGKeyGenerationError, match="Failed to store fingerprint in keyring"
        ):
            generate_agent_key()


class TestGitConfiguration:
    """Tests for git signing configuration."""

    def test_configure_git_signing_success(
        self, mock_keyring, mock_git_commands, mock_gpg_commands, tmp_path
    ):
        """Test successful git configuration."""
        mock_keyring.get_password.return_value = "ABCD1234"
        mock_gpg_commands.return_value = ("", "", 0)  # secret key present
        mock_git_commands.side_effect = [
            ("", "", 0),  # rev-parse (check if git repo)
            ("", "", 0),  # config user.signingkey
            ("", "", 0),  # config commit.gpgsign
        ]

        configure_git_signing(project_root=tmp_path)

        # Verify git commands were called correctly
        assert mock_git_commands.call_count == 3
        assert mock_git_commands.call_args_list[1][0][0] == [
            "config",
            "--local",
            "user.signingkey",
            "ABCD1234",
        ]
        assert mock_git_commands.call_args_list[2][0][0] == [
            "config",
            "--local",
            "commit.gpgsign",
            "true",
        ]

    def test_configure_git_signing_no_key(self, mock_keyring, tmp_path):
        """Test git configuration without existing key."""
        mock_keyring.get_password.return_value = None

        with pytest.raises(GPGError, match="No agent GPG key found"):
            configure_git_signing(project_root=tmp_path)

    def test_configure_git_signing_not_git_repo(
        self, mock_keyring, mock_git_commands, mock_gpg_commands, tmp_path
    ):
        """Test git configuration in non-git directory."""
        mock_keyring.get_password.return_value = "ABCD1234"
        mock_gpg_commands.return_value = ("", "", 0)  # secret key present
        mock_git_commands.return_value = ("", "not a git repository", 1)

        with pytest.raises(GPGConfigurationError, match="Not a git repository"):
            configure_git_signing(project_root=tmp_path)

    def test_configure_git_signing_key_config_fails(
        self, mock_keyring, mock_git_commands, mock_gpg_commands, tmp_path
    ):
        """Test git configuration when setting signingkey fails."""
        mock_keyring.get_password.return_value = "ABCD1234"
        mock_gpg_commands.return_value = ("", "", 0)  # secret key present
        mock_git_commands.side_effect = [
            ("", "", 0),  # rev-parse success
            ("", "config error", 1),  # config user.signingkey fails
        ]

        with pytest.raises(
            GPGConfigurationError, match="Failed to set user.signingkey"
        ):
            configure_git_signing(project_root=tmp_path)

    def test_configure_git_signing_gpgsign_config_fails(
        self, mock_keyring, mock_git_commands, mock_gpg_commands, tmp_path
    ):
        """Test git configuration when setting commit.gpgsign fails."""
        mock_keyring.get_password.return_value = "ABCD1234"
        mock_gpg_commands.return_value = ("", "", 0)  # secret key present
        mock_git_commands.side_effect = [
            ("", "", 0),  # rev-parse success
            ("", "", 0),  # config user.signingkey success
            ("", "config error", 1),  # config commit.gpgsign fails
        ]

        with pytest.raises(
            GPGConfigurationError, match="Failed to set commit.gpgsign"
        ):
            configure_git_signing(project_root=tmp_path)


class TestKeyRetrieval:
    """Tests for key fingerprint retrieval."""

    def test_get_key_fingerprint_success(self, mock_keyring):
        """Test successful fingerprint retrieval."""
        mock_keyring.get_password.return_value = "ABCD1234"

        fingerprint = get_key_fingerprint()

        assert fingerprint == "ABCD1234"
        mock_keyring.get_password.assert_called_once_with(
            "flowspec-agent-gpg", "agent-key-fingerprint"
        )

    def test_get_key_fingerprint_not_found(self, mock_keyring):
        """Test fingerprint retrieval when not found."""
        mock_keyring.get_password.return_value = None

        fingerprint = get_key_fingerprint()

        assert fingerprint is None

    def test_get_key_fingerprint_keyring_error(self, mock_keyring):
        """Test fingerprint retrieval when keyring raises error."""
        mock_keyring.get_password.side_effect = Exception("Keyring error")

        fingerprint = get_key_fingerprint()

        assert fingerprint is None

    def test_key_exists_true(self, mock_keyring):
        """Test key_exists when key is present."""
        mock_keyring.get_password.return_value = "ABCD1234"

        assert key_exists() is True

    def test_key_exists_false(self, mock_keyring):
        """Test key_exists when key is not present."""
        mock_keyring.get_password.return_value = None

        assert key_exists() is False


class TestKeyInfo:
    """Tests for detailed key information retrieval."""

    def test_get_key_info_success(self, mock_keyring, mock_gpg_commands):
        """Test successful key info retrieval."""
        mock_keyring.get_password.return_value = "ABCD1234"
        gpg_output = """pub:u:4096:1:KEYID:1234567890:0
uid:u::::1234567890::HASH::Flowspec Agent <agent@flowspec.local>
"""
        mock_gpg_commands.return_value = (gpg_output, "", 0)

        info = get_key_info()

        assert info is not None
        assert info["fingerprint"] == "ABCD1234"
        assert info["created"] == "1234567890"
        assert info["uid"] == "Flowspec Agent <agent@flowspec.local>"

    def test_get_key_info_no_key(self, mock_keyring):
        """Test key info retrieval when no key exists."""
        mock_keyring.get_password.return_value = None

        info = get_key_info()

        assert info is None

    def test_get_key_info_gpg_fails(self, mock_keyring, mock_gpg_commands):
        """Test key info retrieval when GPG command fails."""
        mock_keyring.get_password.return_value = "ABCD1234"
        mock_gpg_commands.return_value = ("", "error", 1)

        info = get_key_info()

        assert info is None


class TestGitSigningStatus:
    """Tests for checking git signing status."""

    def test_is_git_signing_enabled_true(self, mock_git_commands, tmp_path):
        """Test when git signing is enabled."""
        mock_git_commands.side_effect = [
            ("", "", 0),  # rev-parse success
            ("true\n", "", 0),  # commit.gpgsign is true
            ("ABCD1234\n", "", 0),  # user.signingkey is set
        ]

        assert is_git_signing_enabled(project_root=tmp_path) is True

    def test_is_git_signing_enabled_false_not_repo(self, mock_git_commands, tmp_path):
        """Test when not a git repository."""
        mock_git_commands.return_value = ("", "not a repo", 1)

        assert is_git_signing_enabled(project_root=tmp_path) is False

    def test_is_git_signing_enabled_false_gpgsign_off(
        self, mock_git_commands, tmp_path
    ):
        """Test when commit.gpgsign is not true."""
        mock_git_commands.side_effect = [
            ("", "", 0),  # rev-parse success
            ("false\n", "", 0),  # commit.gpgsign is false
        ]

        assert is_git_signing_enabled(project_root=tmp_path) is False

    def test_is_git_signing_enabled_false_no_signingkey(
        self, mock_git_commands, tmp_path
    ):
        """Test when user.signingkey is not set."""
        mock_git_commands.side_effect = [
            ("", "", 0),  # rev-parse success
            ("true\n", "", 0),  # commit.gpgsign is true
            ("", "", 1),  # user.signingkey not set
        ]

        assert is_git_signing_enabled(project_root=tmp_path) is False


class TestKeyDeletion:
    """Tests for key deletion (rotation)."""

    def test_delete_agent_key_success(self, mock_keyring, mock_gpg_commands):
        """Test successful key deletion."""
        mock_keyring.get_password.return_value = "ABCD1234"
        mock_gpg_commands.return_value = ("", "", 0)

        delete_agent_key()

        mock_gpg_commands.assert_called_once()
        assert "--delete-secret-and-public-key" in mock_gpg_commands.call_args[0][0]
        mock_keyring.delete_password.assert_called_once_with(
            "flowspec-agent-gpg", "agent-key-fingerprint"
        )

    def test_delete_agent_key_no_key(self, mock_keyring, mock_gpg_commands):
        """Test key deletion when no key exists."""
        mock_keyring.get_password.return_value = None

        delete_agent_key()

        # Should return early without calling GPG
        mock_gpg_commands.assert_not_called()
        mock_keyring.delete_password.assert_not_called()

    def test_delete_agent_key_gpg_fails(self, mock_keyring, mock_gpg_commands):
        """Test key deletion when GPG command fails."""
        mock_keyring.get_password.return_value = "ABCD1234"
        mock_gpg_commands.return_value = ("", "delete error", 1)

        with pytest.raises(GPGError, match="Failed to delete GPG key"):
            delete_agent_key()

    def test_delete_agent_key_keyring_fails(self, mock_keyring, mock_gpg_commands):
        """Test key deletion when keyring deletion fails."""
        mock_keyring.get_password.return_value = "ABCD1234"
        mock_gpg_commands.return_value = ("", "", 0)
        mock_keyring.delete_password.side_effect = Exception("Keyring error")

        with pytest.raises(GPGError, match="Failed to delete fingerprint from keyring"):
            delete_agent_key()


class TestCommandExecution:
    """Tests for command execution helpers."""

    def test_run_gpg_command_timeout(self, mock_keyring):
        """Test GPG command timeout handling."""
        with patch("flowspec_cli.signing.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("gpg", 30)

            with pytest.raises(GPGError, match="GPG command timed out"):
                from flowspec_cli.signing import _run_gpg_command

                _run_gpg_command(["--version"])

    def test_run_gpg_command_not_found(self, mock_keyring):
        """Test GPG command when GPG is not installed."""
        with patch("flowspec_cli.signing.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            with pytest.raises(GPGError, match="GPG not found"):
                from flowspec_cli.signing import _run_gpg_command

                _run_gpg_command(["--version"])

    def test_run_git_command_timeout(self, mock_keyring):
        """Test git command timeout handling."""
        with patch("flowspec_cli.signing.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("git", 10)

            with pytest.raises(GPGConfigurationError, match="Git command timed out"):
                from flowspec_cli.signing import _run_git_command

                _run_git_command(["status"])

    def test_run_git_command_not_found(self, mock_keyring):
        """Test git command when git is not installed."""
        with patch("flowspec_cli.signing.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()

            with pytest.raises(GPGConfigurationError, match="Git not found"):
                from flowspec_cli.signing import _run_git_command

                _run_git_command(["status"])
