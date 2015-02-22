# -*- coding: utf-8 -*-
from django.db import models
from math import ceil, floor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from django import forms
from django.core.validators import MinValueValidator

class Estacionamiento(models.Model):
	propietario = models.CharField(max_length = 50, help_text = "Nombre Propio")
	nombre = models.CharField(max_length = 50)
	direccion = models.TextField(max_length = 120)

	telefono1 = models.CharField(blank = True, null = True, max_length = 30)
	telefono2 = models.CharField(blank = True, null = True, max_length = 30)
	telefono3 = models.CharField(blank = True, null = True, max_length = 30)

	email1 = models.EmailField(blank = True, null = True)
	email2 = models.EmailField(blank = True, null = True)

	rif = models.CharField(max_length = 12)

	# Campos para referenciar al esquema de tarifa

	content_type = models.ForeignKey(ContentType, null = True)
	object_id = models.PositiveIntegerField(null = True)
	esquemaTarifa = GenericForeignKey()
	tarifa = models.DecimalField(decimal_places = 2, max_digits = 256, blank = True, null = True)
	apertura = models.TimeField(blank = True, null = True)
	cierre = models.TimeField(blank = True, null = True)
	reservasInicio = models.TimeField(blank = True, null = True)
	reservasCierre = models.TimeField(blank = True, null = True)
	nroPuesto = models.IntegerField(blank = True, null = True)

	def __str__(self):
		return self.nombre+' '+str(self.id)

class Reserva(models.Model):
	estacionamiento = models.ForeignKey(Estacionamiento)
	inicioReserva = models.DateTimeField()
	finalReserva = models.DateTimeField()

	def __str__(self):
		return self.estacionamiento.nombre+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+')'

class EsquemaTarifario(models.Model):

	# No se cuantos digitos deberiamos poner
	tarifa = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		abstract = True
	def __str__(self):
		return str(self.tarifa)


class TarifaHora(EsquemaTarifario):

	def calcularPrecio(self,horaInicio,horaFinal):
		a=horaFinal-horaInicio
		a=a.days*24+a.seconds/3600
		a=ceil(a) #  De las horas se calcula el techo de ellas
		return(Decimal(self.tarifa*a).quantize(Decimal('1.00')))
	def  tipo(self):
		return("Por Hora")
	def formCampos(self):
		return [(forms.DecimalField(required = True, initial=0, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))]),True,{'class':'form-control', 'placeholder':'Tarifa'},'0')]

class TarifaMinuto(EsquemaTarifario):

	def calcularPrecio(self,horaInicio,horaFinal):
		minutes = horaFinal-horaInicio
		minutes = minutes.days*24*60+minutes.seconds/60
		return (Decimal(minutes)*Decimal(self.tarifa/60)).quantize(Decimal('1.00'))
	
	def  tipo(self):
		return("Por Minuto")
	def formCampos(self):
		return [(forms.DecimalField(required = True, initial=0, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))]),True,{'class':'form-control', 'placeholder':'Tarifa'},'0')]

class TarifaHorayFraccion(EsquemaTarifario):

	def calcularPrecio(self,horaInicio,horaFinal):
		time = horaFinal-horaInicio
		time = time.days*24*3600+time.seconds
		if(time>3600):
			valor = (floor(time/3600)*self.tarifa)
			if((time%3600)==0):
				pass
			elif((time%3600)>1800):
				valor += self.tarifa
			else:
				valor += self.tarifa/2
		else:
			valor = self.tarifa
		return(Decimal(valor).quantize(Decimal('1.00')))
	
	def  tipo(self):
		return("Por Hora y Fraccion")
	def formCampos(self):
		return [(forms.DecimalField(required = True, initial=0, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))]),True,{'class':'form-control', 'placeholder':'Tarifa'},'0')]
	
class TarifaHorayPicos(EsquemaTarifario):

	def calcularPrecio(self,horaInicio,horaFinal):
		
		return(Decimal('1'))
	
	def  tipo(self):
		return("Por Horas Pico")
	def formCampos(self):
		return [(forms.DecimalField(required = True, initial=0, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))]),True,{'class':'form-control', 'placeholder':'TarifaNoPico'},'0'),\
			(forms.DecimalField(required = True, initial=0, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))]),True,{'class':'form-control', 'placeholder':'TarifaPico'},'0'),\
			(forms.TimeField(required = True, initial="00:01",label = 'Horario Apertura'),True,{'class':'form-control', 'placeholder':'HorarioPicoInic'},"'00:00'"),\
			(forms.TimeField(required = True, initial="00:01", label = 'Horario Apertura'),True,{'class':'form-control', 'placeholder':'HorarioPicoFin'},"'00:00'")]
