/**
 * @brief control code for the arm
 */

#include <Servo.h>
#include <stdint.h>

#define ARM_CTRL_0 (5)
#define ARM_CTRL_1 (6)
#define ARM_CTRL_2 (7)
#define ARM_CTRL_3 (8) 
#define ARM_CTRL_4 (9)
#define ARM_CTRL_5 (10)

#define ARM_ADC_0 (A0)
#define ARM_ADC_1 (A1)
#define ARM_ADC_2 (A2)
#define ARM_ADC_3 (A3)
#define ARM_ADC_4 (A4)
#define ARM_ADC_5 (A5)

const size_t NUM_ARM_JOINTS = 6;

static uint8_t ARM_ADC_PIN_ARRAY[NUM_ARM_JOINTS] = {ARM_ADC_0, 
                                                    ARM_ADC_1, 
                                                    ARM_ADC_2, 
                                                    ARM_ADC_3, 
                                                    ARM_ADC_4, 
                                                    ARM_ADC_5};

static uint8_t ARM_CTRL_PIN_ARRAY[NUM_ARM_JOINTS] = {ARM_CTRL_0, 
                                                     ARM_CTRL_1, 
                                                     ARM_CTRL_2, 
                                                     ARM_CTRL_3, 
                                                     ARM_CTRL_4, 
                                                     ARM_CTRL_5};

static Servo servoArray[NUM_ARM_JOINTS];
void setServo(uint8_t index, uint8_t percent);
void read_and_output_adc(uint8_t adc_value_buffer[]);
void output_adc();
uint16_t convert_adc_to_torque(uint16_t adc);

void setup() {
  for(size_t i = 0; i < NUM_ARM_JOINTS; i++)
  {
    servoArray[i].attach(ARM_CTRL_PIN_ARRAY[i]);
  }

  Serial.begin(115200); //115200 Baud Rate
  Serial.setTimeout(15);
}

void loop() {

  if(Serial.available() > 0)
  {
    //Processing, let's assume a 1-byte packet with each joint as a percent from 0 -> 255
    uint8_t rx_msg[NUM_ARM_JOINTS] = {0}; 
    /*******TODO: Implement the actual RX task of this****/
    for(size_t i = 0; i < NUM_ARM_JOINTS; i++)
    {
      rx_msg[i] = Serial.read(); //Store the data into the buffer
      setServo(i, rx_msg[i]);
    }

    Serial.flush();
  }
  read_and_output_adc();
}

/**
 * @param index index of the servo inside the Servoarray object
 * @param percent 0-255 percent
 */
void setServo(uint8_t index, uint8_t percent)
{
  const uint16_t SERVO_MIN_MS = 900;
  const uint16_t SERVO_MAX_MS = 2000;
  //uint16_t microseconds = map(percent, 0, 255, SERVO_MIN_MS, SERVO_MAX_MS) /*Maybe try this?*/
  uint16_t microseconds = ((SERVO_MAX_MS-SERVO_MIN_MS)*(percent/255.0) + SERVO_MIN_MS); //Floating point math, i know.
  Servo *servoObject = servoArray + index;
  servoObject->writeMicroseconds(microseconds); //Actually write the value
}

void read_and_output_adc()
{
  for(uint8_t i = 0; i < NUM_ARM_JOINTS; i++)
  {
    uint16_t result = analogRead(ARM_ADC_PIN_ARRAY[i]);
    uint16_t torque = convert_adc_to_torque(result);
    Serial.print("Torque Value for ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(torque);
  }
}

uint16_t convert_adc_to_torque(uint16_t adc)
{
    return map(adc, 0, 1023, 500, 0); //Something like this?
}
