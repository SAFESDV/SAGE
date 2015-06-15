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
                      'horizonte'   : 2}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_dos_campos(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horizonte'   : 2}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_tres_campos(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'horizonte'   : 2},
                      
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # caso borde
    def test_estacionamiento_extended_form_cuatro_bien(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'horizonte'   : 2                    
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_todos_campos_bien(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaMinuto',
                      'esquemaFeriado' : 'TarifaSinFeriado',
                      'horizonte'   : 2
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    # caso borde
    def test_estacionamiento_extended_form_puestos_1(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaSinFeriado',
                      'horizonte'   : 2}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_puestos_0(self):
        form_data = { 'puestosLivianos': 0,
                      'puestosPesados': 0,
                      'puestosMotos' : 0,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaSinFeriado',
                      'horizonte'   : 2}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertRaises(Exception,form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_hora_inicio_igual_hora_cierre(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos' : 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 6,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaSinFeriado',
                      'horizonte'   : 2
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_string_en_campo_puesto(self):
        form_data = { 'puestosLivianos': 'hola',
                      'puestosPesados': 'hola',
                      'puestosMotos': 'hola',
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaSinFeriado',
                      'horizonte'   : 2
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_string_hora_inicio(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos': 2,
                      'horarioin': 'holaa',
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaSinFeriado',
                      'horizonte'   : 2
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_none_en_tarifa(self):
        form_data = { 'puestosLivianos': 2,
                      'puestosPesados': 2,
                      'puestosMotos': 2,
                      'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': None,
                      'esquema':'TarifaHora',
                      'esquemaFeriado' : 'TarifaSinFeriado',
                      'horizonte'   : 2
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
        
#---------------------------------------------------------------------------------------------------
#                CASOS AGREGADOS CON LA IMPLEMENTACION DE TARIFA PARA DIAS FERIADOS
#---------------------------------------------------------------------------------------------------

    #malicia
    def test_estacionamiento_extended_form_esquemaFeriado_esquemaNoValido(self):
        form_data = { 'puestos': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaMinuto',
                      'esquemaFeriado' : 'ñalskdj',
                      'horizonte'   : 2
                    }
        
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #borde
    def test_estacionamiento_extended_form_tarifaFeriado_NoValido(self):
        form_data = { 'puestos': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaMinuto',
                      'esquemaFeriado' : 'TarifaHoraDiaFeriado',
                      'tarifaFeriado' : -1.001,
                      'horizonte'   : 2
                    }
        
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #borde todos los campos bien     
    def test_estacionamiento_extended_form_valido_con_esquemaFeriado(self):
        form_data = { 'puestos': 2,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaMinuto',
                      'esquemaFeriado' : 'TarifaHoraDiaFeriado',
                      'tarifaFeriado' : 5.05,
                      'horizonte'   : 2
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
        
        
