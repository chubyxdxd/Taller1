# ROV Subacuático para Inspección de Estructuras Hidráulicas 

Este repositorio contiene el código fuente del sistema de telemetría, control y visión en tiempo real para un ROV (Remotely Operated Vehicle) subacuático. El proyecto está diseñado específicamente para la inspección de superficies planas verticales, como muros de represas, facilitando la detección de patologías en el concreto (como microfisuras) mediante visión artificial.

El sistema utiliza una arquitectura de red local (LAN) estática basada en el protocolo UDP para garantizar una latencia mínima en la transmisión de video y una respuesta inmediata en el control de motores.

## Arquitectura del Sistema (Nodos)

El proyecto está dividido en tres nodos principales que se comunican de manera simultánea e ininterrumpida:

1. **Estación de Superficie (Laptop con Ubuntu)**
   - Actúa como el centro de mando.
   - Utiliza **multithreading (hilos)** en Python para procesar el flujo de video y escuchar la telemetría de los sensores de manera concurrente, sin bloqueos.
   - Captura eventos de teclado (`W`, `A`, `S`, `D`) a través de OpenCV para enviar comandos de maniobra hacia el microcontrolador.

2. **Nodo de Visión Artificial (Raspberry Pi 4)**
   - Se encarga de la captura óptica y el preprocesamiento de imágenes.
   - Captura fotogramas, los comprime en formato JPEG (calidad ajustable) para evitar saturar el ancho de banda del cable umbilical y los transmite a la superficie.

3. **Nodo de Control Físico (ESP32 + W5500)**
   - Cerebro de bajo nivel del ROV.
   - Conectado a la red mediante un módulo Ethernet W5500 por SPI.
   - Recibe los comandos de movimiento y gestiona los propulsores.
   - Transmite telemetría continua (profundidad, estado estructural) de forma no bloqueante utilizando temporizadores (`millis()`).

## Tecnologías y Dependencias

- **Hardware:** ESP32, Módulo Ethernet W5500, Raspberry Pi 4.
- **Lenguajes:** Python 3 (Superficie y Visión), C++ (Control).
- **Librerías Python:** `opencv-python` (`cv2`), `numpy`, `socket`, `threading`.
- **Librerías Arduino:** `SPI.h`, `Ethernet.h`, `EthernetUdp.h`.

## Configuración de Red

El sistema requiere que los tres nodos operen bajo la misma subred. Se recomienda asignar direcciones IP estáticas para garantizar una conexión inmediata al encender el sistema.

*Ejemplo de topología utilizada:*
- **Gateway/Router:** `192.168.0.1`
- **Laptop (Superficie):** `192.168.0.112`
- **ESP32 (Control):** `192.168.0.200`
- **Raspberry Pi (Visión):** Asignación por DHCP o IP estática compatible (Ej. `192.168.0.x`).

**Puertos UDP utilizados:**
- `5005`: Telemetría y comandos (tráfico de texto bidireccional).
- `5006`: Flujo de video (tráfico de bytes masivo unidireccional).

## Uso y Ejecución

1. **Preparar el Hardware:** Conecta la laptop, la Raspberry Pi y el módulo W5500 de la ESP32 al mismo router o switch de red.

2. **Nodo de Control:** Sube el código C++ a la ESP32 usando Arduino IDE.

3. **Nodo de Visión:** En la Raspberry Pi, ejecuta el script de transmisión de video:

```bash
python3 nodo_vision.py
```

4. **Estación de Superficie:** En la laptop con Ubuntu, ejecuta el centro de mando:

```bash
python3 nodo_superficie.py
```

5. **Control:** Haz clic en la ventana de video que se abrirá en tu laptop y utiliza las teclas `W`, `A`, `S`, `D` para navegar por el muro. Presiona `Q` para cerrar el sistema de forma segura.

