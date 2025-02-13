from machine import Pin, PWM
import network
import socket
from utime import sleep
import _thread  # Para ejecutar el servidor en un hilo separado

# ----------------------------
# Configuración de la conexión WiFi
# ----------------------------
SSID = ''  # Nombre de la red WiFi
PASSWORD = 'alecamgg'  # Contraseña de la red WiFi
wlan = network.WLAN(network.STA_IF)

wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Espera hasta que se establezca la conexión
while not wlan.isconnected():
    pass

print(f'Conexión con el WiFi {SSID} establecida')
print(wlan.ifconfig())

# ----------------------------
# Configuración del servo motor
# ----------------------------
SERVO_PIN = 13
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)  # Frecuencia de 50 Hz

# ----------------------------
# Configuración del botón físico
# ----------------------------
BOTON_PIN = 32
boton_fisico = Pin(BOTON_PIN, Pin.IN, Pin.PULL_UP)

# ----------------------------
# Configuración de los LEDs
# ----------------------------
LED_ROJO_PIN = 14
LED_VERDE_PIN = 27
led_rojo = Pin(LED_ROJO_PIN, Pin.OUT)
led_verde = Pin(LED_VERDE_PIN, Pin.OUT)

# Encender el LED rojo al inicio para indicar estado inactivo
led_rojo.value(1)

# ----------------------------
# Estado del sistema
# ----------------------------
estado_servo = False  # False: 90° (reposo), True: -30° (activado)

# ----------------------------
# Función para mover el servo a un ángulo determinado
# ----------------------------
def mover_servo(angulo):
    pulso_min = 1000  # Pulso mínimo en microsegundos
    pulso_max = 2500  # Pulso máximo en microsegundos
    pulso = pulso_min + (angulo / 180) * (pulso_max - pulso_min)
    servo.duty_u16(int(pulso * 65535 / 20000))

# ----------------------------
# Función para actualizar el estado del servo y los LEDs
# ----------------------------
def actualizar_estado(nuevo_estado):
    global estado_servo
    estado_servo = nuevo_estado
    
    if estado_servo:
        mover_servo(-30)  # Posición activa del servo
        led_rojo.value(0)  # Apagar LED rojo
        led_verde.value(1)  # Encender LED verde
    else:
        mover_servo(90)  # Posición de reposo del servo
        led_rojo.value(1)  # Encender LED rojo
        led_verde.value(0)  # Apagar LED verde

# ----------------------------
# Manejo de interrupción del botón físico
# ----------------------------
def boton_irq(pin):
    sleep(0.1)  # Pequeño debounce
    if boton_fisico.value() == 0:
        actualizar_estado(not estado_servo)

boton_fisico.irq(trigger=Pin.IRQ_FALLING, handler=boton_irq)

# ----------------------------
# Función para generar la página web del servidor
# ----------------------------
def web_page():
    return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dispensador de comida Automatizado</title>
</head>
<body>
    <h1>Bienvenido a Atenea's Candy</h1>
    <button onclick="toggleButton()">Presionar Botón</button>
    <p id="status">Estado: En reposo</p>
    <script>
        function toggleButton() {
            fetch('/toggle')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('status').innerText = "Estado: " + data;
                });
        }
        setInterval(() => {
            fetch('/status')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('status').innerText = "Estado: " + data;
                });
        }, 1000);
    </script>
</body>
</html>"""

# ----------------------------
# Servidor web ejecutado en un hilo separado
# ----------------------------
def servidor_web():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()
        
        if '/toggle' in request:
            actualizar_estado(not estado_servo)
            response = "Activado" if estado_servo else "En reposo"
            conn.send(f'HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{response}'.encode())
        elif '/status' in request:
            response = "Activado" if estado_servo else "En reposo"
            conn.send(f'HTTP/1.1 200 OK\nContent-Type: text/plain\n\n{response}'.encode())
        else:
            conn.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n'.encode() + web_page().encode())
        
        conn.close()

# ----------------------------
# Iniciar el servidor en un hilo separado
# ----------------------------
_thread.start_new_thread(servidor_web, ())

# Bucle infinito para mantener el ESP32 en ejecución
while True:
    sleep(1)

