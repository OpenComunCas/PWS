#*-* coding:UTF-8*-*

"""
    Este trasto actúa como servidor de pruebas, reenvía los datos al thingspeak y poco más.
"""

import serial
import requests
import time
import sys
import json

"""
JUE == Cafrada
"""

port = sys.argv[1]

ser = serial.Serial("/dev/tty"+port, 9600)

with open("server_cfg.json", "r") as f:
    cfg = json.load(f)
    MEASURES_WRITE_KEY = cfg['MEASURES_KEY']['WRITE']
    MEASURES_READ_KEY = cfg['MEASURES_KEY']['READ']

    ACTIONS_WRITE_KEY = cfg['ACTIONS_KEY']['WRITE']
    ACTIONS_READ_KEY = cfg['ACTIONS_KEY']['READ']

def update_measures(data):
    r = requests.get("https://api.thingspeak.com/update?api_key="+MEASURES_WRITE_KEY+"&field1="+data["soil"]+"&field2="+data["light"]+"&field3="+data["temp"]+"&field4="+data["timestamp"]) #JUE
    print(r.text)

def update_actions(action):
    timestamp = str(int(time.time()))
    r = requests.get("https://api.thingspeak.com/update?api_key="+ACTIONS_WRITE_KEY+"&field1="+action+"&field2="+timestamp)  # JUE
    print(r.text)


while True:
    cmd = ser.readline().decode()
    if cmd == "!action>\r\n": #JUE
        update_actions(ser.readline().decode())
    if cmd == "!data>\r\n": #JUE
        data = {}
        recv = ser.readline().decode()
        for pair in recv[:-2].split(":"): #JUE
            k,v = pair.split("!")
            data[k] = v
            data['timestamp'] = str(int(time.time())) # JUE
            
        print(data)
        update_measures(data)

        
