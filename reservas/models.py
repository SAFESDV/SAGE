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
    estacionamiento = models.ForeignKey(Estacionamiento)
    inicioReserva   = models.DateTimeField()
    finalReserva    = models.DateTimeField()
    estado          = models.CharField(max_length = 25)
    tipo_vehiculo   = models.CharField(max_length = 7)

    def __str__(self):
        return self.estacionamiento.nombre+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+')'