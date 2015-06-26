# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import urllib
from django.http import HttpResponse, Http404
from django.utils.dateparse import parse_datetime
from urllib.parse import urlencode
from matplotlib import pyplot
from decimal import Decimal
from collections import OrderedDict

from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from estacionamientos.models import *
from reservas.models import Reserva
from transacciones.models import *
from transacciones.controller import *
from billetera.controller import *

def validarHorarioReserva(inicioReserva, finReserva, apertura, cierre, horizonte):
    if inicioReserva >= finReserva:
        return (False, 'El horario de inicio de reservacion debe ser menor al horario de fin de la reserva.')
    if finReserva - inicioReserva < timedelta(hours=1):
        return (False, 'El tiempo de reserva debe ser al menos de 1 hora.')
    if inicioReserva.date() < datetime.now().date():
        return (False, 'La reserva no puede tener lugar en el pasado.')
    if finReserva.date() > (datetime.now().date() + timedelta(days=horizonte)):
        return (False, 'La reserva debe estar dentro de los próximos ' + str(horizonte) + ' día(s).')
    if apertura.hour==0 and apertura.minute==0 \
        and cierre.hour==23 and cierre.minute==59:
        seven_days=timedelta(days=7)
        if finReserva-inicioReserva<=seven_days :
            return (True,'')
        else:
            return(False,"Se puede reservar un puesto por un maximo de " +str(horizonte) + " dias")
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
    
def reserva_Cambiable(inicioReserva,finReserva,horizonte):
    
    tiempo_reserva    = 0
    tiempo_diferencia = 0
    fecha_maxima      = datetime.now() + timedelta(days=horizonte)
    minuto            = timedelta(minutes=1)
    
    if inicioReserva >= finReserva:
        return (False)
    if finReserva - inicioReserva < timedelta(hours=1):
        return (False)
    if inicioReserva.date() < datetime.now().date():
        return (False)
    
    else:
    
        # Calculamos la diferencia entre el inicio de la reserva y el final
        
        fecha_Temp        = inicioReserva
        
        while fecha_Temp < finReserva:
            fecha_Temp += minuto
            tiempo_reserva += 1
            
        # Calculamos la diferencia entre el final de la reserva y la fecha maxima permitida
            
        fecha_Temp        = fecha_maxima   
            
        while fecha_Temp < finReserva:
            fecha_Temp += minuto
            tiempo_diferencia += 1
        
        if (tiempo_diferencia <= tiempo_reserva/2):
            return True
            
        else:
            return False


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
    
    elif (tipo == 'Discapacitados'):
        
        count = 0
        for r in sorted(ocupacion):
            count += r[1]
            if count > capacidadDiscapacitados:
                return False
        return True
    
    else:
        return False

def cancelar_reserva(idReserva,idbilletera):
    
    try:
        reser = Reserva.objects.get(id = idReserva,estado = "Válido")
        print("se puede cancelar!")
    except:
        print("Cai en except")
        raise
    
    reser.estado = 'Cancelado'
    print(reser)
    reser.save()
    relacion = TransReser.objects.get(reserva = reser)
    trans = relacion.transaccion
    trans.estado = 'Cancelado'
    trans.save()
    
    try:   
        recargar_saldo(idbilletera, relacion.transaccion.monto)
    except:
        return render(
                    request,
                    'reserva_confirmar_cancelar.html',
                    { "color"   : "red"
                     , 'mensaje' : 'No se puede hacer un reembolso a esta billetera porque excede el limite'
                     , 'billetera' : form
                     }
                      )
    
def reservas_activas(idEstacionamiento):
    reservasAct = Reserva.objects.filter(estado = 'Válido')
    return reservaAct

def reservas_inactivas(idEstacionamiento):
    reservasIna = Reserva.objects.filter(estado = 'Cancelado')
    return reservaIna

def get_transacciones(idReserva):
    
    reserva_selec = Reserva.objects.get(id = idReserva)
    relacion = TransReser.objects.get(reserva = reserva_selec)
    
    return relacion.transaccion

def calcular_Precio_Reserva(reserva,estacionamiento):
    montoReserva = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(reserva.inicioReserva,reserva.finalReserva,reserva.estacionamiento.id,reserva.tipo_vehiculo)
    return montoReserva

def calcular_Precio_Reserva2(reserva,diasFeriados):
    
    iniReserva = reserva.inicioReserva
    listaDiasReserva = []

    while (iniReserva.day <= reserva.finalReserva.day):
        
        listaDiasReserva.append(iniReserva)
        iniReserva += timedelta(days = 1)
    
    estacionamientotarifa = EsquemaTarifarioM2M.objects.filter( estacionamiento = reserva.estacionamiento )

    if len(estacionamientotarifa) == 2:
        esquema_no_feriado = estacionamientotarifa[0]
        esquema_feriado = estacionamientotarifa[1]
        
    numDias = len(listaDiasReserva)
    monto = 0
    montoTotal = 0
    
    # CASO 1: RESERVA EN UN SOLO DIA
    
    if (numDias == 1):
        
        coincidencia = False
        
        for diaFeriado in diasFeriados:
            
            if (listaDiasReserva[0].day == diaFeriado.fecha.day and 
                listaDiasReserva[0].month == diaFeriado.fecha.month):
                monto = Decimal(
                    esquema_feriado.tarifa.calcularPrecio(reserva.inicioReserva,reserva.finalReserva))
                
                coincidencia = True
                break
            
        if (not coincidencia):
                
                monto = Decimal(
                    esquema_no_feriado.tarifa.calcularPrecio(reserva.inicioReserva,reserva.finalReserva)
                )
                                
        montoTotal += monto
    
    # CASO 2: RESERVA DE MULTIPLES DIAS
        
    elif (numDias > 1):
        
        coincidencia = False
        cont = 1
        
        # Se define el inicio y el final de cada dia
            
        for diaReserva in listaDiasReserva:
            
        
            coincidencia = False
            
            if (cont == 1):
                inicioDia = reserva.inicioReserva
                finalDia = datetime(reserva.inicioReserva.year, reserva.inicioReserva.month, 
                                    reserva.inicioReserva.day, 23, 59)
            elif (cont == numDias):
                inicioDia = datetime(reserva.finalReserva.year, reserva.finalReserva.month, 
                                     reserva.finalReserva.day, 0, 0)
                finalDia = reserva.finalReserva
            else:
                inicioDia = datetime(diaReserva.year, diaReserva.month, 
                                     diaReserva.day, 0, 0)
                
                finalDia  = datetime(diaReserva.year, diaReserva.month, 
                                     diaReserva.day, 23, 59)
                
            # Se Calcula la tarifa de los dias que coinciden con los dias feriados    
                
            for diaFeriado in diasFeriados:
                 
                if (diaReserva.day == diaFeriado.fecha.day and 
                    diaReserva.month == diaFeriado.fecha.month):
                    
                    monto = Decimal(
                        esquema_feriado.tarifa.calcularPrecio(inicioDia,finalDia)
                    )
                    coincidencia = True
                    break
                     
            if (not coincidencia):
                
                monto = Decimal(
                        esquema_no_feriado.tarifa.calcularPrecio(inicioDia,finalDia)
                        )
            
            montoTotal += monto
            cont += 1
            
    return montoTotal
    
    
    
    
    
    
    
    
    
