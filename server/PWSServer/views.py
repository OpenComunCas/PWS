from django.shortcuts import render
from django.http import HttpResponse
from PWSServer.models import Planta,Medida
from rest_framework.decorators import api_view
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_all(request,id_planta):
    return HttpResponse(Medida.objects.all())
    #medidas.append({"time":medida[0],"temperatura":medida[1],"humedad relativa":medida[2],"humedad en tierra":medida[3],"luz":medida[4],"distancia":medida[5]})

@api_view(['GET', 'POST'])
def current(request):
    if request.method == 'GET':
        medida = Medida.objects.latest('id')
        return HttpResponse(jsonify(medida))
        pass
    if request.method == 'POST':
        data = request.get_json()
        m = Medida(temperatura=data['temp'], humedad_relativa=data['hrel'], humedad_tierra=data['htie'], luz=data['luz'], distancia=data['ultr'])
        m.save()
        return HttpResponse("OOOK")

