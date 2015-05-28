# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import EditarEstacionamientoForm

###################################################################
#                    PROPIETARIO FORM
###################################################################

class EditarEstacionamientoFormTestCase(TestCase):

    # malicia
    def test_campos_vacios(self):
        form_data = {}
        form = EditarEstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_CI_propietario_valida(self):
        form_data = {
            'CI_prop': '19564959'
        }
        form = EditarEstacionamientoForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_CI_propietario_invalido_caracteres_en_campo(self):
        form_data = {
            'CI_prop': 'as19564959sa'
        }
        form = EditarEstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_CI_propietario_invalido_simbolos_especiales(self):
        form_data = {
            'CI_prop': '!19564959!'
        }
        form = EditarEstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())
        

