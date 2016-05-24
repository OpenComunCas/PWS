class RHandler():
    def __init__(self):
        pass
    
    def handle_menssage(self,content_type,message):
        handler = "handler_"+content_type.lower()
        response = self.handler(message)
        return chat_id,
