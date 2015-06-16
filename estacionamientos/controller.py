# -*- coding: utf-8 -*-

# Archivo con funciones de control para SAGE
from estacionamientos.models import (
    Estacionamiento,
    EsquemaTarifario,
    EsquemaTarifarioM2M,
    TarifaHora,
    TarifaMinuto,
    TarifaHorayFraccion,
    TarifaFinDeSemana,
    TarifaHoraPico,
    DiasFeriadosEscogidos,
)
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from transacciones.models import *
from transacciones.controller import *

# chequeo de horarios de extended
def HorarioEstacionamiento(HoraInicio, HoraFin):
	return HoraFin > HoraInicio

def get_client_ip(request):
	
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
		
	return ip

def tasa_reservaciones(id_estacionamiento,tipo_V,prt=False):
	
	e = Estacionamiento.objects.get(id = id_estacionamiento)
	ahora = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
	reservas_filtradas = e.reserva_set.filter(finalReserva__gt=ahora, tipo_vehiculo = tipo_V)
	lista_fechas=[(ahora+timedelta(i)).date() for i in range(7)]
	lista_valores=[0 for i in range(7)]
	ocupacion_por_dia = OrderedDict(zip(lista_fechas,lista_valores))
	UN_DIA = timedelta(days = 1)
	
	for reserva in reservas_filtradas:
		# Caso del inicio de la reserva
		if (reserva.inicioReserva < ahora):
			reserva_inicio = ahora
		else:
			reserva_inicio = reserva.inicioReserva
			
		reserva_final = reserva.finalReserva
		final_aux = reserva_inicio.replace(hour=0,minute=0,second=0,microsecond=0)
		
		while (reserva_final.date()>reserva_inicio.date()): 
			final_aux += UN_DIA
			longitud_reserva = final_aux-reserva_inicio
			ocupacion_por_dia[reserva_inicio.date()] += longitud_reserva.seconds/60+longitud_reserva.days*24*60
			reserva_inicio = final_aux
			
		longitud_reserva = reserva_final-reserva_inicio
		ocupacion_por_dia[reserva_inicio.date()] += longitud_reserva.seconds/60 + longitud_reserva.days*24*60
			
	return ocupacion_por_dia

def calcular_porcentaje_de_tasa(hora_apertura,hora_cierre, capacidad, ocupacion):
	
	factor_divisor = timedelta(hours = hora_cierre.hour,minutes=hora_cierre.minute)
	factor_divisor -= timedelta(hours = hora_apertura.hour,minutes=hora_apertura.minute)
	factor_divisor = Decimal(factor_divisor.seconds)/Decimal(60)
	
	if (hora_apertura == time(0,0) and hora_cierre == time(23,59)):
		factor_divisor +=1 # Se le suma un minuto
		
	for i in ocupacion.keys():
		ocupacion[i] = (Decimal(ocupacion[i])*100/(factor_divisor*capacidad)).quantize(Decimal('1.0'))



def consultar_ingresos(rif):
	
    listaEstacionamientos = Estacionamiento.objects.filter(rif = rif)
    ingresoTotal = 0
    listaIngresos = []
    listaTransacciones = []

    for estacionamiento in listaEstacionamientos:
        transreser = TransReser.objects.filter(
            reserva__estacionamiento__nombre = estacionamiento.nombre,
            reserva__estado = 'Válido'
        )
        

        for	tr in transreser:
            listaTransacciones += [tr.transaccion]
		
        ingreso = [estacionamiento.nombre, 0]
		
        for trans in listaTransacciones:
            ingreso[1] += transaccion_monto(trans.id)
        listaIngresos += [ingreso]
        ingresoTotal  += ingreso[1]

    return listaIngresos, ingresoTotal
   
def seleccionar_feriados(diaFeriado, estacionamiento): #una lista de objeto que contiene la fecha y la descripción del día feriado
	

	feriadosEscogidos = DiasFeriadosEscogidos.objects.all()
	
	
	
	diasFeriados = {'AñoNuevo'  : datetime(year = datetime.now().year, month = 1, day = 1), 
                    'DeclaracionIndependencia'  : datetime(year =  datetime.now().year, month =  4, day = 19), 
                    'DiaTrabajador'  : datetime(year=  datetime.now().year, month = 5, day  = 1),  
                    'BatallaCarabobo'  :  datetime(year=  datetime.now().year, month = 6, day  = 24),  
                    'DiaIndependencia'  : datetime(year=  datetime.now().year, month = 7, day  = 5 ), 
                    'NatalicioSimonBolivar'  :  datetime(year=  datetime.now().year, month = 7, day  = 24 ), 
                    'DiaResistenciaIndigena'  : datetime(year=  datetime.now().year, month = 10, day  = 12  ),
                    'VisperaNavidad': datetime(year=  datetime.now().year, month = 12, day  = 24 ),
                    'Navidad'  : datetime(year=  datetime.now().year, month = 12, day  = 25 ), 
                    'FinAño'  :  datetime(year=  datetime.now().year, month = 12, day  = 31 ) }
	
	for dia in feriadosEscogidos:
		for dias in diasFeriados:
			if (dia.fecha == diasFeriados[dias] and (dia.estacionamiento == estacionamiento)):
				dia.delete()
				break
	
	for dia in diaFeriado:
		     
		feriadosEscogidos = DiasFeriadosEscogidos(fecha = diasFeriados[dia],
												descripcion = dia,
												estacionamiento = estacionamiento)
		feriadosEscogidos.save()
		
def seleccionar_feriado_extra(diaFecha, diaDescripcion, estacionamiento): #una lista de objeto que contiene la fecha y la descripción del día feriado
	
			     
	feriadosEscogidos = DiasFeriadosEscogidos(fecha = diaFecha,
											descripcion = diaDescripcion,
											estacionamiento = estacionamiento)
	feriadosEscogidos.save()

def limpiarEsquemasTarifarios(_id):
	
	#limpiando la base de datos
        estacionamientotarifa = EsquemaTarifarioM2M.objects.filter( estacionamiento = _id )
        estacionamientotarifa.delete()
        estacionamientotarifa = TarifaHora.objects.filter(estacionamiento = _id)
        estacionamientotarifa.delete()
        estacionamientotarifa = TarifaHoraPico.objects.filter(estacionamiento = _id)
        estacionamientotarifa.delete()
        estacionamientotarifa = TarifaFinDeSemana.objects.filter(estacionamiento = _id)
        estacionamientotarifa.delete()
        estacionamientotarifa = TarifaHorayFraccion.objects.filter(estacionamiento = _id)
        estacionamientotarifa.delete()
        estacionamientotarifa = TarifaMinuto.objects.filter(estacionamiento = _id)
        estacionamientotarifa.delete()
