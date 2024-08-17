#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);        // For debugging
  SerialBT.begin("ESP32_BT");  // Name of the Bluetooth device
  Serial.println("Bluetooth Started");
}

void loop() {
  if (SerialBT.available()) {
    char incomingByte = SerialBT.read();
    Serial.write(incomingByte); // Forward to ATmega328P
  }

  if (Serial.available()) {
    char incomingByte = Serial.read();
    SerialBT.write(incomingByte); // Forward to Bluetooth
  }
}
