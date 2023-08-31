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
#define red_pin 33
#define green_pin 34
#define blue_pin 35

int motorspeed = 0;
int desireddistance = 0;
int desiredspeed = 0;
int distance =0;
unsigned long previousTime = 0;
float speed = 0.0;

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
  pinMode(red_pin , OUTPUT);
  pinMode(green_pin , OUTPUT);
  pinMode(blue_pin , OUTPUT);


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
    sendSensorData(distance, currentA, voltageA, speed);
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
    while (receivedChar != 'A'|| receivedChar != 'K'|| receivedChar != 'J')
    {
      manual(receivedChar);
    }

  }
  indicator(motorspeed); 
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - previousTime;
  if (elapsedTime >= 1000) {
    speed = calculateSpeed(distance, elapsedTime);
    previousTime = currentTime;
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
  bluetoothSerial.print('F');
}

void backward(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  digitalWrite(MOTOR_A_IN1_PIN, LOW);
  digitalWrite(MOTOR_A_IN2_PIN, HIGH);
  analogWrite(MOTOR_A_EN_PIN, motorspeed2);

  digitalWrite(MOTOR_B_IN1_PIN, LOW);
  digitalWrite(MOTOR_B_IN2_PIN, HIGH);
  analogWrite(MOTOR_B_EN_PIN, motorspeed2);
  bluetoothSerial.print('B');
}

void left(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  digitalWrite(MOTOR_A_IN1_PIN, HIGH);
  digitalWrite(MOTOR_A_IN2_PIN, LOW);
  analogWrite(MOTOR_A_EN_PIN, motorspeed2);

  digitalWrite(MOTOR_B_IN1_PIN, LOW);
  digitalWrite(MOTOR_B_IN2_PIN, HIGH);
  analogWrite(MOTOR_B_EN_PIN, motorspeed2);
  bluetoothSerial.print('L');
}

void right(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  digitalWrite(MOTOR_A_IN1_PIN, LOW);
  digitalWrite(MOTOR_A_IN2_PIN, HIGH);
  analogWrite(MOTOR_A_EN_PIN, motorspeed2);

  digitalWrite(MOTOR_B_IN1_PIN, HIGH);
  digitalWrite(MOTOR_B_IN2_PIN, LOW);
  analogWrite(MOTOR_B_EN_PIN, motorspeed2);
  bluetoothSerial.print('R');
}

void stop() {

  digitalWrite(MOTOR_A_IN1_PIN, LOW);
  digitalWrite(MOTOR_A_IN2_PIN, LOW);
  analogWrite(MOTOR_A_EN_PIN, 0);

  digitalWrite(MOTOR_B_IN1_PIN, LOW);
  digitalWrite(MOTOR_B_IN2_PIN, LOW);
  analogWrite(MOTOR_B_EN_PIN, 0);
  bluetoothSerial.print('S');
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
  indicator(velocity); 
}

void sendSensorData(int distance, float currentA, float voltageA, int motorspeed4) {
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
  
  bluetoothSerial.print(" Speed :");
  bluetoothSerial.print(motorspeed4);
  bluetoothSerial.print(" m/s ");
  bluetoothSerial.println();
}
void indicator(int motorspeed3) // Indicates the motor speed 
{
  if (motorspeed3 <= 80)
  {
    digitalWrite(red_pin,HIGH);
    digitalWrite(green_pin,LOW);
    digitalWrite(blue_pin,LOW);
  }
  else if(motorspeed3 > 80 && motorspeed3 <= 160 )
  {
    digitalWrite(red_pin,LOW);
    digitalWrite(green_pin,HIGH);
    digitalWrite(blue_pin,LOW);
  }
  else if (motorspeed3 >160 && motorspeed3<255)
  {
    digitalWrite(red_pin,LOW);
    digitalWrite(green_pin,LOW);
    digitalWrite(blue_pin,HIGH);
  }
}
float calculateSpeed(int distance, unsigned long elapsedTime) {
  float timeInSeconds = elapsedTime / 1000.0;  
  float speed = distance / timeInSeconds;      
  speed /= 100.0;                              
  return speed;
}



