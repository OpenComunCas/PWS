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

    def last(self):
        self.cursor.execute('SELECT * FROM datos where time = (select max(time) from datos)')
        tmp = self.cursor.fetchall()[0]
        return Medida(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5])

#
#
#
#
class Medida():
    def __init__(self,timestamp,temp,hrel,htie,luz,ultr):
        self.timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        self.temp = float(temp)
        self.hrel = float(hrel)
        self.htie = float(htie)
        self.luz  = float(luz)
        self.ultr = float(ultr)
        self.dict = {}
        self.dict["time"] = self.timestamp
        self.dict["temperatura"] = self.temp
        self.dict["humedad_relativa"] = self.hrel
        self.dict["humedad_tierra"] = self.htie
        self.dict["luz"] = self.luz
        self.dict["ultrasonido"] = self.ultr

    def __getitem__(self,key):
        return self.dict[key]
