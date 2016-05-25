from .command import CommandHandler 
from .plaintext import PlainTextHandler 
class TextHandler():
    def __init__(self):
        self.handlers = {}
        self.handlers["command"] = CommandHandler()
        self.handlers["plain"] = PlainTextHandler()
    
    def handle(self,message):
        if message["text"][0] == '/':
            return self.handlers["command"].handle_message(message)
        else:
            return self.handlers["plain"].handle_message(message)
