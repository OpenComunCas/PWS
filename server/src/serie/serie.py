#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
serie.py

Script para la comunicación por medio de puerto serie con el Arduino monitor del sistema

"""

import serial
import time
import db.medidas as m 
PORT = '/dev/ttyACM0'
BAUD = 115200
TIMEOUT = 2.01

ser = serial.Serial()

def open():
  print 'Iniciando Arduino...'
  print 'Configurando conexión serie: \nPuerto: '+PORT+'\nBaudrate: '+str(BAUD)+'\nTimeout: '+str(TIMEOUT)
  ser.port = PORT
  ser.baudrate = BAUD
  ser.timeout = TIMEOUT
  ser.open() 

  time.sleep(4)

def close():
  ser.close()

def setConfig(port=PORT, baud=BAUD, timeout=TIMEOUT):
  ser.port = port
  ser.baudrate = baudrate
  ser.timeout = timeout

def getConfig():
  return {'port':ser.port, 'baudrate':ser.baudrate, 'timeout':ser.timeout}

def get_data():
    open()
    ser.write("all\n")
    datos = ser.read(1024).split("\r")[0].split(",")
    close()
    return datos

def main():
    datos = get_data()
    m.insertar(float(datos[0]),float(datos[1]),float(datos[2]),float(datos[3]),float(datos[4]))
    

if __name__ == "__main__":
    open()
    ser.write("all\n")
    datos = ser.read(1024).split("\n")[0].split(",")
    m.insertar(float(datos[0]),float(datos[1]),float(datos[2]),float(datos[3]),float(datos[4]))
    close()
