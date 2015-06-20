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

from datetime import datetime, date, timedelta

from reservas.controller import (
    validarHorarioReserva,
    marzullo,
    calcular_Precio_Reserva,
)

from estacionamientos.controller import (
    HorarioEstacionamiento,
    get_client_ip,
    tasa_reservaciones,
    calcular_porcentaje_de_tasa,
    consultar_ingresos,
    seleccionar_feriados,
    seleccionar_feriado_extra,
    limpiarEsquemasTarifarios
)

from billetera.forms import (
    BilleteraElectronicaForm,                          
)

from estacionamientos.forms import (
    EstacionamientoExtendedForm,
    EstacionamientoForm,
    EditarEstacionamientoForm,
    RifForm,
    CedulaForm,
    ElegirFechaForm,
    AgregarFeriadoForm,
)

from reservas.forms import (
    ReservaForm,
    CancelarReservaForm,
    PagoForm,
)

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

from propietarios.models import Propietario
from reservas.models import *

from django.template.context_processors import request
from django.forms.forms import Form
from unittest.case import _id
from transacciones.models import *

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
            return render(
                request, 
                'catalogo-estacionamientos.html',
                {'color'   : 'red'
                , 'mensaje' : 'No se pueden agregar más estacionamientos'
                }
            )

        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            
            try:
                propietario = Propietario.objects.get(
                    Cedula = form.cleaned_data['CI_prop'],
                    cedulaTipo = form.cleaned_data['cedulaTipo']
                )
            except ObjectDoesNotExist:
                return render(
                        request,
                        'catalogo-estacionamientos.html',
                        { "form"    : form
                        , 'estacionamientos': estacionamientos
                        , "color"   : "red"
                        ,'mensaje'  : "La cédula ingresada no esta asociada a ningún usuario."
                        }
                    )
            
              
            obj = Estacionamiento(
                nombre      = form.cleaned_data['nombre'],
                CI_prop     = form.cleaned_data['CI_prop'],
                cedulaTipo  = form.cleaned_data['cedulaTipo'],
                direccion   = form.cleaned_data['direccion'],
                rif         = form.cleaned_data['rif'],
                telefono1   = form.cleaned_data['telefono_1'],
                telefono2   = form.cleaned_data['telefono_2'],
                email1      = form.cleaned_data['email_1']
            )
            obj.save()
                     
            # Recargamos los estacionamientos ya que acabamos de agregar
            estacionamientos = Estacionamiento.objects.all()
            form = EstacionamientoForm()

    return render(
        request,
        'catalogo-estacionamientos.html',
        { 'form': form
        , 'estacionamientos': estacionamientos
        }
    )

def estacionamiento_detail(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'GET':
        estacionamientotarifa = EsquemaTarifarioM2M.objects.filter( estacionamiento = _id )
        
        if len(estacionamientotarifa) == 2:
            esquema_no_feriado = estacionamientotarifa[0]
            esquema_feriado = estacionamientotarifa[1]   
            
            if esquema_no_feriado and esquema_feriado:
                form_data = {
                    'horarioin' : estacionamiento.apertura,
                    'horarioout' : estacionamiento.cierre,
                    'tarifa' : esquema_no_feriado.tarifa.tarifa,
                    'tarifa2' : esquema_no_feriado.tarifa.tarifa2,
                    'inicioTarifa2' : esquema_no_feriado.tarifa.inicioEspecial,
                    'finTarifa2' : esquema_no_feriado.tarifa.finEspecial,
                    'tarifaFeriado' : esquema_feriado.tarifa.tarifa,
                    'tarifaFeriado2' : esquema_feriado.tarifa.tarifa2,
                    'inicioTarifaFeriado2' :esquema_feriado.tarifa.inicioEspecial,
                    'finTarifaFeriado2' : esquema_feriado.tarifa.finEspecial,
                    'puestosLivianos' : estacionamiento.capacidadLivianos,
                    'puestosPesados' : estacionamiento.capacidadPesados,
                    'puestosMotos' : estacionamiento.capacidadMotos,
                    'puestosDiscapacitados' : estacionamiento.capacidadDiscapacitados,
                    'esquema' : esquema_no_feriado.tarifa.__class__.__name__,
                    'esquemaFeriado': esquema_feriado.tarifa.__class__.__name__,
                    'horizonte' : estacionamiento.horizonte
                }
                form = EstacionamientoExtendedForm(data = form_data)
                
        else:
             form = EstacionamientoExtendedForm()
             esquema_no_feriado = None
             esquema_feriado = None
    
    elif request.method == 'POST':
        
        limpiarEsquemasTarifarios(_id)
        # Leemos el formulario
        form = EstacionamientoExtendedForm(request.POST)
        # Si el formulario


        if form.is_valid(): 
            horaIn                  = form.cleaned_data['horarioin']
            horaOut                 = form.cleaned_data['horarioout']
            tarifa                  = form.cleaned_data['tarifa']
            tarifa2                 = form.cleaned_data['tarifa2']
            esquema                 = form.cleaned_data['esquema']
            inicioTarifa2           = form.cleaned_data['inicioTarifa2']
            finTarifa2              = form.cleaned_data['finTarifa2']
            tarifaFeriado           = form.cleaned_data['tarifaFeriado']
            tarifaFeriado2          = form.cleaned_data['tarifaFeriado2']
            esquemaFeriado          = form.cleaned_data['esquemaFeriado']
            inicioTarifaFeriado2    = form.cleaned_data['inicioTarifaFeriado2']
            finTarifaFeriado2       = form.cleaned_data['finTarifaFeriado2']
            horizonte               = form.cleaned_data['horizonte']
            
            esquemaTarifa = eval(esquema)(
                tarifa         = tarifa,
                tarifa2     =  tarifa2,
                estacionamiento =  estacionamiento,
                inicioEspecial = inicioTarifa2,
                finEspecial    = finTarifa2,
                tipoDia = 'Dia Normal'
            )
            esquemaTarifa.save()
            
            esquemaTarifaFeriado = eval(esquemaFeriado)(
                tarifa         = tarifaFeriado,
                tarifa2     =  tarifaFeriado2,
                estacionamiento =  estacionamiento,
                inicioEspecial = inicioTarifaFeriado2,
                finEspecial    = finTarifaFeriado2,
                tipoDia = 'Dia Feriado'
            )
            esquemaTarifaFeriado.save()
            
            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            

            
            if not HorarioEstacionamiento(horaIn, horaOut):
                return render(
                    request,
                    'template-mensaje.html',
                    { 'color':'red'
                    , 'mensaje': 'El horario de apertura debe ser menor al horario de cierre'
                    }
                )
                
            # debería funcionar con excepciones
            esquema_no_feriado = EsquemaTarifarioM2M(
                                                     estacionamiento= estacionamiento,
                                                     tarifa = esquemaTarifa
                                                     )
            esquema_no_feriado.save()
            
            esquema_feriado = EsquemaTarifarioM2M(
                                                  estacionamiento= estacionamiento,
                                                  tarifa = esquemaTarifaFeriado
                                                  )
            esquema_feriado.save()
            
            esquema_no_feriado = esquemaTarifa 
            esquema_feriado = esquemaTarifaFeriado

            estacionamiento.apertura  = horaIn
            estacionamiento.cierre    = horaOut
            estacionamiento.capacidadLivianos = form.cleaned_data['puestosLivianos']
            estacionamiento.capacidadPesados = form.cleaned_data['puestosPesados']
            estacionamiento.capacidadMotos = form.cleaned_data['puestosMotos']
            estacionamiento.capacidadDiscapacitados = form.cleaned_data['puestosDiscapacitados']
            estacionamiento.horizonte = horizonte

            if (estacionamiento.capacidadLivianos + estacionamiento.capacidadPesados + estacionamiento.capacidadMotos + estacionamiento.capacidadDiscapacitados <= 0):
                return render(
                    request,
                    'template-mensaje.html',
                    { 'color':'red'
                    , 'mensaje': 'El estacionamiento debe tener al menos un puesto'
                    }
                )

            estacionamiento.save()
            form = EstacionamientoExtendedForm()
            
        else:
            esquema_no_feriado = None
            esquema_feriado = None
                
    return render(
        request,
        'detalle-estacionamiento.html',
        { 'form': form
        , 'estacionamiento' : estacionamiento
        , 'esquema_no_feriado' : esquema_no_feriado
        , 'esquema_feriado' : esquema_feriado
        }
    )
    
def estacionamiento_editar(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'GET':
        
        
        
        if estacionamiento.CI_prop:
            
            form_data = {
                'CI_prop' : estacionamiento.CI_prop,
                'cedulaTipo' : estacionamiento.cedulaTipo
                }
            form = EditarEstacionamientoForm(data = form_data)
        else:
            form = EditarEstacionamientoForm()

    elif request.method == 'POST':
        # Leemos el formulario
        form = EditarEstacionamientoForm(request.POST)
        
        # Si el formulario
        if form.is_valid():
            
            try:
                propietario = Propietario.objects.get(Cedula = form.cleaned_data['CI_prop'],
                                                      cedulaTipo = form.cleaned_data['cedulaTipo'])
            except ObjectDoesNotExist:
                return render(
                        request,
                        'editar-datos-estacionamiento.html',
                        { "form"    : form
                        , 'estacionamiento': estacionamiento
                        , "color"   : "red"
                        ,'mensaje'  : "La cédula ingresada no esta asociada a ningún usuario."
                        }
                    )
                
            estacionamiento.CI_prop = form.cleaned_data['CI_prop']
            estacionamiento.cedulaTipo = form.cleaned_data['cedulaTipo']
                                               
            estacionamiento.save()
                                         
            # Recargamos los estacionamientos ya que acabamos de agregar
            form = EditarEstacionamientoForm()

    return render(
        request,
        'editar-datos-estacionamiento.html',
        { 'form': form
        , 'estacionamiento': estacionamiento
        }
    )

    # Verificamos que el estacionamiento este parametrizado
    if (estacionamiento.apertura is None):
        return HttpResponse(status = 403) # Esta prohibido entrar aun

    # Si se hace un GET renderizamos los estacionamientos con su formulario
    if request.method == 'GET':
        form = ReservaForm()

    # Si es un POST estan mandando un request
    elif request.method == 'POST':
        form = ReservaForm(request.POST)
        # Verificamos si es valido con los validadores del formulario
        if form.is_valid():
         
            inicioReserva = form.cleaned_data['inicio']
            finalReserva = form.cleaned_data['final']
            tipo_vehiculo_tomado = form.cleaned_data['tipo_vehiculo']
            tipo_vehiculo_tomado = str(tipo_vehiculo_tomado)
            
            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            
            
            m_validado = validarHorarioReserva(
                inicioReserva,
                finalReserva,
                estacionamiento.apertura,
                estacionamiento.cierre,
                estacionamiento.horizonte,
            )

            # Si no es valido devolvemos el request
            if not m_validado[0]:
                return render(
                    request,
                    'template-mensaje.html',
                    { 'color'  :'red'
                    , 'mensaje': m_validado[1]
                    }
                )

            if marzullo(_id, inicioReserva, finalReserva, tipo_vehiculo_tomado):
                print("funciono marzullo!")
                reservaFinal = Reserva(
                    estacionamiento = estacionamiento,
                    inicioReserva   = inicioReserva,
                    finalReserva    = finalReserva,
                    estado          = 'Válido',
                    tipo_vehiculo   = tipo_vehiculo_tomado
                )

                monto = Decimal(
                    estacionamiento.tarifa.calcularPrecio(
                        inicioReserva,finalReserva
                    )
                )

                request.session['monto'] = float(
                    estacionamiento.tarifa.calcularPrecio(
                        inicioReserva,
                        finalReserva
                    )
                )
                
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
                request.session['tipo_vehiculo']       = tipo_vehiculo_tomado
                return render(
                    request,
                    'confirmar.html',
                    { 'id'      : _id
                    , 'monto'   : monto
                    , 'reserva' : reservaFinal
                    , 'color'   : 'green'
                    , 'mensaje' : 'Existe un puesto disponible'
                    }
                )
            else:
                # Cambiar mensaje
                return render(
                    request,
                    'template-mensaje.html',
                    {'color'   : 'red'
                    , 'mensaje' : 'No hay un puesto disponible para ese horario'
                    }
                )
    
    print(esquema_no_feriado)
    
    return render(
        request,
        'reserva.html',
        { 'form': form
        , 'estacionamiento': estacionamiento
        , 'esquema_no_feriado' : esquema_no_feriado
        , 'esquema_feriado' : esquema_feriado
        }
    )

def estacionamiento_pago(request,_id):
    form = PagoForm()
    
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    
    if (estacionamiento.apertura is None):
        return HttpResponse(status = 403) # No esta permitido acceder a esta vista aun
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            
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
                nombre          = request.session['nombre'],
                apellido        = request.session['apellido'],
                cedula          = request.session['cedula'],
                cedulaTipo      = request.session['cedulaTipo'],
                estacionamiento = estacionamiento,
                inicioReserva   = inicioReserva,
                finalReserva    = finalReserva,
                estado          = 'Válido',
                tipo_vehiculo   = request.session['tipo_vehiculo']
            )

            # Se guarda la reserva en la base de datos
            
            reservaFinal.save()

            monto = float(request.session['monto'])
            monto = Decimal(monto).quantize(Decimal('1.00'))
            #monto = Decimal(request.session['monto']).quantize("1.00")
            
            trans = Transaccion(
                fecha = datetime.now(),
                tipo = 'Reserva',
                estado     = 'Válido',
                monto = monto
            )
            
            trans.save()
            
            transTdc = TransTDC(
                nombre           = form.cleaned_data['nombre'],
                cedulaTipo       = form.cleaned_data['cedulaTipo'],
                cedula           = form.cleaned_data['cedula'],
                tarjetaTipo      = form.cleaned_data['tarjetaTipo'],
                tarjeta          = form.cleaned_data['tarjeta'][-4:],
                monto            = monto,
                transaccion      = trans
            )
            
            transTdc.save()
            
            transReser = TransReser(
                transaccion = trans,
                reserva = reservaFinal
            )
            
            transReser.save()
            

            return render(
                request,
                'pago.html',
                { "id"      : _id
                , "pago"    : transReser
                , "pago2"   : transTdc
                , "color"   : "green"
                , 'mensaje' : "Se realizo el pago de reserva satisfactoriamente."
            
                }
                          
            )
    return render(
        request,
        'pago.html',
        { 'form' : form }
    )

def estacionamiento_modo_pago(request, _id):    
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    
    if (estacionamiento.apertura is None):
        return HttpResponse(status = 403) # No esta permitido acceder a esta vista aun
    
    return render(
        request,
        'ModoPago.html'
    )

def estacionamiento_reserva(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento_selec = Estacionamiento.objects.get(id = _id)
        diasFeriados = DiasFeriadosEscogidos.objects.filter(estacionamiento = estacionamiento_selec)
    except ObjectDoesNotExist:
        raise Http404

    estacionamientotarifa = EsquemaTarifarioM2M.objects.filter( estacionamiento = estacionamiento_selec )
    
    esquema_no_feriado = None
    esquema_feriado = None
    
    if (len(estacionamientotarifa) == 2):
    
        esquema_no_feriado = estacionamientotarifa[0]
        esquema_feriado = estacionamientotarifa[1]

    # Verificamos que el estacionamiento este parametrizado
    if (estacionamiento_selec.apertura is None):
        return HttpResponse(status = 403) # Esta prohibido entrar aun

    # Si se hace un GET renderizamos los estacionamientos con su formulario
    if request.method == 'GET':
        form = ReservaForm()

    # Si es un POST estan mandando un request
    elif request.method == 'POST':
        form = ReservaForm(request.POST)
        # Verificamos si es valido con los validadores del formulario
        if form.is_valid():

            inicioReserva = form.cleaned_data['inicio']
            finalReserva = form.cleaned_data['final']
            tipo_vehiculo_tomado = form.cleaned_data['tipo_vehiculo']
            tipo_vehiculo_tomado = str(tipo_vehiculo_tomado)

            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            m_validado = validarHorarioReserva(
                inicioReserva,
                finalReserva,
                estacionamiento_selec.apertura,
                estacionamiento_selec.cierre,
                estacionamiento_selec.horizonte
            )

            # Si no es valido devolvemos el request
            if not m_validado[0]:
                return render(
                    request,
                    'template-mensaje.html',
                    { 'color'  :'red'
                    , 'mensaje': m_validado[1]
                    }
                )

            if marzullo(_id, inicioReserva, finalReserva, tipo_vehiculo_tomado):
                reservaFinal = Reserva(
                    estacionamiento = estacionamiento_selec,
                    inicioReserva   = inicioReserva,
                    finalReserva    = finalReserva,
                    estado          = 'Válido',
                    tipo_vehiculo = tipo_vehiculo_tomado
                )
            
                montoTotal = calcular_Precio_Reserva(reservaFinal,diasFeriados)
                request.session['monto'] = float(montoTotal)
                    
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
                request.session['tipo_vehiculo']       = tipo_vehiculo_tomado
                request.session['nombre']              = form.cleaned_data['nombre']
                request.session['apellido']            = form.cleaned_data['apellido']
                request.session['cedula']              = form.cleaned_data['cedula']
                request.session['cedulaTipo']          = form.cleaned_data['cedulaTipo']
                request.session['tipo_vehiculo']       = form.cleaned_data['tipo_vehiculo']
                
                return render(
                    request,
                    'confirmar.html',
                    { 'id'      : _id
                    , 'monto'   : montoTotal
                    , 'reserva' : reservaFinal
                    , 'color'   : 'green'
                    , 'mensaje' : 'Existe un puesto disponible'
                    }
                )
            else:
                # Cambiar mensaje
                return render(
                    request,
                    'template-mensaje.html',
                    {'color'   : 'red'
                    , 'mensaje' : 'No hay un puesto disponible para ese horario'
                    }
                )

    return render(
        request,
        'reserva.html',
        { 'form': form
        , 'estacionamiento': estacionamiento_selec
        , 'esquema_no_feriado' : esquema_no_feriado
        , 'esquema_feriado' : esquema_feriado
        }
    )

def estacionamiento_ingreso(request):
    form = RifForm()
    
    if request.method == 'POST':
        form = RifForm(request.POST)
        if form.is_valid():

            _rif = form.cleaned_data['rif']
            
            try:
                estacionamiento_selec = Estacionamiento.objects.get(rif = _rif)
                
            except ObjectDoesNotExist:
                return render(
                        request,
                        'consultar-ingreso.html',
                        { "form"    : form
                        , "color"   : "red"
                        ,'mensaje'  : "No hay estacionamiento registrado bajo el rif escogido"
                        }
                    )  
                  
            listaIngresos, ingresoTotal,listaTransacciones = consultar_ingresos(_rif)

            return render(
                request,
                'consultar-ingreso.html',
                { "estacionamiento" : estacionamiento_selec
                ,  "ingresoTotal"    : ingresoTotal
                , "listaIngresos"   : listaIngresos
                , "listaTransacciones" : listaTransacciones
                , "form"            : form
                }
            )

    return render(
        request,
        'consultar-ingreso.html',
        { "form" : form }
    )
    
def estacionamiento_consulta_reserva(request):
    form = CedulaForm()
    if request.method == 'POST':
        form = CedulaForm(request.POST)
        if form.is_valid():

            cedula        = form.cleaned_data['cedula']
            facturas      = Reserva.objects.filter(cedula = cedula)
            listaFacturas = []

            listaFacturas = sorted(
                list(facturas),
                key = lambda r: r.inicioReserva
            )
            return render(
                request,
                'consultar-reservas.html',
                { "listaFacturas" : listaFacturas
                , "form"          : form
                }
            )
    return render(
        request,
        'consultar-reservas.html',
        { "form" : form }
    )

def receive_sms(request):
    ip = get_client_ip(request) # Busca el IP del telefono donde esta montado el SMS Gateway
    port = '8000' # Puerto del telefono donde esta montado el SMS Gateway
    phone = request.GET.get('phone', False)
    sms = request.GET.get('text', False)
    if (not sms or not phone):
        return HttpResponse(status=400) # Bad request
    
    phone = urllib.parse.quote(str(phone)) # Codificacion porcentaje del numero de telefono recibido
    
    # Tratamiento del texto recibido
    try:
        sms = sms.split(' ')
        id_sms = int(sms[0])
        inicio_reserva = sms[1] + ' ' + sms[2]
        final_reserva = sms[3] + ' ' + sms[4]
        inicio_reserva = parse_datetime(inicio_reserva)
        final_reserva = parse_datetime(final_reserva)
    except:
        return HttpResponse(status=400) # Bad request
    
    # Validacion del id de estacionamiento recibido por SMS
    try:
        estacionamiento = Estacionamiento.objects.get(id = id_sms)
    except ObjectDoesNotExist:
        text = 'No existe el estacionamiento ' + str(id_sms) + '.'
        text = urllib.parse.quote(str(text))
        urllib.request.urlopen('http://{0}:{1}/sendsms?phone={2}&text={3}&password='.format(ip, port, phone, text))
        return HttpResponse('No existe el estacionamiento ' + str(id_sms) + '.')
    
    # Validacion de las dos fechas recibidas por SMS
    m_validado = validarHorarioReserva(
        inicio_reserva,
        final_reserva,
        estacionamiento.apertura,
        estacionamiento.cierre,
    )
    if m_validado[0]:
        '''reserva_sms = Reserva(
            estacionamiento = estacionamiento,
            inicioReserva   = inicio_reserva,
            finalReserva    = final_reserva,
        )
        reserva_sms.save()'''
        text = 'Se realizó la reserva satisfactoriamente.'
        text = urllib.parse.quote(str(text))
        urllib.request.urlopen('http://{0}:{1}/sendsms?phone={2}&text={3}&password='.format(ip, port, phone, text))
    else:
        text = m_validado[1]
        text = urllib.parse.quote(str(text))
        urllib.request.urlopen('http://{0}:{1}/sendsms?phone={2}&text={3}&password='.format(ip, port, phone, text))
        return HttpResponse(m_validado[1])
    
    return HttpResponse('')
    
def tasa_de_reservacionDiscapacitados(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    if (estacionamiento.apertura is None):
        return render(
            request, 'template-mensaje.html',
            { 'color'   : 'red'
            , 'mensaje' : 'Se debe parametrizar el estacionamiento primero.'
            }
        )
    ocupacionDiscapacitados = tasa_reservaciones(_id,'Discapacitados')
    calcular_porcentaje_de_tasa(estacionamiento.apertura, estacionamiento.cierre,
                                estacionamiento.capacidadDiscapacitados,
                                ocupacionDiscapacitados)
    datos_ocupacionDiscapacitados = urlencode(ocupacionDiscapacitados)
    
    return render(
        request,
        'tasa-reservacion-discapacitados.html',
        { "ocupacionDiscapacitados" : ocupacionDiscapacitados
        , "datos_ocupacionDiscapacitados": datos_ocupacionDiscapacitados
        }
    )
    
def tasa_de_reservacionLivianos(request, _id):
    _id = int(_id)
        # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    if (estacionamiento.apertura is None):
        return render(
            request, 'template-mensaje.html',
            { 'color'   : 'red'
            , 'mensaje' : 'Se debe parametrizar el estacionamiento primero.'
            }
        )
    ocupacionLivianos = tasa_reservaciones(_id,'Liviano')
    calcular_porcentaje_de_tasa(estacionamiento.apertura, estacionamiento.cierre,
                                estacionamiento.capacidadLivianos,
                                ocupacionLivianos)
    datos_ocupacionLivianos = urlencode(ocupacionLivianos) # Se convierten los datos del diccionario en el formato key1=value1&key2=value2&...
        
    return render(
        request,
        'tasa-reservacion.html',
        { "ocupacionLivianos" : ocupacionLivianos
        , "datos_ocupacionLivianos": datos_ocupacionLivianos
        }
    )
       
def tasa_de_reservacionPesados(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    if (estacionamiento.apertura is None):
        return render(
            request, 'template-mensaje.html',
            { 'color'   : 'red'
            , 'mensaje' : 'Se debe parametrizar el estacionamiento primero.'
            }
        )
    ocupacionPesados = tasa_reservaciones(_id,'Pesado')
    calcular_porcentaje_de_tasa(estacionamiento.apertura, estacionamiento.cierre,
                                estacionamiento.capacidadPesados,
                                ocupacionPesados)
    datos_ocupacionPesados = urlencode(ocupacionPesados)
    return render(
        request,
        'tasa-reservacion-pesados.html',
        { "ocupacionPesados" : ocupacionPesados
        , "datos_ocupacionPesados": datos_ocupacionPesados
        }
        )
        
def tasa_de_reservacionMotos(request, _id):
    _id = int(_id)
        # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    if (estacionamiento.apertura is None):
        return render(
            request, 'template-mensaje.html',
            { 'color'   : 'red'
            , 'mensaje' : 'Se debe parametrizar el estacionamiento primero.'
            }
        )
    ocupacionMotos = tasa_reservaciones(_id,'Moto')
    calcular_porcentaje_de_tasa(estacionamiento.apertura, estacionamiento.cierre,
                                estacionamiento.capacidadMotos,
                                ocupacionMotos)

    datos_ocupacionMotos = urlencode(ocupacionMotos)
       
    return render(
        request,
        'tasa-reservacion-motos.html',
        { "ocupacionMotos" : ocupacionMotos
        , "datos_ocupacionMotos": datos_ocupacionMotos
        }
    )

def grafica_tasa_de_reservacion(request):
    
    # Recuperacion del diccionario para crear el grafico
    try:
        datos_ocupacionLivianos = request.GET.dict()
        datos_ocupacionLivianos = OrderedDict(sorted((k, float(v)) for k, v in datos_ocupacionLivianos.items()))
        response = HttpResponse(content_type='image/png')
    except:
        return HttpResponse(status=400) # Bad request
    
    # Si el request no viene con algun diccionario
    if (not datos_ocupacionLivianos):
        return HttpResponse(status=400) # Bad request
    
    # Configuracion y creacion del grafico de barras con la biblioteca pyplot
    pyplot.switch_backend('Agg') # Para que no use Tk y aparezcan problemas con hilos
    pyplot.bar(range(len(datos_ocupacionLivianos)), datos_ocupacionLivianos.values(), hold = False, color = '#6495ed')
    pyplot.ylim([0,100])
    pyplot.title('Distribución de los porcentajes por fecha')
    pyplot.ylabel('Porcentaje (%)')
    pyplot.grid(True, 'major', 'both')
    pyplot.savefig(response, format='png') # Guarda la imagen creada en el HttpResponse creado
    pyplot.close()
    
    return response

def Estacionamiento_Dias_Feriados(request, _id):
    
    _id = int(_id)
    
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
        DiasFeriados = DiasFeriadosEscogidos.objects.all()
    except ObjectDoesNotExist:
        raise Http404

    # Si es un GET, mandamos un formulario vacio
    if request.method == 'GET':
         form = ElegirFechaForm()

    # Si es POST, se verifica la información recibida
    elif request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form =  ElegirFechaForm(request.POST)
        
        if form.is_valid():
            diaFeriado =  form.cleaned_data['esquema_diasFeriados']
            seleccionar_feriados(diaFeriado, estacionamiento)
        
        # Arle
        return render(
                  request,
                  'dias_feriados.html',
                  { "form" : form 
                   , "color"   : "green"
                   ,'mensaje'  : "Se han actualizado la lista de Fechas Feriadas."
                   }
                )
                    
    return render(
        request,
        'dias_feriados.html',
        { "form" : form 
        }
        )

    # Fin Arle
    
def Estacionamiento_Dia_Feriado_Extra(request, _id):
    
    _id = int(_id)
    
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
        DiasFeriados = DiasFeriadosEscogidos.objects.all()
    except ObjectDoesNotExist:
        raise Http404

    # Si es un GET, mandamos un formulario vacio
    if request.method == 'GET':
         form = AgregarFeriadoForm()

    # Si es POST, se verifica la información recibida
    elif request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form =  AgregarFeriadoForm(request.POST)
        
        if form.is_valid():
            diaFecha =  form.cleaned_data['fecha']
            diaDescripcion =  form.cleaned_data['descripcion']
            seleccionar_feriado_extra(diaFecha, diaDescripcion, estacionamiento)
        
    # Arle  
        return render(
            request,
            'dia_feriado_extra.html',
            { "form" : form 
            , "color"   : "green"
            ,'mensaje'  : "Se han actualizado la lista de Fechas Feriadas."
            }
          )
        
    return render(

                request,
                'dia_feriado_extra.html',
                { "form" : form }
                )
    
    # Fin Arle
def Mostrar_Dias_Feriados(request, _id):
    
    _id = int(_id)
    
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
        DiasFeriados = DiasFeriadosEscogidos.objects.all()
    except ObjectDoesNotExist:
        raise Http404
    
    Comprobacion = "false"
    
    for dia in DiasFeriados:
        if(dia.estacionamiento == estacionamiento):
            Comprobacion = "true"
            break


    print(DiasFeriados)
    return render(
                request,
                'catalogo_dias_feriados.html',
                {"estacionamientos": estacionamiento
                ,"DiasFeriados" : DiasFeriados
                , "Comprobacion" : Comprobacion
                }
            )

