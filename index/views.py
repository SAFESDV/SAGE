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

from django.template.context_processors import request
from django.forms.forms import Form

# Create your views here.


def index_page(request):
    
    if request.method == 'GET':
        pass
        
    elif request.method == 'POST':
        pass
    
    return render(
    request,
    'index.html',
    {'mensaje' : 'No se pueden agregar más estacionamientos'}
    )