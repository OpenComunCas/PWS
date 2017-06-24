#*-* coding:UTF-8*-*

"""
    Este trasto actúa como servidor de pruebas, reenvía los datos al thingspeak y poco más.
"""

import serial
import requests
import time

"""
JUE == Cafrada
"""

ser = serial.Serial("/dev/ttyACM0", 9600)

with open("server_cfg.json", "r") as f:
    cfg = json.load(f)
    READ_API_KEY = cfg['API_KEY']['WRITE']
    WRITE_API_KEY = cfg['API_KEY']['READ']

def update_thingspeak(data):
    r = requests.get("https://api.thingspeak.com/update?api_key="+WRITE_API_KEY+"&field1="+data["soil"]+"&field2="+data["light"]+"&field3="+data["temp"]+"&field4="+data["timestamp"]) #JUE

    print(r.text)


while True:
    cmd = ser.readline().decode()
    if cmd == "!action>\r\n": #JUE
        print(ser.readline())
    if cmd == "!data>\r\n": #JUE
        data = {}
        recv = ser.readline().decode()
        for pair in recv[:-2].split(":"): #JUE
            k,v = pair.split("!")
            data[k] = v
            data['timestamp'] = str(int(time.time())) # JUE
            
        print(data)
        update_thingspeak(data)

        
