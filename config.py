#!/usr/bin/env python3
"""
WirelessPen Configuration File
Configuration settings for the WirelessPen framework.
"""

import os
from pathlib import Path

# Framework Information
FRAMEWORK_NAME = "WirelessPen"
VERSION = "2.2.0"
FRAMEWORK_VERSION = VERSION  # Alias for compatibility
BUILD = "Professional Edition"
AUTHOR = "Crypt0xDev"

# Author information dict for tests
AUTHOR_INFO = {
    "name": AUTHOR,
    "email": "crypt0xdev@users.noreply.github.com",
    "github": "https://github.com/Crypt0xDev",
}
GITHUB = "https://github.com/Crypt0xDev/WirelessPen"
LICENSE = "MIT"
BUILD_DATE = "2024-11-04"

# System Requirements
MIN_PYTHON_VERSION = "3.6"
REQUIRED_OS = ["Linux", "Kali", "Ubuntu", "Debian", "Arch"]

# Network Configuration
DEFAULT_SCAN_TIME = 30
DEAUTH_COUNT = 20
HANDSHAKE_TIMEOUT = 300
WPS_TIMEOUT = 600
PMKID_TIMEOUT = 120
MAX_RETRIES = 3

# Channels Configuration
WIFI_CHANNELS_2_4GHZ = list(range(1, 15))  # 1-14
WIFI_CHANNELS_5GHZ = [
    36,
    40,
    44,
    48,
    52,
    56,
    60,
    64,
    100,
    104,
    108,
    112,
    116,
    120,
    124,
    128,
    132,
    136,
    140,
    149,
    153,
    157,
    161,
    165,
]
COMMON_CHANNELS = [1, 6, 11]  # Most used 2.4GHz channels

# File Paths
HOME_DIR = Path.home()
OUTPUT_DIR = HOME_DIR / "WirelessPen_Results"
TEMP_DIR = "/tmp/wirelesspen"
LOG_DIR = OUTPUT_DIR / "logs"

# Wordlist Paths (in order of preference)
WORDLIST_PATHS = [
    "/usr/share/wordlists/rockyou.txt",
    "/usr/share/wordlists/wpa2.txt",
    "/usr/share/wordlists/fasttrack.txt",
    "/opt/wordlists/rockyou.txt",
    "~/wordlists/rockyou.txt",
    "/usr/share/dict/american-english",
    "/usr/share/dict/words",
]

# Tool Dependencies
CORE_DEPENDENCIES = {
    "aircrack-ng": {
        "commands": ["aircrack-ng", "airodump-ng", "aireplay-ng", "airmon-ng"],
        "package": "aircrack-ng",
        "min_version": "1.5",
        "critical": True,
        "description": "WiFi security auditing tools",
    },
    "wireless-tools": {
        "commands": ["iwconfig", "iwlist"],
        "package": "wireless-tools",
        "min_version": "30",
        "critical": True,
        "description": "Wireless network configuration tools",
    },
    "iw": {
        "commands": ["iw"],
        "package": "iw",
        "min_version": "5.0",
        "critical": True,
        "description": "Modern wireless configuration tool",
    },
    "macchanger": {
        "commands": ["macchanger"],
        "package": "macchanger",
        "min_version": "1.7",
        "critical": True,
        "description": "MAC address manipulation tool",
    },
    "ethtool": {
        "commands": ["ethtool"],
        "package": "ethtool",
        "min_version": "5.0",
        "critical": True,
        "description": "Network interface information tool",
    },
}

OPTIONAL_DEPENDENCIES = {
    "reaver": {
        "commands": ["reaver", "wash"],
        "package": "reaver",
        "min_version": "1.6",
        "critical": False,
        "description": "WPS PIN attack tools",
        "features": ["wps", "pixie"],
    },
    "bully": {
        "commands": ["bully"],
        "package": "bully",
        "min_version": "1.1",
        "critical": False,
        "description": "WPS brute force tool",
        "features": ["wps"],
    },
    "hcxtools": {
        "commands": ["hcxdumptool", "hcxpcapngtool"],
        "package": "hcxtools",
        "min_version": "6.0",
        "critical": False,
        "description": "PMKID and hash extraction tools",
        "features": ["pmkid"],
    },
    "hashcat": {
        "commands": ["hashcat"],
        "package": "hashcat",
        "min_version": "6.0",
        "critical": False,
        "description": "Advanced password recovery tool",
        "features": ["pmkid", "handshake"],
    },
    "hostapd": {
        "commands": ["hostapd"],
        "package": "hostapd",
        "min_version": "2.9",
        "critical": False,
        "description": "Access point daemon",
        "features": ["evil_twin"],
    },
    "dnsmasq": {
        "commands": ["dnsmasq"],
        "package": "dnsmasq",
        "min_version": "2.80",
        "critical": False,
        "description": "DHCP and DNS server",
        "features": ["evil_twin"],
    },
}

# Supported Hardware (chipsets and drivers)
SUPPORTED_HARDWARE = {
    "realtek": {
        "chipsets": ["RTL8812AU", "RTL8821AU", "RTL8188EU", "RTL8192EU", "RTL8814AU"],
        "drivers": ["rtl8812au", "rtl8821au", "rtl8188eu", "8812au"],
        "monitor_mode": True,
        "injection": True,
    },
    "atheros": {
        "chipsets": ["AR9271", "ATH9K", "ATH10K", "QCA9377", "QCA6174"],
        "drivers": ["ath9k_htc", "ath9k", "ath10k_pci"],
        "monitor_mode": True,
        "injection": True,
    },
    "mediatek": {
        "chipsets": ["MT7610U", "MT7612U", "MT76x2U", "MT7921"],
        "drivers": ["mt76x2u", "mt7610u", "mt76x0u"],
        "monitor_mode": True,
        "injection": True,
    },
    "intel": {
        "chipsets": ["AC7260", "AC8265", "AX200", "AX210"],
        "drivers": ["iwlwifi"],
        "monitor_mode": False,  # Limited support
        "injection": False,
    },
    "broadcom": {
        "chipsets": ["BCM43142", "BCM4360", "BCM43602"],
        "drivers": ["brcmfmac", "b43", "wl"],
        "monitor_mode": False,  # Limited support
        "injection": False,
    },
}

# Aliases for compatibility with tests
WIRELESS_CARDS = {}
for vendor, info in SUPPORTED_HARDWARE.items():
    cards = []
    chipsets = info["chipsets"]
    drivers = info["drivers"]
    for chip, drv in zip(chipsets, drivers):
        cards.append({"chipset": chip, "driver": drv})
    WIRELESS_CARDS[vendor] = cards

# Attack Modes Configuration (for tests)
ATTACK_MODES = {
    "handshake": {
        "name": "Handshake Capture",
        "description": "Capture WPA/WPA2 handshake for offline cracking",
    },
    "pmkid": {
        "name": "PMKID Attack",
        "description": "Extract PMKID hash for hashcat cracking",
    },
    "wps": {"name": "WPS Attack", "description": "Attack WPS-enabled access points"},
    "evil_twin": {
        "name": "Evil Twin",
        "description": "Create rogue access point to capture credentials",
    },
}

# Default Configuration (for tests)
DEFAULT_CONFIG = {
    "scan_time": DEFAULT_SCAN_TIME,
    "deauth_count": DEAUTH_COUNT,
    "handshake_timeout": HANDSHAKE_TIMEOUT,
    "wps_timeout": WPS_TIMEOUT,
}

# Attack Configurations
ATTACK_CONFIGS = {
    "handshake": {
        "timeout": HANDSHAKE_TIMEOUT,
        "deauth_count": DEAUTH_COUNT,
        "deauth_interval": 10,
        "max_rounds": 5,
        "output_format": "cap",
    },
    "pmkid": {
        "timeout": PMKID_TIMEOUT,
        "output_format": "pcapng",
        "hashcat_mode": 22000,
    },
    "wps": {
        "timeout": WPS_TIMEOUT,
        "delay": 15,
        "max_attempts": 11000,
        "lockout_time": 300,
    },
    "deauth": {"packet_count": DEAUTH_COUNT, "interval": 1, "broadcast": True},
}

# Color and UI Configuration
UI_CONFIG = {
    "banner_width": 80,
    "table_width": 90,
    "progress_bar_width": 50,
    "enable_colors": True,
    "enable_unicode": True,
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_handler": True,
    "console_handler": True,
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
}

# Security Configuration
SECURITY_CONFIG = {
    "require_confirmation": True,
    "destructive_attacks": ["deauth", "evil_twin"],
    "max_session_time": 3600,  # 1 hour
    "auto_cleanup": True,
}


def get_output_directory():
    """Get the configured output directory."""
    return OUTPUT_DIR


def get_wordlist():
    """Find the first available wordlist."""
    for path in WORDLIST_PATHS:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            return expanded_path
    return None


def create_directories():
    """Create necessary directories."""
    directories = [OUTPUT_DIR, LOG_DIR, TEMP_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def get_dependency_by_command(command):
    """Get dependency info by command name."""
    all_deps = {**CORE_DEPENDENCIES, **OPTIONAL_DEPENDENCIES}
    for dep_name, dep_info in all_deps.items():
        if command in dep_info["commands"]:
            return dep_name, dep_info
    return None, None
