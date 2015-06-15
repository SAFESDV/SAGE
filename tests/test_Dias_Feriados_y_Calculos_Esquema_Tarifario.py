# -*- coding: utf-8 -*-

from estacionamientos.models import *
from django.test import TestCase
from datetime import *
from estacionamientos.forms import *
from estacionamientos.controller import *

class DiasFeriadosTestCase(TestCase):
    
#----------------------------------------------------------------------------------
#                 PRUEBAS PARA RESERVAR SOBRE DIAS FERIADOS                        
#----------------------------------------------------------------------------------

#Debo  hacer uso de DiasFeriadosEscogidos en estacionamientos.model para rellenar una lista de 
#dias feriados

    def crearEstacionamiento(self):
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()

    def testReservarHastaLas1159DeUnDiaFeriado(self):
        
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()
        
        Dia1 = DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 6, day = 24), 
                                               descripcion = "Batalla de carabobo",  
                                               estacionamiento = e)
        Dia1.save()
        Dia2 = DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 7, day = 24), 
                                               descripcion = "Natalicio del libertador",  
                                               estacionamiento = e)
        Dia2.save()           
        Tarifa = TarifaHora(
            tarifa = 2,
            estacionamiento = e,
            tipoDia = 'Dia Feriado'
        )
        Tarifa.save()
        esquemaParaFeriado = EsquemaTarifarioM2M(
            estacionamiento = e,
            tarifa = Tarifa
        )
        
        
        esquemaParaFeriado.save()
        inicioReserva = datetime(year = 2015, month = 6, day = 24, hour = 0, minute= 0)
        finalReserva = datetime(year = 2015, month = 6, day = 24, hour = 23, minute = 59)
        valor = esquemaParaFeriado.tarifa.calcularPrecio(inicioReserva,finalReserva ) 
        
        self.assertEqual(valor,48) #Deberia cobrarse 48
    
    def testReservarHastaLas000DeUnDiaFeriado(self):
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()
        
        Dia1 = DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 12, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = e)
        Dia1.save()
        Dia2 = DiasFeriadosEscogidos(fecha   = datetime(year = 2016, month = 1, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = e)
        Dia2.save()           
        Tarifa = TarifaHora(
            tarifa = 2,
            estacionamiento = e,
            tipoDia = 'Dia Feriado'
        )
        Tarifa.save()
        esquemaParaFeriado = EsquemaTarifarioM2M(
            estacionamiento = e,
            tarifa = Tarifa
        )
        esquemaParaFeriado.save()
        valor = esquemaParaFeriado.tarifa.calcularPrecio(datetime(year = 2015, month = 12, day = 31, hour = 23, minute= 0), datetime(year = 2016, month = 1, day = 1, hour = 0, minute = 0)) 
        
        self.assertEqual(valor,2) #Deberia cobrarse 2 
        
    def testReservarDesde1130DiaNormalA0030DiaFeriado(self):
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()
        
        Dia1 = DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 12, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = e)
        Dia1.save()
        Dia2 = DiasFeriadosEscogidos(fecha   = datetime(year = 2016, month = 1, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = e)
        Dia2.save()           
        Tarifa = TarifaHora(
            tarifa = 2,
            estacionamiento = e,
            tipoDia = 'Dia Feriado'
        )
        Tarifa.save()
        
        Tarifa2 = TarifaMinuto(
            tarifa = 1,
            estacionamiento = e,
            tipoDia = 'Dia Normal'                       
        )
        Tarifa2.save()
        
        esquemaParaFeriado = EsquemaTarifarioM2M(
            estacionamiento = e,
            tarifa = Tarifa
        )
        esquemaParaFeriado.save()
        valor = esquemaParaFeriado.tarifa.calcularPrecio(datetime(year = 2015, month = 12, day = 30, hour = 23, minute= 30), datetime(year = 2015, month = 12, day = 31, hour = 0, minute = 30)) 
        
        self.assertEqual(valor,2) #Deberia cobrarse 2 
    
    def testReservarDesde1130FeriadoA0030Normal(self):
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()
        
        Dia1 = DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 12, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = e)
        Dia1.save()
        Dia2 = DiasFeriadosEscogidos(fecha   = datetime(year = 2016, month = 1, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = e)
        Dia2.save()           
        Tarifa = TarifaHora(
            tarifa = 2,
            estacionamiento = e,
            tipoDia = 'Dia Feriado'
        )
        Tarifa.save()
        
        Tarifa2 = TarifaMinuto(
            tarifa = 1,
            estacionamiento = e,
            tipoDia = 'Dia Normal'                       
        )
        Tarifa2.save()
        
        esquemaParaFeriado = EsquemaTarifarioM2M(
            estacionamiento = e,
            tarifa = Tarifa
        )
        esquemaParaFeriado.save()
        valor = esquemaParaFeriado.tarifa.calcularPrecio(datetime(year = 2016, month = 1, day = 1, hour = 23, minute= 30), datetime(year = 2016, month = 1, day = 2, hour = 0, minute = 30)) 
        
        self.assertEqual(valor,2) #Deberia cobrarse 2 
    
    def testReservarEnHoraPicoUnDiaFeriado(self):
        
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()
        
        Dia1 = DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 6, day = 24), 
                                               descripcion = "Batalla de carabobo",  
                                               estacionamiento = e)
        Dia1.save()
        Dia2 = DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 7, day = 24), 
                                               descripcion = "Natalicio del libertador",  
                                               estacionamiento = e)
        Dia2.save()           
        
        inicio = time(23,0)
        fin = time(23,59)
        
        Tarifa = TarifaHoraPico(
            tarifa = 5,
            estacionamiento = e,
            tipoDia = 'Dia Feriado',
            tarifa2 = 10,
            inicioEspecial=inicio,
            finEspecial=fin
        )
        Tarifa.save()
        
        Tarifa2 = TarifaHora(
            tarifa = 1,
            estacionamiento = e,
            tipoDia = 'Dia Normal',
                                   
        )
        Tarifa2.save()
        
        esquemaParaFeriado = EsquemaTarifarioM2M(
            estacionamiento = e,
            tarifa = Tarifa
        )
        esquemaParaFeriado.save()
        
        inicioReserva = datetime(year = 2015, month = 6, day = 24, hour = 23, minute= 0)
        finalReserva = datetime(year = 2015, month = 6, day = 24, hour = 23, minute = 59)
        valor = esquemaParaFeriado.tarifa.calcularPrecio(inicioReserva,finalReserva )   
              
        self.assertEqual(valor,Decimal(9.83).quantize(Decimal("1.00")) 
    
    def testReservarEnFinDeSemanaUnDiaFeriado(self):
        
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()
        
        Dia1 = DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 12, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = e)
        Dia1.save()
        Dia2 = DiasFeriadosEscogidos(fecha   = datetime(year = 2016, month = 1, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = e)
        Dia2.save()           
        
        
        Tarifa = TarifaFinDeSemana(
            tarifa = 5,
            estacionamiento = e,
            tipoDia = 'Dia Feriado',
            tarifa2 = 10,
        )
        Tarifa.save()
        
        Tarifa2 = TarifaHorayFraccion(
            tarifa = 1,
            estacionamiento = e,
            tipoDia = 'Dia Normal',
                                   
        )
        Tarifa2.save()
        
        esquemaParaFeriado = EsquemaTarifarioM2M(
            estacionamiento = e,
            tarifa = Tarifa
        )
        esquemaParaFeriado.save()
        valor = esquemaParaFeriado.tarifa.calcularPrecio(datetime(year = 2016, month = 12, day = 31, hour = 23, minute= 30),
                                                          datetime(year = 2017, month = 1, day = 1, hour = 0, minute= 30))
        
        self.assertEqual(valor,10) #Deberia cobrarse 10
