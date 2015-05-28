# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamientos', '0002_auto_20150514_0403'),
    ]

    operations = [
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('nomb_prop', models.CharField(help_text='Nombre Propio', primary_key=True, serialize=False, max_length=50)),
                ('telefono3', models.CharField(null=True, blank=True, max_length=30)),
                ('email2', models.EmailField(null=True, blank=True, max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='estacionamiento',
            name='email2',
        ),
        migrations.RemoveField(
            model_name='estacionamiento',
            name='telefono3',
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='propietario',
            field=models.ForeignKey(to='estacionamientos.Propietario'),
        ),
    ]
