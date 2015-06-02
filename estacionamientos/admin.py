# -*- coding: utf-8 -*-
from django.contrib import admin
from estacionamientos.models import Estacionamiento, TarifaMinuto,\
    TarifaHorayFraccion, TarifaHora

admin.site.register(Estacionamiento)
admin.site.register(TarifaHora)
admin.site.register(TarifaMinuto)
admin.site.register(TarifaHorayFraccion)