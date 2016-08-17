from django.shortcuts import render
from django.http import HttpResponse
from PWSServer.models import Celda,Medida
from rest_framework.decorators import api_view
from django.core import serializers
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_all(request,id_planta,tipo):
    return HttpResponse(serializers.serialize("json", Medida.objects.all().filter(planta=Celda.objects.get(pk=id_planta))))

@api_view(['GET', 'POST'])
def current(request,id_celda):
    if request.method == 'GET':
        medida = Medida.objects.latest('pk')
        return HttpResponse(serializers.serialize("json",medida))

    if request.method == 'POST':
        data = request.body
        data=eval(data.strip().decode("UTF-8"))
        p = Celda.objects.get(pk=id_celda)
        m = Medida(temperatura=data['temp'], humedad_relativa=data['hrel'], humedad_tierra=data['htie'], luz=data['luz'], distancia=data['ultr'],celda=p)
        m.save()
        return HttpResponse("OOOK")
