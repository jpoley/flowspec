"""Tests for the ``flowspec gpg`` Typer subcommands.

Focus: pin the "read keyring state exactly once per invocation" contract
for all three commands (``setup``, ``status``, ``rotate``). The underlying
signing primitives are mocked; see ``tests/test_signing.py`` for their
contracts.

Background (see PR #1244 Copilot feedback):
    ``key_exists()`` is implemented in terms of ``get_key_fingerprint()``,
    and ``get_key_info()`` used to call ``get_key_fingerprint()`` as well.
    Chaining any of these issues multiple keyring reads and, under
    transient keyring failures, can produce inconsistent output (e.g.
    "Configured" with fingerprint "unknown").
"""

import flowspec_cli.gpg_cli as gpg_cli_module
from unittest.mock import patch

from typer.testing import CliRunner

from flowspec_cli.gpg_cli import gpg_app

runner = CliRunner()


class TestModuleSurface:
    """Static guardrails for the ``gpg_cli`` module surface."""

    def test_key_exists_is_not_imported(self):
        """``key_exists`` must not be used in ``gpg_cli`` — it re-reads the keyring.

        Callers should branch on ``get_key_fingerprint()`` directly so the
        fingerprint is cached in a local and keyring access happens once.
        """
        assert not hasattr(gpg_cli_module, "key_exists"), (
            "gpg_cli must not import key_exists; use get_key_fingerprint once "
            "and branch on the cached value"
        )


class TestSetupCommandKeyringReads:
    """``gpg setup`` must read ``get_key_fingerprint`` exactly once."""

    @patch("flowspec_cli.gpg_cli.configure_git_signing")
    @patch("flowspec_cli.gpg_cli.delete_agent_key")
    @patch("flowspec_cli.gpg_cli.generate_agent_key")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_reads_fingerprint_once_when_key_exists(
        self, mock_get_fp, mock_generate, mock_delete, mock_configure
    ):
        """Existing-key path: one keyring read, no regeneration, fingerprint forwarded."""
        fp = "A" * 40
        mock_get_fp.return_value = fp

        result = runner.invoke(gpg_app, ["setup"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1, (
            f"expected 1 get_key_fingerprint call, got {mock_get_fp.call_count}"
        )
        mock_generate.assert_not_called()
        mock_delete.assert_not_called()
        mock_configure.assert_called_once_with(
            project_root=mock_configure.call_args[1]["project_root"], fingerprint=fp
        )

    @patch("flowspec_cli.gpg_cli.configure_git_signing")
    @patch("flowspec_cli.gpg_cli.delete_agent_key")
    @patch("flowspec_cli.gpg_cli.generate_agent_key")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_reads_fingerprint_once_when_no_key(
        self, mock_get_fp, mock_generate, mock_delete, mock_configure
    ):
        """No-key path: one keyring read, generates key, fingerprint forwarded."""
        new_fp = "B" * 40
        mock_get_fp.return_value = None
        mock_generate.return_value = new_fp

        result = runner.invoke(gpg_app, ["setup"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1
        mock_generate.assert_called_once()
        mock_delete.assert_not_called()
        mock_configure.assert_called_once_with(
            project_root=mock_configure.call_args[1]["project_root"], fingerprint=new_fp
        )

    @patch("flowspec_cli.gpg_cli.configure_git_signing")
    @patch("flowspec_cli.gpg_cli.delete_agent_key")
    @patch("flowspec_cli.gpg_cli.generate_agent_key")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_force_regenerates_with_one_fingerprint_read(
        self, mock_get_fp, mock_generate, mock_delete, _mock_configure
    ):
        """--force: one keyring read, delete + regenerate."""
        mock_get_fp.return_value = "C" * 40
        mock_generate.return_value = "D" * 40

        result = runner.invoke(gpg_app, ["setup", "--force"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1
        mock_delete.assert_called_once()
        mock_generate.assert_called_once()


class TestStatusCommandKeyringReads:
    """``gpg status`` must read ``get_key_fingerprint`` exactly once."""

    @patch("flowspec_cli.gpg_cli.is_git_signing_enabled")
    @patch("flowspec_cli.gpg_cli.get_key_info")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_reads_fingerprint_once_when_configured(
        self, mock_get_fp, mock_get_info, mock_git_enabled
    ):
        """Configured path: one keyring read; get_key_info receives cached fp."""
        fingerprint = "E" * 40
        mock_get_fp.return_value = fingerprint
        mock_get_info.return_value = {"fingerprint": fingerprint}
        mock_git_enabled.return_value = True

        result = runner.invoke(gpg_app, ["status"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1, (
            f"expected 1 get_key_fingerprint call, got {mock_get_fp.call_count}"
        )
        # The cached fingerprint must be forwarded to avoid another keyring
        # read inside ``get_key_info``.
        mock_get_info.assert_called_once_with(fingerprint=fingerprint)

    @patch("flowspec_cli.gpg_cli.is_git_signing_enabled")
    @patch("flowspec_cli.gpg_cli.get_key_info")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_reads_fingerprint_once_when_not_configured(
        self, mock_get_fp, mock_get_info, mock_git_enabled
    ):
        """Not-configured path: one keyring read, no get_key_info call."""
        mock_get_fp.return_value = None

        result = runner.invoke(gpg_app, ["status"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1
        mock_get_info.assert_not_called()
        # ``is_git_signing_enabled`` is only inspected on the configured path.
        mock_git_enabled.assert_not_called()


class TestRotateCommandKeyringReads:
    """``gpg rotate`` must read ``get_key_fingerprint`` exactly once."""

    @patch("flowspec_cli.gpg_cli.configure_git_signing")
    @patch("flowspec_cli.gpg_cli.generate_agent_key")
    @patch("flowspec_cli.gpg_cli.delete_agent_key")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_reads_fingerprint_once_when_no_key(
        self, mock_get_fp, mock_delete, mock_generate, _mock_configure
    ):
        """No-key path: one keyring read, no rotation work."""
        mock_get_fp.return_value = None

        result = runner.invoke(gpg_app, ["rotate"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1
        mock_delete.assert_not_called()
        mock_generate.assert_not_called()

    @patch("flowspec_cli.gpg_cli.configure_git_signing")
    @patch("flowspec_cli.gpg_cli.generate_agent_key")
    @patch("flowspec_cli.gpg_cli.delete_agent_key")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_reads_fingerprint_once_when_rotating(
        self, mock_get_fp, mock_delete, mock_generate, mock_configure
    ):
        """Existing-key path (--yes): one keyring read; fingerprints forwarded."""
        old_fp = "F" * 40
        new_fp = "G" * 40
        mock_get_fp.return_value = old_fp
        mock_generate.return_value = new_fp

        result = runner.invoke(gpg_app, ["rotate", "--yes"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1
        # Cached old fingerprint forwarded to delete_agent_key.
        mock_delete.assert_called_once_with(cached_fingerprint=old_fp)
        mock_generate.assert_called_once()
        # New fingerprint forwarded to configure_git_signing.
        mock_configure.assert_called_once_with(
            project_root=mock_configure.call_args[1]["project_root"], fingerprint=new_fp
        )
