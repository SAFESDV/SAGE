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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombreUsuario', models.CharField(max_length=50)),
                ('apellidoUsuario', models.CharField(max_length=50)),
                ('cedulaTipo', models.CharField(max_length=1)),
                ('cedula', models.CharField(max_length=10)),
                ('PIN', models.CharField(max_length=4)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('nomb_prop', models.CharField(max_length=50, serialize=False, help_text='Nombre Propio', primary_key=True)),
                ('telefono3', models.CharField(max_length=30, blank=True, null=True)),
                ('email2', models.EmailField(max_length=254, blank=True, null=True)),
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
            name='email1',
            field=models.EmailField(max_length=254, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='propietario',
            field=models.ForeignKey(to='estacionamientos.Propietario'),
        ),
    ]
