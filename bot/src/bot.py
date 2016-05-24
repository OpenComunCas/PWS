import telepot
import json
import time
from requests_handler.dispacher import Dispacher

class WeatherBot():
    def __init__(self):
        with open('data.json') as data_file:    
            data = json.load(data_file)
            self.bot = telepot.Bot(data["BOT_TOKEN"])
            self.handle_send = {}
            self.handle_send["text"] = self.send_text
            self.message_dispacher = Dispacher()
            self.bot.message_loop(self.handle_message)

    def handle_message(self,message):
        content_type, chat_type, chat_id = telepot.glance(message)
        print(message)
        content_type,response_content = self.message_dispacher.handle_menssage(content_type,message)
        handle_send = self.handle_send[content_type] 
        handle_send(chat_id,response_content)
        
    def send_text(self,chat_id,content):
        self.bot.sendMessage(chat_id, content)

    def send_photo(self,chat_id,content):
        self.bot.sendPhoto(chat_id, content)

    def send_audio(self,chat_id,content):
        self.bot.sendAudio(chat_id, content)

    def send_document(self,chat_id,content):
        self.bot.sendDocumment(chat_id, content)

bot = WeatherBot()

if __name__ == "__main__":
    while True:
        time.sleep(10)
