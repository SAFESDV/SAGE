# -*- coding: utf-8 -*-
from django.db import models
from math import ceil, floor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from datetime import timedelta

class BilleteraElectronica(models.Model):
    nombreUsuario    = models.CharField(max_length = 50)
    apellidoUsuario  = models.CharField(max_length = 50)
    cedulaTipo       = models.CharField(max_length = 1)
    cedula           = models.CharField(max_length = 10)
    PIN              = models.CharField(max_length = 4)
    saldo            = models.DecimalField(max_digits = 7, decimal_places = 2)
    
    def __str__(self):
        return str(self.id)+" "+ str(self.cedula)
    
class PagoRecargaBilletera(models.Model):
    fechaTransaccion = models.DateTimeField()
    cedulaTipo       = models.CharField(max_length = 1)
    cedula           = models.CharField(max_length = 10)
    ID_Billetera     = models.CharField(max_length = 4)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)
    tarjetaTipo      = models.CharField(max_length = 6)

    def __str__(self):
        return str(self.id)+" "+str(self.ID_Billetera)+" "+str(self.cedulaTipo)+"-"+str(self.cedula)+"-"+str(self.monto)