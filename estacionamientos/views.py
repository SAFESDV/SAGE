# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils import dateparse
import re

import urllib
import datetime
from decimal import Decimal
from estacionamientos.controller import HorarioEstacionamiento, validarHorarioReserva, marzullo
from estacionamientos.forms import (
    EstacionamientoExtendedForm,
    EstacionamientoForm,
    ReservaForm,
    PagoForm,
    RifForm,
    CedulaForm,
)
from estacionamientos.models import (
    Estacionamiento,
    Reserva,
    Pago,
    TarifaHora,
    TarifaMinuto,
    TarifaHorayFraccion,
    TarifaFinDeSemana,
    TarifaHoraPico
)
from django.http.response import HttpResponseRedirect, HttpResponse
from django.utils.dateparse import parse_datetime


# Usamos esta vista para procesar todos los estacionamientos
def estacionamientos_all(request):
    estacionamientos = Estacionamiento.objects.all()

    # Si es un GET, mandamos un formulario vacio
    if request.method == 'GET':

        form = EstacionamientoForm()

    # Si es POST, se verifica la información recibida
    elif request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form = EstacionamientoForm(request.POST)

        # Parte de la entrega era limitar la cantidad maxima de
        # estacionamientos a 5
        if len(estacionamientos) >= 5:
            return render(request, 'templateMensaje.html',
                                  {'color'   : 'red', 
                                   'mensaje' : 'No se pueden agregar más estacionamientos'
                                  }
                        )

        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            obj = Estacionamiento(
                propietario = form.cleaned_data['propietario'],
                nombre      = form.cleaned_data['nombre'],
                direccion   = form.cleaned_data['direccion'],
                rif         = form.cleaned_data['rif'],
                telefono1   = form.cleaned_data['telefono_1'],
                telefono2   = form.cleaned_data['telefono_2'],
                telefono3   = form.cleaned_data['telefono_3'],
                email1      = form.cleaned_data['email_1'],
                email2      = form.cleaned_data['email_2']
            )
            obj.save()
            # Recargamos los estacionamientos ya que acabamos de agregar
            estacionamientos = Estacionamiento.objects.all()
            form = EstacionamientoForm()

    return render(request, 'base.html', {'form': form, 'estacionamientos': estacionamientos})

def estacionamiento_detail(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')

    if request.method == 'GET':
        form = EstacionamientoExtendedForm()

    elif request.method == 'POST':
        # Leemos el formulario
        form = EstacionamientoExtendedForm(request.POST)
        # Si el formulario
        if form.is_valid():
            horaIn        = form.cleaned_data['horarioin']
            horaOut       = form.cleaned_data['horarioout']
            reservaIn     = form.cleaned_data['horario_reserin']
            reservaOut    = form.cleaned_data['horario_reserout']
            tarifa        = form.cleaned_data['tarifa']
            tipo          = form.cleaned_data['esquema']
            inicioTarifa2 = form.cleaned_data['inicioTarifa2']
            finTarifa2    = form.cleaned_data['finTarifa2']
            tarifa2       = form.cleaned_data['tarifa2']

            esquemaTarifa = eval(tipo)(tarifa         = tarifa,
                                       tarifa2        = tarifa2, 
                                       inicioEspecial = inicioTarifa2, 
                                       finEspecial    = finTarifa2)

            esquemaTarifa.save()
            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            m_validado = HorarioEstacionamiento(horaIn, horaOut, reservaIn, reservaOut)
            if not m_validado[0]:
                return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})
            # debería funcionar con excepciones

            estacionamiento.tarifa         = tarifa
            estacionamiento.apertura       = horaIn
            estacionamiento.cierre         = horaOut
            estacionamiento.reservasInicio = reservaIn
            estacionamiento.reservasCierre = reservaOut
            estacionamiento.esquemaTarifa  = esquemaTarifa
            estacionamiento.nroPuesto      = form.cleaned_data['puestos']

            estacionamiento.save()
            form = EstacionamientoExtendedForm()

    return render(request, 'estacionamiento.html', {'form': form, 'estacionamiento': estacionamiento})


def estacionamiento_reserva(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')

    # Si se hace un GET renderizamos los estacionamientos con su formulario
    if request.method == 'GET':
        form = ReservaForm()

    # Si es un POST estan mandando un request
    elif request.method == 'POST':
        form = ReservaForm(request.POST)
        print(request.POST)
        # Verificamos si es valido con los validadores del formulario
        if form.is_valid():
            
            inicioReserva = form.cleaned_data['inicio']
            print(form.cleaned_data)
            finalReserva = form.cleaned_data['final']

            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            m_validado = validarHorarioReserva(inicioReserva, 
                                               finalReserva, 
                                               estacionamiento.reservasInicio, 
                                               estacionamiento.reservasCierre
                                            )

            # Si no es valido devolvemos el request
            if not m_validado[0]:
                return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})

            if marzullo(_id, inicioReserva, finalReserva):
                reservaFinal = Reserva( estacionamiento=estacionamiento,
                                        inicioReserva=inicioReserva,
                                        finalReserva=finalReserva,
                                    )

                monto = Decimal(estacionamiento.esquemaTarifa.calcularPrecio(inicioReserva,finalReserva))

                request.session['monto'] = float(estacionamiento.esquemaTarifa.calcularPrecio(inicioReserva,finalReserva))
                request.session['finalReservaHora']    = finalReserva.hour
                request.session['finalReservaMinuto']  = finalReserva.minute
                request.session['inicioReservaHora']   = inicioReserva.hour
                request.session['inicioReservaMinuto'] = inicioReserva.minute
                request.session['anioinicial']         = inicioReserva.year
                request.session['mesinicial']          = inicioReserva.month
                request.session['diainicial']          = inicioReserva.day
                request.session['aniofinal']           = finalReserva.year
                request.session['mesfinal']            = finalReserva.month
                request.session['diafinal']            = finalReserva.day
                return render(request, 'estacionamientoPagarReserva.html', 
                                       {'id'      : _id,
                                        'monto'   : monto,
                                        'reserva' : reservaFinal,
                                        'color'   : 'green', 
                                        'mensaje' : 'Existe un puesto disponible'
                                       }
                            )
            else:
                # Cambiar mensaje
                return render(request, 'templateMensaje.html', 
                                        {'color'   : 'red', 
                                         'mensaje' : 'No hay un puesto disponible para ese horario'
                                        }
                            )

    return render(request, 'estacionamientoReserva.html', {'form': form, 'estacionamiento': estacionamiento})

def estacionamiento_pago(request,_id):
    form = PagoForm()
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            try:
                estacionamiento = Estacionamiento.objects.get(id = _id)
            except ObjectDoesNotExist:
                return render(request, '404.html')
            inicioReserva = datetime.datetime(year   = request.session['anioinicial'], 
                                              month  = request.session['mesinicial'], 
                                              day    = request.session['diainicial'], 
                                              hour   = request.session['inicioReservaHora'],
                                              minute = request.session['inicioReservaMinuto']
                                            )

            finalReserva  = datetime.datetime(year   = request.session['aniofinal'], 
                                              month  = request.session['mesfinal'],
                                              day    = request.session['diafinal'], 
                                              hour   = request.session['finalReservaHora'],
                                              minute = request.session['finalReservaMinuto']
                                             )

            reservaFinal = Reserva( estacionamiento = estacionamiento,
                                    inicioReserva   = inicioReserva,
                                    finalReserva    = finalReserva,
                                )

            # Se guarda la reserva en la base de datos
            reservaFinal.save()

            monto = Decimal(request.session['monto']).quantize(Decimal('1.00'))
            pago = Pago(fechaTransaccion = datetime.datetime.now(),
                        cedula           = form.cleaned_data['cedula'],
                        cedulaTipo       = form.cleaned_data['cedulaTipo'],
                        monto            = monto,
                        tarjetaTipo      = form.cleaned_data['tarjetaTipo'],
                        reserva          = reservaFinal,
                        )

            # Se guarda el recibo de pago en la base de datos
            pago.save()

            return render(request,'pago.html',{"id"      : _id,
                                               "pago"    : pago,
                                               "color"   : "green",
                                               'mensaje' : "Se realizo el pago de reserva satisfactoriamente."
                                              }
                        )

    return render(request, 'pago.html', {'form':form})


def estacionamiento_ingreso(request):
    form = RifForm()
    if request.method == 'POST':
        form = RifForm(request.POST)
        if form.is_valid():

            rif                   = form.cleaned_data['rif']
            listaEstacionamientos = Estacionamiento.objects.filter(rif = rif) 
            ingresoTotal          = 0
            listaIngresos         = []

            for estacionamiento in listaEstacionamientos:
                listaFacturas = Pago.objects.filter(reserva__estacionamiento__nombre = estacionamiento.nombre)
                ingreso       = [estacionamiento.nombre, 0]
                for factura in listaFacturas:
                    ingreso[1] += factura.monto
                listaIngresos += [ingreso]
                ingresoTotal  += ingreso[1]

            return render(request,'estacionamientoIngreso.html',{ "ingresoTotal"  : ingresoTotal,
                                                                  "listaIngresos" : listaIngresos,
                                                                  "form"          : form,
                                                                }
                          )

    return render(request, 'estacionamientoIngreso.html', {"form" : form })

def estacionamiento_consulta_reserva(request):
    form = CedulaForm()
    if request.method == 'POST':
        form = CedulaForm(request.POST)
        if form.is_valid():

            cedula        = form.cleaned_data['cedula']
            facturas      = Pago.objects.filter(cedula = cedula) 
            listaFacturas = []

            for factura in facturas:
                listaFacturas += [factura]
            listaFacturas.sort(key=lambda r: r.reserva.inicioReserva)

            return render(request,'estacionamientoConsultarReservas.html',
                                    { "listaFacturas" : listaFacturas,
                                      "form"          : form,
                                    }
                          )

    return render(request, 'estacionamientoConsultarReservas.html', {"form" : form })

def receive_sms(request):
    # Procesamiento del mensaje
    '''sms = 'nombre        in 2015-02-15    07:00   out   2015-02-20 10:00    '
    sms = re.split('in', sms)
    sms = re.split('out', sms)
    sms[0] = sms[0].strip()
    sms[0] = re.sub('\s{2,}', ' ', sms[0])
    sms[0] = re.sub('(\s)*in(\s)*', '', sms[0])
    sms[1] = sms[1].strip()
    sms[1] = re.sub('\s{2,}', ' ', sms[1])
    horario_in = parse_datetime(sms[0])
    horario_out = parse_datetime(sms[1])
    print(horario_in)
    print(horario_out)'''
    
    
    phone = request.GET.get('phone', False)
    text = request.GET.get('text', False)
    # print(phone)
    # print(text)
    phone = urllib.parse.quote(str(phone))
    text = urllib.parse.quote(str(text))
    print('http://192.168.0.135:8000/sendsms?phone={0}&text={1}&password='.format(phone,text))
    f = urllib.request.urlopen('http://192.168.0.135:8000/sendsms?phone={0}&text={1}&password='.format(phone,text))
    print(f.read(100).decode('utf-8'))
    return HttpResponse('')
    #urllib.request.urlopen('http://192.168.0.135:8000/sendsms?phone={0}&text={1}&password='.format(phone,text))
    #return render(request, 'sms.html', {'text':text})