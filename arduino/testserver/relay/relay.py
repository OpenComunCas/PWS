#*-* coding:UTF-8*-*

"""
    Este trasto actúa como relé, reenvía los datos de los sensores al servdiro de test.
"""

import serial
import requests
import time
import sys
import json

port = sys.argv[1]
ser = serial.Serial("/dev/tty"+port, 9600)

with open("relay_cfg.json", "r") as f:
    cfg = json.load(f)

baseurl = cfg['URL']
soil_endpoint = baseurl+'/soil/'
action_endpoint = baseurl+'/action/'


def new_measure(data):
    r = requests.post(soil_endpoint, data=json.dumps(data))
    print(r.text)

def new_action(data):
    r = requests.post(action_endpoint, data=json.dumps(data))
    print(r.text)


while True:
    cmd = ser.readline().decode()
    if cmd == "!action>\r\n": 
        recv = ser.readline().decode()
        data = {'action':recv[:-2], 'timestamp': str(int(time.time()))}
        new_action(data)

    if cmd == "!data>\r\n": 
        data = {}
        recv = ser.readline().decode()
        for pair in recv[:-2].split(":"): 
            k,v = pair.split("!")
            data[k] = v
            data['timestamp'] = str(int(time.time())) 
            
        print(data)
        new_measure(data)
