import telepot
import time

BOT_TOKEN = '189752430:AAF45NDGJboBXNzqGozBetr0YLrEWE1avsU'
bot = telepot.Bot(BOT_TOKEN)

def handle():
    content_type, chat_type, chat_id = telepot.glance(message)

    if content_type == 'text' and message['text'] == '/datos':
        actualUser = message['from']['username']
        actualId = message['from']['id']
        #self.users.append({actualId: actualUser})
            
        data = requests.get('http://localhost:5000/current/').json()
        retval = 'time: ' + str(data['time']) + '\n' + \
                     'Temperatura: ' + str(data['tmp']) + '\n' + \
                     'Humedad Relativa: ' + str(data['hr']) + '\n' + \
                     'Humedad en Tierra: ' + str(data['ht']) + '\n' + \
                     'Luz: ' + str(data['luz']) + '\n' + \
                     'Distancia: ' + str(data['distancia']) + '\n'

        bot.sendMessage(actualId, retval)
        return actualId,retval

def main():
    bot.message_loop(handle)
    while 1:
        time.sleep(10)

if __name__ == '__main__':
    main()


