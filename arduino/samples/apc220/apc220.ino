/* APC220 BEACON SAMPLE.
 *  Envía datos, parpadea y luego espera un segundo segundo.
 */

void setup() {
 Serial.begin(9600);
 pinMode(13, OUTPUT);
}

void loop() {
  Serial.println("Hello, World!");
  digitalWrite(13, HIGH);
  delay(100);
  digitalWrite(13, LOW);
  delay(1000);
}
