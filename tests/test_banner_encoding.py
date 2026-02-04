"""Tests for banner encoding detection and fallback.

These tests verify the Windows Unicode encoding fix for issue #1186.
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

from flowspec_cli import BANNER, BANNER_ASCII, _can_encode_unicode


class TestCanEncodeUnicode:
    """Tests for _can_encode_unicode() function."""

    def test_returns_false_when_stdout_is_none(self) -> None:
        """Test that function returns False when sys.stdout is None."""
        with patch.object(sys, "stdout", None):
            assert _can_encode_unicode() is False

    def test_returns_false_when_encoding_is_none(self) -> None:
        """Test that function returns False when stdout.encoding is None."""
        mock_stdout = MagicMock()
        mock_stdout.encoding = None
        with patch.object(sys, "stdout", mock_stdout):
            assert _can_encode_unicode() is False

    def test_returns_false_when_encoding_is_empty_string(self) -> None:
        """Test that function returns False when stdout.encoding is empty."""
        mock_stdout = MagicMock()
        mock_stdout.encoding = ""
        with patch.object(sys, "stdout", mock_stdout):
            assert _can_encode_unicode() is False

    def test_returns_true_for_utf8_encoding(self) -> None:
        """Test that function returns True for UTF-8 encoding."""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "utf-8"
        with patch.object(sys, "stdout", mock_stdout):
            assert _can_encode_unicode() is True

    def test_returns_false_for_cp1252_encoding(self) -> None:
        """Test that function returns False for cp1252 (Windows legacy encoding)."""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "cp1252"
        with patch.object(sys, "stdout", mock_stdout):
            assert _can_encode_unicode() is False

    def test_returns_false_for_ascii_encoding(self) -> None:
        """Test that function returns False for ASCII encoding."""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "ascii"
        with patch.object(sys, "stdout", mock_stdout):
            assert _can_encode_unicode() is False

    def test_returns_false_when_encoding_attribute_missing(self) -> None:
        """Test that function returns False when encoding attribute is missing."""
        mock_stdout = MagicMock(spec=[])  # No encoding attribute
        with patch.object(sys, "stdout", mock_stdout):
            assert _can_encode_unicode() is False

    def test_handles_lookup_error_for_invalid_encoding(self) -> None:
        """Test that function handles LookupError for invalid encoding names."""
        mock_stdout = MagicMock()
        mock_stdout.encoding = "invalid-encoding-name-xyz"
        with patch.object(sys, "stdout", mock_stdout):
            # Should return False rather than raising LookupError
            assert _can_encode_unicode() is False

    def test_handles_type_error_for_non_string_encoding(self) -> None:
        """Test that function handles TypeError for non-string encoding values."""
        mock_stdout = MagicMock()
        mock_stdout.encoding = 12345  # Non-string value
        with patch.object(sys, "stdout", mock_stdout):
            # Should return False rather than raising TypeError
            assert _can_encode_unicode() is False


class TestShowBanner:
    """Tests for show_banner() function."""

    def test_uses_ascii_banner_when_unicode_not_supported(self) -> None:
        """Test that ASCII banner is used when _can_encode_unicode() returns False."""
        from flowspec_cli import show_banner

        with patch("flowspec_cli._can_encode_unicode", return_value=False):
            with patch("flowspec_cli.console") as mock_console:
                show_banner()
                # Verify console.print was called
                assert mock_console.print.called
                # Get the first call's argument (the Align object containing banner)
                first_call = mock_console.print.call_args_list[0]
                banner_align = first_call[0][0]
                # Extract the Text object from Align
                banner_text = str(banner_align.renderable)
                # ASCII banner should NOT contain Unicode box-drawing characters
                assert "█" not in banner_text
                assert "╔" not in banner_text
                assert "═" not in banner_text

    def test_uses_unicode_banner_when_supported(self) -> None:
        """Test that Unicode banner is used when _can_encode_unicode() returns True."""
        from flowspec_cli import show_banner

        with patch("flowspec_cli._can_encode_unicode", return_value=True):
            with patch("flowspec_cli.console") as mock_console:
                show_banner()
                # Verify console.print was called
                assert mock_console.print.called
                # Get the first call's argument (the Align object containing banner)
                first_call = mock_console.print.call_args_list[0]
                banner_align = first_call[0][0]
                # Extract the Text object from Align
                banner_text = str(banner_align.renderable)
                # Unicode banner SHOULD contain box-drawing characters
                assert "█" in banner_text or "╔" in banner_text or "═" in banner_text


class TestBannerConstants:
    """Tests for banner constant definitions."""

    def test_banner_ascii_is_defined(self) -> None:
        """Test that BANNER_ASCII constant exists and is non-empty."""
        assert BANNER_ASCII is not None
        assert len(BANNER_ASCII) > 0

    def test_banner_ascii_contains_only_ascii(self) -> None:
        """Test that BANNER_ASCII contains only ASCII characters."""
        for char in BANNER_ASCII:
            assert ord(char) < 128, (
                f"Non-ASCII character found: {char!r} (ord={ord(char)})"
            )

    def test_banner_unicode_contains_box_drawing(self) -> None:
        """Test that BANNER contains Unicode box-drawing characters."""
        # These are the box-drawing characters used in the Unicode banner
        box_chars = ["█", "╔", "═", "╗", "║", "╚", "╝"]
        has_box_char = any(char in BANNER for char in box_chars)
        assert has_box_char, "Unicode BANNER should contain box-drawing characters"

    def test_banners_have_similar_line_count(self) -> None:
        """Test that both banners have similar structure."""
        unicode_lines = [line for line in BANNER.strip().split("\n") if line.strip()]
        ascii_lines = [
            line for line in BANNER_ASCII.strip().split("\n") if line.strip()
        ]
        # Allow some variance but should be similar
        assert abs(len(unicode_lines) - len(ascii_lines)) <= 2
