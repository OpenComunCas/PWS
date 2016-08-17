from django.db import models

# Create your models here.
# especie, alarmas, usuarios,
# celda tiene alarmas y usuario se suscribe a alarmas.
# Especie tiene parametros.
# Celda tiene parametros.
# Celda tiene especie

TIPO_UMBRAL = (
    ('MAX', 'Maximo'),
    ('MIN', 'Minimo')
)
TIPO_MEDIDA = (
    ('T', 'temperatura'),
    ('R', 'humedad_relativa'),
    ('H', 'humedad_tierra'),
    ('L', 'luz'),
    ('D', 'distancia')
)

class Alarma(models.Model):
    tipo = models.CharField(max_length=1, choices=TIPO_MEDIDA)
    tipo_umbral = models.CharField(max_length=3, choices=TIPO_UMBRAL)
    valor = models.FloatField(null=True, blank=True, default=0.0)

class AlarmaTemporal(models.Model):
    alarma=models.ForeignKey(Alarma,on_delete=models.CASCADE)
    tiempo_minutos = models.FloatField(null=True, blank=True, default=0.0)

class Especie(models.Model):
    name = models.CharField(max_length=50)

class Celda(models.Model):
    name = models.CharField(max_length=50)
    especie = models.ForeignKey(Especie,default=None)

class Medida(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField(null=True, blank=True, default=None)
    humedad_tierra = models.FloatField(null=True, blank=True, default=None)
    humedad_relativa = models.FloatField(null=True, blank=True, default=None)
    luz = models.FloatField(null=True, blank=True, default=None)
    distancia = models.FloatField(null=True, blank=True, default=None)
    celda = models.ForeignKey(Celda, on_delete=models.CASCADE)
