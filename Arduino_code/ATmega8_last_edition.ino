#include <SoftwareSerial.h>

#define MOTOR_A_EN_PIN 3
#define MOTOR_A_IN1_PIN 4
#define MOTOR_A_IN2_PIN 5

#define MOTOR_B_EN_PIN 6
#define MOTOR_B_IN1_PIN 7
#define MOTOR_B_IN2_PIN 8

#define current_sensor 9
#define trig_pin 10
#define echo_pin 11
#define voltage_pin 12

int motorspeed = 0;
int desireddistance = 0;
int desiredspeed = 0;
int distance =0;

SoftwareSerial bluetoothSerial(2, 3); // RX, TX pins on ATmega8


void setup() {
  pinMode(MOTOR_A_EN_PIN, OUTPUT);
  pinMode(MOTOR_A_IN1_PIN, OUTPUT);
  pinMode(MOTOR_A_IN2_PIN, OUTPUT);

  pinMode(MOTOR_B_EN_PIN, OUTPUT);
  pinMode(MOTOR_B_IN1_PIN, OUTPUT);
  pinMode(MOTOR_B_IN2_PIN, OUTPUT);

  pinMode(current_sensor, INPUT);
  pinMode(trig_pin, OUTPUT);
  pinMode(echo_pin, INPUT);
  pinMode(voltage_pin, INPUT);

  Serial.begin(9600);
  bluetoothSerial.begin(9600);
}

void loop() {

  if (bluetoothSerial.available()) 
  {
    char receivedChar = bluetoothSerial.read();
    distance = measureDistance();
    float currentA = measureCurrentA();
    float voltageA = measureVoltageA();
    sendSensorData(distance, currentA, voltageA);
    while ( receivedChar != 'M'|| receivedChar != 'B'|| receivedChar != 'F'|| receivedChar != 'R'|| receivedChar != 'L' || receivedChar != 'S' )
    {
      if (receivedChar == 'K') // indicator that the msg is for distance
      {
         desireddistance = bluetoothSerial.read();
      }
      else if (receivedChar == 'J') //indicator that the msg is for speed
      {
         desiredspeed = bluetoothSerial.read();
      }
       autonomousControl(distance,desiredspeed);
    }
    while (receivedChar != 'A'|| receivedChar != 'D'|| receivedChar != 'V')
    {
      manual(receivedChar);
    }

  }


}

void manual(char command) {  // Process commands received from the GUI
  motorspeed =120;
  switch (command) {
    case 'F':
      while(command == 'F'){
      forward(motorspeed);
      motorspeed = motorspeed + 20;
      }
      break;
    case 'B':
      while(command == 'B'){
      backward(motorspeed);
      motorspeed = motorspeed + 20;
      }
      break;
    case 'L':
      while(command == 'L'){
      left(motorspeed);
      motorspeed = motorspeed + 20;
      }
      break;
    case 'R':
      while(command == 'R'){
      right(motorspeed);
      motorspeed = motorspeed + 20;
      }
      break;
    case 'S':
      stop();
      break;
    default:
      break;
  }
}

void forward(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  digitalWrite(MOTOR_A_IN1_PIN, HIGH);
  digitalWrite(MOTOR_A_IN2_PIN, LOW);
  analogWrite(MOTOR_A_EN_PIN, motorspeed2);


  digitalWrite(MOTOR_B_IN1_PIN, HIGH);
  digitalWrite(MOTOR_B_IN2_PIN, LOW);
  analogWrite(MOTOR_B_EN_PIN, motorspeed2);
}

void backward(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  digitalWrite(MOTOR_A_IN1_PIN, LOW);
  digitalWrite(MOTOR_A_IN2_PIN, HIGH);
  analogWrite(MOTOR_A_EN_PIN, motorspeed2);

  digitalWrite(MOTOR_B_IN1_PIN, LOW);
  digitalWrite(MOTOR_B_IN2_PIN, HIGH);
  analogWrite(MOTOR_B_EN_PIN, motorspeed2);
}

void left(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  digitalWrite(MOTOR_A_IN1_PIN, HIGH);
  digitalWrite(MOTOR_A_IN2_PIN, LOW);
  analogWrite(MOTOR_A_EN_PIN, motorspeed2);

  digitalWrite(MOTOR_B_IN1_PIN, LOW);
  digitalWrite(MOTOR_B_IN2_PIN, HIGH);
  analogWrite(MOTOR_B_EN_PIN, motorspeed2);
}

void right(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  digitalWrite(MOTOR_A_IN1_PIN, LOW);
  digitalWrite(MOTOR_A_IN2_PIN, HIGH);
  analogWrite(MOTOR_A_EN_PIN, motorspeed2);

  digitalWrite(MOTOR_B_IN1_PIN, HIGH);
  digitalWrite(MOTOR_B_IN2_PIN, LOW);
  analogWrite(MOTOR_B_EN_PIN, motorspeed2);
}

void stop() {

  digitalWrite(MOTOR_A_IN1_PIN, LOW);
  digitalWrite(MOTOR_A_IN2_PIN, LOW);
  analogWrite(MOTOR_A_EN_PIN, 0);

  digitalWrite(MOTOR_B_IN1_PIN, LOW);
  digitalWrite(MOTOR_B_IN2_PIN, LOW);
  analogWrite(MOTOR_B_EN_PIN, 0);
}

int measureDistance() {
  // Measure the distance from the wall using distance sensors
  long duration = 0;
  digitalWrite(trig_pin, LOW);
  delayMicroseconds(2);
  digitalWrite(trig_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig_pin, LOW);
  duration = pulseIn(echo_pin, HIGH);
  distance = duration * 0.034 / 2;

  return distance;
}

float measureCurrentA() {
  // Measure current using current sensors
  int adc = analogRead(current_sensor);
  float voltage = adc*5/1023.0;
  float current = (voltage-2.5)/0.185;
  return current;
}

float measureVoltageA() {
  // Measure voltage using voltage sensors
  float value = analogRead(voltage_pin);
  float voltage = map_this(value , 0.0 , 1024.0 , 0.0 , 12.0);
  return voltage;
}
float map_this(float value, float fromlow, float fromhigh, float tolow, float tohigh)
{
	return (value - fromlow) * (tohigh - tolow) / (fromhigh - fromlow) + tolow;	
}

void autonomousControl(int distance2 , int velocity) 
{
  int error = desireddistance - distance2;
  int correction = 0.5*error; // 0.5 is a propotional constant
  int left_side = velocity + correction;
  int right_side = velocity - correction;

  left_side = constrain(left_side,0,255);
  right_side = constrain(right_side,0,255);

  digitalWrite(MOTOR_A_IN1_PIN, HIGH);
  digitalWrite(MOTOR_A_IN2_PIN, LOW);
  analogWrite(MOTOR_A_EN_PIN, left_side);

  digitalWrite(MOTOR_B_IN1_PIN, HIGH);
  digitalWrite(MOTOR_B_IN2_PIN, LOW);
  analogWrite(MOTOR_B_EN_PIN, right_side);
}

void sendSensorData(int distance, float currentA, float voltageA) {
  // Send sensor data to the GUI via Bluetooth serial communication
  bluetoothSerial.print("Distance: ");
  bluetoothSerial.print(distance);
  bluetoothSerial.print(" cm");

  bluetoothSerial.print(" Current: ");
  bluetoothSerial.print(currentA);
  bluetoothSerial.print(" A");

  bluetoothSerial.print(" Voltage: ");
  bluetoothSerial.print(voltageA);
  bluetoothSerial.print(" V");
  bluetoothSerial.println();
}