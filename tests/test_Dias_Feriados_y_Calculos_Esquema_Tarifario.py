# -*- coding: utf-8 -*-

from estacionamientos.models import *
from django.test import TestCase
from datetime import *
from estacionamientos.forms import *
from estacionamientos.controller import *

class DiasFeriadosTestCase(TestCase):

#----------------------------------------------------------------------------------
#             PRUEBAS PARA ESCOGER DIAS FERIADOS ACTUALES Y EXTRAS
#----------------------------------------------------------------------------------

    def testNoEscogerDiasFeriadosPorDefecto(self):
        pass
    
    def testEscogerUnDiaFeriadoPorDefecto(self):
        pass
    
    def testEscogerTodosLosDiasFeriadosPorDefecto(self):
        pass
    
    def testAgregarUnDiaFeriadoExtraSinFeriadosPorDefecto(self):
        pass
    
    def testAgregarUnDiaFeriadoExtraConUnFeriadoPorDefecto(self):
        pass
    
#----------------------------------------------------------------------------------
#                 PRUEBAS PARA RESERVAR SOBRE DIAS FERIADOS                        
#----------------------------------------------------------------------------------

#Debo hacer uso de DiasFeriadosEscogidos en estacionamientos.model para rellenar una lista de 
#dias feriados

    def RellenarDiasFeriados(self,est):
        DiasFeriadosEscogidos(fecha   = datetime(year = 2015, month = 12, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = est)
        
        DiasFeriadosEscogidos(fecha   = datetime(year = 2016, month = 1, day = 31), 
                                               descripcion = "Fin de año",  
                                               estacionamiento = est)
                            

    def testReservarHastaLas1159DeUnDiaFeriado(self):
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 0),capacidadLivianos = 100,capacidadPesados = 100,capacidadMotos = 100)
        e.save()
        self.RellenarDiasFeriados(e)
        
        Tarifa = TarifaHora(tarifa=2)
        
        esquemaTarif = EsquemaTarifario(
            tarifa = 2.0,
            estacionamiento = e,
            tipoDia = 'TarifaHora'
        )
        
        esquemaParaFeriado = EsquemaTarifarioM2M(
            estacionamiento = e,
            tarifa = Tarifa
        )
        esquemaParaFeriado.save()

        valor = esquemaParaFeriado.tarifa.calcularPrecio(datetime(year = 2015, month = 12, day = 31, hour = 23, minute= 0), datetime(year = 2015, month = 12, day = 31, hour = 23, minute = 59)) 
        
        self.assertEqual(valor,2) #Deberia cobrarse 2 
    
    def testReservarHastaLas000DeUnDiaFeriado(self):
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 0),capacidadLivianos = 100,capacidadPesados = 100,capacidadMotos = 100)
        e.save()
        self.RellenarDiasFeriados(e)
        
        Tarifa = TarifaHora(tarifa=2)
        
        esquemaTarif = EsquemaTarifario(
            tarifa = 2.0,
            estacionamiento = e,
            tipoDia = 'TarifaHora'
        )
        
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
            cierre = time(hour = 23,  minute = 0),capacidadLivianos = 100,capacidadPesados = 100,capacidadMotos = 100)
        e.save()
        self.RellenarDiasFeriados(e)
        
        Tarifa = TarifaHora(tarifa=2)
        
        esquemaTarif = EsquemaTarifario(
            tarifa = 2.0,
            estacionamiento = e,
            tipoDia = 'Dia Feriado'
        )
        
        esquemaTarif2 = EsquemaTarifario(
            tarifa = 1.0,
            estacionamiento = e,
            tipoDia = 'Dia Normal'
        )
         
        esquemaParaFeriado = EsquemaTarifarioM2M(
            estacionamiento = e,
            tarifa = Tarifa
        )
        esquemaParaFeriado.save()

        valor = esquemaParaFeriado.tarifa.calcularPrecio(datetime(year = 2015, month = 12, day = 30, hour = 23, minute= 30), datetime(year = 2015, month = 12, day = 31, hour = 0, minute = 30)) 
        self.assertEqual(valor,3) #Deberia cobrarse 2 
    
    def testReservarHastaLas0000DeUnDiaFeriado(self):
        pass
    def testReservarDesde1110A001(self):
        pass
    
    def testReservarDesde1110FeriadoA001Normal(self):
        pass
    
    def testReservarDesde1110NormalA001Feriado(self):
        pass
    
    def testReservar1159De31DicA000De1Enero(self):
        pass
    
    