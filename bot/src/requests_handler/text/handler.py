from .command import CommandHandler 

class TextHandler():
    def __init__(self):
        self.handlers = {}
        self.handlers["command"] = CommandHandler()
    
    def handle(self,message):
        if message["text"][0] == '/':
            return self.handlers["command"].handle_message(message)
        else:
            return "text","ok"
