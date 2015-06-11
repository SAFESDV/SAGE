# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from transacciones.models import *

admin.site.register(Transaccion)
admin.site.register(TransBilletera)
admin.site.register(TransTDC)
admin.site.register(TransReser)