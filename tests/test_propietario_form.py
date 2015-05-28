# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import PropietarioForm

###################################################################
#                    PROPIETARIO FORM
###################################################################

class EstacionamientoAllFormTestCase(TestCase):

    # malicia
    def test_campos_vacios(self):
        form_data = {}
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_solo_un_campo_necesario(self):
        form_data = {
            'Cedula': '19564959'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_todos_los_campos_necesarios(self):
        form_data = {
            'Cedula': '19564959',
            'nomb_prop': 'Francisco Sucre'
        }
        form = PropietarioForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_CI_propietario_invalido_caracteres_en_campo(self):
        form_data = {
            'Cedula': 'as19564959sa',
            'nomb_prop': 'Francisco Sucre'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_CI_propietario_invalido_simbolos_especiales(self):
        form_data = {
            'Cedula': '!19564959!',
            'nomb_prop': 'Francisco Sucre'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())
        
   # malicia
    def test_Nombre_propietario_invalido_digitos_en_campo(self):
        form_data = {
            'Cedula': '19564959',
            'nomb_prop': '12313Francisco Sucre12313'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_Nombre_propietario_invalido_simbolos_especiales(self):
        form_data = {
            'Cedula': '19564959',
            'nomb_prop': '!Francisco Sucre!'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())        

    # malicia
    def test_Nombre_propietario_invalido_caracteres_especiales(self):
        form_data = {
            'Cedula': '19564959',
            'nomb_prop': 'Frañcíscó Sùcrë'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())   

    # malicia
    def test_agregar_telefonos(self):
        form_data = {
            'Cedula': '19564959',
            'nomb_prop': 'Francisco Sucre',
            'telefono_prop': '02129322878'
        }
        form = PropietarioForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_formato_invalido_telefono(self):
        form_data = {
            'Cedula': '19564959',
            'nomb_prop': 'Francisco Sucre',
            'telefono_prop': '02459322878'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_agregar_correos_electronicos(self):
        form_data = {
            'Cedula': '19564959',
            'nomb_prop': 'Francisco Sucre',
            'telefono_prop': '02129322878',
            'email_prop': 'adminsitrador@gmail.com'
        }
        form = PropietarioForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_correo_electronico_invalido(self):
        form_data = {
            'Cedula': '19564959',
            'nomb_prop': 'Francisco Sucre',
            'telefono_prop': '02459322878',
            'email_prop': 'adminsitrador@z<x@cc@zxgmail.com'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())
