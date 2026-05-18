import socket
import threading
import cv2
import numpy as np

ESP32_IP = "192.168.0.200"
ESP32_PORT = 8888
LAPTOP_IP = "0.0.0.0"

sock_esp32 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_esp32.bind((LAPTOP_IP, 5005))

sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_video.bind((LAPTOP_IP, 5006))

sock_video.settimeout(0.1) 

def escuchar_telemetria_esp32():
    while True:
        try:
            data, _ = sock_esp32.recvfrom(1024)
            print(f"\n[Telemetría]: {data.decode('utf-8')}")
        except Exception:
            pass

hilo_telemetria = threading.Thread(target=escuchar_telemetria_esp32, daemon=True)
hilo_telemetria.start()

print("Estación de superficie iniciada...")

cv2.namedWindow("Vision Subacuatica", cv2.WINDOW_NORMAL)
print("Video para navegar. 'Q' para salir.")

while True:
    try:
        data, addr = sock_video.recvfrom(65535)
        np_arr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if frame is not None:
            cv2.imshow("Vision Subacuatica", frame)
            
    except socket.timeout:
        pass
    except Exception as e:
        pass
        
    tecla = cv2.waitKey(1) & 0xFF
    
    if tecla == ord('w'):
        sock_esp32.sendto(b"w", (ESP32_IP, ESP32_PORT))
        print("Control: ARRIBA")
    elif tecla == ord('s'):
        sock_esp32.sendto(b"s", (ESP32_IP, ESP32_PORT))
        print("Control: ABAJO")
    elif tecla == ord('a'):
        sock_esp32.sendto(b"a", (ESP32_IP, ESP32_PORT))
        print("Control: IZQUIERDA")
    elif tecla == ord('d'):
        sock_esp32.sendto(b"d", (ESP32_IP, ESP32_PORT))
        print("Control: DERECHA")
    elif tecla == ord('q'):
        print("Cerrando estación de control...")
        break

cv2.destroyAllWindows()
sock_esp32.close()
sock_video.close()
