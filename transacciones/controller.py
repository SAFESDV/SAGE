# -*- coding: utf-8 -*-

# Archivo con funciones de control para SAGE
from estacionamientos.models import Estacionamiento, DiasFeriadosEscogidos
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from transacciones.models import *
from itertools import chain


def transaccion_monto(_id):
	
	try:
		trans = Transaccion.objects.get(id = _id)
	except:
		raise
	
	monto = Decimal(0.00).quantize(Decimal("1.00"))
	
	detalles = list(chain(
								TransBilletera.objects.filter(transaccion = trans),
								TransTDC.objects.filter(transaccion = trans)							
							))
	
	for det in detalles:
		monto += det.monto
	
	return monto