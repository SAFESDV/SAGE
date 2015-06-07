# -*- coding: utf-8 -*-

# Archivo con funciones de control para SAGE
from estacionamientos.models import Estacionamiento
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from pagos.models import Pago

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

def tasa_reservaciones(id_estacionamiento,prt=False):
	
	e = Estacionamiento.objects.get(id = id_estacionamiento)
	ahora = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
	reservas_filtradas = e.reserva_set.filter(finalReserva__gt=ahora)
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

    for estacionamiento in listaEstacionamientos:
        listaFacturas = Pago.objects.filter(
            reserva__estacionamiento__nombre = estacionamiento.nombre,
            reserva__estado = 'Válido'
        )
        
        ingreso = [estacionamiento.nombre, 0]
        
        for factura in listaFacturas:
            ingreso[1] += factura.monto
        listaIngresos += [ingreso]
        ingresoTotal  += ingreso[1]

    return listaIngresos, ingresoTotal
   
def seleccionar_feriados(fechaFeriado, descFeriado): #una lista de objeto que contiene la fecha y la descripción del día feriado
	
	diaferiado = DiasFeriadosEscogidos(fechaFeriado, descFeriado)
	diaferiado.save()
	
		
	
	
	