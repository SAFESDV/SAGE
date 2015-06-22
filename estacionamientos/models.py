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
    cedulaTipo  = models.CharField(max_length = 1)
    direccion   = models.TextField(max_length = 120)
    telefono1   = models.CharField(blank = True, null = True, max_length = 30)
    telefono2   = models.CharField(blank = True, null = True, max_length = 30)
    email1      = models.EmailField(blank = True, null = True)
    rif         = models.CharField(max_length = 12)
    horizonte   = models.IntegerField(blank = True, null = True)


    apertura     = models.TimeField(blank = True, null = True)
    cierre       = models.TimeField(blank = True, null = True)
    capacidadLivianos  = models.IntegerField(blank = True, null = True)
    capacidadPesados   = models.IntegerField(blank = True, null = True)
    capacidadMotos     = models.IntegerField(blank = True, null = True)
    capacidadDiscapacitados = models.IntegerField(blank = True, null = True)
    content_type        = models.ForeignKey(ContentType, null = True)
    object_id           = models.PositiveIntegerField(null = True)
    fronteraTarifaria = GenericForeignKey()
    
    def __str__(self):
        return self.nombre+' '+str(self.id)

    
class ConfiguracionSMS(models.Model):
    estacionamiento = models.ForeignKey(Estacionamiento)
    inicioReserva   = models.DateTimeField()
    finalReserva    = models.DateTimeField()

    def __str__(self):
        return self.estacionamiento.nombre+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+')'

class EsquemaTarifarioM2M(models.Model):  
    #Relaciona estacionamiento con el esquema tarifario con estacionamiento (Many to Many)
    
    estacionamiento     = models.ForeignKey(Estacionamiento)
    content_type        = models.ForeignKey(ContentType, null = True)
    object_id           = models.PositiveIntegerField(null = True)
    tarifa              = GenericForeignKey()
        
class EsquemaTarifario(models.Model):

    tarifa              = models.DecimalField(max_digits=20, decimal_places=2)
    tarifaEspecial      = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2)
    inicioEspecial      = models.TimeField(blank = True, null = True)
    finEspecial         = models.TimeField(blank = True, null = True)
    tipoDia             = models.CharField(max_length = 50)
    tipoVehiculo        = models.CharField(max_length = 50)
    
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
            minutosFinDeSemana*self.tarifaEspecial/60
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
            minutosPico*self.tarifaEspecial/60 +
            minutosValle*self.tarifa/60
        ).quantize(Decimal('1.00'))

    def tipo(self):
        return("Tarifa diferenciada por hora pico")
        
class DiasFeriadosEscogidos(models.Model):
    
    fecha   = models.DateTimeField()
    descripcion = models.CharField(max_length = 50)    
    estacionamiento = models.ForeignKey(Estacionamiento) 
    
    def __str__(self):
        return ' ('+str(self.fecha)+')'
    
class FronterasTarifarias(models.Model):  
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return str(self.id)
    
    def porcentajeEsquema(self,inicioReserva,finReserva,estacionamiento_id):
        #Esta funcion determinará qué porcentaje de tiempo ocupa un esquema tarifario en una reserva
        
        diasFeriados = DiasFeriadosEscogidos.objects.filter(id = estacionamiento_id)
        
        tiempo_reserva = finReserva - inicioReserva
        tiempo_reserva_min = tiempo_reserva.seconds/60 + (tiempo_reserva.days*24*60)  
        minutosNoFeriados = 0
        minutosFeriados = 0
        minuto = timedelta(minutes=1)

        coincidencia = False
        
        # Se define el inicio y el final de cada dia
            
        tiempoActual = inicioReserva
        minuto       = timedelta(minutes=1)
        print(diasFeriados)
        while tiempoActual < finReserva:
            horaActual = tiempoActual.time()
            
            for diaFeriado in diasFeriados:
                 
                if (tiempoActual.day == diaFeriado.fecha.day and 
                    tiempoActual.month == diaFeriado.fecha.month):
                    
                    coincidencia = True
                    minutosFeriados += 1

                    if tiempoActual.day != (tiempoActual + minuto).day:
                        coincidencia = False
                    break
                     
            if (not coincidencia):
                minutosNoFeriados += 1
                
            tiempoActual += minuto
        minutosNoFeriados -= 1
        proporcionFeriado = Decimal(minutosFeriados/tiempo_reserva_min).quantize(Decimal('1.00'))
        proporcionNoFeriado =  Decimal(minutosNoFeriados/tiempo_reserva_min).quantize(Decimal('1.00'))
            
        return (proporcionFeriado, proporcionNoFeriado) 

    def consultarEsquemaTarifario(self, inicioReserva, finReserva, estacionamiento_id, tipo_vehiculo):
        
        esquemaTarifario = EsquemaTarifarioM2M.objects.filter(estacionamiento = estacionamiento_id)
        
        if len(esquemaTarifario)>0:
            for esquema in esquemaTarifario:
                if (esquema.tarifa.tipoVehiculo == tipo_vehiculo and esquema.tarifa.tipoDia == 'Dia Feriado'):
                    precioFeriado = esquema.tarifa.calcularPrecio(inicioReserva, finReserva)
        
                elif (esquema.tarifa.tipoVehiculo == tipo_vehiculo and esquema.tarifa.tipoDia == 'Dia Normal'):
                    precioNoFeriado = esquema.tarifa.calcularPrecio(inicioReserva, finReserva)
                    
        return (precioFeriado, precioNoFeriado)
        
class PrecioTarifaMasTiempo(FronterasTarifarias):
    #Se calcula en base a la tarifa que ocupe mas tiempo en el cruce
       
    def calcularPrecioFrontera(self, inicioReserva, finReserva, estacionamiento_id, tipo_vehiculo):
        
        (porcentajeFeriado, porcentajeNormal) = self.porcentajeEsquema(inicioReserva,finReserva,estacionamiento_id)
        print(porcentajeNormal, porcentajeFeriado)
        (precioFeriado, precioNoFeriado) = self.consultarEsquemaTarifario(inicioReserva, finReserva, estacionamiento_id, tipo_vehiculo)
        
        if porcentajeFeriado > porcentajeNormal:
            return precioFeriado
         
        else: 
            return precioNoFeriado    

    def tipoFrontera(self):
    
        return("Precio completo o feriados")

class PrecioTarifaMasCara(FronterasTarifarias):
    #Se calcula en base a la tarifa mas cara
    
    def calcularPrecioFrontera(self, inicioReserva, finReserva, estacionamiento_id, tipo_vehiculo):

        (precioFeriado, precioNoFeriado) = self.consultarEsquemaTarifario(inicioReserva, finReserva, estacionamiento_id, tipo_vehiculo)
                    
        if precioFeriado > precioNoFeriado:
            return precioFeriado
        else:
            return precioNoFeriado
    
        return -1
    
    def tipoFrontera(self):
    
        return("Precio tarifa mas cara")

class PrecioProporcional(FronterasTarifarias):

    def calcularPrecioFrontera(self, inicioReserva, finReserva, estacionamiento_id, tipo_vehiculo):

        (precioFeriado, precioNoferiado) = self.consultarEsquemaTarifario(inicioReserva, finReserva, estacionamiento_id, tipo_vehiculo)
        print(precioFeriado, precioNoferiado)
        (porcentajeFeriado, porcentajeNormal) = self.porcentajeEsquema(inicioReserva,finReserva,estacionamiento_id)
        print("Porcentajes")
        print(porcentajeFeriado, porcentajeNormal)
        
        precioF = Decimal(precioFeriado*porcentajeFeriado).quantize(Decimal('1.00'))
        precioNF = Decimal(precioNoferiado*porcentajeNormal).quantize(Decimal('1.00'))
        print( 'precios')
        print(precioF, precioNF)
        precioTotal = precioF + precioNF
        print(precioTotal)  
        return  precioTotal
    
    def tipoFrontera(self):
    
        return("Precio porporcional")
