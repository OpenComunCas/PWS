import telepot
from .text.handler import TextHandler

class HandlerError(Exception):
    pass

class IHandler():
    def __init__(self):
        pass
    
    def handle_message(self,message):
        pass
    
class Dispacher():
    def __init__(self):
        self.handlers = {}
        self.handlers["text"] = TextHandler().handle
    
    def handle_menssage(self,content_type,message):
        handler = self.handlers[content_type.lower()]
        content_type,response = handler(message)
        return content_type,response
