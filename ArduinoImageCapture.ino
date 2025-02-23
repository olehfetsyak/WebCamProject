#include <Wire.h>
#include <SPI.h>
#include <ArduCAM.h>
#include <SD.h>

#define CS_PIN 7

ArduCAM myCAM(OV2640, CS_PIN);

void setup() {
  // Sets the baud rate for communication
  Serial.begin(115200);
  
  SPI.begin();

  // "Resets" Camera
  myCAM.InitCAM(); 

  // Self explanatory
  myCAM.set_format(JPEG); 
  myCAM.OV2640_set_JPEG_size(OV2640_320x240);

  // Configure PIN as iutput
  pinMode(CS_PIN, OUTPUT);
  // Send hgh Volt.
  digitalWrite(CS_PIN, HIGH);
}

void loop() {
  // Clear any previous image stored in buffer
  myCAM.clear_fifo_flag();
  myCAM.flush_fifo();
  
  myCAM.start_capture();

  // Wait for image to be captured, get_bit waits to recieve the final JPEG bit from the capture
  while (!myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK)) {};

  // Send each byte of the image from the fifi buffer over the cable
  uint32_t length = myCAM.read_fifo_length();
  
  delay(1000);

  // Prepare camera for sending bytes
  myCAM.set_fifo_burst();

  // Send bytes one by one over the cable
  for (uint32_t i = 0; i < length; i++) {
    Serial.write(myCAM.read_fifo());
  }
  Serial.write(0xFF);
  Serial.write(0xD9);

  delay(1000);

}
