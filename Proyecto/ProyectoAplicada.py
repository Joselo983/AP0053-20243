from machine import Pin, PWM
import network
import socket
from utime import sleep
import _thread  # Para ejecutar el servidor en un hilo separado

# Configuración del WiFi
ssid = 'moto g(6) 4250'
password = '1013591400'
wlan = network.WLAN(network.STA_IF)

wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

print('Conexión con el WiFi %s establecida' % ssid)
print(wlan.ifconfig())

# Configuración del servo
servo_pin = 13
servo = PWM(Pin(servo_pin))
servo.freq(50)

# Configuración del botón físico con interrupción
boton_pin = 32
boton_fisico = Pin(boton_pin, Pin.IN, Pin.PULL_UP)

# Configuración de los LEDs
led_rojo_pin = 14
led_verde_pin = 27
led_rojo = Pin(led_rojo_pin, Pin.OUT)
led_verde = Pin(led_verde_pin, Pin.OUT)

# Encender el LED rojo al iniciar
led_rojo.value(1)  # Asegura que el LED rojo esté encendido desde el inicio

# Estado del sistema
estado_servo = False  # False: 90° (reposo), True: -30° (activado)

# Función para mover el servo
def mover_servo(angulo):
    pulso_min = 1000
    pulso_max = 2500
    pulso = pulso_min + (angulo / 180) * (pulso_max - pulso_min)
    servo.duty_u16(int(pulso * 65535 / 20000))

# Función para actualizar el estado
def actualizar_estado(nuevo_estado):
    global estado_servo
    estado_servo = nuevo_estado
    if estado_servo:
        mover_servo(-30)
        led_rojo.value(0)
        led_verde.value(1)
    else:
        mover_servo(90)
        led_rojo.value(1)
        led_verde.value(0)

# Interrupción del botón físico
def boton_irq(pin):
    sleep(0.1)  # Pequeño debounce
    if boton_fisico.value() == 0:
        actualizar_estado(not estado_servo)

boton_fisico.irq(trigger=Pin.IRQ_FALLING, handler=boton_irq)

# Página web con actualización en tiempo real
def web_page():
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dispensador de comida Automatizado</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background: url('https://github.com/AlecamG/Proyecto/blob/main/pexels-cottonbro-9667253.jpg?raw=true') no-repeat center center fixed;
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #fff;
        }
        .container {
            max-width: 900px;
            margin: 20px auto;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #2980b9;
        }
        h2 {
            border-bottom: 2px solid #2980b9;
            padding-bottom: 5px;
            color: #2c3e50;
        }
        h2, h3 {
            border-bottom: 2px solid #2980b9;
            padding-bottom: 5px;
            color: #000;
        }
        p, ul {
            font-size: 1.1em;
            line-height: 1.6;
            color: #2c3e50;
        }
        ul {
            list-style-type: square;
            padding-left: 20px;
        }
        .section {
            margin-bottom: 20px;
            padding: 15px;
            background: #ecf0f1;
            border-radius: 10px;
        }
        footer {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            background: #2c3e50;
            color: white;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
    <h1>Bienvenido a Terry's and Thomas</h1>
    <p class="subtitulo">Realizado por: Juan Esteban Silva Santisteban-20231005159, Jose David Ardila Sanabria-20231005064 y Juan Pablo Sarta Fierro-20231005174</p>
    <h1>Control de Servo y LEDs</h1>
    
    <div class="button-container">
        <button class="big-button" onclick="toggleButton()">Presionar Botón</button>
        <p id="status">Estado: En reposo</p>
    </div>
</div>

<style>
    .container {
        text-align: center;
    }
    
    .button-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
    }
    
    .big-button {
        font-size: 20px;
        padding: 15px 30px;
        margin-bottom: 10px;
    }
    
    #status {
        font-size: 18px;
        font-weight: bold;
    }
</style>


    <script>
        function toggleButton() {
            fetch('/toggle')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('status').innerText = "Estado: " + data;
                });
        }

        function updateStatus() {
            fetch('/status')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('status').innerText = "Estado: " + data;
                });
        }

        setInterval(updateStatus, 1000);  // Actualiza cada segundo
    </script>
        <div class="section">
            <h2>Introducción</h2>
            <p>En la actualidad, el cuidado de las mascotas es una prioridad para muchas personas, quienes buscan soluciones prácticas y efectivas que faciliten su vida diaria. Una de las principales dificultades que enfrentan los dueños de mascotas es el manejo del alimento en grandes cantidades, lo cual puede generar incomodidades al momento de servir las raciones diarias.</p>
        </div>        
        <div class="section">
            <h2>Descripción del problema</h2>
            <p>Muchos dueños de mascotas optan por comprar bolsas grandes de alimento para economizar, pero al momento de servir las raciones, manipular estas bolsas resulta incómodo, especialmente cuando se hace de manera frecuente. La falta de un sistema práctico para almacenar y dispensar porciones adecuadas de alimento puede generar conflictos, desorden y pérdida de tiempo.</p>
        </div>
        
        <div class="section">
            <h2>Objetivos</h2>
            <p>El objetivo de este proyecto es desarrollar un dispensador de alimentos automatizado utilizando un microcontrolador ESP32. Este dispositivo será capaz de almacenar entre 4 y 5 porciones de alimento, permitiendo a los dueños de mascotas dispensar las raciones necesarias de manera remota y eficiente.</p>
        </div>
      
        <div class="section">
            <h2>Componentes a utilizar</h2>
            <ul>
                <li>ESP 32</li>
                <li>Servo motor SG90</li>
                <li>Jumpers</li>
                <li>2 resistencias de 18 ohms</li>
                <li>1 LED rojo</li>
                <li>1 LED verde</li>
                <li>Cable micro usb para la alimentación del Esp 32</li>
                <li>Un telefono o Computador con acceso a internet</li>
                <li>Software: Thonny y Visual Studio Code</li>
            </ul>
        </div>
        <div class="section">
            <h2>Diseño del producto:</h2>
            <div class="section">
                <h2>Electronico:</h2>    
                <div class="image-container">
                    <img src="https://github.com/AlecamG/Proyecto/blob/main/Proyecto%20programacion.png?raw=true" alt="Montaje electronico" class="imagen-seccion">
                </div>
            </div>
            <style>
                .image-container {
                    text-align: center; /* Centra la imagen dentro del contenedor */
                    margin: 20px 0; /* Espaciado alrededor de la imagen */
                }
            
                .image-container img {
                    width: 60%; /* Ajusta el tamaño al 80% del contenedor */
                    max-width: 600px; /* Limita el tamaño máximo de la imagen */
                    height: auto; /* Mantiene la relación de aspecto de la imagen */
                }
            </style>

            <div class="section">
                <h2>Montaje final:</h2>
                <div class="image-container">
                    <img src="https://github.com/AlecamG/Proyecto/blob/main/Montaje%20practico.png?raw=true" alt="Montaje electronico" class="imagen-seccion">
                </div>
            </div>
            <style>
                .image-container {
                    text-align: center; /* Centra la imagen dentro del contenedor */
                    margin: 20px 0; /* Espaciado alrededor de la imagen */
                }
            
                .image-container img {
                    width: 60%; /* Ajusta el tamaño al 80% del contenedor */
                    max-width: 600px; /* Limita el tamaño máximo de la imagen */
                    height: auto; /* Mantiene la relación de aspecto de la imagen */
                }
            </style>
            <div class="section">
                
        </div>

        <div class="section">
            <h2>Proceso de la construcción</h2>
            <p>El desarrollo del dispensador de alimentos automatizado con un microcontrolador ESP32 se llevó a cabo en varias etapas, desde la programación inicial hasta el ensamblaje final del dispositivo. A continuación, se detallan los pasos seguidos durante la construcción del prototipo.</p>
            
            <h3>1. Programación y pruebas iniciales</h3>
            <p>La primera fase del proyecto consistió en la programación del ESP32 para controlar el servomotor SG90. Se inició con un código simple que permitía al servomotor girar automáticamente 90 grados, simulando la apertura y cierre del dispensador de alimentos.</p>
            <p>Una vez verificado el funcionamiento básico del servomotor, se incorporó un pulsador que permitiera controlar el movimiento del servo de manera manual.</p>
            
            <h3>2. Incorporación de indicadores luminosos</h3>
            <p>Se agregaron dos LEDs para indicar el estado del dispensador:</p>
            <ul>
                <li><b>LED rojo:</b> Indica que el dispensador está en estado "cerrado".</li>
                <li><b>LED verde:</b> Indica que el dispensador está en estado "abierto".</li>
            </ul>
            
            <h3>3. Construcción del mecanismo de dispensador</h3>
            <p>Se utilizó un tubo cilíndrico para almacenar el alimento y una hélice acoplada al servomotor para regular su salida.</p>
            
            <h3>4. Ensamblaje del sistema electrónico</h3>
            <p>Los componentes electrónicos se soldaron y organizaron en una protoboard compacta dentro de la estructura del dispensador.</p>
            
            <h3>5. Integración y pruebas finales</h3>
            <p>Se realizaron pruebas para verificar la correcta operación del servomotor, LEDs y pulsador, asegurando la funcionalidad del dispensador.</p>
        </div>

        <div class="section">
            <h2>Conclusiones</h2>
            <p>El desarrollo del dispensador de alimentos automatizado con un microcontrolador ESP32 ha demostrado ser una solución efectiva para mejorar la experiencia de los dueños de mascotas al enfrentar el reto de manejar y servir raciones de alimento de manera eficiente.  </p>
            <p>No solo optimiza la alimentación de las mascotas, sino que también representa una aplicación práctica de la programación y la electrónica en la vida cotidiana. A través de la integración de un ESP32, servomotores y sensores visuales, se logró diseñar un sistema eficiente y accesible, que demuestra la importancia de la automatización en la mejora de tareas rutinarias. Además, este proyecto abre la puerta a futuras mejoras, como la incorporación de control remoto mediante una aplicación móvil o la adaptación a diferentes tipos de alimentos. </p>
        </div>

        <div class="section">
            <h2>Nuestra inspiración:</h2>
            <div class="image-row">
                <img src="https://github.com/Joselo983/AP0053-20243/blob/main/Proyecto/b88342d9-ec24-4ab0-820a-e1e5adca3939.jpeg?raw=true" alt="Atenea">
                <img src="https://github.com/Joselo983/AP0053-20243/blob/main/Proyecto/8B2C971C-00F4-4CFC-9F81-D3FDFCD374CF.jpeg?raw=true" alt="Candy">
            </div>
            
            <style>
                .image-row {
                    display: flex; /* Activa el modelo flexbox */
                    justify-content: space-between; /* Espacio entre las imágenes */
                    gap: 10px; /* Espacio entre las imágenes */
                    margin: 20px 0; /* Espaciado alrededor del contenedor */
                }
            
                .image-row img {
                    max-width: 50%; /* Hace que la imagen no se desborde */
                    height: auto; /* Mantiene la relación de aspecto de la imagen */
                    border-radius: 10px; /* Bordes redondeados */
                }
            </style>
            <p> Terry y Thomas, ellos dos nos inspiraron a relizar este proyecto, ya que queremos darle un mejor cuidado. </p>
        </div>
    </div>
    <footer>
        <p>&copy; 2025 Proyecto de Dispensador de Alimentos Automatizado</p>
    </footer>
</body>
</html>"""
    return html

# Servidor web en un hilo separado
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
            conn.send('HTTP/1.1 200 OK\nContent-Type: text/plain\n\n' + response)

        elif '/status' in request:
            response = "Activado" if estado_servo else "En reposo"
            conn.send('HTTP/1.1 200 OK\nContent-Type: text/plain\n\n' + response)

        else:
            response = web_page()
            conn.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + response)

        conn.close()

# Ejecutar el servidor en un hilo separado
_thread.start_new_thread(servidor_web, ())

# Bucle infinito para mantener el ESP32 funcionando
while True:
    sleep(1)