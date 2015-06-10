# -*- coding: utf-8 -*-
from django.contrib import admin
from estacionamientos.models import Estacionamiento, TarifaMinuto,\
    TarifaHorayFraccion, TarifaHora, DiasFeriadosEscogidos, EsquemaTarifarioM2M

admin.site.register(Estacionamiento)
admin.site.register(TarifaHora)
admin.site.register(TarifaMinuto)
admin.site.register(TarifaHorayFraccion)
admin.site.register(DiasFeriadosEscogidos)
admin.site.register(EsquemaTarifarioM2M)