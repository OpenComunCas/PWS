from django.core.management.base import BaseCommand, CommandError
from PWSServer.models import Celda,Medida,Especie
muestras = [{'hrel': 41.51063547370273, 'htie': 289, 'ultr': 636, 'temp': 664, 'luz': 292},
{'hrel': 98.38939149826437, 'htie': 971, 'ultr': 600, 'temp': 414, 'luz': 562},
{'hrel': 79.53589873581556, 'htie': 68, 'ultr': 484, 'temp': 51, 'luz': 912},
{'hrel': 25.787728517046805, 'htie': 953, 'ultr': 483, 'temp': 274, 'luz': 529},
{'hrel': 68.79611444876815, 'htie': 636, 'ultr': 668, 'temp': 549, 'luz': 47},
{'hrel': 93.8230106452252, 'htie': 575, 'ultr': 271, 'temp': 941, 'luz': 982}]

class Command(BaseCommand):
    args ='<id_celda>'
    help = 'populate database with random values'

    def add_arguments(self, parser):
        parser.add_argument('id_celda', nargs='+', type=int)

    def handle(self, *args, **options):
        for id_celda in options['id_celda']:
            especie = Especie(name="abc")
            especie.save()
            celda = Celda(pk=1,name=" celda prueba",especie=especie)
            celda.save()
            celda = Celda.objects.get(pk=celda.pk)
            for data in muestras: 
                m = Medida(temperatura=data['temp'], humedad_relativa=data['hrel'], humedad_tierra=data['htie'], luz=data['luz'], distancia=data['ultr'],celda=celda)
                m.save()
            self.stdout.write(self.style.SUCCESS('Successfully saved celda "%s"' % id_celda))
