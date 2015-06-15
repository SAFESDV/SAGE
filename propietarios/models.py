# -*- coding: utf-8 -*-
from django.db import models
from math import ceil, floor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from datetime import timedelta

class Propietario(models.Model):
    
    cedulaTipo       = models.CharField(max_length = 1)
    Cedula      = models.CharField(max_length = 50)
    nomb_prop   = models.CharField(max_length = 50)
    telefono3   = models.CharField(blank = True, null = True, max_length = 30)
    email2      = models.EmailField(blank = True, null = True)
    
    def __str__(self):
        return self.nomb_prop
    
class Persona(models.Model):
    
    cedulaTipo  = models.CharField(max_length = 1)
    cedula      = models.CharField(max_length = 50)
    nombre      = models.CharField(max_length = 50)
    apellido    = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.nomb_prop