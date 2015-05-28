# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamientos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estacionamiento',
            name='propietario',
        ),
        migrations.AddField(
            model_name='estacionamiento',
            name='CI_prop',
            field=models.CharField(max_length=50, default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propietario',
            name='Cedula',
            field=models.CharField(max_length=50, default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propietario',
            name='id',
            field=models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False, default=123),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='propietario',
            name='nomb_prop',
            field=models.CharField(max_length=50),
        ),
    ]
