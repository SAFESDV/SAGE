# -*- coding: utf-8 -*-
# Archivo con funciones de control para SAGE
from billetera.models import BilleteraElectronica
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist

def consultar_saldo(ID_Billetera, pin):
    
    try:
        BE = BilleteraElectronica.objects.get(id = ID_Billetera, PIN = pin)
    
    except ObjectDoesNotExist:
        return -1
        
    return BE.saldo
    
def recargar_saldo(ID_Billetera, monto):
    
    BE = BilleteraElectronica.objects.get(id = ID_Billetera)
    monto2 = Decimal(monto).quantize(Decimal("1.00"))
    minMonto = Decimal(0.01).quantize(Decimal("1.00"))
    maxMonto = Decimal(10000.00).quantize(Decimal("1.00"))
    
    if (monto2 >= minMonto and (monto2 + BE.saldo <= maxMonto)):
        BE.saldo += Decimal(monto).quantize(Decimal("1.00"))
        BE.save()
        
def consumir_saldo(ID_Billetera, monto):
    
    BE = BilleteraElectronica.objects.get(id = ID_Billetera)
    monto2 = Decimal(monto).quantize(Decimal("1.00"))
    minMonto = Decimal(0.01).quantize(Decimal("1.00"))
    maxMonto = Decimal(10000.00).quantize(Decimal("1.00"))
    
    if (BE.saldo - monto2 >= Decimal(0).quantize(Decimal("1.00")) and monto2 >= 0):
        BE.saldo -= Decimal(monto).quantize(Decimal("1.00"))
        BE.save()
        
    
    
    