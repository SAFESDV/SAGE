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

from billetera.forms import (
    BilleteraElectronicaForm,
)

from billetera.models import *

from billetera.controller import (
    consultar_saldo,
    recargar_saldo,
    consumir_saldo,
)

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

def estacionamiento_cancelar_reserva(request, _id):
    id = int(_id)
    
    form = CancelarReservaForm()
    if request.method == 'POST':
        form = CancelarReservaForm(request.POST)
        if form.is_valid():
            
            numeroTransaccion   = form.cleaned_data['numTransac']
            numeroCedula        = form.cleaned_data['cedula']
            try:
                factura      = transaccion.objects.get(id = numeroTransaccion, cedula = numeroCedula)
            except:
                return render(
                    request,
                    'cancelar-reservas.html',
                    {  "color"    : "red"
                     , 'mensaje'  : 'ID no existe o CI no corresponde al registrado en el recibo de pago.'
                     , "form"     : form
                    }
                )
            
            if factura.reserva.estado != 'Válido':
                return render(
                    request,
                    'cancelar-reservas.html',
                    {  "color"   : "red"
                     , 'mensaje' : 'ID no existe o CI no corresponde al registrado en el recibo de pago.'
                     , "form" : form 
                     }
                )
            
            request.session['facturaid'] = factura.id
            return render(
                request,
                'cancelar_reserva_confirmar.html',
                { 
                  'billetera': BilleteraElectronicaPagoForm()
                }
            )
                            
    return render(
        request,
        'cancelar-reservas.html',
        { "form" : form }
    )
    
def confirmar_cancelar_reserva(request):
    form = BilleteraElectronicaPagoForm()
    
    factura = Pago.objects.get(id = request.session['facturaid'])
    
    if request.method == 'POST':
        form = BilleteraElectronicaPagoForm(request.POST)
        if form.is_valid():
            numeroID  = form.cleaned_data['id']
            numeroPin = form.cleaned_data['pin']
            try:
                billetera = BilleteraElectronica.objects.get(id = numeroID, PIN = numeroPin)
            except:
                return render(
                    request,
                    'cancelar_reserva_confirmar.html',
                    { "color"   : "red"
                     , 'mensaje' : 'Autenticación denegada.'
                     , 'billetera' : form
                     }
                )
             
            try:   
                recargar_saldo(billetera.id, factura.monto)
            except:
                return render(
                    request,
                    'cancelar_reserva_confirmar.html',
                    { "color"   : "red"
                     , 'mensaje' : 'Error al reembolsar reservación (Límite de saldo excedido).'
                     , 'billetera' : form
                     }
                )
                
            factura.reserva.estado = 'Cancelado'
            factura.reserva.save()
            
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