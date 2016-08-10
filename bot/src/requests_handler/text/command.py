import requests

class ICommand(object):
    def can_handle(self,message):
        return message['text'].startswith(self.command)

    def handle_message(message):
        pass

class HelloCommand(ICommand):
    def __init__(self):
        self.command = "/hello"

    def handle_message(self,message):
        return "text","hello,World"

class CurrentDataCommand(ICommand):
    def __init__(self):
        self.command = "/datos"

    def handle_message(self,message):
        data = requests.get('http://localhost:5000/current').json()
        retval = 'time: ' + str(data['time']) + '\n' + \
                     'Temperatura: ' + str(data['tmp']) + '\n' + \
                     'Humedad Relativa: ' + str(data['hr']) + '\n' + \
                     'Humedad en Tierra: ' + str(data['ht']) + '\n' + \
                     'Luz: ' + str(data['luz']) + '\n' + \
                     'Distancia: ' + str(data['distancia']) + '\n'

        return "text",retval

class CurrentDataCommand(ICommand):
    def __init__(self):
        self.command = "/info"

    def handle_message(self,message):
        data = requests.get('http://localhost:5000/current/').json()
        retval = 'time: ' + str(data['time']) + '\n' + \
                     'Temperatura: ' + str(data['tmp']) + '\n' + \
                     'Humedad Relativa: ' + str(data['hr']) + '\n' + \
                     'Humedad en Tierra: ' + str(data['ht']) + '\n' + \
                     'Luz: ' + str(data['luz']) + '\n' + \
                     'Distancia: ' + str(data['distancia']) + '\n'

        return "text",retval





class CommandHandler():
    def __init__(self):
       self.commands = [HelloCommand(),CurrentDataCommand()]

    def handle_message(self,message):
        for command in self.commands:
            if command.can_handle(message):
                handler = command
                break
        return handler.handle_message(message)
