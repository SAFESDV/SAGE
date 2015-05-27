# -*- coding: utf-8 -*-
# Archivo con funciones de control para SAGE
from billetera.models import BilleteraElectronica
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict

def consultar_saldo(id, pin):
    
    duenioBilletera = BilleteraElectronica.objects.filter(saldo, id = id, PIN = pin)
    
    if (duenioBilletera != None):
        return duenioBilletera.saldo
    
    else:
        return -1