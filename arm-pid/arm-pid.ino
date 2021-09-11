// Read in 12-bits Magnetic Encoder AEAT-6012-A06 into Arduino Nano

/* Pins for SPI On Arduino/Encoder
 *  MISO - 50 / DO - 5
 *  SCK - 52 / CLK - 4
 *  SS - 53 / CSn - 2 (active low)
 *  MOSI - 51
 *  
 *  Datasheet: https://docs.broadcom.com/doc/AV02-0188EN
 *  
 *  Max SPI speed: <=1MHz "Maximum Read-out Frequency"?
 *  Data shifted MSB or LSB first?: MSB first (D11 - D0)  
 *  Clk idle when high or low? (Clock polarity) : Idle high
 *  Clk samples on rising or falling egde ? (Clock phase?): Rising (second) edge
*/

// Includes
#include <SPI.h>
#include <RobotLib.h>
#include "CytronMotorDriver.h"
// #include <Arduino_FreeRTOS.h>

// Set Arduino SPI pins
// For arduino mega 2560:
//  - CSn = any GPIO
//  - CLK = 52
//  - DO = 50
// const int CSn = 2;  // Chip select (Encoder Input)
// const int CLK = 52;  // Clock signal (Encoder Input)
// const int DO = 50;   // Serial Data (Encoder Output): 0 or 1, depending on the bar angle



CytronMD motors[6] = 
  {
    CytronMD(PWM_DIR, 2, 38),
    CytronMD(PWM_DIR, 3, 40),
    CytronMD(PWM_DIR, 4, 42),
    CytronMD(PWM_DIR, 5, 44),
    CytronMD(PWM_DIR, 6, 46),
    CytronMD(PWM_DIR, 7, 48),
  };

const int spi_pins[6][3] =
  {
    {1,8,12},
    {1,8,12},
    {1,8,12},
    {1,8,12},
    {1,8,12},
    {1,8,12},
  };

const int analogPins[6] =
  {
    A0,
    A1,
    A2,
    A3,
    A4,
    A5,
  };

double sensor_voltage[6] = {0, 0, 0, 0, 0, 0};
double sensor_current[6] = {0, 0, 0, 0, 0, 0};

int joint_positions[6] = {0, 0, 0, 0, 0, 0};

PIDController pid1;
String message;
int loopCounter = 0;
// Variables
float prevEncDegrees, currEncDegrees, encAngVel = 0.0;
unsigned long startTime, endTime;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(2);

  pid1.begin(0, 0.8, 0.5, 0.2); // Initalize PIDController with initial value 0, P=0.8, I=0.5, D=0.2

  int rows =  sizeof spi_pins / sizeof spi_pins[0]; // should be 6
  Serial.println(rows);
  for(int i = 0; i < rows; i++){

  int CSn = spi_pins[i][0]; 
  int CLK = spi_pins[i][1];   
  int DO = spi_pins[i][2];    

  pinMode(38, OUTPUT);
  // Initialize Arduino pins
  pinMode(CSn, OUTPUT);
  //pinMode(CLK, OUTPUT);
  //pinMode(DO, INPUT);

  // Write starting levels
  digitalWrite(CLK, HIGH);
  digitalWrite(CSn, HIGH);
  
  }
  
  SPI.begin();
  
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE2));  // MODE2: sample on clk falling edge cuz t_DOvalid
  
}

void loop() {
  // readEncoders();
  // pidTesting();
  updateMessage();
  updateValues();
  controlMotors();
}

void controlMotors(){
  if(message == "1up") {
    motors[0].setSpeed(255); 
  }
  if(message == "1down") {
    motors[0].setSpeed(128); 
  }
  if(message == "1stop") {
    motors[0].setSpeed(0);  
  } 

  if(message == "2up") {
    motors[1].setSpeed(50); 
  }
  if(message == "2down") {
    motors[1].setSpeed(-50); 
  }
  if(message == "2stop") {
    motors[1].setSpeed(0);  
  } 
  

  if(message == "3up") {
    motors[2].setSpeed(255); 
  }
  if(message == "3down") {
    motors[2].setSpeed(-128); 
  }
  if(message == "3stop") {
    motors[2].setSpeed(0);  
  } 

  if(message == "4up") {
    motors[3].setSpeed(50); 
  }
  if(message == "4down") {
    motors[3].setSpeed(-50); 
  }
  if(message == "4stop") {
    motors[3].setSpeed(0);  
  } 

  if(message == "5up") {
    motors[4].setSpeed(50); 
  }
  if(message == "5down") {
    motors[4].setSpeed(-50); 
  }
  if(message == "5stop") {
    motors[4].setSpeed(0);  
  } 


}
void updateValues(){
    for(int i = 0; i < 5; i++){
    sensor_voltage[i] = ((analogRead(analogPins[i]) /1024.0) * 5);  // read the input pin
    sensor_current[i] = abs(((20 * sensor_voltage[i]) - 50));
    if(sensor_current[i] > 0.5 || loopCounter % 20 == 0){
      Serial.print("c,"); Serial.print(i + 1); Serial.print(","); Serial.println(sensor_current[i]);
    }
    loopCounter++;
  }

    // Serial.println("c," + i + "," + sensor_current[4]);

}
void updateMessage(){
  message = Serial.readString();
  if(message != ""){
      Serial.println(message);
  }
}

void pidTesting(){
  float output = pid1.update(joint_positions[0], 50); // Get next output to send to device given our state is at 0.5 and we want to move to 1.
  //TODO: sent output to motor

}

void readEncoders()
{
  int rows =  sizeof spi_pins / sizeof spi_pins[0]; // should be 6
  for(int i = 0; i < rows; i++){

  int CSn = spi_pins[i][0]; 
  int CLK = spi_pins[i][1];   
  int DO = spi_pins[i][2];    
  uint8_t receivedBytes[2] = {0};
  
  // Set SS to low to activate DO
  digitalWrite(CSn, LOW);

  // Time between falling edge of CSn and first falling edge of CLK, t_CLKFE = 500ns = 0.5us
  delayMicroseconds(1);

  // Send value to encoder and recieve 12 bits from encoder via SPI; MSBFIRST not defined for transfer16()
  // Data sent doesn't matter since it's only a read, it gets overwritten
  receivedBytes[0] = SPI.transfer(0x0);
  receivedBytes[1] = SPI.transfer(0x0);
  
  // Deselect encoder SS to initiate next read-out of angular position
  digitalWrite(CSn, HIGH);
  uint16_t result = ((receivedBytes[0] & ~(static_cast<uint8_t>(1 << 7))) << 5) | (receivedBytes[1] >> 3);
  
  // Calculate degrees
  currEncDegrees = (float(result)/4096.0)*360;

  // Calculate angular velocity
  endTime = micros();
  float dt = endTime - startTime;
  float dv = currEncDegrees - prevEncDegrees;
  encAngVel = 0.3 * (dv/dt*1e6) + 0.7 * (encAngVel); // apply moving average filter

  // Reset values
  prevEncDegrees = currEncDegrees;
  startTime = endTime;


//  Serial.print("Raw angular position: "); Serial.println(result); 
  // Serial.print("Angular position: "); Serial.print(currEncDegrees); Serial.println("degrees");

  joint_positions[i] = currEncDegrees;
  // Serial.print("Angular velocity: "); Serial.println(encAngVel); Serial.println("degrees/sec"); Serial.println();
  } 
}