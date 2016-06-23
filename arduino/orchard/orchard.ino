/*
 *  Aplicación de control del huerto
*/

#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/wdt.h>

#include <MsTimer2.h>

#include <DHT.h>

//Constantes
#define DHTTYPE DHT22

const byte I2CADDR = 4;

const byte LEDPIN = 13;
const byte RELAYIN1 = 3;
//const byte RELAYIN2 = 2;
const byte DHTPIN = 4;
const byte LIGHTPIN = A0;
const byte SOILPIN = A1;


//Variables generales
DHT dht(DHTPIN, DHTTYPE);

float temp, hum;
int light, soil;
int riego;

/*
   Variable de estado interno del sistema.
   Cada uno de sus bits controla un comportamiento concreto

   bit 0 -> modo debug
   bit 1 -> actuación
   bit 2 -> comunicación
   bit 3 -> sensorización
   bit 4 -> control
   bit 5 -> reservado
   bit 6 -> reservado
   bit 7 -> reservado

*/

byte estado = B00011110;

int len;

void setup() {
  pinMode(LEDPIN, OUTPUT);

  //Conexión serie con ESP8266
  Serial.begin(115200);

  //Configuración del módulo de relés
  //HIGH -> Apagado. LOW -> Encendido
  pinMode(RELAYIN1, OUTPUT);
  //pinMode(RELAYIN2, OUTPUT);
  digitalWrite(RELAYIN1, HIGH);
  //digitalWrite(RELAYIN2, HIGH);

  //Configuración del módulo DHT22
  dht.begin();
  pinMode(DHTPIN, INPUT);

  //Configuración de Timer para el actuador
  MsTimer2::set(10000, detenerRiego);

  //Configuración del watchdog
  wdt_enable(WDTO_8S);

}


//Configuración del modo de bajo consumo
void sleepNow(){
  
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  sleep_mode();

  sleep_disable();
}


//Función del actuador
void detenerRiego() {
  digitalWrite(RELAYIN1, HIGH);
  MsTimer2::stop();
  riego = 0;
}


void loop() {
  wdt_reset();
  delay(500);

  if (estado & 16) { //Comprueba estado control

    //Realiza mediciones
    if (estado & 8) { //comprueba estado sensorización
      digitalWrite(LEDPIN, HIGH);

      temp = dht.readTemperature();
      hum = dht.readHumidity();
      light = analogRead(LIGHTPIN);
      soil = analogRead(SOILPIN);

      digitalWrite(LEDPIN, LOW);
    }

    //Comprueba umbrales y activa actuadores
    if ((soil < 500) && (estado & 2) && (riego == 0)) { //riego sólo si está activado
      digitalWrite(RELAYIN1, LOW);
      MsTimer2::start();
      riego = 1;
    }
    //else
    //  digitalWrite(RELAYIN1, HIGH);

    //Envía por serie
    if (estado & 4) {

      Serial.print("Datos!\n");
      //delay(100);
      Serial.print("Luz: ");
      Serial.print(light);
      Serial.print("\nSoil: ");
      Serial.print(soil);
      Serial.print("\nTemp: ");
      Serial.print(temp);
      Serial.print("\nHumedad: ");
      Serial.print(hum);
      delay(200);
    }
  }

  //Reinicio el watchdog
  wdt_reset();

  //Y me pongo a dormir, a los 8 segundos todo se reiniciará
  sleepNow();

}

