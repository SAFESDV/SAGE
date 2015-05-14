# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BilleteraElectronica',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombreUsuario', models.CharField(max_length=50)),
                ('apellidoUsuario', models.CharField(max_length=50)),
                ('cedulaTipo', models.CharField(max_length=1)),
                ('cedula', models.CharField(max_length=10)),
                ('PIN', models.CharField(max_length=4)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='email1',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='email2',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
