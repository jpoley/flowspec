"""GPG signing module for Flowspec agents.

This module provides GPG key generation and management for agent commit signing.
Agents can generate their own GPG keys, configure git to use them, and include
the key fingerprint in telemetry output.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

import keyring

# Constants
KEYRING_SERVICE = "flowspec-agent-gpg"
KEYRING_USERNAME = "agent-key-fingerprint"
GPG_KEY_NAME = "Flowspec Agent"
GPG_KEY_EMAIL = "agent@flowspec.local"


class GPGError(Exception):
    """Base exception for GPG-related errors."""

    pass


class GPGKeyGenerationError(GPGError):
    """Raised when GPG key generation fails."""

    pass


class GPGConfigurationError(GPGError):
    """Raised when git configuration for GPG signing fails."""

    pass


def _run_gpg_command(
    args: list[str], input_data: Optional[str] = None
) -> tuple[str, str, int]:
    """Run a GPG command and return stdout, stderr, and return code.

    Args:
        args: Command arguments (excluding 'gpg' itself)
        input_data: Optional input to pass via stdin

    Returns:
        Tuple of (stdout, stderr, returncode)
    """
    cmd = ["gpg"] + args
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            timeout=30,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        raise GPGError("GPG command timed out")
    except FileNotFoundError:
        raise GPGError("GPG not found. Please install gnupg.")


def _run_git_command(
    args: list[str], cwd: Optional[Path] = None
) -> tuple[str, str, int]:
    """Run a git command and return stdout, stderr, and return code.

    Args:
        args: Command arguments (excluding 'git' itself)
        cwd: Optional working directory

    Returns:
        Tuple of (stdout, stderr, returncode)
    """
    cmd = ["git"] + args
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=10,
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        raise GPGConfigurationError("Git command timed out")
    except FileNotFoundError:
        raise GPGConfigurationError("Git not found. Please install git.")


def generate_agent_key() -> str:
    """Generate a new GPG key for the Flowspec agent.

    Creates an RSA 4096-bit key with no expiration for:
    - Name: "Flowspec Agent"
    - Email: "agent@flowspec.local"

    The key fingerprint is stored in the system keyring for later retrieval.

    Returns:
        The GPG key fingerprint (40-character hex string)

    Raises:
        GPGKeyGenerationError: If key generation fails
    """
    # Check if key already exists
    existing = get_key_fingerprint()
    if existing:
        return existing

    # Generate key using batch mode
    key_params = f"""
%no-protection
Key-Type: RSA
Key-Length: 4096
Name-Real: {GPG_KEY_NAME}
Name-Email: {GPG_KEY_EMAIL}
Expire-Date: 0
%commit
""".strip()

    stdout, stderr, returncode = _run_gpg_command(
        ["--batch", "--status-fd", "1", "--generate-key"], input_data=key_params
    )

    if returncode != 0:
        raise GPGKeyGenerationError(f"Failed to generate GPG key: {stderr}")

    # Extract fingerprint from the key-creation status output.
    # Expected format: [GNUPG:] KEY_CREATED <type> <fingerprint>
    fingerprint = None
    for line in stdout.splitlines():
        if line.startswith("[GNUPG:] KEY_CREATED "):
            parts = line.split()
            if len(parts) >= 4:
                fingerprint = parts[3]
                break

    if not fingerprint:
        raise GPGKeyGenerationError("Failed to extract fingerprint from generated key")

    # Store fingerprint in keyring
    try:
        keyring.set_password(KEYRING_SERVICE, KEYRING_USERNAME, fingerprint)
    except Exception as e:
        raise GPGKeyGenerationError(f"Failed to store fingerprint in keyring: {e}")

    return fingerprint


def configure_git_signing(project_root: Optional[Path] = None) -> None:
    """Configure git to sign commits with the agent's GPG key.

    Sets the following local git config options:
    - user.signingkey: The agent's GPG key fingerprint
    - commit.gpgsign: true (enable automatic commit signing)

    Args:
        project_root: Project directory for local git config (default: current directory)

    Raises:
        GPGConfigurationError: If git configuration fails
        GPGError: If no agent key exists (call generate_agent_key() first)
    """
    fingerprint = get_key_fingerprint()
    if not fingerprint:
        raise GPGError("No agent GPG key found. Run generate_agent_key() first.")

    # Verify the exact secret key fingerprint is still present in the GPG keyring
    stdout, _, returncode = _run_gpg_command(
        ["--list-secret-keys", "--with-colons", fingerprint]
    )
    fingerprint_found = any(
        line.startswith("fpr:") and line.split(":")[9] == fingerprint
        for line in stdout.splitlines()
    )
    if returncode != 0 or not fingerprint_found:
        raise GPGError(
            "Agent GPG secret key not found in keyring. Regenerate with generate_agent_key()."
        )

    cwd = project_root if project_root else Path.cwd()

    # Check if we're in a git repository
    _, _, returncode = _run_git_command(["rev-parse", "--git-dir"], cwd=cwd)
    if returncode != 0:
        raise GPGConfigurationError(f"Not a git repository: {cwd}")

    # Set signing key
    _, stderr, returncode = _run_git_command(
        ["config", "--local", "user.signingkey", fingerprint], cwd=cwd
    )
    if returncode != 0:
        raise GPGConfigurationError(f"Failed to set user.signingkey: {stderr}")

    # Enable commit signing
    _, stderr, returncode = _run_git_command(
        ["config", "--local", "commit.gpgsign", "true"], cwd=cwd
    )
    if returncode != 0:
        raise GPGConfigurationError(f"Failed to set commit.gpgsign: {stderr}")


def get_key_fingerprint() -> Optional[str]:
    """Retrieve the stored GPG key fingerprint from keyring.

    Returns:
        The 40-character hex fingerprint, or None if not found
    """
    try:
        fingerprint = keyring.get_password(KEYRING_SERVICE, KEYRING_USERNAME)
        return fingerprint
    except Exception:
        return None


def key_exists() -> bool:
    """Check if an agent GPG key already exists.

    Returns:
        True if a key fingerprint is stored in the keyring, False otherwise
    """
    return get_key_fingerprint() is not None


def get_key_info() -> Optional[dict[str, str]]:
    """Get detailed information about the agent's GPG key.

    Returns:
        Dictionary with key details (fingerprint, uid, creation date), or None if no key exists
    """
    fingerprint = get_key_fingerprint()
    if not fingerprint:
        return None

    stdout, _, returncode = _run_gpg_command(
        ["--list-keys", "--with-colons", fingerprint]
    )

    if returncode != 0:
        return None

    # Parse key information from colon-separated output
    key_info = {"fingerprint": fingerprint}

    for line in stdout.splitlines():
        parts = line.split(":")
        if line.startswith("pub:"):
            # pub:u:4096:1:KEYID:CREATION:EXPIRATION
            if len(parts) >= 6:
                key_info["created"] = parts[5]
        elif line.startswith("uid:"):
            # uid:u::::CREATION::UID
            if len(parts) >= 10:
                key_info["uid"] = parts[9]

    return key_info


def is_git_signing_enabled(project_root: Optional[Path] = None) -> bool:
    """Check if GPG commit signing is enabled in the git repository.

    Args:
        project_root: Project directory to check (default: current directory)

    Returns:
        True if commit.gpgsign is true and user.signingkey is set, False otherwise
    """
    cwd = project_root if project_root else Path.cwd()

    # Check if we're in a git repository
    _, _, returncode = _run_git_command(["rev-parse", "--git-dir"], cwd=cwd)
    if returncode != 0:
        return False

    # Check commit.gpgsign
    stdout, _, returncode = _run_git_command(
        ["config", "--local", "commit.gpgsign"], cwd=cwd
    )
    if returncode != 0 or stdout.strip().lower() != "true":
        return False

    # Check user.signingkey
    stdout, _, returncode = _run_git_command(
        ["config", "--local", "user.signingkey"], cwd=cwd
    )
    if returncode != 0 or not stdout.strip():
        return False

    return True


def delete_agent_key() -> None:
    """Delete the agent's GPG key from the keyring and GPG keychain.

    This is useful for key rotation. After deletion, call generate_agent_key()
    to create a new key.

    Raises:
        GPGError: If key deletion fails
    """
    fingerprint = get_key_fingerprint()
    if not fingerprint:
        return  # No key to delete

    # Delete from GPG keychain
    _, stderr, returncode = _run_gpg_command(
        ["--batch", "--yes", "--delete-secret-and-public-key", fingerprint]
    )

    if returncode != 0:
        raise GPGError(f"Failed to delete GPG key: {stderr}")

    # Delete from keyring
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_USERNAME)
    except Exception as e:
        raise GPGError(f"Failed to delete fingerprint from keyring: {e}")


__all__ = [
    "generate_agent_key",
    "configure_git_signing",
    "get_key_fingerprint",
    "key_exists",
    "get_key_info",
    "is_git_signing_enabled",
    "delete_agent_key",
    "GPGError",
    "GPGKeyGenerationError",
    "GPGConfigurationError",
]
