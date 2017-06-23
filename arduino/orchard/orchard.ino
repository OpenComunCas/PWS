/* 
 * PWS. Nodo de recogida de datos.
 */
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/wdt.h>
#include <DHT.h>

#define DHTTYPE DHT11

const byte LEDPIN = 13;
const byte RELAYPIN = 7;
const byte DHTPIN = 4;
const byte SOILPIN = A0;
const byte LIGHTPIN = A5;
const int SOIL_THRESHOLD = 500;

DHT dht(DHTPIN, DHTTYPE);
float temp;
int light, soil;

ISR(WDT_vect){
  wdt_disable();  // disable watchdog
}

void myWatchdogEnable(const byte interval){ 
  MCUSR = 0;                          // reset various flags
  WDTCSR |= 0b00011000;               // see docs, set WDCE, WDE
  WDTCSR =  0b01000000 | interval;    // set WDIE, and appropriate delay

  wdt_reset();
  set_sleep_mode (SLEEP_MODE_PWR_DOWN); 
  sleep_mode();            // now goes to Sleep and waits for the interrupt
} 

void setup() {
  Serial.begin(9600);

  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, LOW);
  pinMode(RELAYPIN, OUTPUT);
  digitalWrite(RELAYPIN, LOW);
  
  dht.begin();
  pinMode(DHTPIN, INPUT);
  
  //Configuracion del Watchdog
  wdt_enable(WDTO_8S);
}

void loop() {
  wdt_reset();
  delay(200);

  temp = dht.readTemperature();
  light = analogRead(LIGHTPIN);
  soil = analogRead(SOILPIN);

  wdt_reset();

  if (soil <= SOIL_THRESHOLD){
    wdt_reset();
    digitalWrite(RELAYPIN, HIGH);
    digitalWrite(LEDPIN, HIGH);
    delay(1500);
    digitalWrite(LEDPIN, LOW);
    digitalWrite(RELAYPIN, LOW);
  }
     
  Serial.print("L:");
  Serial.print(light);
  Serial.print("S:");
  Serial.print(soil);
  Serial.print("T:");
  Serial.println(temp);
  delay(200);

  int i;
  for (i = 0; i <15; i++){ 
    myWatchdogEnable (0b100001);  // 8 seconds
  }    
}
