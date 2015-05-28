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
    #BE = BilleteraElectronica.objects.get(id = id_billetera)
    if monto>Decimal("0.1"):
        BE.saldo = BE.saldo + Decimal(monto)
        BE.save()