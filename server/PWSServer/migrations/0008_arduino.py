# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PWSServer', '0007_auto_20160817_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arduino',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('identificador', models.IntegerField()),
                ('celda', models.ForeignKey(to='PWSServer.Celda', default=None)),
            ],
        ),
    ]
