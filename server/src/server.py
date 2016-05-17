from flask import Flask,jsonify
import db.medidas as m
import os
import serie.serie as sr
from datetime import datetime
app = Flask(__name__)

@app.route("/all")
def get_all():
    medidas=[]
    for medida in m.get_all():
        medidas.append({"time":medida[0],"temperatura":medida[1],"humedad relativa":medida[2],"humedad en tierra":medida[3],"luz":medida[4],"distancia":medida[5]})
    return jsonify({"medidas":medidas})

@app.route("/current/")
def get_current():
    medida = m.get_last()
    #medida = 12,12,12,12,12,12
    return jsonify({"time":str(medida[0]),"tmp":medida[1],"hr":medida[2],"ht":medida[3],"luz":medida[4],"distancia":medida[5]})


if __name__ == "__main__":
    if not os.path.isfile("./db/example.db"):
        m.medidas().init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

