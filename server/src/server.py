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

@app.route("/current")
def get_current():
    medida = m.medidas().last()
    return jsonify({"time":str(medida["time"]),"tmp":medida["temperatura"],"hr":medida["humedad_relativa"],"ht":medida["humedad_tierra"],"luz":medida["luz"],"distancia":medida["ultrasonido"]})

@app.route("/current/<meassure>")
def get_meassure(meassure):
    try:
        return jsonify({meassure:m.medidas().last()[meassure]})
    except KeyError:
        return "error"
    


if __name__ == "__main__":
    if not os.path.isfile("./db/example.db"):
        m.medidas().init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

