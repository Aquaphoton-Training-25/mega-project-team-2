#define  input1 10
#define  input2 11
#define  enable1 12
#define  input3 13
#define  input4 14
#define  enable2 15
#define  RGBled1 2
#define  RGBled2 3
#define  RGBled3 4
#define  echopin 5
#define  trigpin 6
#define  voltmeter 7
#define  Ameter 8
#define  buzzer 9


#include <PID_v1.h>

int volt, ampere;
int speed = 0;
double dis = 0;
double distance;
double duration;
char movement;
char command;

// PID Variables
double setpoint = 20.0;  // Desired distance from the wall in centimeters
double input;           // Current distance from the wall
double output;          // Control output for adjusting direction

// Create PID object
PID myPID(&input, &output, &setpoint, 2, 5, 1, DIRECT);  // Adjust PID parameters as needed

void setup() {
    pinMode(trigpin, OUTPUT);
    pinMode(echopin, INPUT);
    pinMode(RGBled1, OUTPUT);
    pinMode(RGBled2, OUTPUT);
    pinMode(RGBled3, OUTPUT);
    pinMode(voltmeter, INPUT);  
    pinMode(Ameter, INPUT);     
    pinMode(buzzer, OUTPUT);
    pinMode(input1, OUTPUT);
    pinMode(input2, OUTPUT);
    pinMode(input3, OUTPUT);
    pinMode(input4, OUTPUT);
    pinMode(enable1, OUTPUT);
    pinMode(enable2, OUTPUT);

    Serial.begin(9600);

    
    myPID.SetMode(AUTOMATIC);
    myPID.SetOutputLimits(-255, 255);  
}

void loop() {   
    if (Serial.available() > 0) {
        command = Serial.read();
        if (command == 'M') {
            manual();
        } else if (command == 'A') {
            autonomous();
        }
    }
}

void manual() {
    while (true) {
        if (Serial.available() > 0) {
            char newCommand = Serial.read();
            if (newCommand == 'A') {
                return;  
            }
        }
          analogWrite(enable1, 135);
            analogWrite(enable2, 135);
            digitalWrite(RGBled1, LOW);
            digitalWrite(RGBled2, HIGH);
            digitalWrite(RGBled3, LOW);
        

        if (Serial.available() > 0) {
            movement = Serial.read();
            switch (movement) {
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

        send_signals();
    }
}

void autonomous() {
    if (Serial.available() > 0) {
        dis = Serial.parseFloat();  // Read distance as float
        setpoint = dis;             // Update setpoint from serial input
    }

    while (true) {
        send_signals();
        ultrasonic();  
        input = distance;  

        
        myPID.Compute();

        
        if (output > 0) {
            
            left();
            analogWrite(enable1, constrain(255 - abs(output), 0, 255));
            analogWrite(enable2, constrain(255 - abs(output), 0, 255));
        } else {
            
            right();
            analogWrite(enable1, constrain(255 + abs(output), 0, 255));
            analogWrite(enable2, constrain(255 + abs(output), 0, 255));
        }

        if (Serial.available() > 0) {
            char newCommand = Serial.read();
            if (newCommand == 'M') {
                return;  
            }
        }
    }
}

void SPD() {
    switch (speed) {
        case 0:
            analogWrite(enable1, 0);
            analogWrite(enable2, 0);
            digitalWrite(RGBled1, LOW);
            digitalWrite(RGBled2, LOW);
            digitalWrite(RGBled3, LOW);
            break;
        case 1:
            analogWrite(enable1, 60);
            analogWrite(enable2, 60);
            digitalWrite(RGBled1, HIGH);
            digitalWrite(RGBled2, LOW);
            digitalWrite(RGBled3, LOW);
            break;
        case 2:
            analogWrite(enable1, 135);
            analogWrite(enable2, 135);
            digitalWrite(RGBled1, LOW);
            digitalWrite(RGBled2, HIGH);
            digitalWrite(RGBled3, LOW);
            break;
        case 3:
            analogWrite(enable1, 255);
            analogWrite(enable2, 255);
            digitalWrite(RGBled1, LOW);
            digitalWrite(RGBled2, LOW);
            digitalWrite(RGBled3, HIGH);
            break;
        default:
            break;
    }
}

void forward() {
    digitalWrite(input1, HIGH);
    digitalWrite(input2, LOW);
    digitalWrite(input3, HIGH);
    digitalWrite(input4, LOW);
}

void backward() {
    digitalWrite(input1, LOW);
    digitalWrite(input2, HIGH);
    digitalWrite(input3, LOW);
    digitalWrite(input4, HIGH);
}

void right() {
    digitalWrite(input1, LOW);
    digitalWrite(input2, HIGH);
    digitalWrite(input3, HIGH);
    digitalWrite(input4, LOW);
}

void left() {
    digitalWrite(input1, HIGH);
    digitalWrite(input2, LOW);
    digitalWrite(input3, LOW);
    digitalWrite(input4, HIGH);
}

void stop() {
    digitalWrite(input1, LOW);
    digitalWrite(input2, LOW);
    digitalWrite(input3, LOW);
    digitalWrite(input4, LOW);
}

void ultrasonic() {
    digitalWrite(trigpin, LOW);
    delay(2);
    digitalWrite(trigpin, HIGH);
    delay(10);
    digitalWrite(trigpin, LOW);

    duration = pulseIn(echopin, HIGH);
    distance = duration * 0.034 / 2;
}

void meters() {
    volt = analogRead(voltmeter);
    ampere = analogRead(Ameter);
}

void send_signals() {
    ultrasonic();
    meters();

    Serial.write(volt);
    Serial.write(ampere);
    Serial.write(distance);
    Serial.print("D:"); Serial.print(distance); Serial.print(",");
    Serial.print("V:"); Serial.print(volt); Serial.print(",");
    Serial.print("A:"); Serial.println(ampere);
}
