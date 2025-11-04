# WirelessPen v2.2.0 - Guía de Usuario

## 📖 Índice
- [Introducción](#introducción)
- [Instalación](#instalación)
- [Primeros Pasos](#primeros-pasos)
- [Modos de Ataque](#modos-de-ataque)
- [Ejemplos Prácticos](#ejemplos-prácticos)
- [Solución de Problemas](#solución-de-problemas)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## 📡 Introducción

WirelessPen es un framework profesional para pruebas de penetración inalámbrica diseñado para profesionales de seguridad y propósitos educativos. Esta guía te ayudará a utilizar todas las funcionalidades del framework de manera efectiva y responsable.

### Características Principales
- ✅ Captura de handshakes WPA/WPA2/WPA3
- ✅ Ataques PMKID sin clientes
- ✅ Explotación de vulnerabilidades WPS
- ✅ Ataques Evil Twin
- ✅ Deautenticación dirigida
- ✅ Reconocimiento de redes avanzado

## 🛠️ Instalación

### Instalación Automática (Recomendada)
```bash
# Descargar e instalar
sudo ./install.sh

# Verificar instalación
sudo wirelesspen --check
```

### Instalación Manual
```bash
# Instalar dependencias principales
sudo apt update
sudo apt install -y aircrack-ng wireless-tools iw macchanger ethtool

# Instalar herramientas opcionales
sudo apt install -y reaver bully hcxtools hashcat hostapd dnsmasq

# Hacer ejecutable
chmod +x main.py

# Crear enlace simbólico (opcional)
sudo ln -sf $(pwd)/main.py /usr/local/bin/wirelesspen
```

## 🚀 Primeros Pasos

### 1. Verificación del Sistema
```bash
# Verificar dependencias y hardware
sudo wirelesspen --check

# Listar interfaces WiFi disponibles
sudo wirelesspen --interfaces

# Diagnósticos detallados del adaptador
sudo wirelesspen --diagnostics -i wlan0
```

### 2. Modo Interactivo (Recomendado para Principiantes)
```bash
# Iniciar modo interactivo
sudo wirelesspen

# Comandos disponibles en el modo interactivo:
# help      - Mostrar ayuda
# scan      - Escanear redes
# handshake - Ataque de handshake
# pmkid     - Ataque PMKID
# wps       - Ataque WPS
# deauth    - Ataque de deautenticación
# status    - Estado de la sesión
# exit      - Salir
```

### 3. Escaneo Básico de Redes
```bash
# Escaneo rápido (30 segundos)
sudo wirelesspen scan -i wlan0

# Escaneo extendido (2 minutos)
sudo wirelesspen scan -i wlan0 --scan-time 120

# Escaneo de canal específico
sudo wirelesspen scan -i wlan0 --channel 6
```

## 🎯 Modos de Ataque

### 1. 🤝 Captura de Handshake WPA/WPA2

**Descripción**: Captura el handshake de 4 vías para descifrado offline.

**Uso Básico**:
```bash
sudo wirelesspen handshake -i wlan0
```

**Opciones Avanzadas**:
```bash
# Con parámetros personalizados
sudo wirelesspen handshake -i wlan0 \
  --deauth-count 30 \
  --timeout 600 \
  --verbose

# Dirigido a una red específica
sudo wirelesspen handshake -i wlan0 -t AA:BB:CC:DD:EE:FF
```

**Proceso**:
1. Escaneo automático de redes
2. Selección del objetivo
3. Detección de clientes conectados
4. Deautenticación inteligente
5. Captura y verificación del handshake
6. Conversión a formato hashcat

### 2. 🔑 Ataque PMKID (Sin Clientes)

**Descripción**: Ataque clientless que extrae PMKID directamente del AP.

**Uso**:
```bash
# Básico
sudo wirelesspen pmkid -i wlan0

# Automático con directorio personalizado
sudo wirelesspen pmkid --auto -i wlan0 -o /tmp/pmkid_results
```

**Ventajas**:
- No requiere clientes conectados
- Más rápido que handshake tradicional
- Funciona con muchos routers modernos

### 3. 📡 Ataques WPS

**Descripción**: Explota vulnerabilidades en WPS (WiFi Protected Setup).

**PIN Brute Force**:
```bash
sudo wirelesspen wps -i wlan0 --timeout 900
```

**Pixie Dust (CVE-2014-4910)**:
```bash
sudo wirelesspen pixie -i wlan0
```

**Características**:
- Detección automática de WPS habilitado
- Evita bloqueos por intentos fallidos
- Soporte para múltiples herramientas (reaver, bully)

### 4. 👻 Evil Twin Attack

**Descripción**: Despliega un punto de acceso falso para interceptar tráfico.

```bash
sudo wirelesspen evil_twin -i wlan0
```

**Proceso**:
1. Clonación del AP objetivo
2. Deautenticación del AP real
3. Despliegue del AP falso
4. Captura de credenciales

**⚠️ Advertencia**: Este ataque causa interrupciones de servicio.

### 5. 💥 Deautenticación Masiva

**Descripción**: Desconecta clientes del punto de acceso.

```bash
# Deauth dirigido
sudo wirelesspen deauth -i wlan0

# Con parámetros personalizados
sudo wirelesspen deauth -i wlan0 --deauth-count 100
```

**⚠️ Uso Ético**: Solo en redes autorizadas para testing.

## 💡 Ejemplos Prácticos

### Escenario 1: Auditoría de Red Doméstica
```bash
# 1. Verificar sistema
sudo wirelesspen --check

# 2. Escanear redes cercanas
sudo wirelesspen scan -i wlan0 --scan-time 60

# 3. Intentar PMKID (sin interrumpir servicio)
sudo wirelesspen pmkid -i wlan0

# 4. Si PMKID falla, usar handshake
sudo wirelesspen handshake -i wlan0
```

### Escenario 2: Evaluación WPS
```bash
# 1. Escanear redes con WPS
sudo wirelesspen scan -i wlan0

# 2. Filtrar solo redes WPS (en modo interactivo)
sudo wirelesspen
> scan
> # Filtrar por WPS en la selección

# 3. Probar Pixie Dust primero
sudo wirelesspen pixie -i wlan0

# 4. Si falla, intentar brute force
sudo wirelesspen wps -i wlan0
```

### Escenario 3: Pruebas de Resistencia
```bash
# 1. Medir tiempo de reconexión tras deauth
sudo wirelesspen deauth -i wlan0 --deauth-count 10

# 2. Probar detección de evil twin
sudo wirelesspen evil_twin -i wlan0
```

## 🔧 Solución de Problemas

### Problema: No se activa modo monitor
```bash
# Diagnóstico
sudo wirelesspen --diagnostics -i wlan0

# Soluciones manuales
sudo airmon-ng check kill
sudo ip link set wlan0 down
sudo iw wlan0 set type monitor
sudo ip link set wlan0 up

# Verificar
iwconfig wlan0
```

### Problema: No se detectan redes
```bash
# Verificar antena
iwconfig wlan0

# Probar diferentes canales
sudo wirelesspen scan -i wlan0 --channel 1
sudo wirelesspen scan -i wlan0 --channel 6
sudo wirelesspen scan -i wlan0 --channel 11

# Aumentar tiempo de escaneo
sudo wirelesspen scan -i wlan0 --scan-time 120
```

### Problema: Handshake no se captura
```bash
# Verificar clientes conectados
# Aumentar número de paquetes deauth
sudo wirelesspen handshake -i wlan0 --deauth-count 50

# Probar PMKID como alternativa
sudo wirelesspen pmkid -i wlan0

# Verificar que no sea WPA3
```

### Problema: Errores de dependencias
```bash
# Reinstalar dependencias principales
sudo apt update
sudo apt install --reinstall aircrack-ng wireless-tools iw

# Verificar versiones
aircrack-ng --version
iwconfig --version
```

## ❓ Preguntas Frecuentes

### ¿Qué adaptadores WiFi son compatibles?
- **Totalmente compatibles**: Realtek (RTL8812AU, RTL8821AU), Atheros (AR9271, ATH9K)
- **Limitados**: Intel (sin inyección), Broadcom (varía según modelo)
- **Recomendados**: TP-Link AC600 T2U, Alfa AWUS036ACS

### ¿Es legal usar WirelessPen?
- ✅ **Legal**: En redes propias o con autorización explícita
- ❌ **Ilegal**: En redes ajenas sin permiso
- 📄 **Siempre**: Obtener autorización por escrito

### ¿Funciona con WPA3?
- **Parcial**: Algunos ataques PMKID pueden funcionar
- **Limitado**: WPA3 tiene mejores protecciones
- **Recomendado**: Usar herramientas específicas para WPA3

### ¿Cuánto tiempo toma capturar un handshake?
- **Con clientes activos**: 30 segundos - 5 minutos
- **Sin clientes**: Usar PMKID (1-2 minutos)
- **Factores**: Actividad de la red, potencia de señal, configuración del router

### ¿Cómo mejorar las probabilidades de éxito?
1. **Ubicación**: Acercarse al punto de acceso
2. **Horario**: Usar durante horas de actividad (tarde/noche)
3. **Paciencia**: Algunos routers tardan en responder
4. **Múltiples métodos**: Probar PMKID, handshake, WPS

### ¿Qué hacer con los archivos capturados?
```bash
# Para handshakes (.cap)
aircrack-ng -w wordlist.txt capture.cap
hashcat -m 22000 capture.hc22000 wordlist.txt

# Para PMKID (.hash)
hashcat -m 16800 pmkid.hash wordlist.txt
```

### ¿Dónde encontrar wordlists?
- `/usr/share/wordlists/rockyou.txt` (Kali Linux)
- [SecLists](https://github.com/danielmiessler/SecLists)
- [Kaonashi](https://github.com/kaonashi-passwords/Kaonashi)
- Crear wordlists personalizados con `crunch`

## 📚 Recursos Adicionales

### Documentación Técnica
- [doc/TECHNICAL.md](TECHNICAL.md) - Documentación técnica detallada
- [doc/API.md](API.md) - Referencia de la API
- [doc/CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución

### Enlaces Útiles
- [Aircrack-ng Documentation](https://www.aircrack-ng.org/documentation.html)
- [Hashcat Wiki](https://hashcat.net/wiki/)
- [WiFi Security Research](https://www.krackattacks.com/)

### Comunidad
- [GitHub Issues](https://github.com/Crypt0xDev/WirelessPen/issues)
- [Security Forums](https://forum.aircrack-ng.org/)
- [Reddit r/netsec](https://reddit.com/r/netsec)

---

## ⚖️ Recordatorio Legal

**WirelessPen es solo para uso educativo y evaluaciones de seguridad autorizadas. El uso no autorizado de estas técnicas puede ser ilegal y resultar en consecuencias legales graves. Siempre obtén autorización explícita antes de realizar cualquier prueba de penetración.**