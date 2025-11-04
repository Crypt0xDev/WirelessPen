# WirelessPen v2.2.0 - Documentación Técnica

## 🏗️ Arquitectura del Framework

### Estructura de Archivos
```
WirelessPen/
├── main.py              # Script principal del framework
├── config.py            # Configuración centralizada
├── install.sh           # Script de instalación automatizada
├── requirements.txt     # Dependencias de Python
├── LICENSE             # Licencia MIT
├── .gitignore          # Configuración Git
└── doc/                # Documentación
    ├── README.md       # Documentación principal
    ├── CHANGELOG.md    # Historial de cambios
    ├── USER_GUIDE.md   # Guía de usuario
    └── TECHNICAL.md    # Documentación técnica (este archivo)
```

### Diagrama de Arquitectura
```
┌─────────────────────────────────────────────────────────────┐
│                    WirelessPen v2.2.0                      │
│                  Professional Edition                      │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    main.py (Core)                          │
│  ┌─────────────────┬─────────────────┬─────────────────┐   │
│  │  CLI Interface  │  Attack Modes   │  System Utils   │   │
│  │  - Arguments    │  - Handshake    │  - Monitor Mode │   │
│  │  - Interactive  │  - PMKID        │  - Dependencies │   │
│  │  - Help System  │  - WPS/Pixie    │  - Hardware     │   │
│  │  - Banners      │  - Evil Twin    │  - Diagnostics  │   │
│  │                 │  - Deauth       │                 │   │
│  └─────────────────┴─────────────────┴─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   config.py (Configuration)               │
│  - Framework Constants    - Hardware Profiles             │
│  - Attack Parameters     - Dependency Definitions         │
│  - File Paths           - Security Settings               │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 System Tools Integration                  │
│  ┌──────────────┬──────────────┬──────────────┬─────────┐  │
│  │ Aircrack-ng  │ Wireless     │ WPS Tools    │ Others  │  │
│  │ - airodump   │ - iwconfig   │ - reaver     │ - iw    │  │
│  │ - aireplay   │ - iwlist     │ - wash       │ - ethtool│  │
│  │ - aircrack   │ - iwspy      │ - bully      │ - hostapd│  │
│  │ - airmon     │              │              │ - hashcat│  │
│  └──────────────┴──────────────┴──────────────┴─────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Componentes Técnicos

### 1. GlobalState Class
```python
class GlobalState:
    """Manejo centralizado del estado de la aplicación"""
    
    def __init__(self):
        self.network_card: Optional[str] = None
        self.monitor_interface: Optional[str] = None
        self.attack_mode: Optional[str] = None
        self.target_network: Optional[Dict[str, str]] = None
        self.processes: List[subprocess.Popen] = []
        self.temp_files: List[str] = []
        # ... más atributos
```

**Funcionalidades**:
- Gestión de interfaces de red
- Control de procesos en segundo plano
- Limpieza automática de archivos temporales
- Seguimiento de la sesión actual

### 2. Colors Class
```python
class Colors:
    """Sistema avanzado de colores ANSI"""
    
    # Colores básicos y extendidos
    RED = '\033[0;31m\033[1m'
    GREEN = '\033[0;32m\033[1m'
    # ... más colores
    
    # Símbolos especiales
    SUCCESS = f'{GREEN}✓{RESET}'
    FAILURE = f'{RED}✗{RESET}'
    WARNING = f'{YELLOW}⚠{RESET}'
```

**Características**:
- Soporte para 256 colores
- Símbolos Unicode para mejor UX
- Compatibilidad con terminales diferentes

### 3. Sistema de Comandos
```python
def run_command(cmd: str, shell: bool = True, capture: bool = True, timeout: int = 30):
    """Ejecución robusta de comandos del sistema"""
    
def run_command_async(cmd: str, shell: bool = True):
    """Ejecución asíncrona para procesos de larga duración"""
    
def kill_process_group(proc: subprocess.Popen):
    """Terminación segura de grupos de procesos"""
```

**Mejoras**:
- Manejo de timeouts
- Control de grupos de procesos
- Captura de errores detallada
- Logging opcional

## 🔍 Módulos de Ataque Detallados

### 1. Handshake Capture (attack_handshake)

**Flujo de Trabajo**:
```
1. Selección/Validación del Objetivo
   ↓
2. Configuración del Monitor Mode
   ↓
3. Captura de Tráfico (airodump-ng)
   ↓
4. Detección de Clientes Conectados
   ↓
5. Deautenticación Inteligente
   ├─ Clientes específicos (si detectados)
   └─ Broadcast (si no hay clientes)
   ↓
6. Verificación del Handshake
   ├─ aircrack-ng
   └─ tshark (fallback)
   ↓
7. Conversión a Formato Hashcat
   ↓
8. Reporte de Resultados
```

**Características Técnicas**:
- Detección automática de clientes via CSV parsing
- Múltiples rondas de deautenticación
- Verificación cruzada del handshake
- Soporte para diferentes formatos de salida

### 2. PMKID Attack (attack_pmkid_hashcat)

**Proceso Técnico**:
```
1. Configuración de hcxdumptool
   ↓
2. Captura Pasiva del PMKID
   ↓
3. Conversión con hcxpcapngtool
   ↓
4. Formateo para Hashcat (modo 22000)
   ↓
5. Verificación del Hash
```

**Ventajas**:
- No requiere deautenticación
- Más sigiloso que handshake tradicional
- Compatible con hashcat moderno

### 3. Network Scanner (scan_networks)

**Funcionalidades Avanzadas**:
- Filtrado por tipo de cifrado
- Ordenación por múltiples criterios
- Análisis de potencia de señal
- Detección de canales óptimos

**Algoritmo de Selección**:
```python
def scan_networks(scan_time: int = None, target_channel: str = None):
    # 1. Configurar airodump-ng
    # 2. Capturar durante tiempo especificado
    # 3. Parsear CSV resultante
    # 4. Filtrar y ordenar resultados
    # 5. Presentar interfaz de selección interactiva
```

## 🛠️ Sistema de Dependencias

### Verificación Automatizada
```python
CORE_DEPENDENCIES = {
    'aircrack-ng': {
        'commands': ['aircrack-ng', 'airodump-ng', 'aireplay-ng'],
        'package': 'aircrack-ng',
        'min_version': '1.5',
        'critical': True
    },
    # ... más dependencias
}
```

### Matriz de Compatibilidad
| Herramienta | Ubuntu 20.04+ | Debian 11+ | Kali 2023+ | Arch Linux |
|-------------|---------------|------------|------------|------------|
| aircrack-ng | ✅ v1.6+ | ✅ v1.6+ | ✅ v1.7+ | ✅ v1.7+ |
| wireless-tools | ✅ v30+ | ✅ v30+ | ✅ v30+ | ✅ v30+ |
| iw | ✅ v5.9+ | ✅ v5.9+ | ✅ v5.19+ | ✅ v5.19+ |
| reaver | ✅ v1.6.5+ | ✅ v1.6.5+ | ✅ v1.6.6+ | ⚠️ AUR |
| hcxtools | ⚠️ Manual | ⚠️ Manual | ✅ v6.2+ | ✅ v6.2+ |

## 📊 Manejo de Hardware

### Detección de Adaptadores
```python
def detect_wireless_cards() -> List[str]:
    """Detección inteligente de adaptadores WiFi"""
    
    # 1. Escaneo con iwconfig
    # 2. Verificación de capacidades con iw
    # 3. Detección de chipset específico
    # 4. Evaluación de compatibilidad
```

### Profiles de Hardware
```python
SUPPORTED_HARDWARE = {
    'realtek': {
        'chipsets': ['RTL8812AU', 'RTL8821AU'],
        'monitor_mode': True,
        'injection': True,
        'power_management': 'iwconfig {iface} power off'
    }
}
```

### Monitor Mode Activation
```python
def handle_monitor_mode() -> bool:
    """Activación robusta del modo monitor"""
    
    # Método 1: iw moderno
    # Método 2: iwconfig legacy  
    # Método 3: airmon-ng automatizado
    # Fallback: diagnósticos y solución de problemas
```

## 🔐 Seguridad y Validación

### Control de Acceso
```python
def check_root():
    """Verificación de privilegios root"""
    if os.geteuid() != 0:
        print("Root privileges required")
        sys.exit(1)
```

### Validación de Entradas
```python
def validate_bssid(bssid: str) -> bool:
    """Validar formato de dirección MAC"""
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, bssid))

def validate_channel(channel: int) -> bool:
    """Validar canal WiFi"""
    return 1 <= channel <= 14 or channel in WIFI_CHANNELS_5GHZ
```

### Sanitización de Datos
- Escape de caracteres especiales en comandos shell
- Validación de rutas de archivos
- Filtrado de entradas maliciosas
- Límites en tamaños de archivos

## 🚀 Optimizaciones de Performance

### Gestión de Memoria
```python
class GlobalState:
    def cleanup(self):
        """Limpieza proactiva de recursos"""
        # Terminar procesos
        # Remover archivos temporales
        # Liberar memoria
```

### I/O Asíncrono
```python
def run_command_async(cmd: str) -> subprocess.Popen:
    """Ejecución no bloqueante para operaciones largas"""
    proc = subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    return proc
```

### Caching y Optimización
- Cache de resultados de escaneo
- Reutilización de conexiones
- Optimización de operaciones de archivo
- Gestión inteligente de timeouts

## 🐛 Debugging y Logging

### Sistema de Logging
```python
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_handler': True,
    'console_handler': True
}
```

### Modo Verbose
```bash
# Activar debugging detallado
sudo wirelesspen handshake -i wlan0 --verbose

# Salida de ejemplo:
[DEBUG] Executing: iwconfig wlan0 channel 6
[DEBUG] Command completed with exit code 0
[DEBUG] Starting airodump process: PID 12345
```

### Herramientas de Diagnóstico
```python
def wifi_diagnostic():
    """Sistema de diagnóstico de 8 pasos"""
    
    # 1. Información de la interfaz
    # 2. Driver y chipset  
    # 3. Dispositivos USB WiFi
    # 4. Módulos del kernel
    # 5. Capacidades del adaptador
    # 6. Estado actual
    # 7. Verificación modo monitor
    # 8. Procesos interferentes
```

## 📈 Métricas y Monitoring

### Tracking de Sesión
```python
class SessionMetrics:
    start_time: float
    attacks_performed: int
    networks_scanned: int
    handshakes_captured: int
    success_rate: float
```

### Performance Metrics
- Tiempo de activación de monitor mode
- Velocidad de escaneo de redes
- Tasa de éxito en captura de handshakes
- Uso de CPU y memoria
- Throughput de red

## 🔧 API y Extensibilidad

### Estructura de Plugins (Futuro)
```python
class AttackPlugin:
    """Clase base para plugins de ataque"""
    
    def __init__(self, config):
        self.config = config
    
    def execute(self, target):
        raise NotImplementedError
    
    def validate_target(self, target):
        raise NotImplementedError
```

### Hooks del Sistema
```python
# Pre-attack hooks
def before_attack(target_info):
    # Validación personalizada
    # Logging avanzado
    # Notificaciones
    pass

# Post-attack hooks  
def after_attack(results):
    # Procesamiento de resultados
    # Generación de reportes
    # Limpieza personalizada
    pass
```

## 📝 Formato de Datos

### Network Information Structure
```python
{
    'bssid': 'AA:BB:CC:DD:EE:FF',
    'essid': 'NetworkName',
    'channel': '6',
    'encryption': 'WPA2',
    'power': '-45',
    'clients': ['client1_mac', 'client2_mac']
}
```

### Attack Results Format
```python
{
    'attack_type': 'handshake',
    'target': {network_info},
    'success': True,
    'duration': 120.5,
    'files_created': ['handshake.cap', 'handshake.hc22000'],
    'session_id': 'abc12345',
    'timestamp': '2024-11-04T15:30:00Z'
}
```

## 🧪 Testing Framework

### Unit Tests Structure
```
tests/
├── unit/
│   ├── test_commands.py
│   ├── test_network_scan.py
│   ├── test_monitor_mode.py
│   └── test_attacks.py
├── integration/
│   ├── test_full_workflow.py
│   └── test_hardware_compatibility.py
└── fixtures/
    ├── sample_networks.csv
    └── mock_hardware.json
```

### Test Coverage Goals
- **Unit Tests**: >80% cobertura de código
- **Integration Tests**: Flujos completos de trabajo  
- **Hardware Tests**: Compatibilidad con adaptadores reales
- **Performance Tests**: Benchmarks y profiling

## 🔄 CI/CD Pipeline (Futuro)

### Automated Testing
```yaml
# GitHub Actions workflow
name: WirelessPen CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: sudo apt install aircrack-ng wireless-tools
      - name: Run tests
        run: python -m pytest tests/
```

### Quality Assurance
- **Static Analysis**: flake8, mypy, bandit
- **Security Scanning**: Safety, semgrep
- **Code Formatting**: Black, isort
- **Documentation**: Sphinx auto-generation

---

## 📚 Referencias Técnicas

### Protocolos WiFi
- [IEEE 802.11 Standard](https://standards.ieee.org/standard/802_11-2020.html)
- [WPA2/WPA3 Specifications](https://www.wi-fi.org/security)
- [PMKID Attack Research](https://hashcat.net/forum/thread-7717.html)

### Herramientas y Librerías
- [Aircrack-ng Documentation](https://aircrack-ng.org/documentation.html)
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)
- [Linux Wireless APIs](https://wireless.wiki.kernel.org/en/developers/documentation/nl80211)

### Investigación de Seguridad
- [KRACK Attacks](https://www.krackattacks.com/)
- [WPS Vulnerabilities](https://sviehb.files.wordpress.com/2011/12/viehboeck_wps.pdf)
- [WiFi Security Evolution](https://papers.mathyvanhoef.com/)

---

**Nota**: Esta documentación técnica es para desarrolladores y usuarios avanzados. Para uso general, consultar [USER_GUIDE.md](USER_GUIDE.md).