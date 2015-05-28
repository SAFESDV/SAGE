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

from datetime import (
    datetime,
)

from propietarios.forms import PropietarioForm

from propietarios.models import Propietario

def PropietarioAll(request):
    Propietarios = Propietario.objects.all()
    # Si es un GET, mandamos un formulario vacio
    if request.method == 'GET':
        form = PropietarioForm()    
    elif request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form = PropietarioForm(request.POST)
        
        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
                  
            obj = Propietario(
                nomb_prop   = form.cleaned_data['nomb_prop'],
                Cedula      = form.cleaned_data['Cedula'],
                telefono3   = form.cleaned_data['telefono_prop'],
                email2      = form.cleaned_data['email_prop'],
            )
            obj.save()
                                 
            # Recargamos los propietarios ya que acabamos de agregar
            Propietarios = Propietario.objects.all()
            form = PropietarioForm()

    return render(
        request,
        'catalogo-propietario.html',
        { 'form': form
        , 'Propietarios': Propietarios
        }
    )
    
def propietario_editar(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        propietario = Propietario.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'GET':
        if propietario.Cedula:
            
            form_data = {
                'nomb_prop' : propietario.nomb_prop,
                'Cedula' : propietario.Cedula,
                'telefono_prop' : propietario.telefono3,
                'email_prop' : propietario.email2
            }
            form = PropietarioForm(data = form_data)
        else:
            form = PropietarioForm()

    elif request.method == 'POST':
        # Leemos el formulario
        form = PropietarioForm(request.POST)
        
        # Si el formulario
        if form.is_valid():
            propietario.nomb_prop = form.cleaned_data['nomb_prop']
            propietario.Cedula = form.cleaned_data['Cedula']
            propietario.telefono3 = form.cleaned_data['telefono_prop']
            propietario.email2 = form.cleaned_data['email_prop']
                                               
            propietario.save()
                                         
            # Recargamos los estacionamientos ya que acabamos de agregar
            form = PropietarioForm()

    return render(
        request,
        'editar-datos-propietario.html',
        { 'form': form
        , 'propietario': propietario
        }
    )