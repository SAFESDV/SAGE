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
#                 Frontera Tarifaria Mas Cara                     #
###################################################################

class FronteraMasCaraTestCase(TestCase):

    def crearEstacionamiento(self):
        fronteraTarifa = PrecioTarifaMasCara() 
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
        
        feriados2 = DiasFeriadosEscogidos(
            fecha   = datetime(year = 2015, month = 6, day = 27), 
            descripcion = "UnFeriado",  
            estacionamiento = estacionamiento
        )
        feriados2.save()
    
    ######################## Mismos esquemas tarifarios ########################    
    #TDD
    def testTarifaHoraRegularNormal(self):  
        #NoFeriado: esquema TarifaHora. Reserva 5h 
        #Feriado: esquema TarifaHora. Reserva 1h y 30m 
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 11.01
        tarifaFeriado = 5.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 22, 30 )
        finReserva = datetime(2015, 6, 28, 5, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(77.07).quantize(Decimal('1.00')))

    #TDD
    def testTarifaHoraRegularFeriado(self):  
        #NoFeriado: esquema TarifaHora. Reserva 1h 
        #Feriado: esquema TarifaHora. Reserva 5h y 30
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 11.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 18, 30 )
        finReserva = datetime(2015, 6, 28, 1, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(77.07).quantize(Decimal('1.00')))
    
    #TDD
    def testTarifaMinutoRegularNormal(self):  
        #NoFeriado: esquema TarifaMinuto. Reserva 5h 
        #Feriado: esquema TarifaMinuto. Reserva 1h y 30 min
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 11.01
        tarifaFeriado = 5.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaMinuto', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 22, 30 )
        finReserva = datetime(2015, 6, 28, 5, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.56).quantize(Decimal('1.00')))
    
    #TDD
    def testTarifaMinutoRegularFeriado(self):  
        #NoFeriado: esquema TarifaMinuto. Reserva 1h 
        #Feriado: esquema TarifaMinuto. Reserva 5h y 30
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 11.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaMinuto', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 18, 30 )
        finReserva = datetime(2015, 6, 28, 1, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.56).quantize(Decimal('1.00')))
        
    def testTarifaHorayFraccionRegularNormal(self):  
        #NoFeriado: esquema TarifaHorayFraccion. Reserva 5h 
        #Feriado: esquema TarifaHorayFraccion. Reserva 1h y 30 min
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 11.01
        tarifaFeriado = 5.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHorayFraccion', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHorayFraccion', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 22, 30 )
        finReserva = datetime(2015, 6, 28, 5, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.56).quantize(Decimal('1.00')))
    
    def testTarifaHorayFraccionRegularFeriado(self):  
        #NoFeriado: esquema TarifaHorayFraccion. Reserva 1h 
        #Feriado: esquema TarifaHorayFraccion. Reserva 5h y 30
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 11.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHorayFraccion', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHorayFraccion', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 18, 30)
        finReserva = datetime(2015, 6, 28, 1, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.56).quantize(Decimal('1.00')))
        
    #TDD
    def testTarifaFinDeSemanaRegularNormal(self):  
        #NoFeriado: esquema TarifaFinDeSemana. Reserva 5h 
        #Feriado: esquema TarifaFinDeSemana. Reserva 1h y 30 min
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 11.01
        tarifaE = 11.05
        tarifaFeriado = 5.01
        tarifaFeriadoE = 5.05
        estacionamientoTarifa = guardarEsquemasNormal('TarifaFinDeSemana', tarifa, tarifaE, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaFinDeSemana', tarifaFeriado, tarifaFeriadoE, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 22, 30 )
        finReserva = datetime(2015, 6, 28, 5, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.82).quantize(Decimal('1.00')))
    
    #TDD
    def testTarifaFinDeSemanaRegularFeriado(self):  
        #NoFeriado: esquema TarifaFinDeSemana. Reserva 1h 
        #Feriado: esquema TarifaFinDeSemana. Reserva 5h y 30
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaE = 5.05
        tarifaFeriado = 11.01
        tarifaFeriadoE = 11.05
        estacionamientoTarifa = guardarEsquemasNormal('TarifaFinDeSemana', tarifa, tarifaE, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaFinDeSemana', tarifaFeriado, tarifaFeriadoE, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 18, 30)
        finReserva = datetime(2015, 6, 28, 1, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.82).quantize(Decimal('1.00')))
    
    #TDD
    def testTarifaHoraPicoRegularNormal(self):  
        #NoFeriado: esquema TarifaHoraPico. Reserva 5h 
        #Feriado: esquema TarifaHoraPico. Reserva 1h y 30 min
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 11.01
        tarifaE = 11.05
        tarifaFeriado = 5.01
        tarifaFeriadoE = 5.05
        horaPicoIni = time(22, 0)
        horaPicoFin = time(4, 0)
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHoraPico', tarifa, tarifaE, horaPicoIni, horaPicoFin, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHoraPico', tarifaFeriado, tarifaFeriadoE, horaPicoIni, horaPicoFin, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 22, 30 )
        finReserva = datetime(2015, 6, 28, 5, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.56).quantize(Decimal('1.00')))
    
    #TDD
    def testTarifaHoraPicoRegularFeriado(self):  
        #NoFeriado: esquema TarifaHoraPico. Reserva 1h 
        #Feriado: esquema TarifaHoraPico. Reserva 5h y 30
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaE = 5.05
        tarifaFeriado = 11.01
        tarifaFeriadoE = 11.05
        horaPicoIni = time(22, 0)
        horaPicoFin = time(4, 0)
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHoraPico', tarifa, tarifaE, horaPicoIni, horaPicoFin, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHoraPico', tarifaFeriado, tarifaFeriadoE, horaPicoIni, horaPicoFin, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 18, 30)
        finReserva = datetime(2015, 6, 28, 1, 0)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(71.56).quantize(Decimal('1.00')))

    ######################### TarifaHora/TarifaMinuto ##########################
    #borde 
    def testTarifaHoraTarifaMinutoDif001(self):
        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaMinuto. Reserva 20min
        #diferencia en tarifa 0.01
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 5.02
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30)
        finReserva = datetime(2015, 6, 28, 0, 20)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.01).quantize(Decimal('1.00')))
        
    #esquina
    def testTarifaHoraTarifaMinuto59min(self):

        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaMinuto. Reserva 29min
        #diferencia en tarifa 0.01 con 59 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 5.02
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30)
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.01).quantize(Decimal('1.00')))
        
    #esquina
    def testTarifaHoraTarifaMinuto59minPreciosDif001(self):
        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaMinuto. Reserva 29min
        #diferencia entre el precio de 0.01 con 59 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 5.10
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30)
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.02).quantize(Decimal('1.00')))
        
    #malicia
    def testTarifaHoraTarifaMinuto2minEnFrontera(self):
        #NoFeriado: esquema TarifaHora. Reserva 1min 
        #Feriado: esquema TarifaMinuto. Reserva 1min
        #diferencia entre el precio de 0.01 con 2 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 0.15
        tarifaFeriado = 5.10
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 59)
        finReserva = datetime(2015, 6, 28, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(0.17).quantize(Decimal('1.00')))
    
    
    ###################### TarifaHora/TarifaHorayFraccion#######################
    #esquina 
    def testTarifaHoraTarifaHorayFraccionDif001(self):
        #NoFeriado: esquema TarifaHora. Reserva 1h 
        #Feriado: esquema TarifaHorayFraccion. Reserva 29min
        #diferencia en tarifa 0.01
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 5.02
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHorayFraccion', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 0 )
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(10.02).quantize(Decimal('1.00')))
        
    #malicia
    def testTarifaHoraTarifaHorayFraccion89min(self):

        #NoFeriado: esquema TarifaHora. Reserva 1h 
        #Feriado: esquema TarifaHorayFraccion. Reserva 31min
        #diferencia en tarifa 0.01 con 59 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 5.02
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHorayFraccion', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 0)
        finReserva = datetime(2015, 6, 28, 0, 31)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(10.04).quantize(Decimal('1.00')))
        
    #esquina
    def testTarifaHoraTarifaHorayFraccion89minPreciosDif001(self):
        #NoFeriado: esquema TarifaHora. Reserva 1h 
        #Feriado: esquema TarifaHorayFraccion. Reserva 29min
        #diferencia entre el precio de 0.01 con 59 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 3.75
        tarifaFeriado = 5.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHorayFraccion', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 0)
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(7.52).quantize(Decimal('1.00')))
        
    #malicia
    def testTarifaHoraTarifaHorayFraccion2minEnFrontera(self):
        #NoFeriado: esquema TarifaHora. Reserva 1min 
        #Feriado: esquema TarifaMinuto. Reserva 1min
        #diferencia entre el precio de 0.01 con 2 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.09
        tarifaFeriado = 5.10
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHorayFraccion', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 59 )
        finReserva = datetime(2015, 6, 28, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.10).quantize(Decimal('1.00')))
    
    ######################## TarifaHora/TarifaHoraPico #########################
    
    ''' DESCOMENTAR
    #borde 
    def testTarifaHoraTarifaHoraPicoDif001(self):
        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaHoraPico. Reserva 20min
        #diferencia en tarifa 0.01
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 5.02
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHoraPico', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30 )
        finReserva = datetime(2015, 6, 28, 0, 20)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.01).quantize(Decimal('1.00')))
        
    #esquina
    def testTarifaHoraTarifaHoraPico59min(self):

        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaHoraPico. Reserva 29min
        #diferencia en tarifa 0.01 con 59 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 5.02
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHoraPico', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30 )
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.01).quantize(Decimal('1.00')))
        
    #esquina
    def testTarifaHoraTarifaHoraPico59minPreciosDif001(self):
        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaHoraPico. Reserva 29min
        #diferencia entre el precio de 0.01 con 59 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.01
        tarifaFeriado = 5.10
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHorayPico', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30 )
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.02).quantize(Decimal('1.00')))
        
    #malicia
    def testTarifaHoraTarifaHoraPico2minEnFrontera(self):
        #NoFeriado: esquema TarifaHora. Reserva 1min 
        #Feriado: esquema TarifaHoraPico. Reserva 1min
        #diferencia entre el precio de 0.01 con 2 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 0.15
        tarifaFeriado = 5.10
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHorayPico', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 59 )
        finReserva = datetime(2015, 6, 28, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(0.17).quantize(Decimal('1.00')))
    '''
    ######################### TarifaMinuto/TarifaHora ##########################    
        #borde 
    def testTarifaMinutoTarifaHoraDif001(self):
        #NoFeriado: esquema TarifaMinuto. Reserva 30min 
        #Feriado: esquema TarifaHora. Reserva 20min
        #diferencia en tarifa 0.01
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.02
        tarifaFeriado = 5.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaMinuto', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30 )
        finReserva = datetime(2015, 6, 28, 0, 20)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.01).quantize(Decimal('1.00')))
        
    #esquina
    def testTarifaMinutoTarifaHora59min(self):

        #NoFeriado: esquema TarifaMinuto. Reserva 30min 
        #Feriado: esquema TarifaHora. Reserva 29min
        #diferencia en tarifa 0.01 con 59 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.02
        tarifaFeriado = 5.01
        estacionamientoTarifa = guardarEsquemasNormal('TarifaMinuto', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30 )
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.01).quantize(Decimal('1.00')))
        
    #esquina
    def testTarifaMinutoTarifaHora59minPreciosDif01(self):
        #NoFeriado: esquema TarifaMinuto. Reserva 30min 
        #Feriado: esquema TarifaHora. Reserva 29min
        #diferencia entre el precio de 0.01 con 59 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaFeriado = 5.01 
        estacionamientoTarifa = guardarEsquemasNormal('TarifaMinuto', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30 )
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.02).quantize(Decimal('1.00')))
        
    #malicia
    def testTarifaMinutoTarifaHora2minEnFrontera(self):
        #NoFeriado: esquema TarifaMinuto. Reserva 1min 
        #Feriado: esquema TarifaHora. Reserva 1min
        #diferencia entre el precio de 0.01 con 2 min de reserva
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaFeriado = 0.15 
        estacionamientoTarifa = guardarEsquemasNormal('TarifaMinuto', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 59 )
        finReserva = datetime(2015, 6, 28, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(0.17).quantize(Decimal('1.00')))
        
    ######################### TarifaFinDeSemana/TarifaMinuto ########################## 
    
    def testTarifaFinSemanaTarifaMinuto59Min(self):
        #NoFeriado: esquema TarifaFinSemana. Reserva 30min 
        #Feriado: esquema TarifaMinuto. Reserva 29min
        #Reserva 30 min dia Normal de Semana y 29 Minutos Feriados
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaEspecial = 5.20
        tarifaFeriado = 0.15
        estacionamientoTarifa = guardarEsquemasNormal('TarifaFinDeSemana', tarifa, tarifaEspecial, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 26, 23, 30 )
        finReserva = datetime(2015, 6, 27, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.06).quantize(Decimal('1.00')))
        
    def testTarifaFinSemanaTarifaMinuto2Min(self):
        #NoFeriado: esquema TarifaFinSemana. Reserva 30min 
        #Feriado: esquema TarifaMinuto. Reserva 29min
        #Reserva 1 min dia Normal de Semana y 29 Minutos Feriados
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaEspecial = 5.20
        tarifaFeriado = 0.15
        estacionamientoTarifa = guardarEsquemasNormal('TarifaFinDeSemana', tarifa, tarifaEspecial, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 26, 23, 59 )
        finReserva = datetime(2015, 6, 27, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(0.17).quantize(Decimal('1.00')))
        
    def testTarifaFinSemanaTarifaMinuto59MinFinSemana(self):
        #NoFeriado: esquema TarifaFinSemana. Reserva 30min 
        #Feriado: esquema TarifaMinuto. Reserva 29min
        #Reserva 30 min dia Especial y 29 Minutos Feriados
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaEspecial = 5.20
        tarifaFeriado = 0.15
        estacionamientoTarifa = guardarEsquemasNormal('TarifaFinDeSemana', tarifa, tarifaEspecial, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30 )
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.11).quantize(Decimal('1.00')))
        
    def testTarifaFinSemanaTarifaMinuto2MinFinSemana(self):
        #NoFeriado: esquema TarifaFinSemana. Reserva 30min 
        #Feriado: esquema TarifaMinuto. Reserva 29min
        #Reserva 1 min dia Especial y 1 Minutos Feriados
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaEspecial = 5.20
        tarifaFeriado = 0.15
        estacionamientoTarifa = guardarEsquemasNormal('TarifaFinDeSemana', tarifa, tarifaEspecial, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 59 )
        finReserva = datetime(2015, 6, 28, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(0.17).quantize(Decimal('1.00')))
        
    def testTarifaFinSemanaTarifaMinuto2MinFinSemana_TresDias(self):
        #NoFeriado: esquema TarifaFinSemana. Reserva 30min 
        #Feriado: esquema TarifaMinuto. Reserva 29min
        #Reserva 1 min dia Normal, un dia Especial y 1 Minutos dia Feriado
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaEspecial = 5.20
        tarifaFeriado = 0.15
        estacionamientoTarifa = guardarEsquemasNormal('TarifaFinDeSemana', tarifa, tarifaEspecial, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaMinuto', tarifaFeriado, None, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 26, 23, 59 )
        finReserva = datetime(2015, 6, 28, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(124.97).quantize(Decimal('1.00')))
        
    ######################### TarifaHora/TarifaFinDeSemana ########################## 
    
    def testTarifaHoraTarifaFinSemana59Min(self):
        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaFinDeSemana. Reserva 29min
        #Reserva 30 min dia Normal de Semana y 29 Minutos Feriados
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaFeriado = 0.15
        tarifaEspecialFeriado = 5.20
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaFinDeSemana', tarifaFeriado, tarifaEspecialFeriado, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 26, 23, 30 )
        finReserva = datetime(2015, 6, 27, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.10).quantize(Decimal('1.00')))
        
    def testTarifaHoraTarifaFinSemana2Min(self):
        #NoFeriado: esquema TarifaHora. Reserva 1 min 
        #Feriado: esquema TarifaFinDeSemana. Reserva 1 min
        #Reserva 1 min dia Normal de Semana y 1 Minutos Feriados
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaFeriado = 0.15
        tarifaEspecialFeriado = 5.20
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaFinDeSemana', tarifaFeriado, tarifaEspecialFeriado, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 26, 23, 59 )
        finReserva = datetime(2015, 6, 27, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.10).quantize(Decimal('1.00')))
        
    def testTarifaHoraTarifaFinDeSemana59MinFinSemana(self):
        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaFinDeSemana. Reserva 29min
        #Reserva 30 min dia Especial y 29 Minutos Feriados
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaEspecialFeriado = 5.20
        tarifaFeriado = 0.15
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaFinDeSemana', tarifaFeriado, tarifaEspecialFeriado, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 30 )
        finReserva = datetime(2015, 6, 28, 0, 29)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.11).quantize(Decimal('1.00')))
        
    def testTarifaHoraTarifaFinDeSemana2MinFinSemana(self):
        #NoFeriado: esquema TarifaHora. Reserva 1min 
        #Feriado: esquema TarifaFinDeSemana. Reserva 1min
        #Reserva 1 min dia Fin de Semana y 1 Minutos Feriados Fin De Semana
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaEspecialFeriado = 5.20
        tarifaFeriado = 0.15
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaFinDeSemana', tarifaFeriado, tarifaEspecialFeriado, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 27, 23, 59 )
        finReserva = datetime(2015, 6, 28, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(5.10).quantize(Decimal('1.00')))
        
    def testTarifaHoraTarifaFinDeSemana_TresDias(self):
        #NoFeriado: esquema TarifaHora. Reserva 30min 
        #Feriado: esquema TarifaFinDeSemana. Reserva 29min
        #Reserva 1 min dia Normal, un dia Especial y 1 Minutos dia Feriado
        
        estacionamiento = self.crearEstacionamiento()
        self.crearFeriados(estacionamiento)
        tarifa = 5.10
        tarifaFeriado = 0.15
        tarifaEspecialFeriado = 5.20
        estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None, None, None, 'Liviano', estacionamiento)
        estacionamientoTarifa = guardarEsquemasFeriado('TarifaFinDeSemana', tarifaFeriado, tarifaEspecialFeriado, None, None, 'Liviano', estacionamiento)
        inicioReserva = datetime(2015, 6, 26, 23, 59 )
        finReserva = datetime(2015, 6, 28, 0, 1)
        monto = estacionamiento.fronteraTarifaria.calcularPrecioFrontera(inicioReserva, finReserva, estacionamiento.id, 'Liviano')
        self.assertEqual(monto, Decimal(127.50).quantize(Decimal('1.00')))