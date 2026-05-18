#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 0, 200); 

const char* laptopIP = "192.168.0.112"; 
const unsigned int laptopPort = 5005;
const unsigned int localPort = 8888;

EthernetUDP Udp;
char packetBuffer[255];
unsigned long tiempoUltimaTelemetria = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) { ; } 
  
  Ethernet.init(21); 
  Serial.println("Iniciando red con IP estática...");
  
  Ethernet.begin(mac, ip);
  delay(1000);
  
  Serial.print("Conectado. IP ESP32 a: ");
  Serial.println(Ethernet.localIP());
  
  Udp.begin(localPort);
}

void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) {
      char comando = packetBuffer[0];
      if (comando == 'w') Serial.println("Motores: AVANZANDO");
      else if (comando == 's') Serial.println("Motores: RETROCEDIENDO");
      else if (comando == 'a') Serial.println("Motores: IZQUIERDA");
      else if (comando == 'd') Serial.println("Motores: DERECHA");
    }
  }

  if (millis() - tiempoUltimaTelemetria > 2000) {
    tiempoUltimaTelemetria = millis();
    Udp.beginPacket(laptopIP, laptopPort);
    Udp.print("Profundidad: 1.2m | Tension ok | Sin alertas");
    Udp.endPacket();
  }
}