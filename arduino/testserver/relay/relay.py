#*-* coding:UTF-8*-*

"""
    Este trasto actúa como relé, reenvía los datos de los sensores al servdiro de test.
"""

"""
 El tema que recibe los datos (ya sea serie o cualquier otra cosa)
    - Este se puede quedar dormido o algo leyendo de un fichero o algo así
 El tema que procesa esos datos y los envia al server
    - A este tema le puedo meter una cola o algo
"""


import serial
import requests
import time
import sys
import json
import queue
import threading
import random


#Esta clase se encarga de conseguir los datos
class Worker(threading.Thread):     
    def generate_rnd_msg(self):
        self.rnd_msg = {}
        msgs = ['!action>', '!data>']
        rnd = random.randint(0,1)
        self.rnd_msg['msg'] = msgs[rnd]
        if rnd == 0:
            self.rnd_msg['action'] = 'water'
        if rnd == 1:
            self.rnd_msg['data'] = 'soil!500:temp!24:light!800'

    def get_msg(self):
        if self.source == 'serial':
            msg = ser.readline().decode()[:-2]
        if self.source == 'mock':
            time.sleep(5)
            self.generate_rnd_msg()
            msg = self.rnd_msg['msg']
        return msg
        
    def get_action(self):
        if self.source == 'serial':
            action = ser.readline().decode()[:-2] 
        if self.source == 'mock':
            action = self.rnd_msg['action']
        return action
    
    def get_data(self):
        if self.source == 'serial':
            data = ser.readline().decode()[:-2] 
        if self.source == 'mock':
            data = self.rnd_msg['data']
        return data
        
    def run(self):
        #source indica que clase se usa para conseguir los datos (arduino via serie o mock)
        self.source = self._kwargs['source']
        
        if self.source == 'mock':
            self.rnd_msg = {}
        
        if self.source == 'serial':
            self.port = input("Serial port: ")
            self.ser = serial.Serial("/dev/tty"+port, 9600)
            
        while True:
            msg = self.get_msg()
            if msg == "!action>": 
                action = self.get_action()
                cmd = {'msg':'action', 'data': action}
                q.put(cmd)
            if msg == "!data>": 
                cmd = {'msg': 'data', 'data':{}}
                data = self.get_data()
                for pair in data.split(":"): 
                    k,v = pair.split("!")
                    cmd['data'][k] = v
                q.put(cmd)


#La parte que envía los datos al server por un lado
with open("relay_cfg.json", "r") as f:
    cfg = json.load(f)

baseurl = cfg['URL']
soil_endpoint = baseurl+'/insertar'
#action_endpoint = baseurl+'/action/'


def new_measure(data):
    r = requests.post(soil_endpoint, data=json.dumps({'data':data}))
    
    print(r.text)

#TODO 
def new_action(data):
    r = requests.post(action_endpoint, data=json.dumps(data))
    print(r.text)


#cola de trabajos
q = queue.Queue()

#lanzar worker thread
t = Worker(kwargs={'source': 'mock'})
t.start()
while True:
    cmd = q.get()
    print(cmd)
    if cmd['msg'] == "action": 
        #TODO
        #print(cmd['data'])
        #new_action(cmd['data'])
        pass

    if cmd['msg'] == "data": 
        #print(cmd['data'])
        new_measure(cmd['data'])

    q.task_done()
