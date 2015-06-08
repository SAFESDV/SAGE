# -*- coding: utf-8 -*-
from django.db import models
from math import ceil, floor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from datetime import timedelta
from propietarios.models import Propietario
from _datetime import date, datetime

class Estacionamiento(models.Model):
    
    nombre      = models.CharField(max_length = 50)
    CI_prop     = models.CharField(max_length = 50)
    direccion   = models.TextField(max_length = 120)
    telefono1   = models.CharField(blank = True, null = True, max_length = 30)
    telefono2   = models.CharField(blank = True, null = True, max_length = 30)
    email1      = models.EmailField(blank = True, null = True)
    rif         = models.CharField(max_length = 12)

    # Campos para referenciar al esquema de tarifa

    content_type = models.ForeignKey(ContentType, null = True)
    object_id    = models.PositiveIntegerField(null = True)
    tarifa       = GenericForeignKey()
    apertura     = models.TimeField(blank = True, null = True)
    cierre       = models.TimeField(blank = True, null = True)
    capacidad    = models.IntegerField(blank = True, null = True)

    def __str__(self):
        return self.nombre+' '+str(self.id)

    
class ConfiguracionSMS(models.Model):
    estacionamiento = models.ForeignKey(Estacionamiento)
    inicioReserva   = models.DateTimeField()
    finalReserva    = models.DateTimeField()

    def __str__(self):
        return self.estacionamiento.nombre+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+')'
    
class EsquemaTarifario(models.Model):

    # No se cuantos digitos deberiamos poner
    tarifa         = models.DecimalField(max_digits=20, decimal_places=2)
    tarifa2        = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2)
    inicioEspecial = models.TimeField(blank = True, null = True)
    finEspecial    = models.TimeField(blank = True, null = True)
    
    tarifa_feriado         = models.DecimalField(blank = True, null = True, max_digits=20, decimal_places=2)
    tarifa2_feriado        = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2)
    inicioEspecial_feriado = models.TimeField(blank = True, null = True)
    finEspecial_feriado    = models.TimeField(blank = True, null = True)
    

    class Meta:
        abstract = True
    def __str__(self):
        return str(self.tarifa)


class TarifaHora(EsquemaTarifario):
    
    def calcularPrecio(self,horaInicio,horaFinal):
        
        a = horaFinal-horaInicio
        a = a.days*24+a.seconds/3600
        a = ceil(a) #  De las horas se calcula el techo de ellas
        
        return(Decimal(self.tarifa*a).quantize(Decimal('1.00')))
    
    def tipo(self):
        
        return("Por Hora")

class TarifaMinuto(EsquemaTarifario):
    
    def calcularPrecio(self,horaInicio,horaFinal):
        
        minutes = horaFinal-horaInicio
        minutes = minutes.days*24*60+minutes.seconds/60
        
        return (Decimal(minutes)*Decimal(self.tarifa/60)).quantize(Decimal('1.00'))
    
    def tipo(self):
        return("Por Minuto")

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

    def tipo(self):
        return("Por Hora y Fraccion")

class TarifaFinDeSemana(EsquemaTarifario):
    
    def calcularPrecio(self,inicio,final):
        
        minutosNormales    = 0
        minutosFinDeSemana = 0
        tiempoActual       = inicio
        minuto             = timedelta(minutes=1)
        
        while tiempoActual < final:
            # weekday() devuelve un numero del 0 al 6 tal que
            # 0 = Lunes
            # 1 = Martes
            # ..
            # 5 = Sabado
            # 6 = Domingo
            if tiempoActual.weekday() < 5:
                minutosNormales += 1
            else:
                minutosFinDeSemana += 1
            tiempoActual += minuto
            
        return Decimal(
            minutosNormales*self.tarifa/60 +
            minutosFinDeSemana*self.tarifa2/60
        ).quantize(Decimal('1.00'))

    def tipo(self):
        return("Tarifa diferenciada para fines de semana")

class TarifaHoraPico(EsquemaTarifario):
    
    def calcularPrecio(self,reservaInicio,reservaFinal):
        minutosPico  = 0
        minutosValle = 0
        tiempoActual = reservaInicio
        minuto       = timedelta(minutes=1)
        
        while tiempoActual < reservaFinal:
            horaActual = tiempoActual.time()
            
            if horaActual >= self.inicioEspecial and horaActual < self.finEspecial:
                minutosPico += 1
            elif horaActual < self.inicioEspecial or horaActual >= self.finEspecial:
                minutosValle += 1
            tiempoActual += minuto
            
        return Decimal(
            minutosPico*self.tarifa2/60 +
            minutosValle*self.tarifa/60
        ).quantize(Decimal('1.00'))

    def tipo(self):
        return("Tarifa diferenciada por hora pico")
        
    
class DiasFeriados(models.Model): #capaz la usamos!!!! xD
    
    fecha   = models.DateTimeField(primary_key = True)
    descripcion = models.CharField(max_length = 50, primary_key = True)
    
    def rellenarDiasFeriados(self):
        
        diasFeriados = [ [datetime(year=  datetime.now().year, month = 1, day = 1), 'Año Nuevo'], 
                                            [datetime(year=  datetime.now().year, month = 4, day = 19), 'Declaración de la Independecia' ], 
                                            [datetime(year=  datetime.now().year, month = 5, day  = 1), 'Día del trabajo' ], 
                                            [datetime(year=  datetime.now().year, month = 6, day  = 24), 'Batalla de Carabobo' ], 
                                            [datetime(year=  datetime.now().year, month = 7, day  = 5 ), 'Día de la independecia' ], 
                                            [datetime(year=  datetime.now().year, month = 7, day  = 24 ), 'Natalicio de Simón Bolívar ' ],
                                            [datetime(year=  datetime.now().year, month = 10, day  = 12  ), 'Día de la resistencia indígena' ], 
                                            [datetime(year=  datetime.now().year, month = 12, day  = 25 ), 'Navidad' ],
                                            [datetime(year=  datetime.now().year, month = 12, day  = 31 ), 'Fin de Año'  ]]
        
        for elem in diasFeriados:
            dia = DiasFeriados(elem[0], elem[1])
            dia.save()
             
    
class DiasFeriadosEscogidos(models.Model):
    
    fecha   = models.DateTimeField()
    descripcion = models.CharField(max_length = 50)    
    estacionamiento = models.ForeignKey(Estacionamiento) 
    
    def __str__(self):
        return ' ('+str(self.fecha)+','+str(self.descripcion)+')'
