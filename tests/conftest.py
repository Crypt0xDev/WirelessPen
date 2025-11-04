# Test configuration for WirelessPen
import pytest
import tempfile
import os
from unittest.mock import MagicMock

# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "hardware: mark test as requiring hardware"
    )
    config.addinivalue_line(
        "markers", "root: mark test as requiring root privileges"
    )

# Common fixtures
@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def mock_interface():
    """Mock wireless interface name."""
    return "wlan0test"

@pytest.fixture
def sample_network():
    """Sample network data for testing."""
    return {
        'bssid': 'AA:BB:CC:DD:EE:FF',
        'essid': 'TestNetwork',
        'channel': '6',
        'encryption': 'WPA2',
        'power': '-45',
        'beacons': '100',
        'iv': '0',
        'lan_ip': '0.0.0.0',
        'id_length': '11',
        'cipher': 'CCMP',
        'authentication': 'PSK'
    }

@pytest.fixture
def mock_process():
    """Mock subprocess for command execution."""
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = ""
    mock.stderr = ""
    return mock