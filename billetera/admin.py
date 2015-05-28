# -*- coding: utf-8 -*-
from django.contrib import admin
from billetera.models import (
    BilleteraElectronica,
    PagoRecargaBilletera,
)

admin.site.register(BilleteraElectronica)
admin.site.register(PagoRecargaBilletera)