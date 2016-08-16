from django.db import models

# Create your models here.

class Planta(models.Model):
    name = models.CharField(max_length=50)

class Medida(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField(null=True, blank=True, default=None)
    humedad_tierra = models.FloatField(null=True, blank=True, default=None)
    humedad_relativa = models.FloatField(null=True, blank=True, default=None)
    luz = models.FloatField(null=True, blank=True, default=None)
    distancia = models.FloatField(null=True, blank=True, default=None)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
