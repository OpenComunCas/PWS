#include <avr/interrupt.h>
#include <avr/sleep.h>
long distancia;
long tiempo;
void wakeUpNow(){
  sleep_disable(); 

}

void sleepNow(){
  sleep_mode();
}

void setup(){
  Serial.begin(9600);
  pinMode(9, OUTPUT); /*activación del pin 9 como salida: para el pulso ultrasónico*/
  pinMode(8, INPUT);

}

void loop(){

}
void getDistance(){
    digitalWrite(9,LOW); /* Por cuestión de estabilización del sensor*/
    delayMicroseconds(5);
    digitalWrite(9, HIGH); /* envío del pulso ultrasónico*/
    delayMicroseconds(10);
    tiempo=pulseIn(8, HIGH); /* Función para medir la longitud del pulso entrante. Mide el tiempo que transcurrido entre el envío
    del pulso ultrasónico y cuando el sensor recibe el rebote, es decir: desde que el pin 12 empieza a recibir el rebote, HIGH, hasta que
    deja de hacerlo, LOW, la longitud del pulso entrante*/
    distancia= int(0.017*tiempo); /*fórmula para calcular la distancia obteniendo un valor entero*/
    /*Monitorización en centímetros por el monitor serial*/
    Serial.println(distancia);
}
void serialEvent() {
  while (Serial.available()) {
    String str = Serial.readStringUntil('\n');
    if ( str.equals("dist") ){
      getDistance();
    }else {
      Serial.println("Not implemented yet.");
    }    
  }
}
