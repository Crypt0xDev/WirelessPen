# 🔐 WirelessPen Framework v2.2.0

<div align="center">

![WirelessPen Logo](https://img.shields.io/badge/WirelessPen-v2.2.0-red?style=for-the-badge&logo=wifi&logoColor=white)
[![Python](https://img.shields.io/badge/Python-3.6+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?style=for-the-badge&logo=linux)](https://linux.org)

**🚀 Advanced Wireless Penetration Testing Framework**

*Professional toolkit for wireless security assessment and penetration testing*

[📖 Documentation](doc/) • [🚀 Quick Start](#-quick-start) • [💡 Features](#-features) • [🤝 Contributing](doc/contributing.md)

</div>

---

## 🎯 Overview

**WirelessPen** es un framework avanzado de penetration testing para redes inalámbricas, diseñado para profesionales de ciberseguridad y investigadores éticos. Combina las mejores herramientas de la industria con una interfaz intuitiva y características avanzadas para auditorías de seguridad wireless.

### 🏆 Why WirelessPen?

- 🔧 **Professional Grade**: Arquitectura robusta con manejo avanzado de errores
- 🎨 **Modern UI**: Interfaz colorida con símbolos Unicode y feedback en tiempo real
- 🛡️ **Universal Hardware**: Soporte para todos los chipsets principales (Realtek, Atheros, MediaTek, Intel)
- ⚡ **Advanced Attacks**: Múltiples vectores de ataque con algoritmos inteligentes
- 📚 **Comprehensive Docs**: Documentación completa y guías detalladas

## ✨ Features

### 🎯 Attack Modes
- **🤝 Handshake Capture**: WPA/WPA2 handshake capture con deauth inteligente
- **🔑 PMKID Attack**: Clientless attacks contra redes WPA2/WPA3
- **📡 WPS Attacks**: Pixie Dust y Brute Force con detección automática
- **👻 Evil Twin**: Rogue AP con portal cautivo personalizable
- **💥 Deauth Attack**: Targeted y broadcast deauthentication

### 🔧 Advanced Features
- **🎛️ Monitor Mode**: Activación automática con fallbacks inteligentes
- **📊 Real-time Scanning**: Airodump integration con filtering avanzado
- **🔄 Process Management**: Cleanup automático y manejo de señales
- **📈 Progress Tracking**: Indicadores visuales y estadísticas en tiempo real
- **🛠️ Hardware Detection**: Identificación automática de chipsets y drivers

### 🎨 User Experience
- **🌈 Colorful Interface**: Sistema ANSI con 16 colores y símbolos Unicode
- **📱 Responsive Design**: Adaptación automática al tamaño de terminal
- **🔔 Smart Notifications**: Alertas contextuales y mensajes informativos
- **📋 Detailed Logging**: Logs estructurados con niveles de verbosidad

## 🚀 Quick Start

### 📦 Installation

#### Automated Installation (Recommended)
```bash
# Clone repository
git clone https://github.com/Crypt0xDev/WirelessPen.git
cd WirelessPen

# Run automated installer
chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

#### Manual Installation
```bash
# Install system dependencies
sudo apt update
sudo apt install aircrack-ng wireless-tools iw macchanger ethtool

# Install Python dependencies
pip3 install -r requirements.txt

# Verify installation
sudo python3 main.py --check
```

#### Development Setup
```bash
# Setup development environment
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh
```

### 🎯 Basic Usage

#### Quick Network Scan
```bash
# Auto-detect and scan networks
sudo python3 main.py --scan

# Scan specific interface
sudo python3 main.py --interface wlan0 --scan
```

#### Handshake Attack
```bash
# Interactive mode
sudo python3 main.py --attack handshake

# Direct target attack
sudo python3 main.py --attack handshake --bssid AA:BB:CC:DD:EE:FF --channel 6
```

#### PMKID Attack (Clientless)
```bash
# PMKID attack on all networks
sudo python3 main.py --attack pmkid

# Target specific network
sudo python3 main.py --attack pmkid --bssid AA:BB:CC:DD:EE:FF
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ User Guide](doc/user-guide.md) | Comprehensive usage manual |
| [🔧 Technical Docs](doc/technical.md) | Architecture and API reference |
| [🤝 Contributing](doc/contributing.md) | Contribution guidelines |
| [📝 Changelog](doc/changelog.md) | Version history and updates |
| [🏗️ Architecture](doc/architecture.md) | Project structure and design |

## 🎯 Supported Hardware

### ✅ Tested Chipsets
| Vendor | Chipset | Status | Monitor Mode | Injection |
|--------|---------|--------|--------------|-----------|
| **Realtek** | RTL8188EU/CUS/ETV | ✅ | ✅ | ✅ |
| **Realtek** | RTL8812AU/BU | ✅ | ✅ | ✅ |
| **Atheros** | AR9271 | ✅ | ✅ | ✅ |
| **MediaTek** | MT7612U | ✅ | ✅ | ✅ |
| **Intel** | AC 7260/8260 | ⚠️ | ⚠️ | ❌ |
| **Broadcom** | BCM43xx | ⚠️ | ⚠️ | ❌ |

### 🎯 Recommended Adapters
- **Alfa AWUS036ACS** (802.11ac, dual-band)
- **Panda PAU09** (reliable, good range)
- **TP-Link AC600 T2U** (budget-friendly)

## 🛡️ Security & Ethics

### ⚖️ Legal Notice
**⚠️ IMPORTANTE**: WirelessPen está diseñado para:
- ✅ **Penetration Testing autorizado**
- ✅ **Auditorías de seguridad propias**
- ✅ **Investigación académica ética**
- ✅ **Educación en ciberseguridad**

### 🚫 Prohibited Usage
- ❌ **Redes sin autorización**
- ❌ **Actividades ilegales**
- ❌ **Violación de privacidad**
- ❌ **Uso malicioso**

**Los desarrolladores no se responsabilizan por el uso indebido de esta herramienta.**

## 🤝 Contributing

¡Las contribuciones son bienvenidas! Por favor lee nuestra [Guía de Contribución](doc/CONTRIBUTING.md) para comenzar.

### 🎯 Ways to Contribute
- 🐛 **Report bugs** and suggest fixes
- ✨ **Propose new features** and enhancements
- 📚 **Improve documentation** and examples
- 🧪 **Test on new hardware** and report compatibility
- 🌍 **Translate documentation** to other languages

### 🏆 Contributors
Un agradecimiento especial a todos los [contributors](https://github.com/Crypt0xDev/WirelessPen/graphs/contributors) que han ayudado a mejorar WirelessPen.

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Crypt0xDev/WirelessPen?style=social)
![GitHub forks](https://img.shields.io/github/forks/Crypt0xDev/WirelessPen?style=social)
![GitHub issues](https://img.shields.io/github/issues/Crypt0xDev/WirelessPen)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Crypt0xDev/WirelessPen)

## 📁 Project Structure

```
WirelessPen/
├── 📄 README.md              # Main project documentation
├── 📄 LICENSE                # MIT License
├── 📄 SECURITY.md            # Security policy
├── 📄 .gitignore             # Git ignore rules
│
├── 🔧 Core/
│   ├── main.py               # Main framework script
│   ├── config.py             # Configuration system
│   └── requirements.txt      # Production dependencies
│
├── 📜 scripts/
│   ├── install.sh            # Automated installer
│   └── setup-dev.sh          # Development setup
│
├── ⚙️ configs/
│   ├── pyproject.toml        # Modern Python configuration
│   ├── setup.cfg             # Tool configuration
│   └── requirements-dev.txt  # Development dependencies
│
├── 📚 doc/
│   ├── user-guide.md         # User manual
│   ├── technical.md          # Technical architecture
│   ├── contributing.md       # Contribution guide
│   ├── changelog.md          # Version history
│   └── architecture.md       # Project structure and design
│
├── 🧪 tests/
│   ├── conftest.py           # Test configuration
│   └── __init__.py           # Package marker
│
└── 🤖 .github/
    ├── workflows/ci.yml      # CI/CD pipeline
    ├── ISSUE_TEMPLATE/       # Issue templates
    └── CODEOWNERS            # Code ownership
```

## 📄 License

Este proyecto está licenciado bajo la MIT License - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🔗 Links

- **🌐 Website**: [wirelesspen.dev](https://wirelesspen.dev) *(coming soon)*
- **📧 Contact**: [crypt0xdev@protonmail.com](mailto:crypt0xdev@protonmail.com)
- **💬 Discord**: [Join our community](https://discord.gg/wirelesspen) *(coming soon)*
- **🐦 Twitter**: [@WirelessPen](https://twitter.com/wirelesspen) *(coming soon)*

---

<div align="center">

**⭐ If you find WirelessPen useful, please consider giving it a star! ⭐**

*Made with ❤️ by cybersecurity professionals for the security community*

</div>