#include <SoftwareSerial.h>

SoftwareSerial esp(6,7);
char c;

void setup() {
 Serial.begin(9600);
 esp.begin(115200);
 pinMode(6, INPUT);
 pinMode(7, OUTPUT);
}


void loop() {
  
  if (esp.available()){
    c = esp.read();
    Serial.print(c);
  }

  if (Serial.available()){
    c = Serial.read();
    esp.print(c);
  }
  
}
