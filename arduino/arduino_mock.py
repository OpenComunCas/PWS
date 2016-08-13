# -*- coding:utf-8 -*-

"""
Clase que simula la ejecución de un sensor Arduino
"""

import requests
import sys
import signal
import time
import random
import json

"""
Configuración de umbrales para generar los valores de prueba
"""
TEMPMIN = 0
TEMPMAX = 1023

HRELMIN = 0.0
HRELMAX = 100.0

HTIEMIN = 0
HTIEMAX = 1023
 
LUZMIN = 0
LUZMAX = 1023

ULTRMIN = 0
ULTRMAX = 1023



def signal_handler(signal, frame):
    """ Manejo del CTRL+C """
    print('CTRL+C ! Cerrando...')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)


    url = 'http://localhost:5000/current'


    while(True):
        randtemp = random.randint(TEMPMIN, TEMPMAX)
        randhrel = random.uniform(HRELMIN, HRELMAX)
        randhtie = random.randint(HTIEMIN, HTIEMAX)
        randluz = random.randint(LUZMIN, LUZMAX)
        randultr = random.randint(ULTRMIN, ULTRMAX)
        
        data = {'temp': randtemp, 'hrel': randhrel, 'htie': randhtie, 'luz': randluz, 'ultr': randultr}

        print('sending mock POST request')
        print('data: {}'.format(data))

        r = requests.post(url, json = data)
        r.text
        
        time.sleep(8)




















