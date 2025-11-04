# Contribuir a WirelessPen

¡Gracias por tu interés en contribuir a WirelessPen! Este documento proporciona pautas para contribuir al proyecto de manera efectiva.

## 📋 Tabla de Contenidos
- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Características](#sugerir-características)
- [Desarrollo](#desarrollo)
- [Pull Requests](#pull-requests)
- [Estilo de Código](#estilo-de-código)
- [Testing](#testing)
- [Documentación](#documentación)

## 🤝 Código de Conducta

### Nuestro Compromiso
En el interés de fomentar un ambiente abierto y acogedor, nosotros como contribuyentes y mantenedores nos comprometemos a hacer que la participación en nuestro proyecto y nuestra comunidad sea una experiencia libre de acoso para todos.

### Nuestros Estándares
Ejemplos de comportamiento que contribuye a crear un ambiente positivo incluyen:

✅ **Comportamientos Aceptables**:
- Usar un lenguaje acogedor e inclusivo
- Respetar diferentes puntos de vista y experiencias
- Aceptar constructivamente las críticas
- Enfocarse en lo que es mejor para la comunidad
- Mostrar empatía hacia otros miembros de la comunidad

❌ **Comportamientos Inaceptables**:
- Uso de lenguaje o imágenes sexualizadas
- Comentarios despectivos o ataques personales
- Acoso público o privado
- Publicar información privada sin permiso
- Otras conductas que puedan considerarse inapropiadas

## 🚀 Cómo Contribuir

### Tipos de Contribuciones Bienvenidas

#### 🐛 Corrección de Bugs
- Reportar bugs detalladamente
- Proporcionar fixes para issues existentes
- Mejorar el manejo de errores

#### ✨ Nuevas Características
- Nuevos modos de ataque
- Mejoras en la interfaz de usuario
- Soporte para nuevo hardware
- Optimizaciones de performance

#### 📚 Documentación
- Mejorar guías existentes
- Añadir ejemplos prácticos
- Traducir documentación
- Crear tutoriales en video

#### 🧪 Testing
- Escribir tests unitarios
- Probar en nuevo hardware
- Reportar compatibilidad
- Performance benchmarking

## 🐛 Reportar Bugs

### Antes de Reportar un Bug
1. **Verificar**: Asegúrate de estar usando la versión más reciente
2. **Buscar**: Revisa los issues existentes para evitar duplicados
3. **Reproducir**: Confirma que el bug es reproducible
4. **Documentar**: Recopila información del sistema y logs

### Template para Report de Bug
```markdown
**Descripción del Bug**
Una descripción clara y concisa de qué es el bug.

**Pasos para Reproducir**
1. Ir a '...'
2. Ejecutar comando '....'
3. Ver error

**Comportamiento Esperado**
Descripción de lo que esperabas que pasara.

**Comportamiento Actual**
Descripción de lo que realmente pasó.

**Información del Sistema**
- OS: [e.g. Ubuntu 22.04]
- Python Version: [e.g. 3.8.10]
- WirelessPen Version: [e.g. 2.2.0]
- Hardware: [e.g. TP-Link AC600 T2U]

**Logs Relevantes**
```
Incluir logs o output del comando --verbose
```

**Información Adicional**
Cualquier otro contexto sobre el problema.
```

## 💡 Sugerir Características

### Template para Feature Request
```markdown
**¿Esta feature request está relacionada a un problema?**
Descripción clara del problema. Ej: Estoy frustrado cuando [...]

**Describe la solución que te gustaría**
Descripción clara de lo que quieres que pase.

**Describe alternativas que has considerado**
Descripción de soluciones o features alternativas.

**Contexto Adicional**
Screenshots, mockups, o cualquier otro contexto.

**Consideraciones de Implementación**
Si tienes ideas sobre cómo implementarlo.
```

## 🛠️ Desarrollo

### Configuración del Entorno de Desarrollo

#### 1. Fork y Clone
```bash
# Fork en GitHub
# Luego clonar tu fork
git clone https://github.com/TU_USUARIO/WirelessPen.git
cd WirelessPen

# Añadir upstream remote
git remote add upstream https://github.com/Crypt0xDev/WirelessPen.git
```

#### 2. Configurar Entorno
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Instalar dependencias del sistema
sudo apt install aircrack-ng wireless-tools iw macchanger ethtool
```

#### 3. Verificar Setup
```bash
# Ejecutar tests
python -m pytest tests/

# Verificar linting
flake8 main.py
black --check main.py
mypy main.py

# Ejecutar el framework
sudo python main.py --check
```

### Estructura del Proyecto
```
WirelessPen/
├── main.py              # Script principal
├── config.py            # Configuración
├── tests/               # Tests unitarios
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── doc/                 # Documentación
├── scripts/             # Scripts de utilidad
└── .github/             # GitHub workflows
    └── workflows/
        └── ci.yml
```

### Flujo de Trabajo de Desarrollo

#### 1. Crear Branch de Feature
```bash
# Actualizar main
git checkout main
git pull upstream main

# Crear nueva branch
git checkout -b feature/nombre-descriptivo
```

#### 2. Desarrollar
```bash
# Hacer cambios
# Ejecutar tests frecuentemente
python -m pytest tests/

# Verificar estilo de código
flake8 main.py
black main.py
```

#### 3. Commit
```bash
# Commits atómicos con mensajes descriptivos
git add .
git commit -m "feat: agregar soporte para nuevo chipset MT7921"

# O para bug fixes:
git commit -m "fix: resolver issue con monitor mode en Realtek"
```

### Convenciones de Commit
Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva característica
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato (sin afectar funcionalidad)
- `refactor:` Refactoring de código
- `test:` Añadir o modificar tests
- `chore:` Cambios en build process o herramientas

## 📥 Pull Requests

### Antes de Enviar un PR
- [ ] Tests pasan (`python -m pytest`)
- [ ] Linting pasa (`flake8`, `black`, `mypy`)
- [ ] Documentación actualizada si es necesario
- [ ] CHANGELOG.md actualizado para cambios significativos
- [ ] Commits siguen convenciones
- [ ] Branch está actualizada con main

### Template de Pull Request
```markdown
**Descripción**
Descripción clara de los cambios realizados.

**Tipo de Cambio**
- [ ] Bug fix (cambio no-breaking que soluciona un issue)
- [ ] New feature (cambio no-breaking que añade funcionalidad)
- [ ] Breaking change (fix o feature que causa cambios en funcionalidad existente)
- [ ] Documentation update

**¿Cómo Ha Sido Probado?**
Describe los tests realizados para verificar los cambios.

**Checklist:**
- [ ] Mi código sigue las convenciones del proyecto
- [ ] He realizado self-review de mi código
- [ ] He comentado mi código en áreas difíciles de entender
- [ ] He actualizado la documentación correspondiente
- [ ] Mis cambios no generan warnings nuevos
- [ ] He añadido tests que prueban mi fix/feature
- [ ] Tests nuevos y existentes pasan localmente
```

## 🎨 Estilo de Código

### Python Code Style

#### Herramientas
- **Black**: Formateo automático de código
- **flake8**: Linting y detección de errores
- **mypy**: Type checking
- **isort**: Ordenamiento de imports

#### Configuración (.flake8)
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    venv,
    .venv
```

#### Configuración (pyproject.toml)
```toml
[tool.black]
line-length = 88
target-version = ['py36']

[tool.isort]
profile = "black"
line_length = 88
```

### Convenciones Específicas

#### Naming Conventions
```python
# Variables y funciones: snake_case
network_interface = "wlan0"
def scan_networks():
    pass

# Constantes: UPPER_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Classes: PascalCase
class GlobalState:
    pass

# Private methods: _prefijo
def _internal_helper():
    pass
```

#### Docstrings
```python
def attack_handshake(target: Dict[str, str]) -> bool:
    """
    Capture WPA/WPA2 handshake from target network.
    
    Args:
        target: Dictionary with network information including BSSID, ESSID, channel
    
    Returns:
        True if handshake captured successfully, False otherwise
    
    Raises:
        ValueError: If target information is invalid
        RuntimeError: If monitor mode is not active
    
    Example:
        >>> target = {'bssid': 'AA:BB:CC:DD:EE:FF', 'essid': 'TestNet', 'channel': '6'}
        >>> success = attack_handshake(target)
        >>> print(f"Attack successful: {success}")
    """
```

#### Type Hints
```python
from typing import List, Optional, Dict, Tuple, Any

def parse_networks(csv_file: str) -> List[Dict[str, str]]:
    """Parse airodump CSV and return list of networks."""
    
def run_command(cmd: str, timeout: Optional[int] = None) -> Tuple[int, str, str]:
    """Execute command and return exit code, stdout, stderr."""
```

## 🧪 Testing

### Estructura de Tests
```
tests/
├── unit/
│   ├── test_commands.py         # Test command execution
│   ├── test_network_parsing.py  # Test CSV parsing
│   ├── test_monitor_mode.py     # Test monitor activation
│   └── test_attacks.py          # Test attack functions
├── integration/
│   ├── test_full_handshake.py   # End-to-end handshake test
│   └── test_hardware_compat.py  # Hardware compatibility
├── fixtures/
│   ├── sample_scan.csv          # Sample airodump output
│   ├── mock_iwconfig.txt        # Mock iwconfig output
│   └── test_config.py           # Test configuration
└── conftest.py                  # Pytest configuration
```

### Escribir Tests

#### Unit Tests
```python
import pytest
from unittest.mock import patch, MagicMock
from main import run_command, parse_airodump_csv

def test_run_command_success():
    """Test successful command execution."""
    code, stdout, stderr = run_command("echo 'hello'")
    assert code == 0
    assert "hello" in stdout
    assert stderr == ""

def test_run_command_failure():
    """Test failed command execution."""
    code, stdout, stderr = run_command("false")
    assert code == 1

@patch('main.subprocess.run')
def test_run_command_timeout(mock_run):
    """Test command timeout handling."""
    mock_run.side_effect = subprocess.TimeoutExpired('cmd', 30)
    code, stdout, stderr = run_command("sleep 60", timeout=1)
    assert code == 124
    assert "timed out" in stderr
```

#### Integration Tests
```python
import pytest
import tempfile
import os

@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def test_full_handshake_workflow(temp_output_dir):
    """Test complete handshake capture workflow."""
    # Nota: Estos tests requieren hardware real y permisos root
    # Pueden ser skippeados en CI/CD
    if not os.geteuid() == 0:
        pytest.skip("Root privileges required")
    
    # Test implementation...
```

### Ejecutar Tests
```bash
# Todos los tests
python -m pytest

# Tests específicos
python -m pytest tests/unit/test_commands.py

# Con coverage
python -m pytest --cov=main --cov-report=html

# Verbose output
python -m pytest -v

# Skip integration tests
python -m pytest -m "not integration"
```

### Mocking para Tests
```python
@pytest.fixture
def mock_iwconfig():
    """Mock iwconfig command output."""
    return """
wlan0     IEEE 802.11  ESSID:off/any  
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on
"""

@patch('main.run_command')
def test_detect_wireless_cards(mock_run, mock_iwconfig):
    """Test wireless card detection."""
    mock_run.return_value = (0, "wlan0\nwlan1", "")
    
    cards = detect_wireless_cards()
    assert "wlan0" in cards
    assert "wlan1" in cards
```

## 📚 Documentación

### Tipos de Documentación

#### 1. Código (Docstrings)
- Todas las funciones públicas deben tener docstrings
- Usar formato Google/Sphinx style
- Incluir ejemplos cuando sea apropiado

#### 2. API Documentation
- Generar automáticamente con Sphinx
- Mantener actualizada con cambios de código

#### 3. User Documentation
- Guías paso a paso
- Ejemplos prácticos
- Troubleshooting común
- FAQs

#### 4. Technical Documentation
- Arquitectura del sistema
- Diagramas de flujo
- Especificaciones técnicas

### Actualizar Documentación
```bash
# Generar documentación API
sphinx-build -b html doc/ doc/_build/

# Verificar enlaces rotos
sphinx-build -b linkcheck doc/ doc/_build/

# Servir documentación localmente
cd doc/_build && python -m http.server
```

### Markdown Style Guide
- Usar headers jerárquicos (#, ##, ###)
- Incluir tabla de contenidos para docs largos
- Usar code blocks con syntax highlighting
- Añadir emojis para mejorar legibilidad
- Incluir screenshots cuando sea útil

## 🏆 Reconocimiento de Contribuidores

### Hall of Fame
Los contribuidores serán reconocidos en:
- README principal del proyecto
- Release notes
- Documentación de contributors
- Menciones en commits y PRs

### Tipos de Contribución
- 💻 **Code**: Contribuciones de código
- 📖 **Documentation**: Mejoras en documentación
- 🐛 **Bug Reports**: Reportes de bugs detallados
- 💡 **Ideas**: Sugerencias de características
- 🤔 **Answering Questions**: Ayuda en issues
- 📢 **Outreach**: Promoción del proyecto
- 🧪 **Testing**: Testing en diferentes plataformas

## 📞 Obtener Ayuda

### Canales de Comunicación
- **GitHub Issues**: Para bugs y feature requests
- **GitHub Discussions**: Para preguntas generales
- **Email**: [crypt0xdev@protonmail.com](mailto:crypt0xdev@protonmail.com)

### Recursos Útiles
- [Python Style Guide](https://pep8.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)

## 📄 Licencia

Al contribuir a WirelessPen, aceptas que tus contribuciones serán licenciadas bajo la [MIT License](../LICENSE).

---

¡Gracias por tu interés en mejorar WirelessPen! Cada contribución, sin importar su tamaño, es valiosa para la comunidad de seguridad.