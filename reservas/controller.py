# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from estacionamientos.models import Estacionamiento
from reservas.models import Reserva
from transacciones.models import *

def validarHorarioReserva(inicioReserva, finReserva, apertura, cierre):
    if inicioReserva >= finReserva:
        return (False, 'El horario de inicio de reservacion debe ser menor al horario de fin de la reserva.')
    if finReserva - inicioReserva < timedelta(hours=1):
        return (False, 'El tiempo de reserva debe ser al menos de 1 hora.')
    if inicioReserva.date() < datetime.now().date():
        return (False, 'La reserva no puede tener lugar en el pasado.')
    if finReserva.date() > (datetime.now()+timedelta(days=6)).date():
        return (False, 'La reserva debe estar dentro de los próximos 7 días.')
    if apertura.hour==0 and apertura.minute==0 \
        and cierre.hour==23 and cierre.minute==59:
        seven_days=timedelta(days=7)
        if finReserva-inicioReserva<=seven_days :
            return (True,'')
        else:
            return(False,'Se puede reservar un puesto por un maximo de 7 dias.')
    else:
        hora_inicio = time(hour = inicioReserva.hour, minute = inicioReserva.minute)
        hora_final  = time(hour = finReserva.hour   , minute = finReserva.minute)
        if hora_inicio<apertura:
            return (False, 'El horario de inicio de reserva debe estar en un horario válido.')
        if hora_final > cierre:
            return (False, 'El horario de fin de la reserva debe estar en un horario válido.')
        if inicioReserva.date()!=finReserva.date():
            return (False, 'No puede haber reservas entre dos dias distintos')
        return (True,'')
    
def marzullo(idEstacionamiento, hIn, hOut, tipo):
    e = Estacionamiento.objects.get(id = idEstacionamiento)
    ocupacion = []
    
    capacidadLivianos = e.capacidadLivianos
    capacidadPesados = e.capacidadPesados
    capacidadMotos = e.capacidadMotos

    for reserva in e.reserva_set.filter(estado = 'Válido', tipo_vehiculo = tipo):
        ocupacion += [(reserva.inicioReserva, 1), (reserva.finalReserva, -1)]
    ocupacion += [(hIn, 1), (hOut, -1)]

    if (tipo == 'Liviano'):
        
        count = 0
        for r in sorted(ocupacion):
            count += r[1]
            
            if count > capacidadLivianos:
                return False
        return True
    
    elif (tipo == 'Pesado'):
        
        count = 0
        for r in sorted(ocupacion):
            count += r[1]
            if count > capacidadPesados:
                return False
        return True
    
    elif (tipo == 'Moto'):
        
        count = 0
        for r in sorted(ocupacion):
            count += r[1]
            if count > capacidadMotos:
                return False
        return True
    
    else:
        return False
    
def cancelar_reserva(idReserva):
    
    try:
        reser = Reserva.objects.get(id = idReserva)
    except:
        raise
    
    reser.estado = 'Inválido'
    reser.save()
    relacion = TransReser.objects.get(reserva = reser)
    trans = relacion.transaccion
    trans.estado = 'Inválido'
    
def reservas_activas(idEstacionamiento):
    reservasAct = Reserva.objects.filter(estado = 'Válido')
    return reservaAct

def reservas_inactivas(idEstacionamiento):
    reservasIna = Reserva.objects.filter(estado = 'Inválido')
    return reservaIna

def get_transacciones(idReserva):
    transacciones = []
    
    relacion = TransReser.objects.filter(reserva__id = idReserva)
    
    for r in relacion:
        transacciones += [r.transaccion]
    
    return transacciones
    
    
    
    
    
    
    
    
    