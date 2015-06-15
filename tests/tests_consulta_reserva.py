# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import time,datetime
from estacionamientos.controller import consultar_ingresos
from estacionamientos.models import Estacionamiento
from reservas.models import *
from transacciones.models import *

###################################################################
#                    ESTACIONAMIENTO VISTA DISPONIBLE
###################################################################
class consultaReservaTestCase(TestCase):
    
    #TDD
    def test_sin_estacionamiento(self):
        lista, total = consultar_ingresos("J-123456789")
        self.assertTrue(len(lista) == total )

    # TDD
    def test_estacionamiento_sin_pagos(self):
        e = Estacionamiento(
            nombre      = "nom",
            direccion   = "dir",
            rif         = "J-123456789",
            capacidadLivianos = 20,
            capacidadPesados  = 20,
            capacidadMotos    = 20,
            apertura    = time(0,0),
            cierre      = time(23,59),
        )
        e.save()
        lista, total = consultar_ingresos("J-123456789")
        self.assertTrue(len(lista) == 1 and total == 0)

    # TDD
#     def test_un_estacionamiento_un_pago(self):
#         e = Estacionamiento(
#             nombre      = "nom",
#             direccion   = "dir",
#             rif         = "J-123456789",
#             capacidadLivianos = 20,
#             capacidadPesados  = 20,
#             capacidadMotos    = 20,
#             apertura    = time(0,0),
#             cierre      = time(23,59),
#         )
#         e.save()
#         
#         r = Reserva(
#             cedulaTipo      = 'V',
#             cedula          = '12345678',
#             nombre          = 'Julia',
#             apellido        = 'Suárez',
#             estacionamiento = e,
#             inicioReserva = datetime(2015,3,10,3,0),
#             finalReserva  = datetime(2015,3,10,5,0),
#             estado = "Válido",
#             tipo_vehiculo = "Liviano"
#         )
#         r.save()
#         
#         trans = Transaccion(
#                     fecha            = datetime.now(),
#                     tipo             = 'Reserva',
#                     estado           = 'Válido'
#                 )
#         trans.save()
#         
#         tdc =   TransTDC(
#                     nombre           = 'Karla',
#                     cedulaTipo       = 'V',
#                     cedula           = '87654321',
#                     tarjetaTipo      = 'VISTA',
#                     tarjeta          = '5689',
#                     monto            = 100,
#                     transaccion      = trans
#                 )
#         tdc.save()
#         
#         relacion =  TransReser(
#                         transaccion = trans,
#                         reserva = r
#                     )
#         relacion.save()
#         
#         lista, total = consultar_ingresos("J-123456789")
#         self.assertTrue(len(lista) == 1 and total == 150)
#         
#     # TDD malicia
#     def test_un_estacionamiento_muchos_pagos(self):
#         n = 1000
#         e = Estacionamiento(
#             nombre      = "nom",
#             direccion   = "dir",
#             rif         = "J-123456789",
#             capacidadPesados   = n,
#             capacidadLivianos   = n,
#             capacidadMotos   = n,
#             apertura    = time(0,0),
#             cierre      = time(23,59),
#         )
#         e.save()
#         for i in range(0,n):
#             r = Reserva(
#                 cedulaTipo      = 'V',
#                 cedula          = '12345678',
#                 nombre          = 'Julia',
#                 apellido        = 'Suárez',
#                 estacionamiento = e,
#                 inicioReserva = datetime(2015,3,10,3,0),
#                 finalReserva  = datetime(2015,3,10,5,0),
#                 estado = "Válido",
#                 tipo_vehiculo = "Liviano"
#             )
#             r.save()
#             
#             trans = Transaccion(
#                         fecha            = datetime.now(),
#                         tipo             = 'Reserva',
#                         estado           = 'Válido'
#                     )
#             trans.save()
#             
#             tdc =   TransTDC(
#                         nombre           = 'Karla',
#                         cedulaTipo       = 'V',
#                         cedula           = '87654321',
#                         tarjetaTipo      = 'VISTA',
#                         tarjeta          = '5689',
#                         monto            = 100,
#                         transaccion      = trans
#                     )
#             tdc.save()
#             
#             relacion =  TransReser(
#                             transaccion = trans,
#                             reserva = r
#                         )
#             relacion.save()
#                 
#         lista, total = consultar_ingresos("J-123456789")
#         self.assertTrue(len(lista) == 1 and total == n*100)
# 
#     # malicia
#     def test_dos_estacionamiento_muchos_pagos(self):
#         n  = 1000
#         e1 = Estacionamiento(
#             nombre      = "nom1",
#             direccion   = "dir1",
#             rif         = "J-123456789",
#             capacidadLivianos = n,
#             capacidadPesados  = n,
#             capacidadMotos    = n,
#             apertura    = time(0,0),
#             cierre      = time(23,59),
#         )
#         e2 = Estacionamiento(
#             nombre      = "nom2",
#             direccion   = "dir3",
#             rif         = "J-123456789",
#             capacidadLivianos = n,
#             capacidadPesados  = n,
#             capacidadMotos    = n,
#             apertura    = time(0,0),
#             cierre      = time(23,59),
#         )
#         e1.save()
#         e2.save()
#         
#         for i in range(0,n):
#             r = Reserva(
#                     cedulaTipo      = 'V',
#                     cedula          = '12345678',
#                     nombre          = 'Julia',
#                     apellido        = 'Suárez',
#                     estacionamiento = e1,
#                     inicioReserva = datetime(2015,3,10,3,0),
#                     finalReserva  = datetime(2015,3,10,5,0),
#                     estado = "Válido",
#                     tipo_vehiculo = "Liviano"
#                 )
#             r.save()
#             
#             trans = Transaccion(
#                         fecha            = datetime.now(),
#                         tipo             = 'Reserva',
#                         estado           = 'Válido'
#                     )
#             trans.save()
#             
#             tdc =   TransTDC(
#                         nombre           = 'Karla',
#                         cedulaTipo       = 'V',
#                         cedula           = '87654321',
#                         tarjetaTipo      = 'VISTA',
#                         tarjeta          = '5689',
#                         monto            = 100,
#                         transaccion      = trans
#                     )
#             tdc.save()
#             
#             relacion =  TransReser(
#                             transaccion = trans,
#                             reserva = r
#                         )
#             relacion.save()
#         
#         for i in range(0,n):
#             r = Reserva(
#                     cedulaTipo      = 'V',
#                     cedula          = '12345678',
#                     nombre          = 'Julia',
#                     apellido        = 'Suárez',
#                     estacionamiento = e2,
#                     inicioReserva = datetime(2015,3,10,3,0),
#                     finalReserva  = datetime(2015,3,10,5,0),
#                     estado = "Válido",
#                     tipo_vehiculo = "Liviano"
#                 )
#             r.save()
#             
#             trans = Transaccion(
#                         fecha            = datetime.now(),
#                         tipo             = 'Reserva',
#                         estado           = 'Válido'
#                     )
#             trans.save()
#             
#             tdc =   TransTDC(
#                         nombre           = 'Karla',
#                         cedulaTipo       = 'V',
#                         cedula           = '87654321',
#                         tarjetaTipo      = 'VISTA',
#                         tarjeta          = '5689',
#                         monto            = 100,
#                         transaccion      = trans
#                     )
#             tdc.save()
#             
#             relacion =  TransReser(
#                             transaccion = trans,
#                             reserva = r
#                         )
#             relacion.save()
#         lista, total = consultar_ingresos("J-123456789")
#         self.assertTrue(len(lista) == 2 and total == 2*n*100)
# 
#     def test_muchos_estacionamiento_mitad_sin_pagos(self):
#         n  = 100 
#         m  = 10
#         for i in range(0,n):
# 
#             e1 = Estacionamiento(
#                 nombre      = "nom%d"%i,
#                 direccion   = "dir1",
#                 rif         = "J-123456789",
#                 capacidadLivianos = m,
#                 capacidadPesados  = m,
#                 capacidadMotos    = m,
#                 apertura    = time(0,0),
#                 cierre      = time(23,59),
#             )
#             e2 = Estacionamiento(
#                 nombre      = "no%d"%i,
#                 direccion   = "dir3",
#                 rif         = "J-123456789",
#                 capacidadLivianos = m,
#                 capacidadPesados  = m,
#                 capacidadMotos    = m,
#                 apertura    = time(0,0),
#                 cierre      = time(23,59),
#             )
#             e1.save()
#             e2.save()
#             for j in range(0,m):
#                 r = Reserva(
#                     cedulaTipo      = 'V',
#                     cedula          = '12345678',
#                     nombre          = 'Julia',
#                     apellido        = 'Suárez',
#                     estacionamiento = e1,
#                     inicioReserva = datetime(2015,3,10,3,0),
#                     finalReserva  = datetime(2015,3,10,5,0),
#                     estado = "Válido",
#                     tipo_vehiculo = "Liviano"
#                 )
#                 r.save()
#                 
#                 trans = Transaccion(
#                             fecha            = datetime.now(),
#                             tipo             = 'Reserva',
#                             estado           = 'Válido'
#                         )
#                 trans.save()
#                 
#                 tdc =   TransTDC(
#                             nombre           = 'Karla',
#                             cedulaTipo       = 'V',
#                             cedula           = '87654321',
#                             tarjetaTipo      = 'VISTA',
#                             tarjeta          = '5689',
#                             monto            = 100,
#                             transaccion      = trans
#                         )
#                 tdc.save()
#                 
#                 relacion =  TransReser(
#                                 transaccion = trans,
#                                 reserva = r
#                             )
#                 relacion.save()
#         lista, total = consultar_ingresos("J-123456789")
#         self.assertTrue(len(lista) == 2*n and total == n*m*100)
# 
#     def test_muchos_estacionamiento_sin_pagos(self):
#         n  = 1000
#         for i in range(0,n):
#             e1 = Estacionamiento(
#                 nombre      = "nom%d"%i,
#                 direccion   = "dir1",
#                 rif         = "J-123456789",
#                 capacidadLivianos = n,
#                 capacidadPesados  = n,
#                 capacidadMotos    = n,
#                 apertura    = time(0,0),
#                 cierre      = time(23,59),
#             )
#             e1.save()
#         lista, total = consultar_ingresos("J-123456789")
#         self.assertTrue(len(lista) == n and total == 0)
# 
#     def test_muchos_estacionamiento_con_disintos_rif(self):
#         n  = 1000
#         for i in range(0,n):
#             e1 = Estacionamiento(
#                 nombre      = "nom%d"%i,
#                 direccion   = "dir1",
#                 rif         = "J-%i"%(123456789-i),
#                 capacidadLivianos = n,
#                 capacidadPesados  = n,
#                 capacidadMotos    = n,
#                 apertura    = time(0,0),
#                 cierre      = time(23,59),
#             )
#             e1.save()
#             r = Reserva(
#                 cedulaTipo      = 'V',
#                 cedula          = '12345678',
#                 nombre          = 'Julia',
#                 apellido        = 'Suárez',
#                 estacionamiento = e1,
#                 inicioReserva = datetime(2015,3,10,3,0),
#                 finalReserva  = datetime(2015,3,10,5,0),
#                 estado = "Válido",
#                 tipo_vehiculo = "Liviano"
#             )
#             r.save()
#             
#             trans = Transaccion(
#                         fecha            = datetime.now(),
#                         tipo             = 'Reserva',
#                         estado           = 'Válido'
#                     )
#             trans.save()
#             
#             tdc =   TransTDC(
#                         nombre           = 'Karla',
#                         cedulaTipo       = 'V',
#                         cedula           = '87654321',
#                         tarjetaTipo      = 'VISTA',
#                         tarjeta          = '5689',
#                         monto            = 100,
#                         transaccion      = trans
#                     )
#             tdc.save()
#             
#             relacion =  TransReser(
#                             transaccion = trans,
#                             reserva = r
#                         )
#             relacion.save()
#         lista, total = consultar_ingresos("J-123456789")
#         self.assertTrue(len(lista) == 1 and total == 100)

