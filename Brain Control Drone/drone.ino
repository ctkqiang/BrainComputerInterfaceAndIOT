#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);
float Total_angle_x, Total_angle_y, Total_angle_z;
float X,Y,Z,Z2,Z3;
float deg_to_rad = 3.141592654/180.0;

float dt = 0;
long currentTime=0;
long previousTime=0;

//More variables for the code
int mot_activated=0;
float input_THROTTLE=0;

//////////////////////////////motor speed ///////////////////////////
float pwm_L_F, pwm_L_B, pwm_R_F, pwm_R_B;

//////////////////////////////motor pin /////////////////////////////
int L_F_prop=11; 
int L_B_prop=9;
int R_F_prop=3;
int R_B_prop=10;

//////////////////////////////PID FOR ROLL///////////////////////////
float roll_PID, roll_error, roll_previous_error;
float roll_pid_p=0;
float roll_pid_i=0;
float roll_pid_d=0;
///////////////////////////////ROLL PID CONSTANTS////////////////////
double roll_kp=0.05;//0.5
double roll_ki=0.00001;//0
double roll_kd=0.005;//0.0005
float input_roll_angle = 0;   

//////////////////////////////PID FOR PITCH//////////////////////////
float pitch_PID, pitch_error, pitch_previous_error;
float pitch_pid_p=0;
float pitch_pid_i=0;
float pitch_pid_d=0;
///////////////////////////////PITCH PID CONSTANTS///////////////////
double pitch_kp=0.001;//0.5//0.001
double pitch_ki=0.00005;
double pitch_kd=0.001;//0.0001//0.00009//0.001
float input_pitch_angle = 0;   

//////////////////////////////PID FOR YAW//////////////////////////
float yaw_PID, yaw_error, yaw_previous_error;
float yaw_pid_p=0;
float yaw_pid_i=0;
float yaw_pid_d=0;
///////////////////////////////yaw PID CONSTANTS///////////////////
double yaw_kp=0.05;//0.5
double yaw_ki=0;
double yaw_kd=0.01;//0.0001
float input_yaw_angle = 0;   

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}

void loop() {
  mpu6050.update();

 currentTime=millis();
 if(currentTime - previousTime > 100){
   
    Total_angle_x=mpu6050.getAngleX();
    Total_angle_y=mpu6050.getAngleY();

    if(Total_angle_x<32)
    {X= map(Total_angle_x, -25, 32, -90, 0);}
    else
    {X= map(Total_angle_x,32, 75,0,90);}

    if(Total_angle_y<17)
    {Y= map(Total_angle_y, -35, 17, -90, 0);}           
    else
    {Y= map(Total_angle_y,17,64,0,90);}
       
    Z=mpu6050.getAngleZ();

    Z2=sin(0.5*Z*deg_to_rad);
    Z3=Z2*90;
  Serial.println(Z3);
  roll_error = input_roll_angle - X;
  pitch_error = input_pitch_angle - Y;
  yaw_error = input_yaw_angle - Z3;

  Serial.print("  angleX : ");Serial.print(roll_error);
  Serial.print("  angleY : ");Serial.print(pitch_error);
  Serial.print("  angleZ : ");Serial.println(yaw_error);
  
  roll_pid_p = roll_kp*roll_error;
  pitch_pid_p = pitch_kp*pitch_error;
  yaw_pid_p = yaw_kp*yaw_error;

  roll_pid_i += roll_ki*roll_error*0.1;
  pitch_pid_i += pitch_ki*pitch_error*0.1;
  yaw_pid_i += yaw_ki*yaw_error*0.1;

  roll_pid_d = roll_kd*((roll_error - roll_previous_error)/0.1);
  pitch_pid_d = pitch_kd*((pitch_error - pitch_previous_error)/0.1);
  yaw_pid_d = yaw_kd*((yaw_error - yaw_previous_error)/0.1);

  roll_PID = roll_pid_p + roll_pid_i + roll_pid_d; Serial.print("X_PID: "); Serial.print(roll_PID);
  pitch_PID = pitch_pid_p + pitch_pid_i + pitch_pid_d; Serial.print("Y_PID: ");Serial.print(pitch_PID);
  yaw_PID = yaw_pid_p + yaw_pid_i + yaw_pid_d; Serial.print("Z_PID: ");Serial.println(yaw_PID);

      previousTime = currentTime;    
  }

  pwm_R_F  = 100 + input_THROTTLE - roll_PID - pitch_PID - yaw_PID;
  pwm_R_B  = 100 + input_THROTTLE - roll_PID + pitch_PID + yaw_PID;
  pwm_L_B  = 100 + input_THROTTLE + roll_PID + pitch_PID - yaw_PID;
  pwm_L_F  = 100 + input_THROTTLE + roll_PID - pitch_PID + yaw_PID;

  /*pwm_R_F = constrain(pwm_R_F,50,255);
  pwm_R_B = constrain(pwm_R_B,50,255);
  pwm_L_B = constrain(pwm_L_B,50,255);
  pwm_L_F = constrain(pwm_L_F,50,255);*/
  
  roll_previous_error = roll_error; 
  pitch_previous_error = pitch_error;
  yaw_previous_error = yaw_error;



  if(mot_activated)
  {
    analogWrite(L_F_prop, pwm_L_F);
    analogWrite(L_B_prop, pwm_L_B);
    analogWrite(R_F_prop, pwm_R_F);
    analogWrite(R_B_prop, pwm_R_B);
  
    Serial.print("RF: "); Serial.println(pwm_R_F);
    Serial.print("RB: "); Serial.println(pwm_R_B);
    Serial.print("LB: "); Serial.println(pwm_L_B);    
    Serial.print("LF: "); Serial.println(pwm_L_F);    
    Serial.println("   |   ");
  }
  if(!mot_activated)
  {
    analogWrite(L_F_prop, 0);
    analogWrite(L_B_prop, 0);
    analogWrite(R_F_prop, 0);
    analogWrite(R_B_prop, 0);
  }  

  if(Serial.available()>0)
  {
     int control = Serial.read();  
  
     if( control=='q')
     {      
        input_THROTTLE+=10;
        mot_activated=1;
     }
     
     if( control=='e')
     {
        input_THROTTLE-=10;       
        if(input_THROTTLE<=0){input_THROTTLE=0;}    
     }

     if( control=='a'){input_roll_angle-=10;}
      
     if( control=='d'){input_roll_angle+=10;}
      
     if( control=='w'){input_pitch_angle+=10;}
  
     if( control=='s'){input_pitch_angle-=10;}

     if( control=='z'){input_yaw_angle+=10;}

     if( control=='c'){input_pitch_angle-=10;}


  
     if( control=='x')
     {
        input_THROTTLE=0;
        input_roll_angle=0;
        input_pitch_angle=0;
        mot_activated=0;
      }
   }
} 
