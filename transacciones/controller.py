# -*- coding: utf-8 -*-

# Archivo con funciones de control para SAGE
from estacionamientos.models import Estacionamiento, DiasFeriadosEscogidos
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from transacciones.models import *
from itertools import chain

def cacular_precio(_id, inicio, fin):
    
    inicioReserva = inicio
    iniReserva = inicio
    
    finalReserva = fin
    listaDiasReserva = []
    
    estacionamiento_selec = Estacionamiento.objects.get(id = _id)

    while (iniReserva.day <= finalReserva.day):
        
        listaDiasReserva.append(iniReserva)
        iniReserva += timedelta(days = 1) 
    
    estacionamientotarifa = EsquemaTarifarioM2M.objects.filter( estacionamiento = estacionamiento_selec )

    if len(estacionamientotarifa) == 2:
        esquema_no_feriado = estacionamientotarifa[0]
        esquema_feriado = estacionamientotarifa[1]
        
    numDias = len(listaDiasReserva)
    print()
    print("El numero de dias eeeeeeeeeees " + str(numDias))
    print()
    monto = 0
    montoTotal = 0
    
    # CASO 1: RESERVA EN UN SOLO DIA
    
    if (numDias == 1):
        
        coincidencia = False
        
        for diaFeriado in diasFeriados:
            
            print()
            print("el dia de la reserva es ")
            print(listaDiasReserva[0])
            print("el dia feriado es ")
            print(diaFeriado)
            print()
            
            if (listaDiasReserva[0].day == diaFeriado.fecha.day and 
                listaDiasReserva[0].month == diaFeriado.fecha.month):
                print("Entre en tarifa feriada")
                monto = Decimal(
                    esquema_feriado.tarifa.calcularPrecio(inicioReserva,finalReserva)
                )
    
                request.session['monto'] = float(
                    esquema_feriado.tarifa.calcularPrecio(inicioReserva,finalReserva)
                )
                print("monto a agregar " + str(monto))
                coincidencia = True
                break
            
        if (not coincidencia):
                
                monto = Decimal(
                    esquema_no_feriado.tarifa.calcularPrecio(inicioReserva,finalReserva)
                )
                print("Entre en NOOOOO tarifa feriada")
                print("Monto a agregar " + str(monto))
                request.session['monto'] = float(
                    esquema_no_feriado.tarifa.calcularPrecio(inicioReserva,finalReserva)
                )
        montoTotal += monto
        print("Monto =" + str(montoTotal))
    
    # CASO 2: RESERVA DE MULTIPLES DIAS
        
    elif (numDias > 1):
        
        coincidencia = False
        cont = 1
        
        # Se define el inicio y el final de cada dia
            
        for diaReserva in listaDiasReserva:
            
            print("Contador es " + str(cont))
            coincidencia = False
            
            if (cont == 1):
                print("Dia primero")
                inicioDia = inicioReserva
                finalDia = datetime(inicioReserva.year, inicioReserva.month, 
                                    inicioReserva.day, 23, 59)
            elif (cont == numDias):
                print("Dia Ultimo")
                inicioDia = datetime(finalReserva.year, finalReserva.month, 
                                     finalReserva.day, 0, 0)
                finalDia = finalReserva
            else:
                print("Dia intermedio")
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
                    print("monto a agregar " + str(monto))
    
                    request.session['monto'] = float(
                        esquema_feriado.tarifa.calcularPrecio(inicioDia,finalDia)
                    )
                    coincidencia = True
                    break
                     
            if (not coincidencia):
                
                monto = Decimal(
                        esquema_no_feriado.tarifa.calcularPrecio(inicioDia,finalDia)
                )
                print("monto a agregar " + str(monto))

                request.session['monto'] = float(
                    esquema_no_feriado.tarifa.calcularPrecio(inicioDia,finalDia)
                )
            
            montoTotal += monto
            request.session['monto'] = float(montoTotal)
            cont += 1
            print("Monto =" + str(montoTotal))
            
    return montoTotal

def transaccion_monto(_id):
	
	try:
		trans = Transaccion.objects.get(id = _id)
	except:
		raise
	
	monto = Decimal(0.00).quantize(Decimal("1.00"))
	
	detalles = list(chain(
								TransBilletera.objects.filter(transaccion = trans),
								TransTDC.objects.filter(transaccion = trans)							
							))
	
	for det in detalles:
		monto += det.monto
	
	return monto

# def transaccion_crear(_fecha, _tipo):
#     
#     trans = Transaccion(
#                 fecha            = _fecha,
#                 tipo             = _tipo,
#                 estado           = 'Válido'
#             )
#     
#     trans.save()
#     
#     return trans
# 	
# def transaccion_append_billetera(_idT, _idB, monto):
#     
#     trans = Transaccion.objects.get(id = _idT)
#     bill = BilleteraElectronica.objects.get(id = _idB)
#     
#     transBill = TransBilletera(
#                     billetera        = bill,
#                     transaccion      = trans,
#                     monto            = monto
#                 )
#     
#     transBill.save()
#     
#     return transBill
# 
# def transaccion_append_tdc(_idT, nombre, cedulaT, cedula, monto):
#     
#     trans = Transaccion.objects.get(id = _idT)
#     
#     transtdc = TransTDC(
#                     nombre           = models.CharField(max_length = 50)
#                     cedulaTipo       = models.CharField(max_length = 1)
#                     cedula           = models.CharField(max_length = 10)
#                     tarjetaTipo      = models.CharField(max_length = 6)
#                     tarjeta          = models.CharField(max_length = 4)
#                     monto            = models.DecimalField(decimal_places = 2, max_digits = 256)
#                     transaccion      = models.ForeignKey(Transaccion)
#                 )
#     
#     transtdc.save()
#     
#     return transBill
	
	
	