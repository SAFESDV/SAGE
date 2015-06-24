# -*- coding: utf-8 -*-
from django.test import TestCase
from estacionamientos.models import *
from datetime import *
from estacionamientos.forms import *
from estacionamientos.controller import *
from reservas.controller import *
from reservas.forms import *
from reservas.models import *
from billetera.models import *
from billetera.controller import *

class MoverEliminarReserva(TestCase):
    
    def crearEstacionamiento(self):
            fronteraTarifa = PrecioTarifaMasCara() 
            fronteraTarifa.save()
            
            estacionamiento = Estacionamiento(
                nombre      = 'estacionamiento',
                CI_prop     = 12345678,
                cedulaTipo  = 'V',
                direccion   = 'Sartenejas',
                rif         = 'J-123456789',
                horizonte   = 15,
                apertura     = time(0, 0),
                cierre       = time(23, 59),
                capacidadLivianos  = 1,
                capacidadPesados   = 1,
                capacidadMotos     = 1,
                capacidadDiscapacitados = 1,
                fronteraTarifaria = fronteraTarifa 
                )
            estacionamiento.save()
            tarifa = 10
            tarifaFeriado = 5
            estacionamientoTarifa = guardarEsquemasNormal('TarifaHora', tarifa, None,
                                                           None, None, 'Liviano', estacionamiento)
            estacionamientoTarifa = guardarEsquemasFeriado('TarifaHora', tarifaFeriado, None,
                                                            None, None, 'Liviano', estacionamiento)
            return estacionamiento    
    
    def crearBilletera(self):
        billetera = BilleteraElectronica(
            nombreUsuario    = "Francisco",
            apellidoUsuario  = "Sucre",
            cedulaTipo       = "V",
            cedula           = "19564959",
            PIN              = "1234"
    )
        billetera.save()
        return billetera
    
    # TDD
    
    def testMoverUnaReservaDentrodelhorizonte(self):
    
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
        self.assertTrue(reserva_Cambiable(reserva.inicioReserva,reserva.finalReserva,e.horizonte))
    
    # TDD    
        
    def testMoverUnaReservaFueradelhorizonte(self):
    
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
        
    def testMoverUnaReservaMitadDentro(self):
    
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
        self.assertTrue(reserva_Cambiable(reserva.inicioReserva,reserva.finalReserva,e.horizonte)) 
    
    # Malicia
    
    def testMoverUnaReservaInvalidaPor1minuto(self):
    
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
        self.assertFalse(reserva_Cambiable(reserva.inicioReserva,reserva.finalReserva,e.horizonte))        
        
    # Malicia    
        
        def testMoverUnaReservaFinalAnteriorAInicial(self):
    
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
            self.assertFalse(reserva_Cambiable(reserva.inicioReserva,reserva.finalReserva,e.horizonte))                            
            
    
        
    
#     # TDD
#     
#     def testCancelarReservaValida(self):   
#         e = self.crearEstacionamiento()
#         billetera = self.crearBilletera()
#         
#         reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
#                           estacionamiento = e,inicioReserva = datetime.now(),
#                           finalReserva = datetime.now() + timedelta(days= 6),
#                           estado = "Válido", tipo_vehiculo = "liviano")
#         
#         monto = e.fronteraTarifaria.calcularPrecioFrontera(reserva.inicioReserva, reserva.finalReserva, e.id, 'Liviano')
#         cancelar_reserva(reserva.id,billetera.id)
#         self.assertEqual(consultar_saldo(billetera.id), monto, "La reserva fue valida")         
#     
#     def testCancelarReservaInvalida(self):
#           
#         e = self.crearEstacionamiento()
#         billetera = self.crearBilletera()
#         
#         reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
#                           estacionamiento = e,inicioReserva = datetime.now(),
#                           finalReserva = datetime.now() + timedelta(days= 6),
#                           estado = "Válido", tipo_vehiculo = "liviano")
#         
#         monto = calcular_Precio_Reserva(reserva,e)
#         self.assertRaises(Exception, cancelar_reserva(3442,billetera.id)) 
#     
#     def testCancelarReservaCancelada(self):
#         
#         e = self.crearEstacionamiento()
#         billetera = self.crearBilletera()
#         
#         reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
#                           estacionamiento = e,inicioReserva = datetime.now(),
#                           finalReserva = datetime.now() + timedelta(days= 6),
#                           estado = "Cancelado", tipo_vehiculo = "liviano")
#         self.assertRaises(Exception, cancelar_reserva(reserva.id,billetera.id))
#         
#     def testCancelarReservaConBilleteraLLena(self):
#         
#         e = self.crearEstacionamiento()
#         billetera = self.crearBilletera()
#         
#         reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
#                           estacionamiento = e,inicioReserva = datetime.now(),
#                           finalReserva = datetime.now() + timedelta(days= 6),
#                           estado = "Válido", tipo_vehiculo = "liviano")
#         
#         monto = calcular_Precio_Reserva(reserva,e)
#         recargar_saldo(billetera.id, 10000)
#         self.assertRaises(Exception, cancelar_reserva(reserva.id,billetera.id))
#    
#     def testCancelarReservaLiberaPuesto(self):   
#         e = self.crearEstacionamiento()
#         billetera = self.crearBilletera()
#         
#         reserva = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
#                           estacionamiento = e,inicioReserva = datetime.now(),
#                           finalReserva = datetime.now() + timedelta(days= 6),
#                           estado = "Válido", tipo_vehiculo = "Liviano")
#         reserva.save()
#         
#         monto = calcular_Precio_Reserva(reserva,e)
#         cancelar_reserva(reserva.id,billetera.id)
#         
#         reserva2 = Reserva(cedulaTipo = "V",cedula = "19564959", nombre = "Francisco",apellido = "Sucre",
#                   estacionamiento = e,inicioReserva = datetime.now(),
#                   finalReserva = datetime.now() + timedelta(days= 6, minutes = 1),
#                   estado = "Válido", tipo_vehiculo = "Liviano")
#         reserva2.save()
#         
#         self.assertEqual(consultar_saldo(billetera.id), monto, "La reserva fue valida")             
#         