# -*- coding: utf-8 -*-
 
from django.test import TestCase
 
from billetera.forms import BilleteraElectronicaForm
 
###################################################################
#                    BILLETERA_ELECTRONICA FORM
###################################################################
 
class BilleteraElectronicaFormTestCase(TestCase):
 
    # borde
    def test_BilleteraElectronicaForm_Vacio(self):
        form_data = {}
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    # borde
    def test_BilleteraElectronicaForm_UnCampo(self):
        form_data = {
            'nombre': 'Carlos',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_DosCampos(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_TresCampos(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_CuatroCampos(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_CincoCampos(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertTrue(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_NombreInvalidoDigito(self):
        form_data = {
            'nombre': 'Car1os',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_NombreInvalidoSimbolo(self):
        form_data = {
            'nombre': 'Carlos+',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
         
    #borde
    def test_BilleteraElectronicaForm_NombreInvalidoEspacio(self):
        form_data = {
            'nombre': ' Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_ApellidoInvalidoDigito(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'R0dríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_ApellidoInvalidoSimbolos(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez|',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
     
        
    #borde
    def test_BilleteraElectronicaForm_ApellidoInvalidoEspacio(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': ' Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_CedulaTipoInvalido(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'J',
            'cedula': '123456789',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_CedulaInvalida(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': 'V12345',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
         
    #borde
    def test_BilleteraElectronicaForm_Limite_Superior_Cedula(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '999999999',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertTrue(form.is_valid())
     
    #borde
    def test_BilleteraElectronicaForm_Limite_Inferior_Cedula(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '0',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertTrue(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_Limite_Superior_Pin(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '9999',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertTrue(form.is_valid())
 
    #borde
    def test_BilleteraElectronicaForm_Limite_Inferior_Pin(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '0000',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertTrue(form.is_valid())
 
    #malicia
    def test_BilleteraElectronicaForm_PinInvalido(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': 'd234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #malicia
    def test_BilleteraElectronicaForm_PinInvalido_Insuficiente(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'V',
            'cedula': '123456789',
            'pin': '234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #malicia
    def test_BilleteraElectronicaForm_DosCamposErroneos(self):
        form_data = {
            'nombre': 'Car1os',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'foo',
            'cedula': '123456789',
            'tarjetaTipo': 'Vista',
            'pin': '1234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #malicia
    def test_BilleteraElectronicaForm_CuatroCamposErroneos(self):
        form_data = {
            'nombre': 'Car1os',
            'apellido': 'Rodríguez',
            'cedulaTipo': 'foo',
            'cedula': '12345sda6789',
            'pin': '234',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())
 
    #malicia
    def test_BilleteraElectronicaForm_TodosCamposErroneos(self):
        form_data = {
            'nombre': 'Carlos ',
            'apellido': 'Rod ríguez',
            'cedulaTipo': 'foo',
            'cedula': '12345678as9',
            'pin': '23d',
        }
        form = BilleteraElectronicaForm(data = form_data)
        self.assertFalse(form.is_valid())