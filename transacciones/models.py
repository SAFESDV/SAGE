# -*- coding: utf-8 -*-
from django.db import models

from reservas.models import Reserva
from django.db.models.fields.related import ForeignKey
from billetera.models import *

# Create your models here.

class Transaccion(models.Model):
    fecha            = models.DateTimeField()
    tipo             = models.CharField(max_length = 10)
    estado           = models.CharField(max_length = 25)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)

    def __str__(self):
        return str(self.id)
    
class TransBilletera(models.Model):
    billetera        = models.ForeignKey(BilleteraElectronica)
    transaccion      = models.ForeignKey(Transaccion)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)

    def __str__(self):
        return str(self.id)
    
class TransTDC(models.Model):
    nombre           = models.CharField(max_length = 50)
    cedulaTipo       = models.CharField(max_length = 1)
    cedula           = models.CharField(max_length = 10)
    tarjetaTipo      = models.CharField(max_length = 6)
    tarjeta          = models.CharField(max_length = 4)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)
    transaccion      = models.ForeignKey(Transaccion)

    def __str__(self):
        return str(self.id)
    
class Historia(models.Model):
    transaccion      = ForeignKey(Transaccion)
    fecha            = models.DateTimeField()
    tipo             = models.CharField(max_length = 10)
    nombre           = models.CharField(max_length = 50)
    cedulaTipo       = models.CharField(max_length = 1)
    cedula           = models.CharField(max_length = 10)
    modoPago         = models.CharField(max_length = 2)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)
    estado           = models.CharField(max_length = 25)

    def __str__(self):
        return str(self.id)
    
class TransReser(models.Model):
    transaccion      = models.ForeignKey(Transaccion)
    reserva          = models.ForeignKey(Reserva)

    def __str__(self):
        return str(self.id)