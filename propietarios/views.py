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