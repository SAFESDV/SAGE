# -*- coding: utf-8 -*-
 
from django.test import TestCase
 
from estacionamientos.forms import EsquemaTarifarioLiviano
from estacionamientos.forms import EsquemaTarifarioPesado
from estacionamientos.forms import EsquemaTarifarioMoto
from estacionamientos.forms import EsquemaTarifarioDiscapacitados

class TiposDeVehiculosTestCase(TestCase):
    
###################################################################
#                ESQUEMA TARIFARIO LIVIANO FORM                   #
###################################################################
    
    #Borde
    def test_EsquemaTarifaLivianoForm(self):
        form_data = { }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Borde
    def test_EsquemaTarifaLivianoForm_UnCampo(self):
        form_data = {
                'tarifaLivianos': 50
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertFalse(form.is_valid()) 
         
    #Borde    
    def test_EsquemaTarifaLivianoForm_DosCampos(self):
        form_data = {
                'tarifaLivianos': 50,
                'tarifaLivianos2' : 60,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertFalse(form.is_valid())
    
    #Borde
    def test_EsquemaTarifaLivianoForm_TodosLosCamposObligatorios(self):
        form_data = {
                'tarifaLivianos': 50,
                'tarifaLivianosF' : 60,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaLivianoForm_tresCampos(self):
        form_data = {
                'tarifaLivianos': 50,
                'tarifaLivianos2' : 60,
                'tarifaLivianosF' : 70,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaLivianoForm_tresCampos2(self):
        form_data = {
                'tarifaLivianos2': 50,
                'tarifaLivianosF' : 60,
                'tarifaLivianos2F' : 70,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertFalse(form.is_valid())
    
    #Borde 
    def test_EsquemaTarifaLivianoForm_TodosLosCampos(self):
        form_data = {
                'tarifaLivianos': 50,
                'tarifaLivianos2' : 60,
                'tarifaLivianosF' : 70,
                'tarifaLivianos2F' : 70,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Malicia
    def test_EsquemaTarifaLivianoForm_CamposInvalidos(self):
        form_data = {
                'tarifaLivianos': 'ab778',
                'tarifaLivianos2' : 60,
                'tarifaLivianosF' : 70,
                'tarifaLivianos2F' : 70,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertFalse(form.is_valid())
    
    #Malicia     
    def test_EsquemaTarifaLivianoForm_CamposDecimal(self):
        form_data = {
                'tarifaLivianos': 30,
                'tarifaLivianos2' : 60,
                'tarifaLivianosF' : 20,
                'tarifaLivianos2F' : 70,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Malicia     
    def test_EsquemaTarifaLivianoForm_CamposNegativos(self):
        form_data = {
                'tarifaLivianos': -30,
                'tarifaLivianos2' : 60.10,
                'tarifaLivianosF' : 0.01,
                'tarifaLivianos2F' : 70,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Malicia
    def test_EsquemaTarifaLivianoForm_CamposSimbolos(self):
        form_data = {
                'tarifaLivianos': 30,
                'tarifaLivianos2' : 60,
                'tarifaLivianosF' : '*/*-',
                'tarifaLivianos2F' : 70,
                    }
        form = EsquemaTarifarioLiviano(data = form_data)
        self.assertFalse(form.is_valid())
        
###################################################################
#                ESQUEMA TARIFARIO PESADO FORM                    #
###################################################################
    
    #Borde
    def test_EsquemaTarifaPesadoForm(self):
        form_data = { }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Borde
    def test_EsquemaTarifaPesadoForm_UnCampo(self):
        form_data = {
                'tarifaPesados': 50
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaPesadoForm_DosCampos(self):
        form_data = {
                'tarifaPesados': 50,
                'tarifaPesados2' : 60,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaPesadoForm_TodosLosCamposObligatorios(self):
        form_data = {
                'tarifaPesados': 50,
                'tarifaPesadosF' : 60,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertTrue(form.is_valid())
     
    #Borde    
    def test_EsquemaTarifaPesadoForm_tresCampos(self):
        form_data = {
                'tarifaPesados': 50,
                'tarifaPesados2' : 60,
                'tarifaPesadosF' : 70,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaPesadoForm_tresCampos2(self):
        form_data = {
                'tarifaPesados2': 50,
                'tarifaPesadosF' : 60,
                'tarifaPesados2F' : 70,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertFalse(form.is_valid())
    
    #Borde   
    def test_EsquemaTarifaPesadoForm_TodosLosCampos(self):
        form_data = {
                'tarifaPesados': 50,
                'tarifaPesados2' : 60,
                'tarifaPesadosF' : 70,
                'tarifaPesados2F' : 70,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertTrue(form.is_valid())
    
    #Malicia    
    def test_EsquemaTarifaPesadoForm_CamposInvalidos(self):
        form_data = {
                'tarifaPesados': 'ab778',
                'tarifaPesados2' : 60,
                'tarifaPesadosF' : 70,
                'tarifaPesados2F' : 70,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertFalse(form.is_valid())
    
    #Malicia  
    def test_EsquemaTarifaPesadoForm_CamposDecimal(self):
        form_data = {
                'tarifaPesados': 30.50,
                'tarifaPesados2' : 60.10,
                'tarifaPesadosF' : 0.01,
                'tarifaPesados2F' : 70,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Malicia     
    def test_EsquemaTarifaPesadoForm_CamposNegativos(self):
        form_data = {
                'tarifaPesados': -30,
                'tarifaPesados2' : 60.10,
                'tarifaPesadosF' : 0.01,
                'tarifaPesados2F' : 70,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Malicia
    def test_EsquemaTarifaPesadoForm_CamposSimbolos(self):
        form_data = {
                'tarifaPesados': 30,
                'tarifaPesados2' : 60,
                'tarifaPesadosF' : '*/*-',
                'tarifaPesados2F' : 70,
                    }
        form = EsquemaTarifarioPesado(data = form_data)
        self.assertFalse(form.is_valid())
        
###################################################################
#                 ESQUEMA TARIFARIO MOTOS FORM                    #
###################################################################
    
    #Borde
    def test_EsquemaTarifaMotoForm(self):
        form_data = { }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Borde
    def test_EsquemaTarifaMotoForm_UnCampo(self):
        form_data = {
                'tarifaMotos': 50
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertFalse(form.is_valid())
    
    #Borde 
    def test_EsquemaTarifaMotoForm_DosCampos(self):
        form_data = {
                'tarifaMotos': 50,
                'tarifaMotos2' : 60,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertFalse(form.is_valid())
    
    #Borde     
    def test_EsquemaTarifaMotoForm_TodosLosCamposObligatorios(self):
        form_data = {
                'tarifaMotos': 50,
                'tarifaMotosF' : 60,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertTrue(form.is_valid())
    
    #Borde     
    def test_EsquemaTarifaMotoForm_tresCampos(self):
        form_data = {
                'tarifaMotos': 50,
                'tarifaMotos2' : 60,
                'tarifaMotosF' : 70,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaMotoForm_tresCampos2(self):
        form_data = {
                'tarifaMotos2': 50,
                'tarifaMotosF' : 60,
                'tarifaMotos2F' : 70,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertFalse(form.is_valid())
     
    #Borde    
    def test_EsquemaTarifaMotoForm_TodosLosCampos(self):
        form_data = {
                'tarifaMotos': 50,
                'tarifaMotos2' : 60,
                'tarifaMotosF' : 70,
                'tarifaMotos2F' : 70,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Malicia
    def test_EsquemaTarifaMotoForm_CamposInvalidos(self):
        form_data = {
                'tarifaMotos': 'ab778',
                'tarifaMotos2' : 60,
                'tarifaMotosF' : 70,
                'tarifaMotos2F' : 70,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Malicia
    def test_EsquemaTarifaMotoForm_CamposDecimal(self):
        form_data = {
                'tarifaMotos': 30.50,
                'tarifaMotos2' : 60.10,
                'tarifaMotosF' : 0.01,
                'tarifaMotos2F' : 70,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertTrue(form.is_valid())
        
     #Malicia     
    def test_EsquemaTarifaMotoForm_CamposNegativos(self):
        form_data = {
                'tarifaMotos': -30,
                'tarifaMotos2' : 60.10,
                'tarifaMotosF' : 0.01,
                'tarifaMotos2F' : 70,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Malicia
    def test_EsquemaTarifaMotoForm_CamposSimbolos(self):
        form_data = {
                'tarifaMotos': 30,
                'tarifaMotos2' : 60,
                'tarifaMotosF' : '*/*-',
                'tarifaMotos2F' : 70,
                    }
        form = EsquemaTarifarioMoto(data = form_data)
        self.assertFalse(form.is_valid())


###################################################################
#             ESQUEMA TARIFARIO DISCAPACITADOS FORM               #
###################################################################
    
    #Borde
    def test_EsquemaTarifaDiscapacitadosForm(self):
        form_data = { }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Borde
    def test_EsquemaTarifaDiscapacitadosForm_UnCampo(self):
        form_data = {
                'tarifaDiscapacitados': 50
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaDiscapacitadosForm_DosCampos(self):
        form_data = {
                'tarifaDiscapacitados': 50,
                'tarifaDiscapacitados2' : 60,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaDiscapacitadosForm_TodosLosCamposObligatorios(self):
        form_data = {
                'tarifaDiscapacitados': 50,
                'tarifaDiscapacitadosF' : 60,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertTrue(form.is_valid())
    
    #Borde     
    def test_EsquemaTarifaDiscapacitadosForm_tresCampos(self):
        form_data = {
                'tarifaDiscapacitados': 50,
                'tarifaDiscapacitados2' : 60,
                'tarifaDiscapacitadosF' : 70,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertTrue(form.is_valid())
        
    #Borde 
    def test_EsquemaTarifaDiscapacitadosForm_tresCampos2(self):
        form_data = {
                'tarifaDiscapacitados2': 50,
                'tarifaDiscapacitadosF' : 60,
                'tarifaDiscapacitados2F' : 70,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertFalse(form.is_valid())
    
    #Borde     
    def test_EsquemaTarifaDiscapacitadosForm_TodosLosCampos(self):
        form_data = {
                'tarifaDiscapacitados': 50,
                'tarifaDiscapacitados2' : 60,
                'tarifaDiscapacitadosF' : 70,
                'tarifaDiscapacitados2F' : 70,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertTrue(form.is_valid())
    
    #Malicia    
    def test_EsquemaTarifaDiscapacitadosForm_CamposInvalidos(self):
        form_data = {
                'tarifaDiscapacitados': 'ab778',
                'tarifaDiscapacitados2' : 60,
                'tarifaDiscapacitadosF' : 70,
                'tarifaDiscapacitados2F' : 70,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertFalse(form.is_valid())
     
    #Malicia   
    def test_EsquemaTarifaDiscapacitadosForm_CamposDecimal(self):
        form_data = {
                'tarifaDiscapacitados': 30.50,
                'tarifaDiscapacitados2' : 60.10,
                'tarifaDiscapacitadosF' : 0.01,
                'tarifaDiscapacitados2F' : 70,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertTrue(form.is_valid())
        
     #Malicia     
    def test_EsquemaTarifaDiscapacitadosForm_CamposNegativos(self):
        form_data = {
                'tarifaDiscapacitados': -30,
                'tarifaDiscapacitados2' : 60.10,
                'tarifaDiscapacitadosF' : 0.01,
                'tarifaDiscapacitados2F' : 70,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertFalse(form.is_valid())
        
    #Malicia
    def test_EsquemaTarifaDiscapacitadosForm_CamposSimbolos(self):
        form_data = {
                'tarifaDiscapacitados': 30,
                'tarifaDiscapacitados2' : 60,
                'tarifaDiscapacitadosF' : '*/*-',
                'tarifaDiscapacitados2F' : 70,
                    }
        form = EsquemaTarifarioDiscapacitados(data = form_data)
        self.assertFalse(form.is_valid())
        