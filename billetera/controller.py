# -*- coding: utf-8 -*-
# Archivo con funciones de control para SAGE
from billetera.models import BilleteraElectronica
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict

def consultar_saldo(_id, pin):
    
    duenioBilletera = BilleteraElectronica.objects.get(id = _id, PIN = pin)
    
    if (duenioBilletera != None):
        return duenioBilletera.saldo
    
    else:
        return -1
    
def recargar_saldo(ID_Billetera,monto):
    BE = BilleteraElectronica.objects.get(id = ID_Billetera)
    
    if Decimal(monto).quantize(Decimal("1.00"))>=Decimal(0.01).quantize(Decimal("1.00")):
        BE.saldo = BE.saldo + Decimal(monto).quantize(Decimal("1.00"))
        BE.save()