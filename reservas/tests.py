# -*- coding: utf-8 -*-
from django.test import TestCase
from estacionamientos.models import *
from datetime import *
from estacionamientos.forms import *
from estacionamientos.controller import *
from reservas.controller import *
from reservas.forms import *
from reservas.models import *

class TestMoverReserva(TestCase):
    
    # TDD
    
    def MoverUnaReservaDentrodelhorizonte(self):
    
        e = Estacionamiento( 
                    nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
                    rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
                    horizonte = 15,
                    cierre = time(hour = 23,  minute = 59),
                    capacidadLivianos = 100,
                    capacidadPesados = 100,
                    capacidadMotos = 100)
        e.save()
        reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
                          estacionamiento = e,inicioReserva = datetime.now(),
                          finalReserva = datetime.now() + timedelta(days= 6),
                          estado = "Válido", tipo_vehiculo = "liviano")
        reserva.save()
        self.assertTrue(reserva_Cambiable(reserva.iniReserva,reserva.finalReserva,e.horizonte))
    
    # TDD    
        
    def MoverUnaReservaFueradelhorizonte(self):
    
        e = Estacionamiento( 
                    nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
                    rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
                    horizonte = 15,
                    cierre = time(hour = 23,  minute = 59),
                    capacidadLivianos = 100,
                    capacidadPesados = 100,
                    capacidadMotos = 100)
        e.save()
        reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
                          estacionamiento = e,inicioReserva = datetime.now() + timedelta(days= horizonte),
                          finalReserva = datetime.now() + timedelta(days= horizonte + 1),
                          estado = "Válido", tipo_vehiculo = "liviano")
        reserva.save()
        self.assertFalse(reserva_Cambiable(reserva.iniReserva,reserva.finalReserva,e.horizonte)) 
    
    # Borde
        
    def MoverUnaReservaMitadDentro(self):
    
        e = Estacionamiento( 
                    nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
                    rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
                    horizonte = 15,
                    cierre = time(hour = 23,  minute = 59),
                    capacidadLivianos = 100,
                    capacidadPesados = 100,
                    capacidadMotos = 100)
        e.save()
        reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
                          estacionamiento = e,inicioReserva = datetime.now() + timedelta(days= horizonte - 2),
                          finalReserva = datetime.now() + timedelta(days = horizonte + 2),
                          estado = "Válido", tipo_vehiculo = "liviano")
        reserva.save()
        self.assertTrue(reserva_Cambiable(reserva.iniReserva,reserva.finalReserva,e.horizonte)) 
    
    # Malicia
    
    def MoverUnaReservaInvalidaPor1minuto(self):
    
        e = Estacionamiento( 
                    nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
                    rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
                    horizonte = 15,
                    cierre = time(hour = 23,  minute = 59),
                    capacidadLivianos = 100,
                    capacidadPesados = 100,
                    capacidadMotos = 100)
        e.save()
        reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
                          estacionamiento = e,inicioReserva = datetime.now() + timedelta(days= horizonte - 2),
                          finalReserva = datetime.now() + timedelta(days = horizonte + 2, minutes = 1),
                          estado = "Válido", tipo_vehiculo = "liviano")
        reserva.save()
        self.assertFalse(reserva_Cambiable(reserva.iniReserva,reserva.finalReserva,e.horizonte))        
        
    # Malicia    
        
        def MoverUnaReservaFinalAnteriorAInicial(self):
    
            e = Estacionamiento( 
                        nombre = "nombre_est", CI_prop = "123456", direccion = "direccion_est",
                        rif = "J-123456789",apertura = time(hour = 0,  minute = 0),
                        horizonte = 15,
                        cierre = time(hour = 23,  minute = 59),
                        capacidadLivianos = 100,
                        capacidadPesados = 100,
                        capacidadMotos = 100)
            e.save()
            reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
                              estacionamiento = e,finalReserva = datetime.now() + timedelta(days= horizonte - 2),
                              inicioReserva = datetime.now() + timedelta(days = horizonte + 2, minutes = 1),
                              estado = "Válido", tipo_vehiculo = "liviano")
            reserva.save()
            self.assertFalse(reserva_Cambiable(reserva.iniReserva,reserva.finalReserva,e.horizonte))                            