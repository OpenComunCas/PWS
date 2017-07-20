# -*- coding: utf-8 -*-

import json
import os
import csv

import tornado.ioloop
import logging

import handlers.soilhandler as soilhandler
import handlers.actionhandler as actionhandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/soil(/*)', soilhandler.SoilHandler),
            ('/action(/*)', actionhandler.ActionHandler)
        ]
        settings = { 
            "static_path": os.path.join(".", "static"),
            "template_path": os.path.join(".","templates")
        }
        tornado.web.Application.__init__(self, handlers, **settings)        


def init_database():
    sampleDAO.Sample.createTable(ifNotExists=True)

if __name__ == '__main__':
    
    #init storage
    with open('data/soil.csv', 'w') as f:
        fieldnames = ['soil', 'temp', 'light', 'timestamp']
        csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
        csvwriter.writeheader()

    with open('data/action.csv', 'w') as f:
        fieldnames = ['action', 'timestamp']
        csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
        csvwriter.writeheader()


    #init server
    app = Application()
    port = 5050
    print('Running webapp on port {}'.format(port))
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()
