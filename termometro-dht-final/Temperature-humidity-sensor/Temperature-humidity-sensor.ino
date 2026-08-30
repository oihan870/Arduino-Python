#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11

float tempF;
float tempC;
float humidity;

int DT=1000;
int SetTime=500;

DHT TH(DHTPIN,DHTTYPE);
void setup() {
  Serial.begin(115200);
  TH.begin();
  delay(SetTime);
}

void loop() {
  tempC=TH.readTemperature();
  tempF=TH.readTemperature(true);
  humidity=TH.readHumidity();
  Serial.print(tempC);
  Serial.print("degrees C, ");
  Serial.print(tempF);
  Serial.print("degrees F, ");
  Serial.print(humidity);
  Serial.println("% humidity");
  delay(DT);
}
