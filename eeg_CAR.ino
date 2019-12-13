//Initializing the Pin
/*
*  ALL RIGHT RESERVED || ANG JIA YI COPYRIGHT
*/
int ran1;
int ran2;
int power=11;
int car1 = 7;
int car2 = 8;
int button = 4;
int input1 = 0;
int input2 = 0;
int condition = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
pinMode(car1,OUTPUT);
pinMode(car2,OUTPUT);
pinMode(power,OUTPUT);
pinMode(button,INPUT);
pinMode(13,OUTPUT);
digitalWrite(power,HIGH);
analogWrite(car1,0);
analogWrite(car2,0);
//delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:

if(digitalRead(button) == LOW)
{
  while(digitalRead(button) ==LOW);
  if(condition == 0)
  {condition = 1;digitalWrite(power,HIGH);analogWrite(car1,0);analogWrite(car2,0);delay(1000);}
  else
  {condition = 0;digitalWrite(power,LOW);delay(1000);}
}

else if(condition==0) //no brain control
{
  ran1=random(150,210);
  ran2=random(150,210);
  analogWrite(car1,ran1);
  analogWrite(car2,ran2);
  delay(500);
  digitalWrite(13,LOW); //led light indicator no brain control 13 light off
}

else if(condition ==1)
{
    digitalWrite(13,HIGH);
    input1=analogRead(A0);
    input2=analogRead(A2);
    Serial.print("input1=");
    Serial.println(input1);
    Serial.print("input2=");
    Serial.println(input2);
    if(input1>400)
    {
      analogWrite(car1,0);
    }
    if(input2>400)
    {
      analogWrite(car2,0);
    }
   
    if(input1<400 && input1>100)
    {
      analogWrite(car1,160);
    }
    if(input2<400 && input2>100)
    {
      analogWrite(car2,160);
    } 
    if(input1<100 && input1>1)
    {
      analogWrite(car1,180);
    }
    if(input2<100 && input2>1)
    {
      analogWrite(car2,180);
    } 
    if(input1==0)
    {
      analogWrite(car1,210);
    }
    if(input2==0)
    {
      analogWrite(car2,210);
    }
    delay(200);
}
else
{
  analogWrite(car1,0);
  analogWrite(car2,0);  
}
}
