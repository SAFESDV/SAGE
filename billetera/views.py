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

from pagos.forms import (
    PagoForm,
    ModoPagoForm,
    BilleteraElectronicaPagoForm,
    PagoRecargaForm
)

from billetera.forms import (
    BilleteraElectronicaForm,
    BilleteraElectronicaRecargaForm,
)

from billetera.models import (
    BilleteraElectronica,
    PagoRecargaBilletera
)

from billetera.controller import (
    consultar_saldo,
    recargar_saldo,
    consumir_saldo,
)

from estacionamientos.models import (
    Estacionamiento,
    TarifaHora,
    TarifaMinuto,
    TarifaHorayFraccion,
    TarifaFinDeSemana,
    TarifaHoraPico,
)



from django.template.context_processors import request
from django.forms.forms import Form
from reservas.models import Reserva
from pagos.models import Pago

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
                PIN              = form.cleaned_data['pin'],
                saldo            = Decimal(0).quantize(Decimal('1.00'))
            )
            
            billetera.save();
            
            return render(
                request,
                'crearbilletera.html',
                { "billetera"    : billetera
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
    
    form = BilleteraElectronicaPagoForm()
    
    if request.method == 'POST':
        form = BilleteraElectronicaPagoForm(request.POST)
        if form.is_valid():
            saldo = consultar_saldo(form.cleaned_data['id'], form.cleaned_data['pin'])
            
            if(saldo == -1):
                return render(
                        request,
                        'consultar_saldo.html',
                        { "form"    : form
                        , "color"   : "red"
                        ,'mensaje'  : "Autenticación denegada."
                        }
                    )
                
                
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
    form = BilleteraElectronicaPagoForm()
    
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    
    if (estacionamiento.apertura is None):
        return HttpResponse(status = 403) # No esta permitido acceder a esta vista aun
    
    if request.method == 'POST':
        form = BilleteraElectronicaPagoForm(request.POST)
        if form.is_valid():
            try:
                BE = BilleteraElectronica.objects.get(id = form.cleaned_data['id'])
                if (BE.PIN != form.cleaned_data['pin']):
                    return render(
                        request,
                        'billetera_pagar.html',
                        { "form"    : form
                        , "color"   : "red"
                        ,'mensaje'  : "Autenticación denegada."
                        }
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
            if (monto > BE.saldo):
                return render(
                        request,
                        'billetera_pagar.html',
                        { "formIns"    : form
                        , "color"   : "red"
                        ,'mensaje'  : "Saldo es insuficiente."
                        }
                    )
            else:
                consumir_saldo(BE.id, monto)
                
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
                estacionamiento = estacionamiento,
                inicioReserva   = inicioReserva,
                finalReserva    = finalReserva,
                estado          = 'Válido',
                tipo_vehiculo   = request.session['tipo_vehiculo']
            )
            
            # Se guarda la reserva en la base de datos
            reservaFinal.save()
            pago = Pago(
                fechaTransaccion = datetime.now(),
                cedula           = BE.cedula,
                cedulaTipo       = BE.cedulaTipo,
                monto            = monto,
                tarjetaTipo      = "BE",
                reserva          = reservaFinal,
            )
            
            
            # Se guarda el recibo de pago en la base de datos
            pago.save()

            return render(
                request,
                'billetera_pagar.html',
                { "id"      : _id
                , "pago"    : pago
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
    form = BilleteraElectronicaRecargaForm()
    Valido = 0
    if request.method == 'POST':
        form = BilleteraElectronicaRecargaForm(request.POST)
        if form.is_valid():
            try:
                BE = BilleteraElectronica.objects.get(id = form.cleaned_data['id'])
                if (BE.PIN != form.cleaned_data['pin']):
                    return render(
                        request,
                        'billetera_recargar.html',
                        { "form"    : form
                        , "valido": Valido
                        , "color"   : "red"
                        ,'mensaje'  : "Autenticación denegada."
                        }
                    )
                    
                
            except ObjectDoesNotExist:
                return render(
                        request,
                        'billetera_recargar.html',
                        { "form"    : form
                        , "valido": Valido
                        , "color"   : "red"
                        ,'mensaje'  : "Autenticación denegada."
                        }
                    )
            Valido = 1
            return render(
                request,
                'billetera_recargar.html',
                { "color"   : "green"
                , "valido": Valido
                , 'mensaje' : "Se realizo el pago de reserva satisfactoriamente."
                }
            )
    return render(
        request,
        'billetera_recargar.html',
        { 'form' : form 
        , "valido": Valido
        }
    )     
    

def recarga_pago(request):
    form = PagoRecargaForm()
    
    if request.method == 'POST':
        form = PagoRecargaForm(request.POST)
        if form.is_valid():
            
            pago = PagoRecargaBilletera(
                fechaTransaccion = datetime.now(),
                cedulaTipo       = form.cleaned_data['cedulaTipo'],
                cedula           = form.cleaned_data['cedula'],
                ID_Billetera     = form.cleaned_data['ID_Billetera'],
                monto            = form.cleaned_data['monto'],
                tarjetaTipo      = form.cleaned_data['tarjetaTipo'],
            )
            
            BE = BilleteraElectronica.objects.get(id = pago.ID_Billetera)
            if pago.monto + BE.saldo > Decimal(10000.00):
                return render(request,
                    'pago_recarga.html',
                    {
                    'error'   : 1,
                    "color"   : "red",
                    'mensaje' : "Saldo resultante excede el monto maximo"
                    }
                )           
            
            
            # Se guarda el recibo de pago en la base de datos
            pago.save()
            
            recargar_saldo(pago.ID_Billetera,pago.monto)
            

            return render(
                request,
                'pago_recarga.html',
                {
                 "pago"   : pago,
                "color"   : "green",
                'mensaje' : "Se realizo la recarga satisfactoriamente."
                }
            )
    return render(
        request,
        'pago_recarga.html',
        { 'form' : form }
    )
