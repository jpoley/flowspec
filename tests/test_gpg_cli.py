"""Tests for the ``flowspec gpg`` Typer subcommands.

These tests focus on behavior that is easy to regress — notably that
``gpg setup`` reads the keyring exactly once per invocation. The underlying
signing primitives are mocked; see ``tests/test_signing.py`` for their
contracts.
"""

from unittest.mock import patch

from typer.testing import CliRunner

from flowspec_cli.gpg_cli import gpg_app

runner = CliRunner()


class TestSetupCommandKeyringReads:
    """Pin the "read keyring state once" contract in ``setup_command``.

    ``key_exists()`` calls ``get_key_fingerprint()`` internally, so mixing
    both in the same code path silently doubles keyring reads and can expose
    a transient-read inconsistency (see PR #1243 review feedback).
    """

    @patch("flowspec_cli.gpg_cli.configure_git_signing")
    @patch("flowspec_cli.gpg_cli.delete_agent_key")
    @patch("flowspec_cli.gpg_cli.generate_agent_key")
    @patch("flowspec_cli.gpg_cli.key_exists")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_reads_fingerprint_once_when_key_exists(
        self,
        mock_get_fp,
        mock_key_exists,
        mock_generate,
        mock_delete,
        mock_configure,
    ):
        """Existing-key path should call get_key_fingerprint exactly once."""
        mock_get_fp.return_value = "A" * 40

        result = runner.invoke(gpg_app, ["setup"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1, (
            f"expected 1 get_key_fingerprint call, got {mock_get_fp.call_count}"
        )
        # key_exists is redundant with get_key_fingerprint and must not be
        # used on this path.
        assert mock_key_exists.call_count == 0
        # No regeneration should happen.
        mock_generate.assert_not_called()
        mock_delete.assert_not_called()

    @patch("flowspec_cli.gpg_cli.configure_git_signing")
    @patch("flowspec_cli.gpg_cli.delete_agent_key")
    @patch("flowspec_cli.gpg_cli.generate_agent_key")
    @patch("flowspec_cli.gpg_cli.key_exists")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_reads_fingerprint_once_when_no_key(
        self,
        mock_get_fp,
        mock_key_exists,
        mock_generate,
        mock_delete,
        mock_configure,
    ):
        """No-key path should also call get_key_fingerprint exactly once."""
        mock_get_fp.return_value = None
        mock_generate.return_value = "B" * 40

        result = runner.invoke(gpg_app, ["setup"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1
        assert mock_key_exists.call_count == 0
        mock_generate.assert_called_once()
        mock_delete.assert_not_called()

    @patch("flowspec_cli.gpg_cli.configure_git_signing")
    @patch("flowspec_cli.gpg_cli.delete_agent_key")
    @patch("flowspec_cli.gpg_cli.generate_agent_key")
    @patch("flowspec_cli.gpg_cli.key_exists")
    @patch("flowspec_cli.gpg_cli.get_key_fingerprint")
    def test_force_regenerates_with_one_fingerprint_read(
        self,
        mock_get_fp,
        mock_key_exists,
        mock_generate,
        mock_delete,
        mock_configure,
    ):
        """--force path deletes + regenerates with exactly one fingerprint read."""
        mock_get_fp.return_value = "C" * 40
        mock_generate.return_value = "D" * 40

        result = runner.invoke(gpg_app, ["setup", "--force"])

        assert result.exit_code == 0, result.output
        assert mock_get_fp.call_count == 1
        assert mock_key_exists.call_count == 0
        mock_delete.assert_called_once()
        mock_generate.assert_called_once()
