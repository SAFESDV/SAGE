# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import urllib
from django.http import HttpResponse, Http404
from django.utils.dateparse import parse_datetime
from urllib.parse import urlencode
from matplotlib import pyplot
from decimal import Decimal
from collections import OrderedDict

from billetera.forms import *
from billetera.models import *
from billetera.controller import *
from estacionamientos.forms import *

from reservas.controller import (
    validarHorarioReserva,
    marzullo,
)

from reservas.forms import *

from reservas.models import Reserva
from transacciones.models import *
from reservas.controller import *
from transacciones.controller import *
from _datetime import timedelta

def reserva_detalle(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        reserva = Reserva.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    
    relation = TransReser.objects.get(reserva = reserva.id)
    transaccion = relation.transaccion
    

    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass
    return render(
        request,
        'reserva_detalle.html',
        {
          'reservacion': reserva
        , 'transaccion' : transaccion
        }
    )

def estacionamiento_cancelar_reserva(request):
    
    form = BuscarReservaForm()
    if request.method == 'POST':
        form = BuscarReservaForm(request.POST)
        if form.is_valid():
            
            numeroReser   = form.cleaned_data['numReser']
            numeroCedula  = form.cleaned_data['cedula']
            tipoCedula    = form.cleaned_data['cedulaTipo']
            try:
                reserva      = Reserva.objects.get(id = numeroReser, cedula = numeroCedula,
                                                   cedulaTipo = tipoCedula, estado = 'Válido')
            except:
                return render(
                    request,
                    'reserva_cancelar.html',
                    {  "color"    : "red"
                     , 'mensaje'  : 'ID no existe o CI no corresponde al registrado en la reserva.'
                     , "form"     : form
                    }
                )
            
            request.session['reservaid'] = reserva.id
            return render(
                request,
                'reserva_confirmar_cancelar.html',
                { 
                  'billetera': BilleteraLogin()
                }
            )
                            
    return render(
        request,
        'reserva_cancelar.html',
        { "form" : form }
    )
    
def confirmar_cancelar_reserva(request):
    form = BilleteraLogin()
    
    if request.method == 'POST':
        form = BilleteraLogin(request.POST)
        if form.is_valid():
            try:
                autenticar(form.cleaned_data['id'], form.cleaned_data['pin'])
            except:
                return render(
                        request,
                        'reserva_confirmar_cancelar.html',
                        { "billetera"       : form
                        , "color"           : "red"
                        ,'mensaje'          : "Autenticación denegada."
                        }
                    )

            cancelar_reserva(request.session['reservaid'],form.cleaned_data['id'])
            
            return render(
                    request,
                    'reserva_confirmar_cancelar.html',
                    {  "color"    : "green"
                     , 'mensaje'  : 'Reservación cancelada.'
                     , 'billetera' : form
                     }
                )
          
    return render(
        request,
        'reserva_confirmar_cancelar.html',
        {
        'billetera' : form,
        }
    )
    
def Mover_reserva_buscar_original(request):
    
    form = BuscarReservaForm()
    if request.method == 'POST':
        form = BuscarReservaForm(request.POST)
        if form.is_valid():
            
            numeroReser   = form.cleaned_data['numReser']
            numeroCedula  = form.cleaned_data['cedula']
            cedulaTipo    = form.cleaned_data['cedulaTipo']
            try:
                reserva_selec      = Reserva.objects.get(id = numeroReser, cedula = numeroCedula, 
                                                         cedulaTipo = cedulaTipo, estado = 'Válido')
            except:
                return render(
                    request,
                    'reserva_mover_buscar_original.html',
                    {  "color"    : "red"
                     , 'mensaje'  : 'No hay coincidencia entre el ID y la cedula'
                     , "form"     : form
                    }
                )
            
            if not(reserva_Cambiable(reserva_selec.inicioReserva,reserva_selec.finalReserva,
                                     reserva_selec.estacionamiento.horizonte)):
                return render(
                    request,
                    'reserva_mover_buscar_original.html',
                    {  "color"    : "red"
                     , 'mensaje'  : 'Esta reserva esta muy alejada del horizonte del estacionamiento'
                     , "form"     : form
                    }
                )
                
            
            transreser = TransReser.objects.get(reserva = reserva_selec)
                    
            request.session['reservaid'] = reserva_selec.id
            
            return render(
                request,
                'reserva_mover_buscar_original.html',
                { 'reserva'     : reserva_selec,
                  'transreser'  : transreser,
                  'billetera'   : BilleteraLogin(),
                  "form"        : form
                }
            )
                            
    return render(
        request,
        'reserva_mover_buscar_original.html',
        { "form" : form }
    )

def Mover_Reserva_buscar_nueva(request):
    
    form = MoverReservaNuevaForm()
    reserva_selec = Reserva.objects.get(id = request.session['reservaid'])
    transreser = TransReser.objects.get(reserva = reserva_selec)
    _id = reserva_selec.estacionamiento.id
    
    if request.method == 'POST':
        form = MoverReservaNuevaForm(request.POST)
        if form.is_valid():
            
            NuevoInicio   = form.cleaned_data['nuevoInicio']
            try:
                reserva_selec      = Reserva.objects.get(id = request.session['reservaid'], estado = 'Válido')
            except:
                return render(
                    request,
                    'reserva_mover_buscar_nueva.html',
                    {  "color"    : "red"
                     , 'mensaje'  : 'ID no existe o CI no corresponde al registrado en la reserva.'
                     , "form"     : form
                    }
                )
            
            NuevoFinal = NuevoInicio + (reserva_selec.finalReserva - reserva_selec.inicioReserva)
            m_validado = validarHorarioReserva(NuevoInicio, NuevoFinal, reserva_selec.estacionamiento.apertura, 
                                  reserva_selec.estacionamiento.cierre, reserva_selec.estacionamiento.horizonte)
            
            
            # Si no es valido devolvemos el request
            if not m_validado[0]:
                return render(
                    request,
                    'reserva_mover_buscar_nueva.html',
                    { 'color'  :'red'
                    , 'mensaje': m_validado[1]
                    , "form"            : form
                    , 'reserva'         : reserva_selec
                    , 'transreser'      : transreser
                    , 'billetera'       : BilleteraLogin()
                    }
                )
            
            if marzullo(_id, NuevoInicio, NuevoFinal, reserva_selec.tipo_vehiculo):
                
                diasFeriados = DiasFeriadosEscogidos.objects.filter(estacionamiento = reserva_selec.estacionamiento)
                
                reservaNueva = Reserva(
                    estacionamiento = reserva_selec.estacionamiento,
                    inicioReserva   = NuevoInicio,
                    finalReserva    = NuevoFinal,
                    estado          = reserva_selec.estado,
                    tipo_vehiculo   = reserva_selec.tipo_vehiculo,
                    cedula          = reserva_selec.cedula,
                    cedulaTipo      = reserva_selec.cedulaTipo,
                    nombre          = reserva_selec.nombre,
                    apellido        = reserva_selec.apellido,
                )
    
                montoTotal = calcular_Precio_Reserva(reservaNueva,reserva_selec.estacionamiento)
                diferencia = transreser.transaccion.monto - montoTotal
       
                request.session['finalReservaHora']    = NuevoFinal.hour
                request.session['finalReservaMinuto']  = NuevoFinal.minute
                request.session['inicioReservaHora']   = NuevoInicio.hour
                request.session['inicioReservaMinuto'] = NuevoInicio.minute
                request.session['anioinicial']         = NuevoInicio.year
                request.session['mesinicial']          = NuevoInicio.month
                request.session['diainicial']          = NuevoInicio.day
                request.session['aniofinal']           = NuevoFinal.year
                request.session['mesfinal']            = NuevoFinal.month
                request.session['diafinal']            = NuevoFinal.day
                request.session['tipo_vehiculo']       = reserva_selec.tipo_vehiculo
                request.session['nombre']              = reserva_selec.nombre
                request.session['apellido']            = reserva_selec.apellido
                request.session['cedula']              = reserva_selec.cedula
                request.session['cedulaTipo']          = reserva_selec.cedulaTipo
                request.session['monto']               = float(montoTotal)
            
            return render(
                request,
                'reserva_mover_buscar_nueva.html',
                { "form"            : form
                  ,'reserva'         : reserva_selec
                  ,'transreser'      : transreser
                  ,'billetera'       : BilleteraLogin()
                  ,'reservaNueva'    : reservaNueva
                  ,'Monto'           : montoTotal
                  ,'diferencia'      : diferencia
                  ,'mensaje'         : m_validado[1]
                }
            )
            
    return render(
        request,
        'reserva_mover_buscar_nueva.html',
        { "form"        : form,
         'reserva'      : reserva_selec,
         'transreser'   : transreser,
          'billetera'   : BilleteraLogin(),          
          }
    )

def Mover_Reserva_comfirmar(request):
    
    form = BilleteraLogin()
    reserva_selec = Reserva.objects.get(id = request.session['reservaid'])
    transreser = TransReser.objects.get(reserva = reserva_selec)
    _id = reserva_selec.estacionamiento.id
    
    if request.method == 'POST':
        form = BilleteraLogin(request.POST)
        if form.is_valid():
            
            if not (autenticar(form.cleaned_data['id'],form.cleaned_data['pin'])):
                
                return render(
                            request,
                            'reserva_mover_confirmar.html',
                            { "form"    : form
                            , "valido"  : 0
                            , "color"   : "red"
                            ,'mensaje'  : "Autenticación denegada."
                            }
                        )
            
            cancelar_reserva(reserva_selec.id,form.cleaned_data['id'])
            
            return render(
                request,
                'reserva_mover_confirmar.html',
                { "form"             : form
                  ,'reserva'         : reserva_selec
                  ,'transreser'      : transreser
                  ,'billetera'       : BilleteraLogin()
                  , "valido"         : 1
                }
            )
            
    return render(
        request,
        'reserva_mover_confirmar.html',
        { "form"        : form,
          "valido"  : 0,
         'reserva'      : reserva_selec,
         'transreser'   : transreser,
          'billetera'   : BilleteraLogin(),          
          }
    )
        
def Consulta_reserva(request):
    
    form = CedulaForm()
    if request.method == 'POST':
        form = CedulaForm(request.POST)
        if form.is_valid():
            _cedula        = form.cleaned_data['cedula']
            _cedulaTipo    = form.cleaned_data['cedulaTipo']
            facturas       = Reserva.objects.filter(cedula = _cedula,cedulaTipo = _cedulaTipo)
            
            if ((len(facturas)) == 0):
                return render(
                    request,
                    'reserva_consulta.html',
                    {  "color"    : "red"
                     , 'mensaje'  : 'No hay reservas registradas a esta cedula'
                     , "form"     : form
                    }
                )
                
            listaFacturas = []

            listaFacturas = sorted(
                list(facturas),
                key = lambda r: r.inicioReserva
            )
            return render(
                request,
                'reserva_consulta.html',
                { "listaFacturas" : listaFacturas
                , "form"          : form
                }
            )
    return render(
        request,
        'reserva_consulta.html',
        { "form" : form }
    )
