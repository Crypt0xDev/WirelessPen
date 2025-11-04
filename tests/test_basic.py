"""
Basic test suite for WirelessPen Framework.
Tests core functionality without requiring actual wireless hardware.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest  # noqa: E402
from main import Colors, CONFIG, check_python_version, show_version  # noqa: E402


class TestWirelessPenBasic:
    """Test basic framework functionality."""

    def test_colors_defined(self):
        """Test that color constants are properly defined."""
        assert hasattr(Colors, "RED")
        assert hasattr(Colors, "GREEN")
        assert hasattr(Colors, "YELLOW")
        assert hasattr(Colors, "RESET")

    def test_config_structure(self):
        """Test that configuration has required keys."""
        required_keys = [
            "DEFAULT_SCAN_TIME",
            "DEAUTH_COUNT",
            "HANDSHAKE_TIMEOUT",
            "WPS_TIMEOUT",
            "WORDLIST_PATHS",
        ]

        for key in required_keys:
            assert key in CONFIG, f"Missing config key: {key}"

    def test_python_version_check(self):
        """Test Python version checking."""
        # This should not raise an exception on supported Python versions
        try:
            check_python_version()
        except SystemExit:
            # If it exits, it means unsupported Python version
            pytest.fail("Python version check failed - unsupported version")

    def test_show_version(self):
        """Test version display function."""
        # This should execute without errors
        try:
            show_version()
        except SystemExit:
            # Expected behavior - show_version calls sys.exit(0)
            pass
        except Exception as e:
            pytest.fail(f"show_version raised unexpected exception: {e}")


class TestConfigValidation:
    """Test configuration validation."""

    def test_scan_time_is_positive(self):
        """Test that scan time configuration is positive."""
        assert CONFIG["DEFAULT_SCAN_TIME"] > 0

    def test_deauth_count_is_positive(self):
        """Test that deauth count is positive."""
        assert CONFIG["DEAUTH_COUNT"] > 0

    def test_timeouts_are_positive(self):
        """Test that timeout values are positive."""
        assert CONFIG["HANDSHAKE_TIMEOUT"] > 0
        assert CONFIG["WPS_TIMEOUT"] > 0

    def test_wordlist_paths_is_list(self):
        """Test that wordlist paths is a list."""
        assert isinstance(CONFIG["WORDLIST_PATHS"], list)


class TestMockFunctions:
    """Test functions that can be tested without system requirements."""

    def test_color_output_format(self):
        """Test color output formatting."""
        # Test basic color formatting
        test_msg = f"{Colors.RED}Error{Colors.RESET}"
        assert Colors.RED in test_msg
        assert Colors.RESET in test_msg

    def test_config_access(self):
        """Test configuration access patterns."""
        # Test that we can read config values
        scan_time = CONFIG.get("DEFAULT_SCAN_TIME")
        assert scan_time is not None
        assert isinstance(scan_time, int)


if __name__ == "__main__":
    pytest.main([__file__])
