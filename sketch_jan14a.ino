#include <SPI.h>

const uint8_t CS_PIN = 53;

void setup() {
  Serial.begin(9600);
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);
  SPI.begin();   
  SPI.beginTransaction(SPISettings(125000, MSBFIRST, SPI_MODE1));
  //delay(20); ALL DELAYS HAVE BEEN REMOVED SINCE FORUMS SAY TO REFER TO DATASHEET, IF NOT MENTIONED - DELAY NOT NEEDED
}

void loop() {

  //Start transaction
  digitalWrite(CS_PIN, LOW);
  //delayMicroseconds(600);
  
  //Send start bytes
  uint8_t sb1 = SPI.transfer(0xAA);
  Serial.println("sb1:");
  Serial.println(sb1);
  //delayMicroseconds(600);
  uint8_t sb2 = SPI.transfer(0xFF); 
  //delayMicroseconds(600);

  //Send and receive data bytes
  uint8_t b1 = SPI.transfer(0xFF); 
  //delayMicroseconds(600);
  Serial.println("b1:");
  Serial.println(b1);
  uint8_t b2 = SPI.transfer(0xFF);
  Serial.println(b2);
  //delayMicroseconds(600);
  uint8_t b3 = SPI.transfer(0xFF);
  Serial.println(b3);
  //delayMicroseconds(600);
  uint8_t b4 = SPI.transfer(0xFF);  
  Serial.println(b4);
  // //Extract and calculate angle
  // uint16_t data_bytes = (b1 << 8) | b2;  // Combine two bytes and shift it left
  // uint16_t mask = 0x3FFF;  // Mask to extract first 14 bits
  // uint16_t angle_raw = data_bytes & mask;  // Extract first 14 bits
  // //float angle = (float)(angle_raw / 16384.0 * 360);  // Divide by 2^14 and multiply by 360 to get degrees
  // Serial.println(angle_raw);

  //End transaction
  digitalWrite(CS_PIN, HIGH);
  // SPI.endTransaction(); //beginTransaction is outside loop so cannot end inside loop

  delay(150);
}