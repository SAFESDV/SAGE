# -*- coding: utf-8 -*-

from django.test import TestCase

class reserva_eliminarTestCase(TestCase):
    
    def crearEstacionamiento(self):
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()
        
    def testEstacionamientoSinReserva(self):
        e = Estacionamiento( 
            nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
            rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
            cierre = time(hour = 23,  minute = 59),
            capacidadLivianos = 100,
            capacidadPesados = 100,
            capacidadMotos = 100)
        e.save()
        
        
        
        