//Motor Left pins
#define MOTOR_L_EN_PIN 5
#define MOTOR_L_IN1_PIN 6
#define MOTOR_L_IN2_PIN 7

//Motor Right pins
#define MOTOR_R_EN_PIN 10
#define MOTOR_R_IN1_PIN 8
#define MOTOR_R_IN2_PIN 9

//Current and voltage sensors
#define CURRENT_SENSE A0
#define VOLT_SENSE A1

//Ultrasonic sensor
#define TRIG_PIN A2
#define ECHO_PIN A3

//Gyroscope sensor
#define SCL_PIN A5
#define SDA_PIN A4

//Indicator pins
#define BUZZER 3
#define LED 4
#define RGB_R 11
#define RGB_B 13
#define RGB_G 12

int motorspeed = 0;
int desireddistance = 0;
int desiredspeed = 0;
int distance =0;
char send ;

void setup() {
  //Pin initiallization 
  pinMode(MOTOR_L_EN_PIN, OUTPUT);
  pinMode(MOTOR_L_IN1_PIN, OUTPUT);
  pinMode(MOTOR_L_IN2_PIN, OUTPUT);
  
  pinMode(MOTOR_R_EN_PIN, OUTPUT);
  pinMode(MOTOR_R_IN1_PIN, OUTPUT);
  pinMode(MOTOR_R_IN2_PIN, OUTPUT);

  pinMode(CURRENT_SENSE, INPUT);
  pinMode(VOLT_SENSE, INPUT);
  
  pinMode(BUZZER, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(RGB_R, OUTPUT);
  pinMode(RGB_G, OUTPUT);
  pinMode(RGB_B, OUTPUT);

  Serial.begin(9600);
}

void loop() {

  if(Serial.available())
  {
    send = Serial.read();
    if(send == 'M')
    {
      Manual(Serial.read());
    }
    else if (send == 'A')
    {
      Serial.print("enter distance :");
      desireddistance = Serial.read();
      Serial.print("enter velocity");
      desiredspeed = Serial.read();
      Autonomous(desireddistance , desiredspeed );
    }
  }

  Serial.print('V');
  Serial.print(Voltage());
  Serial.print('I');
  Serial.print(Current());
  Serial.print('D');
  Serial.print(measureDistance());
}

void Forward(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);

  analogWrite(MOTOR_L_EN_PIN, motorspeed2);
  digitalWrite(MOTOR_L_IN1_PIN, HIGH);
  digitalWrite(MOTOR_L_IN2_PIN, LOW);

  analogWrite(MOTOR_R_EN_PIN, motorspeed2);
  digitalWrite(MOTOR_R_IN1_PIN, HIGH);
  digitalWrite(MOTOR_R_IN2_PIN, LOW);
}

void Backward(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  
  analogWrite(MOTOR_L_EN_PIN, motorspeed2);
  digitalWrite(MOTOR_L_IN1_PIN, LOW);
  digitalWrite(MOTOR_L_IN2_PIN, HIGH);

  analogWrite(MOTOR_R_EN_PIN, motorspeed2);
  digitalWrite(MOTOR_R_IN1_PIN, LOW);
  digitalWrite(MOTOR_R_IN2_PIN, HIGH);
}

void Left(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);

  analogWrite(MOTOR_L_EN_PIN, motorspeed2);
  digitalWrite(MOTOR_L_IN1_PIN, LOW);
  digitalWrite(MOTOR_L_IN2_PIN, LOW);

  analogWrite(MOTOR_R_EN_PIN, motorspeed2);
  digitalWrite(MOTOR_R_IN1_PIN, HIGH);
  digitalWrite(MOTOR_R_IN2_PIN, LOW);
}

void Right(int motorspeed2) {
  motorspeed2 = constrain(motorspeed2,0,255);
  
  analogWrite(MOTOR_L_EN_PIN, motorspeed2);  
  digitalWrite(MOTOR_L_IN1_PIN, HIGH);
  digitalWrite(MOTOR_L_IN2_PIN, LOW);

  analogWrite(MOTOR_R_EN_PIN, motorspeed2);
  digitalWrite(MOTOR_R_IN1_PIN, LOW);
  digitalWrite(MOTOR_R_IN2_PIN, LOW);
}

void Stop(void) {
  digitalWrite(MOTOR_L_IN1_PIN, LOW);
  digitalWrite(MOTOR_L_IN2_PIN, LOW);
  analogWrite(MOTOR_L_EN_PIN, 0);

  digitalWrite(MOTOR_R_IN1_PIN, LOW);
  digitalWrite(MOTOR_R_IN2_PIN, LOW);
  analogWrite(MOTOR_R_EN_PIN, 0);
}

float map_this(float value, float fromlow, float fromhigh, float tolow, float tohigh)
{
  return (value - fromlow) * (tohigh - tolow) / (fromhigh - fromlow) + tolow; 
}

// Measure the distance from the wall using distance sensors
int measureDistance() {
  long duration = 0;
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}

// Measure current using current sensors
float Current() {
  int adc = analogRead(CURRENT_SENSE);
  float voltage = adc * 5/1023.0;
  float current = (voltage - 2.5) / 0.185;
  return current;
}

// Measure voltage using voltage sensors
float Voltage() {
  float value = analogRead(VOLT_SENSE);
  //Since the arduino cannot handle greater than 5V we need to put a voltage divider to scale the input 
  //R1 , R2 are resistors of the voltage divider 
  //Equation : V1 = Vmax * (R2/(R1+R2))
  float voltage = value * (5.0 / 1023) * ((47 + 33)/33);
  return voltage;
}

// Send sensor data to the GUI via Bluetooth serial communication
/*void sendSensorData(int distance, float currentA, float voltage) {
  Serial.print("V");
  Serial.println(voltage);
  Serial.println(sensorData);
}*/

void Manual(char command) {  // Process commands received from the GUI
  motorspeed =150;
  while(command != 'E'){
  switch (command){
    case 'F':
      Forward(motorspeed);
      motorspeed = motorspeed + 20;
      break;
      
    case 'B':
      Backward(motorspeed);
      motorspeed = motorspeed + 20;
      break;
      
    case 'L':
      Left(motorspeed);
      motorspeed = motorspeed + 20;
      break;
      
    case 'R':
      Right(motorspeed);
      motorspeed = motorspeed + 20;
      break;
      
    case 'S':
      Stop();
      break;
      
    default:
      break;
  }
  RGB(motorspeed);
}
}

void Autonomous(int distance2 , int velocity) 
{
  int error;
  int correction;
  int left_side;
  int right_side;
  RGB(velocity);
  while (distance2 != 0){
   error = distance2 - measureDistance();
   correction = 0.5*error; // 0.5 is a propotional constant
   left_side = velocity + correction;
   right_side = velocity - correction;

  left_side = constrain(left_side,0,255);
  right_side = constrain(right_side,0,255);

  digitalWrite(MOTOR_L_IN1_PIN, HIGH);
  digitalWrite(MOTOR_L_IN2_PIN, LOW);
  analogWrite(MOTOR_L_EN_PIN, left_side);

  digitalWrite(MOTOR_R_IN1_PIN, HIGH);
  digitalWrite(MOTOR_R_IN2_PIN, LOW);
  analogWrite(MOTOR_R_EN_PIN, right_side);  
}
}
void RGB(int speed)
{
  if( speed < 150)
  {
    digitalWrite(RGB_R,HIGH);
  }
  else if ( speed > 150  && speed < 200)
  {
    digitalWrite(RGB_B,HIGH);
  }
  else if ( speed > 200 )
  {
    digitalWrite(RGB_G,HIGH);
  }

}
/*             For testing
 *   digitalWrite(LED, HIGH);
  
  Forward(255);
  delay(3000);
  
  Stop();
  delay(1000);
  
  Backward(255);
  delay(3000);

  Right(255);
  delay(100);

  Stop();
  delay(1000);

  Left(255);
  delay(100);

  Stop();
  digitalWrite(LED, LOW);
  delay(1000);
 */
