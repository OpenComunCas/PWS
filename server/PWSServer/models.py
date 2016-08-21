from django.db import models

TIPO_UMBRAL = (
    ('MAX', 'Maximo'),
    ('MIN', 'Minimo'),
    ('MED', 'Media')
)
TIPO_MEDIDA = (
    ('T', 'temperatura'),
    ('R', 'humedad_relativa'),
    ('H', 'humedad_tierra'),
    ('L', 'luz'),
    ('D', 'distancia')
)

class Especie(models.Model):
    name = models.CharField(max_length=50)

class Parametros(models.Model):
    tipo = models.CharField(max_length=1, choices=TIPO_MEDIDA)
    tipo_umbral = models.CharField(max_length=3, choices=TIPO_UMBRAL)
    valor = models.FloatField(null=True, blank=True, default=0.0)
    especie=models.ForeignKey(Especie,on_delete=models.CASCADE)

class Celda(models.Model):
    name = models.CharField(max_length=50)
    especie = models.ForeignKey(Especie,default=None)

class Arduino(models.Model):
    celda = models.ForeignKey(Celda,default=None)
    identificador = models.CharField(max_length=50)


class Alarma(models.Model):
    tipo = models.CharField(max_length=1, choices=TIPO_MEDIDA)
    tipo_umbral = models.CharField(max_length=3, choices=TIPO_UMBRAL)
    valor = models.FloatField(null=True, blank=True, default=0.0)

class AlarmaCelda(models.Model):
    alarma=models.ForeignKey(Alarma,on_delete=models.CASCADE)
    celda=models.ForeignKey(Celda,on_delete=models.CASCADE)

class AlarmaTemporal(models.Model):
    alarma=models.ForeignKey(Alarma,on_delete=models.CASCADE)
    tiempo_minutos = models.FloatField(null=True, blank=True, default=0.0)

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)

class Suscribe(models.Model):
    """
    relacion - usuario  AlarmaCelda
    para suscribir el usuario a las alarmas de una celda
    """
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    alarma = models.ForeignKey(AlarmaCelda,on_delete=models.CASCADE)

class Medida(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField(null=True, blank=True, default=None)
    humedad_tierra = models.FloatField(null=True, blank=True, default=None)
    humedad_relativa = models.FloatField(null=True, blank=True, default=None)
    luz = models.FloatField(null=True, blank=True, default=None)
    distancia = models.FloatField(null=True, blank=True, default=None)
    celda = models.ForeignKey(Celda, on_delete=models.CASCADE)
