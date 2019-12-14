// Quadcopter type X
//
// M[0]   M[3]
//   \    /
//    \  /
//    /  \
//   /    \
// M[1]   M[2]


//#include <Scheduler.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <PID_v1.h>

const String ESP[] = {"\"your_wifi_ssid\"", "\"your_wifi_password\""}; //e-ssid, psk
const int INTERVAL = 40;  // Controll Cycle [ms]
const int MPU = 0x68;
const int RATIO = 0.95;   // Parameter for Complementary Filter
const int MOTORS[] = {5, 6, 9, 10};
/*
  MOTORS[0] : Front Left
  MOTORS[1] : Back  Left
  MOTORS[2] : Back  Right
  MOTORS[3] : Front Right
*/

uint32_t timer;
double dt;
uint8_t connectionId = 0;
uint16_t Throttle = 0;
float acc[3];       // Roll,Pitch,Yaw angle calculate from acceleration
float gyro[3];      // X,Y,Z
double Outputs[3];  // PID outpus ... 0: Roll, 1: Pitch, 2: Yaw
double angle[6];    // X, Y, Z, BeforeX, BeforeY, BeforeZ
int16_t IMU[7];     // Acx, AcY, AcZ, Tmp, GyX, GyY, GyZ
uint16_t m_power[4] = {0, 0, 0, 0};
int8_t Recv_Data[4];

//Scheduler scheduler = Scheduler();
SoftwareSerial esp8266(3, 4);
PID Roll_PID(&angle[1], &Outputs[0], 0, 1.5, 2.0, 0.005, DIRECT);
PID Pitch_PID(&angle[0], &Outputs[1], 0, 1.5, 2.0, 0.005, DIRECT);
PID Yaw_PID(&angle[2], &Outputs[2], 0, 1.5, 1.5, 0.025, DIRECT);


String sendData(String command, int timeout) {
  String res = "";
  esp8266.print(command);

  long int time = millis();

  while ((time + timeout) > millis()) {
    while (esp8266.available()) {
      char c = esp8266.read();
      res += c;
    }
  }
  //Serial.println(res);
  return res;
}

String recvData() {
  String res = "";

  if (esp8266.available()) {
    if (esp8266.find(":")) {
      while (esp8266.available()) {
        char c = esp8266.read();
        if (c == '\n') {
          //Serial.print("Received -> "); Serial.println(res);
          return res;
        }
        res += c;
      }
    }
  }
  return res;
}

void Get_Sensor_Data() {
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);                // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 14, true); // request a total of 14 registers

  for (int i = 0; i < 7; i++) {
    IMU[i] = Wire.read() << 8 | Wire.read();
  }
  /*
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  */
}

void Attitude_Estimation() {
  acc[0] = atan2(IMU[1],  IMU[2]) * 180 / PI;
  acc[1] = atan2(-IMU[0], IMU[2]) * 180 / PI;
  //acc[2] = atan2(IMU[0], IMU[1]) * 180 / PI;

  gyro[0] += IMU[5] / 131.0 * dt;
  gyro[1] += IMU[6] / 131.0 * dt;
  gyro[2] += (int)(IMU[7] / 131.0 * dt);
  /*
  roll_acc = atan2(AcY,AcZ) * 180 / PI;
  pitch_acc = atan2(-AcX,AcZ) * 180 / PI;
  yaw_acc = atan2(AcX,AcY) * 180 / PI;

  gyroX += GyX / 131.0 * dt;
  gyroY += GyY / 131.0 * dt;
  gyroZ += (int)(GyZ / 131.0 * dt);
  */

  angle[0] = RATIO * (angle[3] + gyro[0]) + (1.0 - RATIO) * acc[0];
  angle[1] = RATIO * (angle[4] + gyro[1]) + (1.0 - RATIO) * acc[1];
  //angle[2] = RATIO*(angle[5] + gyro[2]) + (1.0 - RATIO) * acc[2];
  angle[2] = gyro[2];
}

void pid_compute(uint16_t* rotor_1, uint16_t* rotor_2, uint16_t* rotor_3, uint16_t* rotor_4) {

  Roll_PID.Compute();
  Pitch_PID.Compute();
  Yaw_PID.Compute();

  *rotor_1 = Throttle + (Outputs[0] / 2) + (Outputs[1] / 2) + Outputs[2];
  *rotor_2 = Throttle + (Outputs[0] / 2) - (Outputs[1] / 2) - Outputs[2];
  *rotor_3 = Throttle - (Outputs[0] / 2) - (Outputs[1] / 2) + Outputs[2];
  *rotor_4 = Throttle - (Outputs[0] / 2) + (Outputs[1] / 2) - Outputs[2];
}

void setup() {
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  //Serial.begin(115200);
  esp8266.begin(115200);

  sendData("AT+RST\r\n", 1000);
  sendData("AT+CWMODE=2\r\n", 1000);
  sendData("AT+CWSAP=" + ESP[0] + "," + ESP[1] + ",5,3\r\n", 1000);
  sendData("AT+CIPMUX=1\r\n", 1000);
  sendData("AT+CIPSERVER=1,8530\r\n", 1000);

  for (int i = 0; i < 4; i++) {
    analogWrite(MOTORS[i], 150);
  }
  delay(5);
  for (int i = 0; i < 4; i++) {
    analogWrite(MOTORS[i], 0);
  }

  while (1) {
    if (esp8266.available()) {
      connectionId = esp8266.read() - 48;
      if (esp8266.find("C")) {
        while (esp8266.available()) {
          esp8266.read();
          //Serial.write(esp8266.read());
        }
        break;
      }
    }
    delay(500);
  }

  Roll_PID.SetSampleTime(INTERVAL);
  Pitch_PID.SetSampleTime(INTERVAL);
  Yaw_PID.SetSampleTime(INTERVAL);

  Roll_PID.SetOutputLimits(-75.0, 75.0);
  Pitch_PID.SetOutputLimits(-75.0, 75.0);
  Yaw_PID.SetOutputLimits(-50.0, 50.0);

  Roll_PID.SetMode(AUTOMATIC);
  Pitch_PID.SetMode(AUTOMATIC);
  Yaw_PID.SetMode(AUTOMATIC);

  Get_Sensor_Data();
  Attitude_Estimation();

  angle[3] = RATIO * (angle[3] + gyro[0]) + (1.0 - RATIO) * acc[0];
  angle[4] = RATIO * (angle[4] + gyro[1]) + (1.0 - RATIO) * acc[1];
  angle[5] = gyro[2];

  timer = millis();
}

void loop() {
  dt = (double)(millis() - timer) / 1000;
  timer = millis();

  Get_Sensor_Data();
  Attitude_Estimation();
  pid_compute(&m_power[0], &m_power[1], &m_power[2], &m_power[3]);

  String recv_data = recvData();

  if (recv_data.length() == 20) {
    if (recv_data.charAt(0) == 'T') {
      Recv_Data[0] = (recv_data.substring(1, 4)).toInt();
      Recv_Data[1] = (recv_data.substring(5, 9)).toInt();
      Recv_Data[2] = (recv_data.substring(10, 14)).toInt();
      Recv_Data[3] = (recv_data.substring(15, 19)).toInt();

      /* For Debug
      Serial.print("Throttle -> "); Serial.println(Recv_Data[0]);
      Serial.print("Roll -> "); Serial.println(Recv_Data[1]);
      Serial.print("Pitch -> "); Serial.println(Recv_Data[2]);
      Serial.print("Yaw -> "); Serial.println(Recv_Data[3]);
      */

      if ((Throttle + Recv_Data[0]) < 0) {
        Throttle = 0;
      } else if ((Throttle + Recv_Data[0]) > 150) {
        Throttle = 150;
      } else {
        Throttle += Recv_Data[0];
      }

      m_power[0] += Recv_Data[1] + Recv_Data[2] + Recv_Data[3];
      m_power[1] += Recv_Data[1] - Recv_Data[2] - Recv_Data[3];
      m_power[2] += (-1 * Recv_Data[1]) - Recv_Data[2] + Recv_Data[3];
      m_power[3] += (-1 * Recv_Data[1]) + Recv_Data[2] - Recv_Data[3];
    }
  }

  for (int i = 0; i < 4; i++) {
    if (m_power[i] < 0) {
      m_power[i] = 0;
    } else if (m_power[i] > 200) {
      m_power[i] = 200;
    }
  }

  for (int i = 0; i < 4; i++) {
    analogWrite(MOTORS[i], m_power[i]);
  }

  angle[3] = angle[0];
  angle[4] = angle[1];
  angle[5] = angle[2];

  delay(INTERVAL - (int)(millis() - timer));
}
