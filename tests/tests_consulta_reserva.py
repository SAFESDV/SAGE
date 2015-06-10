# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import time,datetime
from estacionamientos.controller import consultar_ingresos
from pagos.models import Pago
from estacionamientos.models import Estacionamiento
from reservas.models import Reserva

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
    def test_un_estacionamiento_un_pago(self):
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
        r = Reserva(
                estacionamiento = e,
                inicioReserva = datetime(2015,3,10,3,0),
                finalReserva  = datetime(2015,3,10,5,0),
                estado = "Válido",
                tipo_vehiculo = "Liviano"
            )
        r.save()
        p = Pago(
                fechaTransaccion = datetime.now(),
                cedulaTipo       = "V",
                cedula           = "1234567",
                tarjetaTipo      = "VISTA",
                reserva          = r,
                monto            = 150,
            )
        p.save()
        lista, total = consultar_ingresos("J-123456789")
        self.assertTrue(len(lista) == 1 and total == 150)
        
    # TDD malicia
    def test_un_estacionamiento_muchos_pagos(self):
        n = 1000
        e = Estacionamiento(
            nombre      = "nom",
            direccion   = "dir",
            rif         = "J-123456789",
            capacidadPesados   = n,
            capacidadLivianos   = n,
            capacidadMotos   = n,
            apertura    = time(0,0),
            cierre      = time(23,59),
        )
        e.save()
        for i in range(0,n):
            r = Reserva(
                    estacionamiento = e,
                    inicioReserva = datetime(2015,3,10,3,0),
                    finalReserva  = datetime(2015,3,10,5,0),
                    estado = "Válido",
                    tipo_vehiculo = "Liviano"
                )
            r.save()
            p = Pago(
                    fechaTransaccion = datetime.now(),
                    cedulaTipo       = "V",
                    cedula           = "1234567",
                    tarjetaTipo      = "VISTA",
                    reserva          = r,
                    monto            = 100,
                )
            p.save()
        lista, total = consultar_ingresos("J-123456789")
        self.assertTrue(len(lista) == 1 and total == n*100)

    # malicia
    def test_dos_estacionamiento_muchos_pagos(self):
        n  = 1000
        e1 = Estacionamiento(
            nombre      = "nom1",
            direccion   = "dir1",
            rif         = "J-123456789",
            capacidadLivianos = n,
            capacidadPesados  = n,
            capacidadMotos    = n,
            apertura    = time(0,0),
            cierre      = time(23,59),
        )
        e2 = Estacionamiento(
            nombre      = "nom2",
            direccion   = "dir3",
            rif         = "J-123456789",
            capacidadLivianos = n,
            capacidadPesados  = n,
            capacidadMotos    = n,
            apertura    = time(0,0),
            cierre      = time(23,59),
        )
        e1.save()
        e2.save()
        for i in range(0,n):
            r = Reserva(
                    estacionamiento = e1,
                    inicioReserva = datetime(2015,3,10,3,0),
                    finalReserva  = datetime(2015,3,10,5,0),
                    estado = "Válido",
                    tipo_vehiculo = "Liviano"
                )
            r.save()
            p = Pago(
                    fechaTransaccion = datetime.now(),
                    cedulaTipo       = "V",
                    cedula           = "1234567",
                    tarjetaTipo      = "VISTA",
                    reserva          = r,
                    monto            = 100,
                )
            p.save()
        for i in range(0,n):
            r = Reserva(
                    estacionamiento = e2,
                    inicioReserva = datetime(2015,3,10,3,0),
                    finalReserva  = datetime(2015,3,10,5,0),
                    estado = "Válido",
                    tipo_vehiculo = "Liviano"
                )
            r.save()
            p = Pago(
                    fechaTransaccion = datetime.now(),
                    cedulaTipo       = "V",
                    cedula           = "1234567",
                    tarjetaTipo      = "VISTA",
                    reserva          = r,
                    monto            = 100,
                )
            p.save()
        lista, total = consultar_ingresos("J-123456789")
        self.assertTrue(len(lista) == 2 and total == 2*n*100)

    def test_muchos_estacionamiento_mitad_sin_pagos(self):
        n  = 100 
        m  = 10
        for i in range(0,n):

            e1 = Estacionamiento(
                nombre      = "nom%d"%i,
                direccion   = "dir1",
                rif         = "J-123456789",
                capacidadLivianos = m,
                capacidadPesados  = m,
                capacidadMotos    = m,
                apertura    = time(0,0),
                cierre      = time(23,59),
            )
            e2 = Estacionamiento(
                nombre      = "no%d"%i,
                direccion   = "dir3",
                rif         = "J-123456789",
                capacidadLivianos = m,
                capacidadPesados  = m,
                capacidadMotos    = m,
                apertura    = time(0,0),
                cierre      = time(23,59),
            )
            e1.save()
            e2.save()
            for j in range(0,m):
                r = Reserva(
                        estacionamiento = e1,
                        inicioReserva = datetime(2015,3,10,3,0),
                        finalReserva  = datetime(2015,3,10,5,0),
                        estado = "Válido",
                        tipo_vehiculo = "Liviano"
                    )
                r.save()
                p = Pago(
                        fechaTransaccion = datetime.now(),
                        cedulaTipo       = "V",
                        cedula           = "1234567",
                        tarjetaTipo      = "VISTA",
                        reserva          = r,
                        monto            = 100,
                    )
                p.save()

        lista, total = consultar_ingresos("J-123456789")
        self.assertTrue(len(lista) == 2*n and total == n*m*100)

    def test_muchos_estacionamiento_sin_pagos(self):
        n  = 1000
        for i in range(0,n):
            e1 = Estacionamiento(
                nombre      = "nom%d"%i,
                direccion   = "dir1",
                rif         = "J-123456789",
                capacidadLivianos = n,
                capacidadPesados  = n,
                capacidadMotos    = n,
                apertura    = time(0,0),
                cierre      = time(23,59),
            )
            e1.save()
        lista, total = consultar_ingresos("J-123456789")
        self.assertTrue(len(lista) == n and total == 0)

    def test_muchos_estacionamiento_con_disintos_rif(self):
        n  = 1000
        for i in range(0,n):
            e1 = Estacionamiento(
                nombre      = "nom%d"%i,
                direccion   = "dir1",
                rif         = "J-%i"%(123456789-i),
                capacidadLivianos = n,
                capacidadPesados  = n,
                capacidadMotos    = n,
                apertura    = time(0,0),
                cierre      = time(23,59),
            )
            e1.save()
            r = Reserva(
                    estacionamiento = e1,
                    inicioReserva = datetime(2015,3,10,3,0),
                    finalReserva  = datetime(2015,3,10,5,0),
                    estado = "Válido",
                    tipo_vehiculo = "Liviano"
                )
            r.save()
            p = Pago(
                    fechaTransaccion = datetime.now(),
                    cedulaTipo       = "V",
                    cedula           = "1234567",
                    tarjetaTipo      = "VISTA",
                    reserva          = r,
                    monto            = 100,
                )
            p.save()
        lista, total = consultar_ingresos("J-123456789")
        self.assertTrue(len(lista) == 1 and total == 100)

