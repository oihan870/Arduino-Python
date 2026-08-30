int Pin = A2;
int readVal;
int DL = 100;
void setup() {
  pinMode(Pin, INPUT);
  Serial.begin(115200);
}

void loop() {
  readVal = analogRead(Pin);
  Serial.println(readVal);
  delay(DL);
}
