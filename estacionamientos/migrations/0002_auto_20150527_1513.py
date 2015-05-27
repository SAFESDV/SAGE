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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nombreUsuario', models.CharField(max_length=50)),
                ('apellidoUsuario', models.CharField(max_length=50)),
                ('cedulaTipo', models.CharField(max_length=1)),
                ('cedula', models.CharField(max_length=10)),
                ('PIN', models.CharField(max_length=4)),
                ('saldo', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('Cedula', models.CharField(max_length=50)),
                ('nomb_prop', models.CharField(max_length=50)),
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
            name='propietario',
        ),
        migrations.RemoveField(
            model_name='estacionamiento',
            name='telefono3',
        ),
        migrations.AddField(
            model_name='estacionamiento',
            name='CI_prop',
            field=models.CharField(max_length=50, default=2015),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='estacionamiento',
            name='email1',
            field=models.EmailField(null=True, blank=True, max_length=254),
        ),
    ]
