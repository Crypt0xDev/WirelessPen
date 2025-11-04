#!/bin/bash
# WirelessPen v2.2.0 - Automated Installation Script
# Professional Wireless Penetration Testing Framework

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Framework information
SCRIPT_NAME="WirelessPen"
VERSION="2.2.0"
GITHUB_URL="https://github.com/Crypt0xDev/WirelessPen"

# Installation directories
INSTALL_DIR="/opt/wirelesspen"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="$HOME/Desktop"

print_banner() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${BLUE}  ██     ██ ██ ██████  ███████ ██      ███████ ███████ ███████  ${CYAN}║${NC}"
    echo -e "${CYAN}║${BLUE}  ██     ██ ██ ██   ██ ██      ██      ██      ██      ██       ${CYAN}║${NC}"
    echo -e "${CYAN}║${BLUE}  ██  █  ██ ██ ██████  █████   ██      █████   ███████ ███████  ${CYAN}║${NC}"
    echo -e "${CYAN}║${BLUE}  ██ ███ ██ ██ ██   ██ ██      ██      ██           ██      ██  ${CYAN}║${NC}"
    echo -e "${CYAN}║${BLUE}   ███ ███  ██ ██   ██ ███████ ███████ ███████ ███████ ███████  ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                                  ║${NC}"
    echo -e "${CYAN}║${YELLOW}              📡 Wireless Penetration Framework v${VERSION}             ${CYAN}║${NC}"
    echo -e "${CYAN}║${PURPLE}                    Automated Installation Script                  ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo
}

print_step() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')] ${GREEN}➤${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script requires root privileges"
        echo -e "Please run: ${CYAN}sudo $0${NC}"
        exit 1
    fi
}

detect_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$ID
        DISTRO=$NAME
    else
        print_error "Cannot detect operating system"
        exit 1
    fi
    
    print_info "Detected OS: $DISTRO"
}

install_dependencies() {
    print_step "Installing system dependencies..."
    
    case $OS in
        ubuntu|debian|kali)
            apt update -qq
            apt install -y \
                python3 \
                python3-pip \
                aircrack-ng \
                wireless-tools \
                iw \
                macchanger \
                ethtool \
                git \
                curl \
                wget \
                net-tools
            ;;
        arch|manjaro)
            pacman -Sy --noconfirm \
                python \
                python-pip \
                aircrack-ng \
                wireless_tools \
                iw \
                macchanger \
                ethtool \
                git \
                curl \
                wget \
                net-tools
            ;;
        fedora|centos|rhel)
            if command -v dnf &> /dev/null; then
                dnf install -y \
                    python3 \
                    python3-pip \
                    aircrack-ng \
                    wireless-tools \
                    iw \
                    macchanger \
                    ethtool \
                    git \
                    curl \
                    wget \
                    net-tools
            else
                yum install -y \
                    python3 \
                    python3-pip \
                    aircrack-ng \
                    wireless-tools \
                    iw \
                    macchanger \
                    ethtool \
                    git \
                    curl \
                    wget \
                    net-tools
            fi
            ;;
        *)
            print_warning "Unsupported distribution: $DISTRO"
            print_info "Please install dependencies manually:"
            echo "  - Python 3.6+"
            echo "  - aircrack-ng suite"
            echo "  - wireless-tools (iwconfig)"
            echo "  - iw"
            echo "  - macchanger"
            echo "  - ethtool"
            ;;
    esac
}

install_optional_tools() {
    print_step "Installing optional tools for advanced features..."
    
    case $OS in
        ubuntu|debian|kali)
            # Install from repositories if available
            apt install -y reaver bully hashcat hostapd dnsmasq 2>/dev/null || true
            
            # Try to install hcxtools
            if ! command -v hcxdumptool &> /dev/null; then
                print_info "Installing hcxtools from source..."
                cd /tmp
                git clone https://github.com/ZerBea/hcxtools.git 2>/dev/null || true
                if [[ -d hcxtools ]]; then
                    cd hcxtools
                    make && make install 2>/dev/null || print_warning "hcxtools installation failed"
                fi
            fi
            ;;
        *)
            print_info "Please install optional tools manually if needed:"
            echo "  - reaver (WPS attacks)"
            echo "  - bully (WPS attacks)"
            echo "  - hcxtools (PMKID attacks)"
            echo "  - hashcat (password cracking)"
            echo "  - hostapd (Evil Twin attacks)"
            echo "  - dnsmasq (Evil Twin attacks)"
            ;;
    esac
}

install_wireless_drivers() {
    print_step "Checking for wireless drivers..."
    
    # Check for common USB WiFi adapters that need special drivers
    if lsusb | grep -q "0bda:8812\|0bda:8821\|0bda:881a"; then
        print_info "Realtek adapter detected, installing drivers..."
        
        # Install RTL8812AU driver
        if [[ ! -d /tmp/rtl8812au ]]; then
            cd /tmp
            git clone https://github.com/aircrack-ng/rtl8812au.git
            cd rtl8812au
            make && make install
            modprobe 8812au
            print_info "RTL8812AU driver installed"
        fi
    fi
    
    if lsusb | grep -q "148f:7610\|148f:761a\|148f:760a"; then
        print_info "MediaTek adapter detected"
        # Most MediaTek adapters work with kernel drivers
    fi
}

create_installation() {
    print_step "Creating installation directory..."
    
    # Create installation directory
    mkdir -p "$INSTALL_DIR"
    
    # Copy files
    if [[ -f "main.py" ]]; then
        cp main.py "$INSTALL_DIR/"
        cp config.py "$INSTALL_DIR/" 2>/dev/null || true
        cp README.md "$INSTALL_DIR/" 2>/dev/null || true
        cp LICENSE "$INSTALL_DIR/" 2>/dev/null || true
    else
        print_error "main.py not found in current directory"
        exit 1
    fi
    
    # Make executable
    chmod +x "$INSTALL_DIR/main.py"
    
    # Create symlink
    ln -sf "$INSTALL_DIR/main.py" "$BIN_DIR/wirelesspen"
    
    print_info "Installed to: $INSTALL_DIR"
}

create_desktop_shortcut() {
    print_step "Creating desktop shortcut..."
    
    if [[ -d "$DESKTOP_DIR" ]]; then
        cat > "$DESKTOP_DIR/WirelessPen.desktop" << EOF
[Desktop Entry]
Name=WirelessPen
Comment=Professional Wireless Penetration Testing Framework
Exec=sudo python3 $INSTALL_DIR/main.py
Icon=network-wireless
Terminal=true
Type=Application
Categories=Network;Security;
StartupNotify=false
EOF
        chmod +x "$DESKTOP_DIR/WirelessPen.desktop"
        print_info "Desktop shortcut created"
    fi
}

verify_installation() {
    print_step "Verifying installation..."
    
    # Test basic functionality
    if python3 "$INSTALL_DIR/main.py" --version &>/dev/null; then
        print_info "Installation verification successful"
    else
        print_warning "Installation verification failed"
    fi
    
    # Check dependencies
    python3 "$INSTALL_DIR/main.py" --check
}

show_completion() {
    echo
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    INSTALLATION COMPLETED                       ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${YELLOW}📁 Installation Directory:${NC} $INSTALL_DIR"
    echo -e "${YELLOW}🔗 Command Link:${NC} wirelesspen"
    echo -e "${YELLOW}🖥️  Desktop Shortcut:${NC} ~/Desktop/WirelessPen.desktop"
    echo
    echo -e "${CYAN}🚀 USAGE EXAMPLES:${NC}"
    echo -e "  ${PURPLE}Interactive mode:${NC}       sudo wirelesspen"
    echo -e "  ${PURPLE}Network scan:${NC}           sudo wirelesspen scan -i wlan0"
    echo -e "  ${PURPLE}Handshake attack:${NC}       sudo wirelesspen handshake -i wlan0"
    echo -e "  ${PURPLE}System check:${NC}           sudo wirelesspen --check"
    echo -e "  ${PURPLE}Get help:${NC}               sudo wirelesspen --help"
    echo
    echo -e "${YELLOW}📚 DOCUMENTATION:${NC} $GITHUB_URL"
    echo -e "${YELLOW}🐛 ISSUES:${NC} $GITHUB_URL/issues"
    echo
    echo -e "${RED}⚠️  LEGAL NOTICE:${NC} Use only on authorized networks"
    echo -e "${RED}⚠️  ROOT REQUIRED:${NC} Always run with sudo"
    echo
}

main() {
    print_banner
    
    # Perform installation steps
    check_root
    detect_os
    install_dependencies
    install_optional_tools
    install_wireless_drivers
    create_installation
    create_desktop_shortcut
    verify_installation
    show_completion
    
    # Optional: Run immediate check
    echo -e "${YELLOW}Would you like to run a system check now? [Y/n]:${NC} "
    read -r response
    if [[ "$response" != "n" && "$response" != "N" ]]; then
        python3 "$INSTALL_DIR/main.py" --check
    fi
}

# Run installation
main "$@"