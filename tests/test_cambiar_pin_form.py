# -*- coding: utf-8 -*-
 
from django.test import TestCase
 
from billetera.forms import CambiarPinForm

###################################################################
#                    CAMBIAR PIN FORM
###################################################################

class CambiarPinBilleteraTestCase(TestCase):
    
    #Borde
    def test_CambiarPinForm(self):
        form_data = { }
        form = CambiarPinForm(data = form_data)
        self.assertFalse(form.is_valid())
    
    # Borde
    def test_CambiarPinForm_UnCampo(self):
        form_data = { 
                    'pin': '0000',
                    }
        form = CambiarPinForm(data = form_data)
        self.assertFalse(form.is_valid()) 
        
    # Borde
    def test_CambiarPinForm_DosCampos(self):
        form_data = { 
                    'pin': '0000',
                    'pin_verificar': '1111',
                    }
        form = CambiarPinForm(data = form_data)
        self.assertTrue(form.is_valid()) 
    
    # Malicia    
    def test_CambiarPinForm_invalido(self):
        form_data = { 
                    'pin': 'a0l5',
                    'pin_verificar': '1111',
                    }
        form = CambiarPinForm(data = form_data)
        self.assertFalse(form.is_valid()) 
        
    # Borde
    def test_CambiarPinForm_invalido2(self):
        form_data = { 
                    'pin': '0000',
                    'pin_verificar': '111',
                    }
        form = CambiarPinForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # Borde
    def test_CambiarPinForm_invalido2(self):
        form_data = { 
                    'pin': '00000',
                    'pin_verificar': '11',
                    }
        form = CambiarPinForm(data = form_data)
        self.assertFalse(form.is_valid())