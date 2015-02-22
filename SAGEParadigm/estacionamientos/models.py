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
	tarifa = models.CharField(blank = True, null = True, max_length = 255)
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
	#estandar para creacion de tarifas:
	#1 - anhada los atributos que requiera la nueva clase
	#2 - metodo calcular precio: calcula el monto a pagar dado una fecha de inicio y una final, ademas de los atributos de la clase
	#3 - metodo tipo: retorne el nombre de la clase que se mostrara al usuario
	#4 - metodo formCampos: retorna una lista de 4tuplas o 3tuplas, cada una de ellas, el primer elemento es un field de form que se usara para el form, el segundo es un booleanno que indica si se quiere especificar un widget, el tercero el es un diccionario con los widget, y el cuarto es lo que debe tner el campo por default, de ser falso el booleano no se xoloca el diccionario y el default va de tercero
	#5 - metodo fcampos; retorna la cantidad de tuplas que contiene el metodo anterior, para no tener que contar a cada rato, aumenta eficiencia
	#6 - metodo create: este metodo recibe una lista con los elementos retornados del form en el mismo orden que se puesieron en el metodo formCampos, debe retornar el objeto tarifa creado

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
	def fcampos(self):
		return 1
	def create(self, input):
		return TarifaHora(tarifa = input[0])
	def tarifString(self):
		return (str(self.tarifa)+" Bsf.")

class TarifaMinuto(EsquemaTarifario):

	def calcularPrecio(self,horaInicio,horaFinal):
		minutes = horaFinal-horaInicio
		minutes = minutes.days*24*60+minutes.seconds/60
		return (Decimal(minutes)*Decimal(self.tarifa/60)).quantize(Decimal('1.00'))
	
	def  tipo(self):
		return("Por Minuto")
	def formCampos(self):
		return [(forms.DecimalField(required = True, initial=0, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))]),True,{'class':'form-control', 'placeholder':'Tarifa'},'0')]
	def fcampos(self):
		return 1
	def create(self, input):
		return TarifaMinuto(tarifa = input[0])
	def tarifString(self):
		return (str(self.tarifa)+" Bsf.")

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
	def fcampos(self):
		return 1
	def create(self, input):
		return TarifaHorayFraccion(tarifa = input[0])
	def tarifString(self):
		return (str(self.tarifa)+" Bsf.")
	
class TarifaHorayPicos(EsquemaTarifario):
	#se usa atributo heredado tarifa para la tarifa de la hora no pico
	tarifaPico = models.DecimalField(max_digits=10, decimal_places=2)
	inicPico = models.TimeField(blank = True, null = True)
	finPico = models.TimeField(blank = True, null = True)

	def calcularPrecio(self,horaInicio,horaFinal):
		
		return(Decimal('1'))
	
	def  tipo(self):
		return("Por Horas Pico")
	def formCampos(self):
		return [(forms.DecimalField(required = True, initial=0, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))]),True,{'class':'form-control', 'placeholder':'TarifaNoPico'},'0'),\
			(forms.DecimalField(required = True, initial=0, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0'))]),True,{'class':'form-control', 'placeholder':'TarifaPico'},'0'),\
			(forms.TimeField(required = True, initial="00:01",label = 'Horario Apertura'),True,{'class':'form-control', 'placeholder':'HorarioPicoInic'},"'00:00'"),\
			(forms.TimeField(required = True, initial="00:01", label = 'Horario Apertura'),True,{'class':'form-control', 'placeholder':'HorarioPicoFin'},"'00:00'")]
	def fcampos(self):
		return 4
	def create(self, input):
		return TarifaHorayPicos(tarifa = input[0], tarifaPico = input[1],inicPico = input[2], finPico = input[3])
	def tarifString(self):
		return ("Pico: "+str(self.tarifaPico)+" Bsf. - Normal: "+str(self.tarifa)+" Bsf. - Horario pico: ("+str(self.inicPico)+","+str(self.finPico)+")")