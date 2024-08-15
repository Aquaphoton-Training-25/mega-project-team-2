#define  input1 10 
#define  input2 11
#define  enable1 13
#define  input3 1
#define  input4 2
#define  enable2 4 
#define  RGBled1 2
#define  RGBled2 3 
#define  RGBled3 12
#define  echopin 5
#define  trigpin 6
#define  buzzer 9

int  speed = 0;
long distance;
long duration;

void setup() {

pinMode(button, INPUT_PULLUP);
pinMode(trigpin, OUTPUT);
pinMode(echopin, INPUT);
pinMode(RGBled1, OUTPUT);
pinMode(RGBled2, OUTPUT);
pinMode(RGBled3, OUTPUT);
pinMode(buzzer, OUTPUT);
pinMode(input1, OUTPUT);
pinMode(input2, OUTPUT);
pinMode(input3, OUTPUT);
pinMode(input4, OUTPUT);
pinMode(enable1, OUTPUT);
pinMode(enable2, OUTPUT);

Serial.begin(9600);

}

void loop() {

 autonomous();

}

void manual(){
    speed();
    char movement = F;
    switch(movement){
    case 'F':  
      forward();
      break;
    case 'B':  
      backward();
      break;
    case 'L':  
      left();
      break;
    case 'R':
      right();
      break;
    case 'S':
     stop();
     break;
   } 
}

void autonomous(){
  long dis = 10; //distance in cm
  while(command == autonomous){
    speed();
    ultrasonic();
    forward();
  if(distance > dis){
    for(int i = dis; i != distance;){
      right();
      delay(5);
      forward();
      if(i == distance){
        forward();
        digitalWrite(buzzer, LOW);
        break;
      }
      else{
        digitalWrite(buzzer,HIGH);
        continue; 
      }
    }
  }
  else if(distance < dis){
    for(int j = dis; j != distance;){
      left();
      delay(5);
      forward();
      if(j == distance){
        forward();
        digitalWrite(buzzer, LOW);
        break;
      }
      else{
        digitalWrite(buzzer, HIGH);
        continue;
      }
    }
  }
  else if(distance == dis){
    forward();
  }
  } 
}

void speed(){
  int speed = 2;
  if(speed == 0){
    analogWrite(enable1, 0);
    analogWrite(enable2, 0);
  }
  else if(speed == 1){
    analogWrite(enable1, 60);
    analogWrite(enable2, 60);
    digitalWrite(RGBled1, HIGH);
  }
  else if(speed == 2){
    analogWrite(enable1, 135);
    analogWrite(enable2, 135;
    digitalWrite(RGBled2, HIGH);
  }
  else if (speed == 3){
    analogWrite(enable1, 255);
    analogWrite(enable2, 255);
    digitalWrite(RGBled3, HIGH);
  }
}

void forward(){
  digitalWrite(input1, HIGH);
  digitalWrite(input2, LOW);
  digitalWrite(input3, HIGH);
  digitalWrite(input4, LOW);
}
void backward(){
  digitalWrite(input1, LOW);
  digitalWrite(input2, HIGH);
  digitalWrite(input3, LOW);
  digitalWrite(input4, HIGH);
}

void right(){
  digitalWrite(input1, LOW);
  digitalWrite(input2, HIGH);
  digitalWrite(input3, HIGH);
  digitalWrite(input4, LOW);
}

void left(){
  digitalWrite(input1, HIGH);
  digitalWrite(input2, LOW);
  digitalWrite(input3, LOW);
  digitalWrite(input4, HIGH);
}

void stop(){
  digitalWrite(input1, LOW);
  digitalWrite(input2, LOW);
  digitalWrite(input3, LOW);
  digitalWrite(input4, LOW);
}

void ultrasonic(){
  digitalWrite(trigpin, LOW);
  delay(2);
  digitalWrite(trigpin, HIGH);
  delay(10);
  digitalWrite(trigpin, LOW);

  duration= pulseIn(echopin, HIGH);
  distance= duration*0.034/2;
}
