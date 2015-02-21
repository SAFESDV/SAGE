# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

import datetime
from decimal import Decimal
from estacionamientos.controller import HorarioEstacionamiento, validarHorarioReserva, marzullo
from estacionamientos.forms import EstacionamientoExtendedForm
from estacionamientos.forms import EstacionamientoForm
from estacionamientos.forms import EstacionamientoReserva
from estacionamientos.forms import PagoTarjetaDeCredito

from estacionamientos.models import * # No tocar esta linea


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
                          {'color':'red', 'mensaje':'No se pueden agregar más estacionamientos'})

        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            obj = Estacionamiento(
                propietario = form.cleaned_data['propietario'],
                nombre = form.cleaned_data['nombre'],
                direccion = form.cleaned_data['direccion'],
                rif = form.cleaned_data['rif'],
                telefono1 = form.cleaned_data['telefono_1'],
                telefono2 = form.cleaned_data['telefono_2'],
                telefono3 = form.cleaned_data['telefono_3'],
                email1 = form.cleaned_data['email_1'],
                email2 = form.cleaned_data['email_2']
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
            horaIn = form.cleaned_data['horarioin']
            horaOut = form.cleaned_data['horarioout']
            reservaIn = form.cleaned_data['horario_reserin']
            reservaOut = form.cleaned_data['horario_reserout']

            tarif_num = int(form.cleaned_data['esquema'])
            tmonto = form.cleaned_data["field_%d_%d" % (tarif_num,0)]
            esquema = form.lista_de_esquemas[tarif_num][0](tarifa = tmonto)
            esquema.save()
            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            m_validado = HorarioEstacionamiento(horaIn, horaOut, reservaIn, reservaOut)
            if not m_validado[0]:
                return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})
            # debería funcionar con excepciones

            estacionamiento.tarifa = tmonto
            estacionamiento.apertura = horaIn
            estacionamiento.cierre = horaOut
            estacionamiento.reservasInicio = reservaIn
            estacionamiento.reservasCierre = reservaOut
            estacionamiento.esquemaTarifa = esquema
            estacionamiento.nroPuesto = form.cleaned_data['puestos']

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
        form = EstacionamientoReserva()

    # Si es un POST estan mandando un request
    elif request.method == 'POST':
        form = EstacionamientoReserva(request.POST)
        # Verificamos si es valido con los validadores del formulario
        if form.is_valid():
            inicioReserva = form.cleaned_data['inicio']
            finalReserva = form.cleaned_data['final']

            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            m_validado = validarHorarioReserva(inicioReserva, finalReserva, estacionamiento.reservasInicio, estacionamiento.reservasCierre)


            # Si no es valido devolvemos el request
            if not m_validado[0]:
                return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})

            if marzullo(_id, inicioReserva, finalReserva):
                reservaFinal = Reserva(estacionamiento=estacionamiento,inicioReserva=inicioReserva,finalReserva=finalReserva)
                monto = Decimal(estacionamiento.esquemaTarifa.calcularPrecio(inicioReserva,finalReserva))

                request.session['monto'] = float(estacionamiento.esquemaTarifa.calcularPrecio(inicioReserva,finalReserva))
                request.session['finalReservaHora'] = finalReserva.hour
                request.session['finalReservaMinuto'] = finalReserva.minute
                request.session['inicioReservaHora'] = inicioReserva.hour
                request.session['inicioReservaMinuto'] = inicioReserva.minute
                request.session['anioinicial']=inicioReserva.year
                request.session['mesinicial']=inicioReserva.month
                request.session['diainicial']=inicioReserva.day
                request.session['aniofinal']=finalReserva.year
                request.session['mesfinal']=finalReserva.month
                request.session['diafinal']=finalReserva.day
        
                return render(request, 'estacionamientoPagarReserva.html', {'id': _id,'monto': monto,'reserva': reservaFinal,'color':'green', 'mensaje':'Existe un puesto disponible'})
            else:
                # Cambiar mensaje
                return render(request, 'templateMensaje.html', {'color':'red', 'mensaje':'No hay un puesto disponible para ese horario'})

    return render(request, 'estacionamientoReserva.html', {'form': form, 'estacionamiento': estacionamiento})

def estacionamiento_pago(request,_id):
    form = PagoTarjetaDeCredito()
    if request.method == 'POST':
        form = PagoTarjetaDeCredito(request.POST)
        if form.is_valid():
            try:
                estacionamiento = Estacionamiento.objects.get(id = _id)
            except ObjectDoesNotExist:
                return render(request, '404.html')
            inicioReserva = datetime.datetime(year=request.session['anioinicial'], month=request.session['mesinicial'], day=request.session['diainicial'], hour = request.session['inicioReservaHora'],
                                        minute = request.session['inicioReservaMinuto']
                                    )
            finalReserva  = datetime.datetime(year=request.session['aniofinal'], month=request.session['mesfinal'], day=request.session['diafinal'], hour = request.session['finalReservaHora'],
                                        minute = request.session['finalReservaMinuto']
                                    )

            reservaFinal = Reserva( estacionamiento = estacionamiento,
                                    inicioReserva   = inicioReserva,
                                    finalReserva    = finalReserva)
            monto = Decimal(request.session['monto'])
            reservaFinal.save()
            return render(request,'pago.html',{"id": _id,
                                            "color": "green",
                                            'mensaje' : "Se realizo el pago de reserva satisfactoriamente. Id de pago:" + str(reservaFinal.id)})
    return render(request, 'pago.html', {'form':form})
