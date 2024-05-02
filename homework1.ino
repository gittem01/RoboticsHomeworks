#include <helper_3dmath.h>
#include <MPU6050_6Axis_MotionApps612.h>

MPU6050 sensor;

int accx, accy, accz, gyrox, gyroy, gyroz;
uint8_t fifoBuffer[64];
Quaternion q;

void setup()
{
  Serial.begin(9600);

  Serial.println("Start");
  
  sensor.initialize();
  sensor.dmpInitialize();
  sensor.setDMPEnabled(true);

  sensor.CalibrateAccel(6);
  sensor.CalibrateGyro(6);
}

void loop()
{
  sensor.getMotion6(&accx, &accy, &accz, &gyrox, &gyroy, &gyroz);

  if (sensor.dmpGetCurrentFIFOPacket(fifoBuffer))
  {
    float data[3];
    sensor.dmpGetQuaternion(&q, fifoBuffer);
    sensor.dmpGetGravity(&gVec, &q);
    sensor.dmpGetEuler(data, &q);

    Serial.print (accx); Serial.print(" ");
    Serial.print (accy); Serial.print(" ");
    Serial.print (accz); Serial.print(" ");
    Serial.print (data[0]); Serial.print(" ");
    Serial.print (data[1]); Serial.print(" ");
    Serial.print (data[2]); Serial.print("\n");
  }
}