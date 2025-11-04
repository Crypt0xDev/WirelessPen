"""
Tests for configuration module of WirelessPen Framework.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import (
    FRAMEWORK_VERSION, 
    FRAMEWORK_NAME, 
    AUTHOR_INFO, 
    WIRELESS_CARDS, 
    ATTACK_MODES,
    DEFAULT_CONFIG
)


class TestConfigModule:
    """Test configuration module constants and structures."""
    
    def test_framework_constants(self):
        """Test framework identification constants."""
        assert FRAMEWORK_VERSION == "2.2.0"
        assert FRAMEWORK_NAME == "WirelessPen"
        assert isinstance(AUTHOR_INFO, dict)
        assert 'name' in AUTHOR_INFO
        assert 'email' in AUTHOR_INFO
        
    def test_wireless_cards_config(self):
        """Test wireless cards configuration."""
        assert isinstance(WIRELESS_CARDS, dict)
        
        # Test that we have some major vendors
        expected_vendors = ['realtek', 'atheros', 'intel', 'mediatek']
        config_vendors = [vendor.lower() for vendor in WIRELESS_CARDS.keys()]
        
        # At least some major vendors should be present
        found_vendors = [v for v in expected_vendors if any(v in cv for cv in config_vendors)]
        assert len(found_vendors) > 0, "No major wireless vendors found in config"
        
    def test_attack_modes_structure(self):
        """Test attack modes configuration structure."""
        assert isinstance(ATTACK_MODES, dict)
        
        # Check for expected attack modes
        expected_modes = ['handshake', 'pmkid', 'wps', 'evil_twin']
        
        for mode in expected_modes:
            assert mode in ATTACK_MODES, f"Missing attack mode: {mode}"
            mode_config = ATTACK_MODES[mode]
            assert isinstance(mode_config, dict)
            assert 'name' in mode_config
            assert 'description' in mode_config
            
    def test_default_config_structure(self):
        """Test default configuration structure."""
        assert isinstance(DEFAULT_CONFIG, dict)
        
        required_config_keys = [
            'scan_time',
            'deauth_count',
            'handshake_timeout',
            'wps_timeout'
        ]
        
        for key in required_config_keys:
            assert key in DEFAULT_CONFIG, f"Missing default config key: {key}"
            assert isinstance(DEFAULT_CONFIG[key], (int, float))
            assert DEFAULT_CONFIG[key] > 0, f"Config value {key} should be positive"
            
    def test_config_value_ranges(self):
        """Test that configuration values are within reasonable ranges."""
        config = DEFAULT_CONFIG
        
        # Scan time should be reasonable (5 seconds to 10 minutes)
        assert 5 <= config.get('scan_time', 0) <= 600
        
        # Deauth count should be reasonable (1 to 100 packets)
        assert 1 <= config.get('deauth_count', 0) <= 100
        
        # Timeouts should be reasonable (30 seconds to 1 hour)
        assert 30 <= config.get('handshake_timeout', 0) <= 3600
        assert 30 <= config.get('wps_timeout', 0) <= 3600


class TestConfigIntegration:
    """Test configuration integration and consistency."""
    
    def test_wireless_cards_have_required_fields(self):
        """Test that wireless card configs have required fields."""
        for vendor, cards in WIRELESS_CARDS.items():
            assert isinstance(cards, list), f"Vendor {vendor} cards should be a list"
            
            for card in cards:
                assert isinstance(card, dict), f"Card config should be a dict for vendor {vendor}"
                required_fields = ['chipset', 'driver']
                
                for field in required_fields:
                    assert field in card, f"Missing field {field} in card config for {vendor}"
                    
    def test_attack_modes_consistency(self):
        """Test attack modes have consistent structure."""
        for mode_name, mode_config in ATTACK_MODES.items():
            # Each mode should have required fields
            assert 'name' in mode_config
            assert 'description' in mode_config
            
            # Name should be non-empty
            assert len(mode_config['name']) > 0
            assert len(mode_config['description']) > 0
            
            # Mode name should be lowercase and alphanumeric (with underscores)
            assert mode_name.islower()
            assert all(c.isalnum() or c == '_' for c in mode_name)


if __name__ == "__main__":
    pytest.main([__file__])