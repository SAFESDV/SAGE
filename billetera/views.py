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
from datetime import datetime

from estacionamientos.forms import (
    EstacionamientoExtendedForm,
    EstacionamientoForm,
    EditarEstacionamientoForm,
    RifForm,
    CedulaForm)

from reservas.forms import ReservaForm

from billetera.forms import *

from billetera.models import (
    BilleteraElectronica
)

from billetera.controller import *

from estacionamientos.models import (
    Estacionamiento,
    TarifaHora,
    TarifaMinuto,
    TarifaHorayFraccion,
    TarifaFinDeSemana,
    TarifaHoraPico,
)

from transacciones.models import *


from django.template.context_processors import request
from django.forms.forms import Form
from reservas.models import Reserva

def billetera_crear(request):
    form = BilleteraElectronicaForm()
    
    if request.method == 'POST':
        form = BilleteraElectronicaForm(request.POST)
        if form.is_valid():
            
            billetera = BilleteraElectronica(
                nombreUsuario    = form.cleaned_data['nombre'],
                apellidoUsuario  = form.cleaned_data['apellido'],
                cedulaTipo       = form.cleaned_data['cedulaTipo'],
                cedula           = form.cleaned_data['cedula'],
                PIN              = form.cleaned_data['pin']
            )
            
            billetera.save();
            
            return render(
                request,
                'crearbilletera.html',
                { "billetera"    : billetera
                , "saldo"   : consultar_saldo(billetera.id)
                , "color"   : "green"
                , 'mensaje' : "Se ha creado la billetera satisfactoriamente."
                }
            )
    
    return render(
        request,
        'crearbilletera.html',
        {
         'form' : form
        }
    )

def Consultar_Saldo(request):
    
    form = BilleteraLogin()
    
    if request.method == 'POST':
        form = BilleteraLogin(request.POST)
        if form.is_valid():
            
            if not autenticar(form.cleaned_data['id'], form.cleaned_data['pin']):
                return render(
                        request,
                        'consultar_saldo.html',
                        { "form"    : form
                        , "color"   : "red"
                        ,'mensaje'  : "Autenticación denegada."
                        }
                    )
                
            
            saldo = consultar_saldo(form.cleaned_data['id'])
            noSaldo = 1
            if saldo > 0:
                noSaldo = 0
            
            return render(
                        request,
                        'consultar_saldo.html',
                        {"Saldo" : saldo,
                         "nosaldo" : noSaldo,
                         "color" : "red",
                         "mensaje" : "Se recomienda recargar."
                         }
            )
                                   
    return render(
                request,
                'consultar_saldo.html',
                {"form" : form}
                )
    
def billetera_pagar(request, _id):
    form = BilleteraLogin()
    
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    
    if (estacionamiento.apertura is None):
        return HttpResponse(status = 403) # No esta permitido acceder a esta vista aun
    
    if request.method == 'POST':
        form = BilleteraLogin(request.POST)
        if form.is_valid():
            try:
                BE = BilleteraElectronica.objects.get(
                    id = form.cleaned_data['id'],
                    PIN = form.cleaned_data['pin']
                )                
            except ObjectDoesNotExist:
                return render(
                        request,
                        'billetera_pagar.html',
                        { "form"    : form
                        , "color"   : "red"
                        ,'mensaje'  : "Autenticación denegada."
                        }
                    )
            
            monto = Decimal(request.session['monto']).quantize(Decimal('1.00'))
            
            if (monto > consultar_saldo(form.cleaned_data['id'])):
                return render(
                        request,
                        'billetera_pagar.html',
                        { "formIns"    : form
                        , "color"   : "red"
                        ,'mensaje'  : "Saldo es insuficiente."
                        }
                    )
                
            inicioReserva = datetime(
                year   = request.session['anioinicial'],
                month  = request.session['mesinicial'],
                day    = request.session['diainicial'],
                hour   = request.session['inicioReservaHora'],
                minute = request.session['inicioReservaMinuto']
            )

            finalReserva  = datetime(
                year   = request.session['aniofinal'],
                month  = request.session['mesfinal'],
                day    = request.session['diafinal'],
                hour   = request.session['finalReservaHora'],
                minute = request.session['finalReservaMinuto']
            )

            reservaFinal = Reserva(
                cedulaTipo      = request.session['cedulaTipo'],
                cedula          = request.session['cedula'],
                nombre          = request.session['nombre'],
                apellido        = request.session['apellido'],
                estacionamiento = estacionamiento,
                inicioReserva   = inicioReserva,
                finalReserva    = finalReserva,
                estado          = 'Válido',
                tipo_vehiculo   = request.session['tipo_vehiculo']
            )
            # Se guarda la reserva en la base de datos
            reservaFinal.save()
            
            transId = consumir_saldo(BE.id, monto)
            
            relation = TransReser(
                transaccion = Transaccion.objects.get(id = transId),
                reserva     = reservaFinal
            )
            
            relation.save()

            return render(
                request,
                'billetera_pagar.html',
                { "id"      : _id
                , "pago"    : form
                , "relacion" : relation
                , "color"   : "green"
                , 'mensaje' : "Se realizo el pago de reserva satisfactoriamente."
                }
            )
    return render(
        request,
        'billetera_pagar.html',
        { 'form' : form }
    )
    
def billetera_recargar(request):

    form = BilleteraLogin()
    
    if request.method == 'POST':
        form = BilleteraLogin(request.POST)
        if form.is_valid():
            
            if not autenticar(form.cleaned_data['id'], form.cleaned_data['pin']):
                return render(
                        request,
                        'billetera_recargar.html',
                        { "form"    : form
                        , "valido"  : 0
                        , "color"   : "red"
                        ,'mensaje'  : "Autenticación denegada."
                        }
                    )
            
            request.session['passbillid'] = form.cleaned_data['id']
            
            return render(
                request,
                'billetera_recargar.html',
                { "color"   : "green"
                , "valido"  : 1
                , 'mensaje' : "Se realizo el pago de reserva satisfactoriamente."
                }
            )
    return render(
        request,
        'billetera_recargar.html',
        { 'form'   : form
        , "valido" : 0
        }
    )     
    

def recarga_pago(request):
    form = BilleteraRecargaForm()
    
    if request.method == 'POST':
        form = BilleteraRecargaForm(request.POST)
        if form.is_valid():
            try:
                recargar_saldo_TDC(request.session['passbillid'], form)
                return render(
                    request,
                    'pago_recarga.html',
                    {
                     "pago"   : form,
                    "color"   : "green",
                    'mensaje' : "Se realizo la recarga satisfactoriamente."
                    }
                )        
            except:
                return render(request,
                        'pago_recarga.html',
                        {
                        'error'   : 1,
                        "color"   : "red",
                        'mensaje' : "Saldo resultante excede el monto maximo"
                        }
                    )
    return render(
        request,
        'pago_recarga.html',
        { 'form' : form }
    )
