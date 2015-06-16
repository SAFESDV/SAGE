# -*- coding: utf-8 -*-
# Archivo con funciones de control para SAGE
from billetera.models import BilleteraElectronica
from transacciones.models import *
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from transacciones.models import *
from billetera.exceptions import *

def autenticar(_id, _pin):
    try:
        BE = BilleteraElectronica.objects.get(id = _id, PIN = _pin)
    except:
        return False
    return True

def verificarPin(pin1,pin2):
    if pin1!=pin2:
        return False
    else:
        return True
    
def modificarPin(Id,pin1):
    BE = BilleteraElectronica.objects.get(id = Id)
    BE.PIN = pin1
    BE.save()

def consultar_saldo(ID_Billetera):
    
    try:
        saldo = Decimal(0.00).quantize(Decimal("1.00"))
        BE = BilleteraElectronica.objects.get(id = ID_Billetera)
        TBE = TransBilletera.objects.filter(billetera = BE)
        
        for t in TBE:
            if t.transaccion.tipo == 'Recarga':
                saldo += Decimal(t.monto).quantize(Decimal("1.00"))
            elif t.transaccion.tipo == 'Reserva':
                saldo -= Decimal(t.monto).quantize(Decimal("1.00"))
        return saldo
    except ObjectDoesNotExist:
        pass

def recargar_saldo(_id, monto):
    
    BE = BilleteraElectronica.objects.get(id = _id)
    
    if monto < Decimal(0.00).quantize(Decimal("1.00")):
        raise MontoNegativo
    
    elif monto == Decimal(0.00).quantize(Decimal("1.00")):
        raise MontoCero
    
    if Decimal(monto).quantize(Decimal("1.00")) + consultar_saldo(BE.id) <= Decimal(10000.00):
    
        trans = Transaccion(
            fecha  = datetime.now(),
            tipo   = 'Recarga',
            estado = 'Válido',
            monto  = monto
        )
        
        trans.save()
        
        transBill = TransBilletera(
            billetera   = BE,
            transaccion = trans,
            monto       = monto
        )
        transBill.save()
        
        return trans.id
    
    raise SaldoExcedido
        
def recargar_saldo_TDC(_id, form):
    
    BE = BilleteraElectronica.objects.get(id = _id)
    
    if form.cleaned_data['monto'] < Decimal(0.00).quantize(Decimal("1.00")):
        raise MontoNegativo
    
    elif form.cleaned_data['monto'] == Decimal(0.00).quantize(Decimal("1.00")):
        raise MontoCero
            
    if form.cleaned_data['monto'] + consultar_saldo(BE.id) <= Decimal(10000.00):
    
        trans = Transaccion(
            fecha  = datetime.now(),
            tipo   = 'Recarga',
            estado = 'Válido',
            monto  = form.cleaned_data['monto'],
        )
        
        trans.save()
        
        transTdc = TransTDC(
            nombre           = form.cleaned_data['nombre'],
            cedulaTipo       = form.cleaned_data['cedulaTipo'],
            cedula           = form.cleaned_data['cedula'],
            tarjetaTipo      = form.cleaned_data['tarjetaTipo'],
            tarjeta          = form.cleaned_data['tarjeta'][-4:],
            monto            = form.cleaned_data['monto'],
            transaccion      = trans
        )
        
        transBill = TransBilletera(
            billetera   = BE,
            transaccion = trans,
            monto       = form.cleaned_data['monto']
        )
    
        transBill.save()
        transTdc.save()
        
        return transTdc.id
    raise SaldoExcedido

def consumir_saldo(_id, monto):
    
    try:
        BE = BilleteraElectronica.objects.get(id = _id)
    except:
        raise AutenticacionDenegada
    
    if monto < Decimal(0.00).quantize(Decimal("1.00")):
        raise MontoNegativo
    
    elif monto == Decimal(0.00).quantize(Decimal("1.00")):
        raise MontoCero
            
    if consultar_saldo(BE.id) - Decimal(monto).quantize(Decimal("1.00")) >= Decimal(0.00):
    
        trans = Transaccion(
            fecha  = datetime.now(),
            tipo   = 'Reserva',
            estado = 'Válido',
            monto  = monto
        )
        
        trans.save()
        
        transBill = TransBilletera(
            billetera   = BE,
            transaccion = trans,
            monto       = monto
        )
    
        transBill.save()
        
        return trans.id;
    raise SaldoNegativo
        
# def consumir_saldo(ID_Billetera, monto):
#     
#     try:
#         BE = BilleteraElectronica.objects.get(id = ID_Billetera)
#         monto2 = Decimal(monto).quantize(Decimal("1.00"))
#         minMonto = Decimal(0.01).quantize(Decimal("1.00"))
#         maxMonto = Decimal(10000.00).quantize(Decimal("1.00"))
#         
#         if (BE.saldo - monto2 >= Decimal(0).quantize(Decimal("1.00")) and monto2 >= 0):
#             BE.saldo -= Decimal(monto).quantize(Decimal("1.00"))
#             BE.save()
#             
#     except ObjectDoesNotExist:
#         pass
#     
    