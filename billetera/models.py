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
    
    def __str__(self):
        return str(self.id)+" "+ str(self.cedula)