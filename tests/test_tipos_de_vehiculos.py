# -*- coding: utf-8 -*-

from django.test import TestCase
from datetime import time, date
from reservas.forms import *
from estacionamientos.controller import *
from estacionamientos.forms import *
from estacionamientos.models import *
from reservas.models import *
from django.core.exceptions import ValidationError
from reservas.controller import marzullo

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
    
    def hacerReservaNueva(self,est,tipo_vehiculo_dado,fecha_inicio,fecha_fin):
        r = Reserva(
                    estacionamiento = est,
                    inicioReserva   = fecha_inicio,
                    finalReserva    = fecha_fin,
                    estado          = 'Válido',
                    tipo_vehiculo   = tipo_vehiculo_dado
                    )
        r.save()
        return r

    def testEstacionamientoSinPuestos(self):
        form_data = { 'puestosLivianos': 0,
                      'puestosPesados': 0,
                      'puestosMotos' : 0,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertRaises(Exception,form.is_valid())
    
    #Borde
    def testEstacionamientoSoloDeLivianos(self):
        form_data = { 'puestosLivianos': 1,
                      'puestosPesados': 0,
                      'puestosMotos' : 0,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())     
        
    def testEstacionamientoSoloDePesados(self):
        form_data = { 'puestosLivianos': 0,
                      'puestosPesados': 1,
                      'puestosMotos' : 0,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())       

        
    def testEstacionamientoSoloDeMotos(self):
        form_data = { 'puestosLivianos': 0,
                      'puestosPesados': 0,
                      'puestosMotos' : 1,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())       

        
    def testEstacionamientoMotosyLivianos(self):
        form_data = { 'puestosLivianos': 1,
                      'puestosPesados': 0,
                      'puestosMotos' : 1,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    def testEstacionamientoLivianosyPesados(self):
        form_data = { 'puestosLivianos': 1,
                      'puestosPesados': 1,
                      'puestosMotos' : 0,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    def testEstacionamientoPesadosyMotos(self):
        form_data = { 'puestosLivianos': 0,
                      'puestosPesados': 1,
                      'puestosMotos' : 1,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
    '''print("Entre al caso y voy a considerar si reservar causa excepcion")
        self.assertRaises(Exception, self.hacerReservaNueva, (e,'Liviano'))
    '''   
    def testReservarParaLiviano(self):
        e = self.crearEstacionamientoNuevo(1,0,0)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
            
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Liviano'))

        
    def testReservarParaPesado(self):
        e = self.crearEstacionamientoNuevo(0,1,0)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
            
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Pesado'))
        
    def testReservarParaMoto(self):
        e = self.crearEstacionamientoNuevo(0,0,1)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
            
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Moto'))
        
    def testNoSePuedeReservarSinPuesto(self):
        e = self.crearEstacionamientoNuevo(0,1,0)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
            
        self.assertFalse(marzullo(e.id, fecha_inicio, fecha_fin,'Moto'))   
        
    def testLlenarLivianosNoBloqueaLosDemas(self):
        e = self.crearEstacionamientoNuevo(1,1,1)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
        self.hacerReservaNueva(e,'Liviano',fecha_inicio,fecha_fin)
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Moto') and marzullo(e.id, fecha_inicio, fecha_fin,'Pesado'))
        
    def testLlenarPesadosNoBloqueaLosDemas(self):
        e = self.crearEstacionamientoNuevo(1,1,1)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
        self.hacerReservaNueva(e,'Pesado',fecha_inicio,fecha_fin)
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Moto') and marzullo(e.id, fecha_inicio, fecha_fin,'Liviano'))
        
    def testLlenarMotosNoBloqueaLosDemas(self):
        e = self.crearEstacionamientoNuevo(1,1,1)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
        self.hacerReservaNueva(e,'Moto',fecha_inicio,fecha_fin)
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Liviano') and marzullo(e.id, fecha_inicio, fecha_fin,'Pesado'))
        
    def testLlenarLivianosyPesadosNoBloqueaMotos(self):
        e = self.crearEstacionamientoNuevo(1,1,1)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
        self.hacerReservaNueva(e,'Liviano',fecha_inicio,fecha_fin)
        self.hacerReservaNueva(e,'Pesado',fecha_inicio,fecha_fin)
        
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Moto'))
        
    def testLlenarMotosyPesadosNoBloqueaLivianos(self):
        
        e = self.crearEstacionamientoNuevo(1,1,1)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
        self.hacerReservaNueva(e,'Moto',fecha_inicio,fecha_fin)
        self.hacerReservaNueva(e,'Pesado',fecha_inicio,fecha_fin)
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Liviano'))
    
    def testLlenarLivianosyMotosNoBloqueaPesados(self):
        e = self.crearEstacionamientoNuevo(1,1,1)
        ahora=datetime.now().replace(second=0,microsecond=0)
        fecha_inicio=(ahora+timedelta(1)).replace(hour=15,minute=15)
        fecha_fin=fecha_inicio.replace(hour=16,minute=15)
        self.hacerReservaNueva(e,'Liviano',fecha_inicio,fecha_fin)
        self.hacerReservaNueva(e,'Moto',fecha_inicio,fecha_fin)
        self.assertTrue(marzullo(e.id, fecha_inicio, fecha_fin,'Pesado'))