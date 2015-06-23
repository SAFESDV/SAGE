# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import time

from estacionamientos.forms import EstacionamientoExtendedForm

###################################################################
# ESTACIONAMIENTO_EXTENDED_FORM
###################################################################

class ExtendedFormTestCase(TestCase):

    # malicia
    def test_estacionamiento_extended_form_un_campo(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horizonte' : 15}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_dos_campos(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horizonte' : 15}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_tres_campos(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'horizonte' : 15}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # caso borde
    def test_estacionamiento_extended_form_cuatro_bien(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': 12 ,
                      'horizonte' : 15                   
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_todos_campos_bien(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosDiscapacitados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaMinuto',
                      'esquemaFeriado' : 'TarifaMinuto',
                      'horizonte' : 15,
                      'fronteraTarifa': 'PrecioTarifaMasCara'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    # caso borde
    def test_estacionamiento_extended_form_puestos_1(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'puestosDiscapacitados': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaMinuto',
                      'horizonte' : 15,
                      'fronteraTarifa': 'PrecioTarifaMasCara'
                      }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_puestos_0(self):
        form_data = { 'puestosLivianos': 0,
                      'puestosPesados': 0,
                      'puestosDiscapacitados': 2,
                      'puestosMotos' : 0,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaMinuto',
                      'horizonte' : 15
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertRaises(Exception,form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_hora_inicio_igual_hora_cierre(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'puestosDiscapacitados': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 6,  minute = 0),
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaMinuto',
                      'horizonte' : 15,
                      'fronteraTarifa': 'PrecioTarifaMasCara'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_string_en_campo_puesto(self):
        form_data = { 'puestosLivianos': 'hola',
                      'puestosPesados': 'hola',
                      'puestosMotos': 'hola',
                      'puestosDiscapacitados': 'hola',
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaMinuto',
                      'horizonte' : 15,
                      'fronteraTarifa': 'PrecioTarifaMasCara'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_string_hora_inicio(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos': 2,
                      'puestosDiscapacitados': 2,                      
                      'horarioin': 'holaa',
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaMinuto',
                      'tarifaFeriado' : 15,
                      'horizonte' : 15,
                      'fronteraTarifa': 'PrecioTarifaMasCara'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_discapacitados_0(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos': 2,
                      'puestosDiscapacitados': 0,
                      'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaMinuto',
                      'horizonte' : 15,
                      'fronteraTarifa': 'PrecioTarifaMasCara'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
        
        
#---------------------------------------------------------------------------------------------------
#                CASOS AGREGADOS CON LA IMPLEMENTACION DE TARIFA PARA DIAS FERIADOS
#---------------------------------------------------------------------------------------------------

    #malicia
    def test_estacionamiento_extended_form_esquemaFeriado_esquemaNoValido(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos': 2,
                      'puestosDiscapacitados': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaMinuto',
                      'esquemaFeriado' : 'ñalskdj',
                      'horizonte' : 15,
                      'fronteraTarifa': 'PrecioTarifaMasCara'
                    }
        
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #borde
    def test_estacionamiento_extended_form_Horizonte_No_valido(self):
        
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos': 2,
                      'puestosDiscapacitados': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaHora',
                      'horizonte' : 'hola',
                      'fronteraTarifa': 'PrecioTarifaMasCara'
                    }
        
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
