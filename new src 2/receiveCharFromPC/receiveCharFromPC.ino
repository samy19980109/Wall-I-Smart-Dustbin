
// Send 'a' for organic waste and 'b' for recycling
#include <Stepper.h>

const int stepsPerRevolution = 50;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);
char receivedChar;
boolean newData = false;

void setup() {
  // put your setup code here, to run once:
  // initialize the serial port:
  Serial.begin(9600);
  Serial.println("Arduino is ready");
  
  // set the speed at 60 rpm:
  myStepper.setSpeed(60);

  recycle();
  
}

void loop() {
  // put your main code here, to run repeatedly:
  receiveChar();
  showNewData();
}

void receiveChar(){
  if (Serial.available() > 0){
    receivedChar = Serial.read();
    if (receivedChar == 97){
      organic();
    }else if(receivedChar == 98){
      recycle();
    }
    newData = true;
  }
}

void showNewData(){
  if (newData == true){
    Serial.print("This just in...");
    Serial.println(receivedChar);
    newData = false;
  }
}

void organic() {
  if (true) {
    Serial.println("organic:Clockwise");
    myStepper.step(stepsPerRevolution);
    delay(1000);

    Serial.println("counterclockwise");
    myStepper.step(-stepsPerRevolution);
    delay(1000);
  }
}

void recycle() {
  Serial.println("Recycle:counterclockwise");
  myStepper.step(-stepsPerRevolution);
  delay(1000);

  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  delay(1000);
}
