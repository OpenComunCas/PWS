#-*- coding:utf-8 -*-

import tornado.web
import csv

class SoilHandler(tornado.web.RequestHandler):
    #Enabling CORS requests
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-ALlow-Methods", 'GET, OPTIONS')
    
    
    def get(self, action):
        with open('data/soil.csv', 'r') as f:
            data = f.readlines()
        
        self.set_status(200)
        self.write({'result':'ok', 'code':200, 'data':data})
        
    def post(self, action):
        try:
            data = tornado.escape.json_decode(self.request.body)
        
            with open('data/soil.csv', 'a') as f:
                csvwriter = csv.writer(f, delimiter=',')
                csvwriter.writerow([data['soil'], data['temp'], data['light'], data['timestamp']])
            self.set_status(201)
            self.write({'result':'ok', 'code':201})
        except json.decoder.JSONDecodeError:
            self.write_error(status_code=400, msg='JSON Decode Error')
        except KeyError:
            self.write_error(status_code=400, msg='JSON Key Error')
            
    def write_error(self, status_code, **kwargs):
        if status_code in [400]:
            retval = {'result':'error', 'code': status_code, 'message':kwargs['msg']}
        else:
            retval = {'result':'error', 'code': status_code, 'message': 'unknown error'}
            
        self.set_status(status_code)
        self.write(json.dumps(retval))
