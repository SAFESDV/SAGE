# -*- coding: utf-8 -*-

from django.test import TestCase
from decimal import Decimal

from datetime import (
    datetime,
    time
)
from estacionamientos.controller import (
    guardarEsquemasNormal,
    guardarEsquemasFeriado,
)

from estacionamientos.models import (
    Estacionamiento,
    EsquemaTarifario,
    EsquemaTarifarioM2M,
    TarifaHora,
    TarifaMinuto,
    TarifaHorayFraccion,
    TarifaFinDeSemana,
    TarifaHoraPico,
    DiasFeriadosEscogidos,
    PrecioTarifaMasTiempo,
    PrecioTarifaMasCara,
    PrecioProporcional,
)

###################################################################
#                 Frontera Tarifaria Mas Tiempo                      #
###################################################################

class FronteraMasTiempoTestCase(TestCase):

    def crearEstacionamiento(self):
        fronteraTarifa = PrecioTarifaMasTiempo() 
        fronteraTarifa.save()
        
        estacionamiento = Estacionamiento(
            nombre      = 'estacionamiento',
            CI_prop     = 12345678,
            cedulaTipo  = 'V',
            direccion   = 'Sartenejas',
            rif         = 'J-123456789',
            horizonte   = 7,
            apertura     = time(0, 0),
            cierre       = time(23, 59),
            capacidadLivianos  = 2,
            capacidadPesados   = 2,
            capacidadMotos     = 2,
            capacidadDiscapacitados = 2,
            fronteraTarifaria = fronteraTarifa 
            )
        estacionamiento.save()
        return estacionamiento
    
    def crearFeriados(self, estacionamiento):
        feriados = DiasFeriadosEscogidos(
            fecha   = datetime(year = 2015, month = 6, day = 24), 
            descripcion = "BatallaCarabobo",  
            estacionamiento = estacionamiento
            )
        feriados.save()
        
        #TDD
    def testTarifaHoraRegularNormal(self):  
        #NoFeriado: esquema TarifaHora. Reserva 5h 
        #Feriado: esquema TarifaHora. Reserva 1h y 30m 
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 10.01
        tarifaFeriado = 11.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 24, 22, 30 )
        finReserva = datetime(2015, 6, 25, 5, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(70.07).quantize(Decimal('1.00')))

    #TDD
    def testTarifaHoraRegularFeriado(self):  
        #NoFeriado: esquema TarifaHora. Reserva 1h 
        #Feriado: esquema TarifaHora. Reserva 5h y 30
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 10.01
        tarifaFeriado = 11.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 24, 18, 30 )
        finReserva = datetime(2015, 6, 25, 1, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(77.07).quantize(Decimal('1.00')))
    
    #TDD
    def testTarifaMinutoRegularNormal(self):  
        #NoFeriado: esquema TarifaMinuto. Reserva 5h 
        #Feriado: esquema TarifaMinuto. Reserva 1h y 30 min
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 10.01
        tarifaFeriado = 11.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaMinuto', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 24, 22, 30 )
        finReserva = datetime(2015, 6, 25, 5, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(65.06).quantize(Decimal('1.00')))
    
    def testTarifaHoraRegularFeriado(self):  
        #NoFeriado: esquema TarifaHora. Reserva 1h 
        #Feriado: esquema TarifaHora. Reserva 5h y 30
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 10.01
        tarifaFeriado = 11.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaMinuto', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 24, 18, 30 )
        finReserva = datetime(2015, 6, 25, 1, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.56).quantize(Decimal('1.00')))
        