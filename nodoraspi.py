import cv2
import socket
import time

LAPTOP_IP = "192.168.0.112"  
LAPTOP_PORT_VIDEO = 5006     

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

print(f"Iniciando transmisión de frames a {LAPTOP_IP}:{LAPTOP_PORT_VIDEO}...")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error leyendo cámara")
            time.sleep(0.5)
            continue
            
        codificado_exitoso, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        
        if codificado_exitoso:
            bytes_imagen = buffer.tobytes()
            
            try:
                sock.sendto(bytes_imagen, (LAPTOP_IP, LAPTOP_PORT_VIDEO))
                print(f"Fotograma enviado: {len(bytes_imagen)} bytes")
            except Exception as e:
                print("El frame superó el límite de bytes UDP o hay caída de red.", e)
                
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\nTransmisión de cámara finalizada.")
finally:
    cap.release()
    sock.close()
