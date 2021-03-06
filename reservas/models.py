# -*- coding: utf-8 -*-
from django.db import models
from django.db import models
from math import ceil, floor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from datetime import timedelta

from estacionamientos.models import Estacionamiento

# Create your models here.

class Reserva(models.Model):
    cedulaTipo      = models.CharField(max_length = 1)
    cedula          = models.CharField(max_length = 10)
    nombre          = models.CharField(max_length = 64)
    apellido        = models.CharField(max_length = 64)
    estacionamiento = models.ForeignKey(Estacionamiento)
    inicioReserva   = models.DateTimeField()
    finalReserva    = models.DateTimeField()
    estado          = models.CharField(max_length = 25)
    tipo_vehiculo   = models.CharField(max_length = 7)

    def __str__(self):
        return str(self.id) +  ' ' +  self.cedula +  ' ' +self.estacionamiento.nombre+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+ ' ' + self.estado + ')'
