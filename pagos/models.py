# -*- coding: utf-8 -*-
from django.db import models

from reservas.models import Reserva

# Create your models here.

class Pago(models.Model):
    fechaTransaccion = models.DateTimeField()
    cedulaTipo       = models.CharField(max_length = 1)
    cedula           = models.CharField(max_length = 10)
    tarjetaTipo      = models.CharField(max_length = 6)
    reserva          = models.ForeignKey(Reserva)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)

    def __str__(self):
        return str(self.id)+" "+str(self.reserva.estacionamiento.nombre)+" "+str(self.cedulaTipo)+"-"+str(self.cedula)