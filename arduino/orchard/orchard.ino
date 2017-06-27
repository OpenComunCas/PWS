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

int SOIL_THRESHOLD = 500;

DHT dht(DHTPIN, DHTTYPE);
float temp;
int light, soil;

boolean wakeup_flag = false;
String input_cmd = "";
boolean cmd_complete = false;
unsigned long lastSleep;
const unsigned long WAIT_TIME = 5000;

ISR(WDT_vect){
  wdt_disable();  // disable watchdog
}

ISR(PCINT2_vect){
  wakeup_flag = true;
}

void myWatchdogEnable(const byte interval){
  MCUSR = 0;                          // reset various flags
  WDTCSR |= 0b00011000;               // set WDCE, WDE
  WDTCSR =  0b01000000 | interval;    // set WDIE, and appropriate delay
  
  wdt_reset();
  noInterrupts ();

  byte old_ADCSRA = ADCSRA;
  // disable ADC
  ADCSRA = 0;
  // pin change interrupt (D0)
  PCMSK2 |= bit (PCINT16); // want pin 0
  PCIFR  |= bit (PCIF2);   // clear any outstanding interrupts
  PCICR  |= bit (PCIE2);   // enable pin change interrupts for D0 to D7

  set_sleep_mode (SLEEP_MODE_IDLE);
  power_adc_disable();
  power_spi_disable();
  power_timer0_disable();
  power_timer1_disable();
  power_timer2_disable();
  power_twi_disable();
  // UCSR0B &= ~bit (RXEN0);  // disable receiver
  // UCSR0B &= ~bit (TXEN0);  // disable transmitter

  sleep_enable();
  interrupts ();
  sleep_mode();
  
  sleep_disable();
  power_all_enable();
  ADCSRA = old_ADCSRA;
  PCICR  &= ~bit (PCIE2);   // disable pin change interrupts for D0 to D7
  //UCSR0B |= bit (RXEN0);  // enable receiver
  //UCSR0B |= bit (TXEN0);  // enable transmitter
} 

void setup() {
  Serial.begin(9600);
  input_cmd.reserve(12);

  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, LOW);
  pinMode(RELAYPIN, OUTPUT);
  digitalWrite(RELAYPIN, LOW);
  
  dht.begin();
  pinMode(DHTPIN, INPUT);
  
  //Watchdog config
  wdt_enable(WDTO_8S);
}

char inChar;

void loop() {
  if (wakeup_flag == true){
    lastSleep = millis();
    while (true){
      if (Serial.available() > 0){
        inChar = (char)Serial.read();
        input_cmd += inChar;
        if (inChar == '\n'){
           cmd_complete = true;
           break;
        }
      }
      if (millis() - lastSleep >= WAIT_TIME){
        input_cmd = "";
        cmd_complete = false;
        break;
      }
    }
    if (cmd_complete){
      Serial.println(input_cmd);
      if (input_cmd[0] == 's'){
        int newvalue = input_cmd.substring(1).toInt();
        SOIL_THRESHOLD = newvalue;
        Serial.println("ok");
      }
      if (input_cmd[0] == 'q'){
        Serial.println(SOIL_THRESHOLD);
      }
      input_cmd = "";
      cmd_complete = false;
      Serial.flush();
    }
    wakeup_flag = false;
  }
  else{
    wdt_reset();
    temp = dht.readTemperature();
    light = analogRead(LIGHTPIN);
    soil = analogRead(SOILPIN);

    if (soil <= SOIL_THRESHOLD){
      wdt_reset();
      Serial.println(">action");
      Serial.println("water");
      digitalWrite(RELAYPIN, HIGH);
      digitalWrite(LEDPIN, HIGH);
      delay(1500);
      digitalWrite(LEDPIN, LOW);
      digitalWrite(RELAYPIN, LOW);
    }
    Serial.println(">data");
    Serial.print("soil!");
    Serial.print(soil);
    Serial.print(":light!");
    Serial.print(light);
    Serial.print(":temp!");
    Serial.println(temp);
    delay(200);
  }

  int i;
  for (i=0; i<15; i++){
    myWatchdogEnable (0b100001);  // 8 seconds
  }
}


