#define  input1 10
#define  input2 11
#define  enable1 13
#define  input3 1
#define  input4 2
#define  enable2 4
#define  RGBled1 2
#define  RGBled2 3
#define  RGBled3 4
#define  echopin 5
#define  trigpin 6
#define  voltmeter 7
#define  Ameter 8
#define  buzzer 9

float volt, ampere;
int  speed = 0;
double dis = 0;
double distance;
double duration;
char movement;
char command;

void setup()
{

    pinMode(button, INPUT_PULLUP);
    pinMode(trigpin, OUTPUT);
    pinMode(echopin, INPUT);
    pinMode(RGBled1, OUTPUT);
    pinMode(RGBled2, OUTPUT);
    pinMode(RGBled3, OUTPUT);
    pinMode(voltmere, OUTPUT);
    pinMode(Ameter, OUTPUT);
    pinMode(buzzer, OUTPUT);
    pinMode(input1, OUTPUT);
    pinMode(input2, OUTPUT);
    pinMode(input3, OUTPUT);
    pinMode(input4, OUTPUT);
    pinMode(enable1, OUTPUT);
    pinMode(enable2, OUTPUT);

    Serial.begin(9600);

}

void loop()
{
    if(Serial.available() > 0)
    {
        command = Serial.read();
        if(command == M)
        {
            manual();
        }
        else if (command == A)
        {
            autonomous();
        }
    }
}
void manual()
{
    SPD();
    char movement = Serial.read();
    switch(movement)
    {
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

void autonomous()
{
    dis = Serial.read();
    while(true)
    {
        ultrasonic();
        SPD();
        forward();
        if(distance > dis)
        {
            for(int i = dis; i != distance;)
            {
                right();
                delay(10);
                forward();
                if(i == distance)
                {
                    digitalWrite(buzzer, LOW);
                    forward();
                    break;
                }
                else
                {
                    digitalWrite(buzzer,HIGH);
                    continue;
                }
            }
        }
        else if(distance < dis)
        {
            for(int j = dis; j != distance;)
            {
                left();
                delay(10);
                forward();
                if(j == distance)
                {
                    digitalWrite(buzzer, LOW);
                    forward();
                    break;
                }
                else
                {
                    digitalWrite(buzzer, HIGH);
                    continue;
                }
            }
        }
        else if(distance == dis)
        {
            forward();
        }
    }
}

void SPD()
{
    speed = Serial.read();
    if(speed == 0)
    {
        analogWrite(enable1, 0);
        analogWrite(enable2, 0);
    }
    else if(speed == 1)
    {
        analogWrite(enable1, 60);
        analogWrite(enable2, 60);
        digitalWrite(RGBled1, HIGH);
    }
    else if(speed == 2)
    {
        analogWrite(enable1, 135);
        analogWrite(enable2, 135;
        digitalWrite(RGBled2, HIGH);
    }
    else if (speed == 3)
    {
        analogWrite(enable1, 255);
        analogWrite(enable2, 255);
        digitalWrite(RGBled3, HIGH);
    }
}

void forward()
{
    digitalWrite(input1, HIGH);
    digitalWrite(input2, LOW);
    digitalWrite(input3, HIGH);
    digitalWrite(input4, LOW);
}
void backward()
{
    digitalWrite(input1, LOW);
    digitalWrite(input2, HIGH);
    digitalWrite(input3, LOW);
    digitalWrite(input4, HIGH);
}

void right()
{
    digitalWrite(input1, LOW);
    digitalWrite(input2, HIGH);
    digitalWrite(input3, HIGH);
    digitalWrite(input4, LOW);
}

void left()
{
    digitalWrite(input1, HIGH);
    digitalWrite(input2, LOW);
    digitalWrite(input3, LOW);
    digitalWrite(input4, HIGH);
}

void stop()
{
    digitalWrite(input1, LOW);
    digitalWrite(input2, LOW);
    digitalWrite(input3, LOW);
    digitalWrite(input4, LOW);
}

double ultrasonic()
{
    digitalWrite(trigpin, LOW);
    delay(2);
    digitalWrite(trigpin, HIGH);
    delay(10);
    digitalWrite(trigpin, LOW);

    duration= pulseIn(echopin, HIGH);
    distance= duration*0.034/2;
    return distance;
}

void meters()
{
    volt = analogRead(voltmeter);
    Serial.write(volt);
    ampere = analogRead(Ameter);
    Serial.write(ampere);
}

