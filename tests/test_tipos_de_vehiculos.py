from django.test import TestCase
from datetime import time, date
from reservas.forms import *
from estacionamientos.controller import *
from estacionamientos.forms import *
from estacionamientos.models import *
from reservas.models import *
from django.core.exceptions import ValidationError
'''

    CASOS DE PRUEBA PARAMETRIZANDO Y RESERVANDO CON DISTINTOS TIPOS DE VEHICULOS

'''

class TiposDeVehiculoTestCase(TestCase):

    def crearEstacionamientoNuevo(self,puestosLivianos,puestosPesados,puestosMotos,hora_apertura=time(0,0),hora_cierre=time(23,59)):
        e = Estacionamiento(
            nombre      = 'nombre',
            CI_prop     = '1234567',
            direccion   = 'Caracas',
            telefono1   = '02125555555',
            email1      = 'estacionamiento@gmail.com',
            rif         = 'V-123456789',
            capacidadLivianos = puestosLivianos,
            capacidadPesados  = puestosPesados,
            capacidadMotos    = puestosMotos,
            apertura       = hora_apertura,
            cierre         = hora_cierre              
            )
        e.save()
        return e

    def testEstacionamientoSinPuestos(self):
        self.assertRaises(ValidationError,crearEstacionamientoNuevo(0,0,0))
    
    #Borde
    def testEstacionamientoSoloDeLivianos(self):
        e=self.crearEstacionamientoNuevo(1,0,0)
        self.assertTrue(e != None)        
        
    def testEstacionamientoSoloDePesados(self):
        e=self.crearEstacionamientoNuevo(0,1,0)
        self.assertTrue(e != None)        

        
    def testEstacionamientoSoloDeMotos(self):
        e=self.crearEstacionamientoNuevo(0,0,1)
        self.assertTrue(e != None)        

        
    def testEstacionamientoMotosyLivianos(self):
        pass
        
    def testEstacionamientoLivianosyPesados(self):
        pass
        
    def testEstacionamientoPesadosyMotos(self):
        pass
        
    def testReservarParaLiviano(self):
        e = self.crearEstacionamientoNuevo(1,0,0)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
        #self.assertRaise
        
        r = Reserva(
                    estacionamiento = e,
                    inicioReserva   = fecha_inicio,
                    finalReserva    = fecha_fin,
                    estado          = 'V�lido',
                    tipo_vehiculo   = 'Liviano'
                    )
        
    def testReservarParaPesado(self):
        pass
        
    def testReservarParaMoto(self):
        pass
        
    def testLlenarLivianosNoBloqueaLosDemas(self):
        pass
        
    def testLlenarPesadosNoBloqueaLosDemas(self):
        pass
        
    def testLlenarMotosNoBloqueaLosDemas(self):
        pass
        
    def testLlenarLivianosyPesadosNoBloqueaMotos(self):
        pass
        
    def testLlenarMotosyPesadosNoBloqueaLivianos(self):
        pass
    
    def testLlenarLivianosyMotosNoBloqueaPesados(self):
        pass