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

from reservas.controller import (
    validarHorarioReserva,
    marzullo,
)

from reservas.forms import (
    ReservaForm,
    CancelarReservaForm,
)

from reservas.models import Reserva
from transacciones.models import *
from reservas.controller import *
from transacciones.controller import *

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
    
    form = CancelarReservaForm()
    if request.method == 'POST':
        form = CancelarReservaForm(request.POST)
        if form.is_valid():
            
            numeroReser   = form.cleaned_data['numReser']
            numeroCedula  = form.cleaned_data['cedula']
            try:
                reserva      = Reserva.objects.get(id = numeroReser, cedula = numeroCedula, estado = 'Válido')
            except:
                return render(
                    request,
                    'cancelar-reservas.html',
                    {  "color"    : "red"
                     , 'mensaje'  : 'ID no existe o CI no corresponde al registrado en la reserva.'
                     , "form"     : form
                    }
                )
            
            request.session['reservaid'] = reserva.id
            return render(
                request,
                'cancelar_reserva_confirmar.html',
                { 
                  'billetera': BilleteraLogin()
                }
            )
                            
    return render(
        request,
        'cancelar-reservas.html',
        { "form" : form }
    )
    
def confirmar_cancelar_reserva(request):
    form = BilleteraLogin()
    
    if request.method == 'POST':
        form = BilleteraLogin(request.POST)
        if form.is_valid():
            print(form.cleaned_data['id'])
            print(form.cleaned_data['pin'])
            print(autenticar(form.cleaned_data['id'], form.cleaned_data['pin']))
            if not autenticar(form.cleaned_data['id'], form.cleaned_data['pin']):
                return render(
                        request,
                        'cancelar_reserva_confirmar.html',
                        { "billetera"       : form
                        , "color"           : "red"
                        ,'mensaje'          : "Autenticación denegada."
                        }
                    )
                
            trans = get_transacciones(request.session['reservaid'])
            print(request.session['reservaid'])
            print(trans)
            monto = transaccion_monto(trans[0].id)
             
            try:   
                recargar_saldo(form.cleaned_data['id'], monto)
            except:
                return render(
                    request,
                    'cancelar_reserva_confirmar.html',
                    { "color"   : "red"
                     , 'mensaje' : 'No se puede hacer un reembolso a esta billetera porque excede el limite'
                     , 'billetera' : form
                     }
                )
                
            cancelar_reserva(request.session['reservaid'])
            
            return render(
                    request,
                    'cancelar_reserva_confirmar.html',
                    {  "color"    : "green"
                     , 'mensaje'  : 'Reservación cancelada.'
                     , 'billetera' : form
                     }
                )
          
    return render(
        request,
        'cancelar_reserva_confirmar.html',
        {
        'billetera' : form,
        }
    )