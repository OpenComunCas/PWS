/* 
 * Aplicación de control del escenario de pruebas 
 * Tiene varias funciones
 * 1. Lee los sensores de forma periódica, en funcion a los valores obtenidos activa los actuadores
 * 2. Recibe órdenes por I2C de la aplicación de control
 * 3. Envía la información de los sensores vía WiFi
 * 
 * Diego Noceda Davila
 * Febrero 2016
 */

#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/wdt.h>

#include <MsTimer2.h>

#include<Wire.h>
#include <DHT.h>

//Constantes
#define DHTTYPE DHT22

const byte I2CADDR = 4;

const byte LEDPIN = 13;
const byte RELAYIN1 = 3;
const byte RELAYIN2 = 2;
const byte DHTPIN = 4;
const byte LIGHTPIN = A0;
const byte SOILPIN = A1;


//Variables generales
DHT dht(DHTPIN, DHTTYPE);

float temp, hum;
int light, soil;
int riego;

/*
 * Variable de estado interno del sistema. 
 * Cada uno de sus bits controla un comportamiento concreto
 * 
 * bit 0 -> modo debug
 * bit 1 -> actuación
 * bit 2 -> comunicación
 * bit 3 -> sensorización
 * bit 4 -> control
 * bit 5 -> reservado
 * bit 6 -> reservado
 * bit 7 -> reservado
 *
 */
byte estado = B00011110;

int len;

void setup() {
  pinMode(LEDPIN, OUTPUT);

  //Conexión serie con ESP8266
  Serial.begin(115200);

  //Configuración I2C
  Wire.begin(I2CADDR);
  Wire.onRequest(requestEvent); //Registra evento de petición de información
  Wire.onReceive(receiveEvent); //Registra evento de orden
     
  //Configuración del módulo de relés
  //HIGH -> Apagado. LOW -> Encendido
  pinMode(RELAYIN1, OUTPUT);
  pinMode(RELAYIN2, OUTPUT);
  digitalWrite(RELAYIN1, HIGH); 
  digitalWrite(RELAYIN2, HIGH); 

  //Configuración del módulo DHT22
  dht.begin();
  pinMode(DHTPIN, INPUT);

  //Configuración de Timer para el actuador
  MsTimer2::set(10000, detenerRiego);
  
  //Configuracion del Watchdog
  wdt_enable(WDTO_8S);
}

//Modo de bajo consumo
void sleepNow(){
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  sleep_mode();
}

//Función del actuador
void detenerRiego() {
  digitalWrite(RELAYIN1, HIGH);
  MsTimer2::stop();
  riego = 0;
}


void loop() {
  wdt_reset();
  delay(2000);

  if (estado & 16){ //Comprueba estado control
  
    //Realiza mediciones
    if (estado & 8){ //comprueba estado sensorización
      digitalWrite(LEDPIN, HIGH);
      
      temp = dht.readTemperature();
      hum = dht.readHumidity();
      light = analogRead(LIGHTPIN);
      soil = analogRead(SOILPIN);
    
      digitalWrite(LEDPIN, LOW);
    }
    wdt_reset();
    
    //Comprueba umbrales y activa actuadores
    if ((soil < 500) && (estado & 2) && (riego == 0)){ //riego sólo si está activado
      digitalWrite(RELAYIN1, LOW);
      MsTimer2::start();
      riego = 1;
    }
    //else
    //  digitalWrite(RELAYIN1, HIGH);
  
    //Envía cosas al ESP8266
    if (estado & 4){
  
        Serial.print("AT+CIPSTART=\"TCP\",\"192.168.1.31\",5000\r\n");
        delay(100);
  
        len = 45; //Tamaño de los datos a enviar
        
        Serial.print("AT+CIPSEND=");
        Serial.println(len);
        delay(100);
  
        Serial.print("Luz: ");
        Serial.print(light);
        Serial.print("\nSoil: ");
        Serial.print(soil);
        Serial.print("\nTemp: ");
        Serial.print(temp);
        Serial.print("\nHumedad: ");
        Serial.print(hum);
        Serial.print("\n\r\n\r");
        delay(200);
        
        Serial.println("AT+CIPCLOSE");
        delay(200);
        wdt_reset();
     }
  }
  
  wdt_reset();
  //Dormir
  sleepNow();
}

//Funciones I2C
void requestEvent() {
  int buf[7];
  buf[0] = light;
  buf[1] = soil;
  buf[2] = temp;
  buf[3] = (int) temp>>16;
  buf[4] = hum;
  buf[5] = (int) hum>>16;
  buf[6] = estado;

  Wire.write((byte *)buf, sizeof(buf)); 
}

void receiveEvent(int count) {
  estado = Wire.read();
}

