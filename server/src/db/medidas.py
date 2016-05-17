import sqlite3
import datetime 
def insertar(temp,hrel,htie,luz,ultr):
    bd = medidas() 
    bd.insert(temp,hrel,htie,luz,ultr)
    bd.close()

def get_all():
    bd = medidas()
    data = bd.get_all()
    bd.close()
    return data

def get_last():
   medidas = get_all()
   return medidas[len(medidas)-1]

class medidas():
    def __init__(self):
        self.conn = sqlite3.connect('db/example.db')
        self.cursor = self.conn.cursor()
    
    def insert(self,temp,hrel,htie,luz,ultr):
        timestamp = datetime.datetime.now()
        self.cursor.execute('INSERT INTO datos VALUES (?,?,?,?,?,?)',(timestamp,temp,hrel,htie,luz,ultr))
        self.conn.commit()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE datos (time timestamp,temp real, humedadrel real, humedadtier real, luz real, ultrasonido real)''')
   
    def get_all(self):
        self.cursor.execute('SELECT * FROM datos')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
